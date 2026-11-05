"""元画像（images_original フォルダ）を、サイト用に小さくして images フォルダに書き出すスクリプト。

使い方（リポジトリのフォルダで）:
    pip install pillow            ← 最初の1回だけ
    python tools/shrink_images.py
    python tools/link_images.py

- 長い辺を 800px までに縮め、WebP 形式（透過はそのまま）で保存します。1枚あたり数十KBになります
- ファイル名は元のまま（拡張子だけ .webp）なので、link_images.py の結びつけはそのまま使えます
- 元画像は images_original に残ります（.gitignore で GitHub には上げません）
- すでに書き出し済みで、元画像が新しくなっていないものは飛ばします
"""
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow が入っていません。先に  pip install pillow  を実行してください。")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images_original"
DST = ROOT / "images"
MAX_SIDE = 800      # 長い辺の最大ピクセル数
QUALITY = 82        # WebP の画質（0〜100）
EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def main():
    if not SRC.is_dir():
        sys.exit(f"{SRC.name} フォルダがありません。元画像を {SRC} に置いてください。")
    DST.mkdir(exist_ok=True)
    files = sorted(p for p in SRC.iterdir() if p.is_file() and p.suffix.lower() in EXTS)
    done = skipped = 0
    before = after = 0
    for p in files:
        out = DST / (p.stem + ".webp")
        if out.exists() and out.stat().st_mtime >= p.stat().st_mtime:
            skipped += 1
            continue
        try:
            with Image.open(p) as im:
                im = im.convert("RGBA" if ("A" in im.getbands() or "transparency" in im.info) else "RGB")
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
                im.save(out, "WEBP", quality=QUALITY, method=6)
        except Exception as e:  # 壊れた画像などは飛ばして続ける
            print(f"  [失敗] {p.name}: {e}")
            continue
        before += p.stat().st_size
        after += out.stat().st_size
        done += 1
    print(f"{done} 枚を縮小しました（{before / 1e6:.1f}MB → {after / 1e6:.1f}MB）。書き出し済みで飛ばしたもの: {skipped} 枚")


if __name__ == "__main__":
    main()
