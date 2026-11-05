#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canva から書き出したシューズ画像（1.png, 2.png …）を、対応表のモデル名を付けたファイル名でコピーするスクリプト。
元の画像は変更しません。Python 3.8 以降の標準機能だけで動きます。

使い方（画像・対応表・このスクリプトを同じフォルダに置いて）:
    python rename_shoe_images.py

    --images  フォルダ      書き出した画像のフォルダ（省略時はこのスクリプトと同じフォルダ）
    --table   CSVファイル   対応表（省略時は「シューズ画像_モデル対応表.csv」）
    --out     フォルダ      出力先（省略時は「名前付き」フォルダ）

出力するファイル名の例:
    012_asics_メタスピード エッジ トウキョウ.png
    053_PUMA_ヴェロシティ ニトロ 4_要確認.png     … 確度が「低」のもの
    364_判別できず.png

対応表の「モデル（DB表記）」列を Excel で直して保存し、もう一度実行すれば名前も更新されます
（出力先フォルダは毎回作り直します）。
"""
import argparse
import csv
import os
import re
import shutil
import sys

BAD_CHARS = re.compile(r'[\\/:*?"<>|]')   # Windows のファイル名に使えない文字


def clean(text):
    text = text.replace('\u200b', '')            # 見えない文字を除く
    text = BAD_CHARS.sub('-', text)              # S/LAB → S-LAB
    return re.sub(r'\s+', ' ', text).strip()


def decode_zip_name(name):
    """zip の展開環境によって「#U30e1」のように残った日本語を元に戻す"""
    return re.sub(r'#U([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), name)


def find_source(folder, file_name, number, index):
    for cand in (file_name, f'{number}.png'):
        path = os.path.join(folder, cand)
        if os.path.isfile(path):
            return path
    return index.get(file_name)


def new_name(row):
    n = int(row['画像番号'])
    brand, model, conf = row['ブランド'].strip(), row['モデル（DB表記）'].strip(), row['確度'].strip()
    if model.startswith('（DBに該当なし）'):
        label = 'DBになし_' + model.replace('（DBに該当なし）', '')
    elif model.startswith('（判別できず）') or not model:
        label = '判別できず'
    else:
        label = f'{brand}_{model}' if brand and not brand.startswith('（') else model
    suffix = '_要確認' if conf == '低' and label != '判別できず' else ''
    return clean(f'{n:03d}_{label}{suffix}') + '.png'


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description='シューズ画像にモデル名を付けてコピーする')
    ap.add_argument('--images', default=here)
    ap.add_argument('--table', default=os.path.join(here, 'シューズ画像_モデル対応表.csv'))
    ap.add_argument('--out', default=os.path.join(here, '名前付き'))
    args = ap.parse_args()

    with open(args.table, encoding='utf-8-sig', newline='') as fp:
        rows = list(csv.DictReader(fp))
    index = {decode_zip_name(f): os.path.join(args.images, f) for f in os.listdir(args.images)}

    if os.path.isdir(args.out):
        shutil.rmtree(args.out)
    os.makedirs(args.out)

    done, missing = 0, []
    for row in rows:
        src = find_source(args.images, row['ファイル名'], row['画像番号'], index)
        if not src:
            missing.append(row['画像番号'])
            continue
        shutil.copy2(src, os.path.join(args.out, new_name(row)))
        done += 1

    print(f'{done} 枚を「{args.out}」に名前を付けてコピーしました。')
    if missing:
        print(f'見つからなかった画像: {", ".join(missing)}', file=sys.stderr)


if __name__ == '__main__':
    main()
