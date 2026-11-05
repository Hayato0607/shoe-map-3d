#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dash AI シューズデータベースの CSV から、3Dマップ用の data.js を作るスクリプト。
Python 3.8 以降の標準ライブラリだけで動きます（追加インストール不要）。

使い方（リポジトリのフォルダで）:
    python tools/csv_to_datajs.py shoe-database_models_all_YYYYMMDD.csv

    -o data.js            出力先（省略時はリポジトリ直下の data.js）
    --include-spikes      スパイクも含める（初期設定はランニングシューズのみ）
    --include-private     モデル公開が「非公開」のものも含める（公開サイトには載せないこと）

計算結果の内訳は CSV と同じフォルダに score_report_YYYYMMDD.csv として保存されます
（Excel で文字化けしないよう BOM 付き UTF-8）。

──────────────────────────────────────────
■ 反発（-5 低反発・安定 〜 +5 高反発・不安定）
    反発 = 10/9 × { 0.6 ×（反発性 − 5.5）− 0.4 ×（評価_安定性 − 5.5）}

  反発性に使う値：
    ・反発指標（リア・ミッド・フォア）が3つともあるとき → 実測値を10段階に換算して使う
         反発性 = 6.1 ＋（3か所の平均 − 1870）÷ 190   （1〜10 で止める）
         … 実測値と評価_反発性の両方があるシューズ112足で、平均とばらつきが同じになるように決めた換算
           （2026-11-02 のデータで算出。測定方法や機材が変わったら見直すこと）
    ・反発指標がないとき → 評価_反発性（10段階）をそのまま使う

■ 速さ（-5 遅い 〜 +5 速い）
    速さ = 0.7 × ペース点 P ＋ 0.3 × 重量点 W

  ペース点 P：「用途→対象レベル」の組み合わせごとに想定ペースを出し、その平均速度で決める
    1. 対象レベル → フルマラソンのタイム
         sub2.5=2:30, sub3=3:00, sub3.5=3:30, sub4=4:00, sub5=5:00, 完走=6:00
    2. フルマラソンのペース × 用途の係数 = その組み合わせの想定ペース
         トラック 0.82 / レース:5km未満 0.88 / インターバル 0.88 / レース:10km 0.92 /
         テンポ走 0.94 / レース:ハーフ 0.96 / レース:フルマラソン 1.00 /
         ロング走 1.12 / ジョグ 1.25 / リカバリー 1.35
         ウォーキングはレベルによらず 11:00/km、トレイルは路面の区分なので使わない
         （レース距離の係数はリーゲルの式 T2 = T1 ×(D2/D1)^1.06 による）
    3. 全組み合わせの平均速度（km/h）を点数にする
         P = （平均速度 − 12）÷ 1.2   … 12km/h(5:00/km)で 0、18km/h(3:20/km)で +5、6km/h(10:00/km)で −5

  重量点 W： W = （230 − 重量g）÷ 16   … 150g で +5、230g で 0、310g で −5
             重量がないときだけ（評価_軽量性 − 5.5）× 10/9 を使う

  ・各点数は −5〜+5 で止め、最後に小数第1位で四捨五入
  ・用途→対象レベルがないシューズは、速さを空欄（null）にする（推測で埋めない）
──────────────────────────────────────────
"""
import argparse
import csv
import colorsys
import hashlib
import io
import json
import os
import re
import sys
from datetime import date

# ---------- ルールの数値（変えるときはここだけ） ----------
REB_W, STAB_W = 0.6, 0.4
PACE_W, WEIGHT_W = 0.7, 0.3
MARATHON_MIN = {'sub2.5': 150, 'sub3': 180, 'sub3.5': 210, 'sub4': 240, 'sub5': 300, '完走': 360}
USE_FACTOR = {
    'トラック': 0.82, 'レース:5km未満': 0.88, 'インターバル': 0.88, 'レース:10km': 0.92,
    'テンポ走': 0.94, 'レース:ハーフ': 0.96, 'レース:フルマラソン': 1.00,
    'ロング走': 1.12, 'ジョグ': 1.25, 'リカバリー': 1.35,
}
WALK_PACE_SEC = 660          # ウォーキング 11:00/km
IGNORED_USES = {'トレイル'}
SPEED_CENTER_KMH, SPEED_KMH_PER_POINT = 12.0, 1.2
REBOUND_INDEX_COLUMNS = ('反発指標_リア', '反発指標_ミッド', '反発指標_フォア')
REBOUND_INDEX_MEAN, REBOUND_INDEX_PER_POINT, REBOUND_SCORE_MEAN = 1870.0, 190.0, 6.1
WEIGHT_CENTER_G, WEIGHT_G_PER_POINT = 230.0, 16.0

KNOWN_COLORS = {
    'nike': '#ef6c1a', 'adidas': '#3d4450', 'asics': '#1e63c8', 'hoka': '#0f9d8a',
    'saucony': '#c92a62', 'mizuno': '#5b3fc4', 'puma': '#d23a2f', 'newbalance': '#5b8a1c',
    'on': '#0e7490', 'brooks': '#b7791f',
}


def clamp(v, lo=-5.0, hi=5.0):
    return max(lo, min(hi, v))


def r1(v):
    """小数第1位で四捨五入（0.05 → 0.1 のように常に切り上げ側）"""
    if v is None:
        return None
    sign = -1 if v < 0 else 1
    return sign * int(abs(v) * 10 + 0.5 + 1e-9) / 10


def to_num(s):
    s = (s or '').strip().replace(',', '')
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def read_csv(path):
    raw = open(path, 'rb').read()
    for enc in ('utf-8-sig', 'cp932'):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        sys.exit('CSV の文字コードを判別できませんでした（UTF-8 か Shift_JIS で保存してください）')
    return list(csv.DictReader(io.StringIO(text, newline='')))   # セル内の改行にも対応


def parse_use_levels(value):
    """'レース:ハーフ: sub2.5/sub3; ジョグ: sub4' → [('レース:ハーフ','sub2.5'), ...]"""
    pairs = []
    for part in (value or '').split(';'):
        part = part.strip()
        if ':' not in part:
            continue
        use, levels = part.rsplit(':', 1)
        for lv in levels.split('/'):
            lv = lv.strip()
            if lv in MARATHON_MIN:
                pairs.append((use.strip(), lv))
    return pairs


def pace_point(pairs):
    speeds = []
    for use, lv in pairs:
        if use in IGNORED_USES:
            continue
        if use == 'ウォーキング':
            pace = WALK_PACE_SEC
        elif use in USE_FACTOR:
            pace = MARATHON_MIN[lv] * 60 / 42.195 * USE_FACTOR[use]
        else:
            continue
        speeds.append(3600 / pace)
    if not speeds:
        return None, None
    kmh = sum(speeds) / len(speeds)
    return clamp((kmh - SPEED_CENTER_KMH) / SPEED_KMH_PER_POINT), kmh


def weight_point(weight, lightness):
    if weight is not None:
        return clamp((WEIGHT_CENTER_G - weight) / WEIGHT_G_PER_POINT)
    if lightness is not None:
        return clamp((lightness - 5.5) * 10 / 9)
    return None


def rebound_input(r):
    """反発性として使う値と、その根拠（実測／評価）を返す"""
    idx = [to_num(r.get(c)) for c in REBOUND_INDEX_COLUMNS]
    if all(v is not None for v in idx):
        avg = sum(idx) / len(idx)
        score = max(1.0, min(10.0, REBOUND_SCORE_MEAN + (avg - REBOUND_INDEX_MEAN) / REBOUND_INDEX_PER_POINT))
        return score, '実測', avg
    return to_num(r.get('評価_反発性')), '評価', None


def rebound_point(reb, stab):
    if reb is None or stab is None:
        return None
    return clamp(10 / 9 * (REB_W * (reb - 5.5) - STAB_W * (stab - 5.5)))


def brand_color(key, index):
    k = re.sub(r'[\s_-]', '', key.lower())
    if k in KNOWN_COLORS:
        return KNOWN_COLORS[k]
    h = (index * 0.618033988749895) % 1.0           # 色相を黄金比でずらして被りにくくする
    r, g, b = colorsys.hls_to_rgb(h, 0.42, 0.55)
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))


def short_id(prefix, *parts):
    return prefix + hashlib.sha1('/'.join(parts).encode('utf-8')).hexdigest()[:7]


def main():
    ap = argparse.ArgumentParser(description='シューズDBのCSVから data.js を作る')
    ap.add_argument('csv')
    ap.add_argument('-o', '--output', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data.js'))
    ap.add_argument('--include-spikes', action='store_true')
    ap.add_argument('--include-private', action='store_true')
    args = ap.parse_args()

    rows = read_csv(args.csv)
    brands, shoes, report = {}, [], []
    skipped = {'スパイク': 0, '非公開': 0}

    for r in rows:
        category = (r.get('カテゴリ') or '').strip()
        if category == 'スパイク' and not args.include_spikes:
            skipped['スパイク'] += 1
            continue
        if (r.get('モデル公開') or '').strip() == '非公開' and not args.include_private:
            skipped['非公開'] += 1
            continue
        bkey = (r.get('ブランドID') or r.get('ブランド') or '').strip()
        bname = (r.get('ブランド') or bkey).strip()
        name = (r.get('モデル') or '').strip()
        if not bkey or not name:
            continue
        if bkey not in brands:
            brands[bkey] = {'id': short_id('b', bkey), 'name': bname, 'color': brand_color(bkey, len(brands))}

        weight = to_num(r.get('重量(g)'))
        price = to_num(r.get('定価(円)'))
        year = to_num(r.get('発売年'))
        reb, reb_src, reb_idx = rebound_input(r)
        stab = to_num(r.get('評価_安定性'))
        light = to_num(r.get('評価_軽量性'))
        pairs = parse_use_levels(r.get('用途→対象レベル'))
        P, kmh = pace_point(pairs)
        W = weight_point(weight, light)
        speed = r1(clamp(PACE_W * P + WEIGHT_W * W)) if P is not None and W is not None else None
        rebound = r1(rebound_point(reb, stab))

        uses = []
        for u, _ in pairs:
            if u not in uses:
                uses.append(u)
        note = '・'.join(uses)
        if len(note) > 60:
            note = note[:59] + '…'
        if reb_src == '実測':
            note = (note + '（反発は実測値から算出）') if note else '反発は実測値から算出'
        image = (r.get('代表画像URL') or '').strip()
        shoe = {
            'id': short_id('m', bkey, (r.get('モデルID') or name).strip()),
            'brandId': brands[bkey]['id'],
            'name': name,
            'year': int(year) if year else None,
            'speed': speed,
            'rebound': rebound,
            'weight': int(weight) if weight is not None else None,
            'price': int(price) if price is not None else None,
            'image': image if image.startswith('https://') else None,
            'note': note,
        }
        if shoe['year'] is None:
            continue
        shoes.append(shoe)
        report.append({
            'ブランド': bname, 'モデル': name, '発売年': shoe['year'],
            '反発の根拠': reb_src, '反発指標の平均': round(reb_idx) if reb_idx else '',
            '評価_反発性': to_num(r.get('評価_反発性')), '反発性（計算に使った値）': round(reb, 2) if reb is not None else '',
            '評価_安定性': stab, '反発': rebound,
            '用途×レベルの数': len(pairs), '平均想定速度(km/h)': round(kmh, 2) if kmh else '',
            'ペース点P': r1(P) if P is not None else '', '重量(g)': weight, '重量点W': r1(W) if W is not None else '',
            '速さ': speed if speed is not None else '保留（用途→対象レベルなし）',
        })

    shoes.sort(key=lambda s: (s['year'], s['name']))
    out = {'brands': sorted(brands.values(), key=lambda b: b['name'].lower()), 'shoes': shoes}
    header = [
        f'// ランニングシューズ 3Dマップのデータ（{os.path.basename(args.csv)} から {date.today().isoformat()} に自動生成）',
        '// speed:   -5（遅い）〜 +5（速い）    … 用途×対象レベルの想定ペースと重量から算出',
        '// rebound: -5（低反発・安定）〜 +5（高反発・不安定） … 反発指標（実測。ないときは評価_反発性）と評価_安定性から算出',
        '// weight:  重さ（g） / price: 定価（円） / year: 発売年',
        '// 計算ルールは tools/csv_to_datajs.py の冒頭を参照',
    ]
    with open(args.output, 'w', encoding='utf-8', newline='\n') as fp:
        fp.write('\n'.join(header) + '\nwindow.SHOE_DATA = ' + json.dumps(out, ensure_ascii=False, indent=2) + ';\n')

    stamp = re.search(r'(\d{8})', os.path.basename(args.csv))
    rpath = os.path.join(os.path.dirname(os.path.abspath(args.csv)), f'score_report_{stamp.group(1) if stamp else "latest"}.csv')
    with open(rpath, 'w', encoding='utf-8-sig', newline='') as fp:
        w = csv.DictWriter(fp, fieldnames=list(report[0].keys()))
        w.writeheader()
        w.writerows(report)

    held = sum(1 for s in shoes if s['speed'] is None)
    measured = sum(1 for x in report if x['反発の根拠'] == '実測')
    print(f'data.js を書き出しました: {os.path.abspath(args.output)}')
    print(f'  ブランド {len(out["brands"])} / シューズ {len(shoes)}（速さ保留 {held}、反発を実測値から出したもの {measured}）')
    print(f'  除外: スパイク {skipped["スパイク"]} / 非公開 {skipped["非公開"]}')
    print(f'計算の内訳: {rpath}')


if __name__ == '__main__':
    main()
