"""images フォルダの画像とシューズを、ファイル名で結びつけて images.js を作るスクリプト。

使い方（リポジトリのフォルダで）:
    python tools/link_images.py

ファイル名の形:  012_asics_メタスピード エッジ トウキョウ.png
    先頭の番号     … 何でもよい（並べ替え用）。なくてもよい
    ブランド名     … data.js のブランド名と照合（大文字小文字・空白の違いは無視）
    残り           … この中に「シューズ名」が含まれていれば結びつける

結びつけのルール:
    - 末尾の「_要確認」は無視して比べる
    - ブランドが一致するシューズの中から、名前がファイル名に含まれるものを探す
      （全角/半角、大文字/小文字、空白の有無の違いは無視）
    - 複数あてはまるときは、いちばん長い名前を選ぶ
      （「メタスピード エッジ」と「メタスピード エッジ トウキョウ」なら後者）
    - 名前のすぐ後ろに数字が続く場合は別モデルとみなす
      （「ハイペリオン 2」の画像を「ハイペリオン」に、「ノヴァブラスト 30」を「ノヴァブラスト 3」に付けない）
    - 1つのシューズに複数の画像が当たったときは、
      名前がぴったり同じもの → 「_要確認」が付いていないもの → 番号が小さいもの の順で選ぶ
    - 名前の一部だけが一致した画像は、レポートで「部分一致」と表示する（目で確認してください）
    - 「判別できず」「DBになし」の画像は対象外として扱う

出力:
    images.js                  … ブラウザが読む対応表（index.html が data.js の画像より優先して使う）
    image_link_report.csv      … 結びつけ結果の一覧（Excel で開けます。.gitignore 推奨）
Python 3.8 以降。追加インストールは不要。
"""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DATA_JS = ROOT / "data.js"
IMAGE_DIR = ROOT / "images"
OUT_JS = ROOT / "images.js"
REPORT = ROOT / "image_link_report.csv"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

# ファイル名のブランド表記が data.js と違うときの読み替え（左：ファイル名側、右：data.js のブランド名）
BRAND_ALIASES = {
    "hokaoneone": "HOKA",
    "nb": "NewBalance",
    "ua": "UNDER ARMOUR",
    "tnf": "THE NORTH FACE",
}


def norm(s: str) -> str:
    """全角半角・大文字小文字をそろえ、区切り文字を1つの空白にする。"""
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[\s_\u3000・]+", " ", s)
    return s.strip()


def squash(s: str) -> str:
    return s.replace(" ", "")


def load_data():
    text = DATA_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.SHOE_DATA\s*=\s*(\{.*\})\s*;?\s*$", text, re.S)
    if not m:
        sys.exit("data.js から window.SHOE_DATA を読み取れませんでした。")
    return json.loads(m.group(1))


def split_filename(stem: str):
    """'012_asics_メタスピード エッジ' → ('012', 'asics', 'メタスピード エッジ')"""
    parts = stem.split("_")
    num = parts.pop(0) if parts and parts[0].strip().isdigit() else ""
    if len(parts) >= 2:
        return num, parts[0], "_".join(parts[1:])
    return num, "", "_".join(parts)


def match(hay_sq: str, name_sq: str):
    """名前がファイル名に含まれていれば 'exact' / 'partial'、別モデルや不一致なら None"""
    if not name_sq:
        return None
    if hay_sq == name_sq:
        return "exact"
    i = hay_sq.find(name_sq)
    if i < 0:
        return None
    after = hay_sq[i + len(name_sq):]
    if after[:1].isdigit() or after[:1] in ("."):
        return None          # 「ハイペリオン」+「2」のように番号違いは別モデル
    return "partial"


SKIP_WORDS = ("判別できず", "DBになし")


def main():
    if not IMAGE_DIR.is_dir():
        sys.exit(f"{IMAGE_DIR} フォルダがありません。画像をここに置いてください。")
    data = load_data()
    brands = {b["id"]: b["name"] for b in data["brands"]}
    brand_by_norm = {squash(norm(n)): n for n in brands.values()}
    for k, v in BRAND_ALIASES.items():
        brand_by_norm.setdefault(squash(norm(k)), v)

    shoes = [
        {"id": s["id"], "brand": brands.get(s["brandId"], ""), "name": s["name"],
         "n": norm(s["name"]), "year": s.get("year")}
        for s in data["shoes"]
    ]

    files = sorted(p for p in IMAGE_DIR.iterdir() if p.is_file() and p.suffix.lower() in EXTS)
    info = {}          # ファイル名 → [結果, メモ]
    best = {}          # シューズid → (並び順キー, ファイル, 一致の種類)
    matched_to = {}    # ファイル名 → (シューズ, 一致の種類)

    for p in files:
        stem = unicodedata.normalize("NFC", p.stem)
        if any(w in stem for w in SKIP_WORDS):
            info[p.name] = ["対象外", ""]
            continue
        unsure = "要確認" in stem
        stem_clean = re.sub(r"[_\s]*要確認$", "", stem)
        _, brand_part, model_part = split_filename(stem_clean)
        brand = brand_by_norm.get(squash(norm(brand_part))) if brand_part else None
        if brand_part and not brand:
            info[p.name] = ["見つからない", f"ブランド「{brand_part}」が data.js にない"]
            continue
        hay = squash(norm(model_part))
        pool = [s for s in shoes if brand is None or s["brand"] == brand]
        cands = [(s, match(hay, squash(s["n"]))) for s in pool]
        cands = [(s, m) for s, m in cands if m]
        if not cands:
            info[p.name] = ["見つからない", "同じ名前のシューズが data.js にない"]
            continue
        longest = max(len(squash(s["n"])) for s, _ in cands)
        for s, m in cands:
            if len(squash(s["n"])) != longest:
                continue
            key = (m != "exact", unsure, p.name)
            if s["id"] not in best or key < best[s["id"]][0]:
                best[s["id"]] = (key, p, m)
            matched_to.setdefault(p.name, (s, m))

    links = {sid: {"url": "images/" + quote(p.name), "file": p.name} for sid, (_, p, _) in best.items()}
    used = {v["file"]: sid for sid, v in links.items()}
    shoe_by_id = {s["id"]: s for s in shoes}
    rows = []
    for p in files:
        label = lambda s: f"{s['brand']} {s['name']} ({s['year']})"
        if p.name in used:
            s = shoe_by_id[used[p.name]]
            m = best[s["id"]][2]
            rows.append([p.name, "OK" if m == "exact" else "部分一致", label(s),
                         "" if m == "exact" else "名前の一部だけ一致。正しい画像か確認してください"])
        elif p.name in matched_to:
            s, _ = matched_to[p.name]
            rows.append([p.name, "重複（不使用）", label(s), f"{links[s['id']]['file']} を使用中"])
        else:
            rows.append([p.name] + [info.get(p.name, ["見つからない", ""])[0], ""] + [info.get(p.name, ["", ""])[1]])

    linked = {k: v["url"] for k, v in links.items()}
    missing = [s for s in shoes if s["id"] not in linked]
    for s in missing:
        rows.append(["", "画像なし", f"{s['brand']} {s['name']} ({s['year']})", ""])

    OUT_JS.write_text(
        "// シューズ画像の対応表（tools/link_images.py で自動生成。手で直さず、画像のファイル名を直して再実行）\n"
        "// キーは data.js の shoes の id、値は images フォルダの画像パス\n"
        "window.SHOE_IMAGES = " + json.dumps(linked, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    with REPORT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["画像ファイル", "結果", "結びついたシューズ", "メモ"])
        w.writerows(rows)

    from collections import Counter
    c = Counter(r[1] for r in rows if r[0])
    print(f"画像 {len(files)} 枚 → シューズ {len(linked)} / {len(shoes)} 足に結びつけました。")
    print("  内訳: " + "、".join(f"{k} {v}枚" for k, v in c.items()))
    print(f"  画像がないシューズ: {len(missing)} 足")
    for r in rows:
        if r[1] == "部分一致":
            print(f"  [部分一致] {r[0]} → {r[2]}")
    print(f"詳しくは {REPORT.name} を Excel で開いて確認してください。出力: {OUT_JS.name}")

if __name__ == "__main__":
    main()
