#!/usr/bin/env python3
"""
docs/images/_raw/*.png を原本に、edits.yaml の定義を適用して
docs/images/*.webp と index.html 用 *.png を再生成する。

Usage:
  python3 tools/images/regenerate.py            # 全再生成
  python3 tools/images/regenerate.py --dry-run  # 何が出力されるか表示のみ
  python3 tools/images/regenerate.py diff_align # 特定ファイルのみ
"""
import os
import sys
import glob
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow が必要です: pip install Pillow")

try:
    import yaml
except ImportError:
    sys.exit("PyYAML が必要です: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent.parent
IMG_DIR = ROOT / "docs" / "images"
RAW_DIR = IMG_DIR / "_raw"
EDITS_YAML = Path(__file__).resolve().parent / "edits.yaml"

TARGET_MAX_WIDTH = 720
WEBP_QUALITY = 85
WEBP_METHOD = 6  # 0(fast)〜6(best compression)

# index.html が参照する dst。これらは WebP に加えて PNG も出力する。
# 2026-04-20: index.html も全面 webp 化したので現在は空。必要になったら再度追加。
INDEX_HTML_REFS: set[str] = set()


def load_edits():
    """edits.yaml を読み、dst -> spec の dict を返す"""
    if not EDITS_YAML.exists():
        return {}
    with open(EDITS_YAML) as f:
        data = yaml.safe_load(f) or {}
    entries = data.get("entries", []) or []
    out = {}
    for e in entries:
        dst = e.get("dst")
        if not dst:
            continue
        out[dst] = e
    return out


def apply_ops(im: Image.Image, ops: list) -> Image.Image:
    for op in ops or []:
        if "mask" in op:
            vals = op["mask"]
            x, y, w, h = vals[:4]
            color = vals[4] if len(vals) > 4 else "#D5D5D5"
            draw = ImageDraw.Draw(im)
            draw.rectangle([x, y, x + w, y + h], fill=color)
        elif "highlight" in op:
            # 矩形の枠線を描く（中身は透過のまま）
            vals = op["highlight"]
            x, y, w, h = vals[:4]
            color = vals[4] if len(vals) > 4 else "#E53935"  # Material Red 600
            stroke = vals[5] if len(vals) > 5 else 6
            draw = ImageDraw.Draw(im)
            draw.rectangle([x, y, x + w, y + h], outline=color, width=stroke)
        elif "crop" in op:
            x, y, w, h = op["crop"]
            im = im.crop((x, y, x + w, y + h))
        elif "resize" in op:
            width = op["resize"] if not isinstance(op["resize"], list) else op["resize"][0]
            ratio = width / im.width
            im = im.resize((width, int(im.height * ratio)), Image.LANCZOS)
        else:
            raise ValueError(f"unknown op: {op}")
    return im


def downscale(im: Image.Image, max_w: int = TARGET_MAX_WIDTH) -> Image.Image:
    if im.width <= max_w:
        return im
    ratio = max_w / im.width
    return im.resize((max_w, int(im.height * ratio)), Image.LANCZOS)


def process_one(raw_path: Path, dst_name: str, edits: dict, dry: bool):
    im = Image.open(raw_path)
    spec = edits.get(dst_name, {})
    if spec:
        im = apply_ops(im, spec.get("ops"))
    im = downscale(im, TARGET_MAX_WIDTH)

    stem = dst_name.rsplit(".", 1)[0]
    webp_out = IMG_DIR / f"{stem}.webp"
    png_out = IMG_DIR / f"{stem}.png"

    if dry:
        print(f"  [dry] {webp_out.name}")
        if dst_name in INDEX_HTML_REFS:
            print(f"  [dry] {png_out.name}")
        return

    # RGBA を保ったまま WebP 出力
    im.save(webp_out, "WEBP", quality=WEBP_QUALITY, method=WEBP_METHOD)
    if dst_name in INDEX_HTML_REFS:
        im.save(png_out, "PNG", optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="*", help="再生成対象（stem 名、未指定で全部）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not RAW_DIR.exists():
        sys.exit(f"原本ディレクトリが見つかりません: {RAW_DIR}")

    edits = load_edits()

    # 処理対象を決める
    # 原本 _raw/*.png を起点に、同名 dst を生成
    # edits.yaml で src/dst が違うエントリは追加で処理
    jobs = []  # (raw_path, dst_name)
    processed_dsts = set()

    # 1. edits.yaml のエントリ（src 明示 or 省略）
    for dst_name, spec in edits.items():
        src_name = spec.get("src", dst_name)
        raw_path = RAW_DIR / src_name
        if not raw_path.exists():
            print(f"⚠️  原本なし: _raw/{src_name} (for dst {dst_name})", file=sys.stderr)
            continue
        jobs.append((raw_path, dst_name))
        processed_dsts.add(dst_name)

    # 2. _raw の全ファイル（edits 未定義 = そのまま downscale）
    for raw_path in sorted(RAW_DIR.glob("*.png")):
        name = raw_path.name
        if name in processed_dsts:
            continue  # 既に edits で処理済み
        jobs.append((raw_path, name))

    # フィルタ
    if args.targets:
        stems = {t.rsplit(".", 1)[0] for t in args.targets}
        jobs = [(r, d) for r, d in jobs if d.rsplit(".", 1)[0] in stems]
        if not jobs:
            sys.exit(f"対象なし: {args.targets}")

    print(f"処理対象: {len(jobs)} 件")
    for raw_path, dst_name in jobs:
        edit_mark = " (edited)" if dst_name in edits else ""
        index_mark = " +png" if dst_name in INDEX_HTML_REFS else ""
        print(f"  {raw_path.name} → {dst_name}{edit_mark}{index_mark}")
        process_one(raw_path, dst_name, edits, args.dry_run)

    if not args.dry_run:
        # 結果サイズ表示
        webp_total = sum(f.stat().st_size for f in IMG_DIR.glob("*.webp"))
        png_total = sum(f.stat().st_size for f in IMG_DIR.glob("*.png") if f.parent == IMG_DIR)
        print(f"\n✅ 完了")
        print(f"  WebP: {len(list(IMG_DIR.glob('*.webp')))} files, {webp_total/1024/1024:.1f} MB")
        print(f"  PNG (index.html用): {len(list(IMG_DIR.glob('*.png')))} files, {png_total/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
