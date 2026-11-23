"""FIXED checks. Usage: python3 check.py <build_dir> [--config deck.json]

Always checks:  no Type 3 fonts, zero /SMask (blurred shadows or alpha images), only JPEG images.
From the deck config (build_dir/deck.json, or --config):
  "banned":               words or phrases that must not appear in the slide text (case-insensitive)
  "allowed_placeholders": bracketed text allowed on a slide, e.g. ["[reviewer name]"]; any other [..] fails
Then rasterizes the PDF itself to build_dir/pages/ (p-01.png ...) for the page-by-page review.
"""
import json
import os
import re
import subprocess
import sys

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
d = args[0]
cfg_path = args[args.index("--config") + 1] if "--config" in args else os.path.join(d, "deck.json")
cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
banned = [w.lower() for w in cfg.get("banned", [])]
allowed = {p.lower() for p in cfg.get("allowed_placeholders", [])}

pdf = os.path.join(d, "deck.pdf")
html = open(os.path.join(d, "deck.html")).read()
fails = []

fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
if "Type 3" in fonts:
    fails.append("Type 3 font in PDF (use static TTF fonts)")
raw = open(pdf, "rb").read()
if raw.count(b"/SMask"):
    fails.append(f"{raw.count(b'/SMask')} /SMask (blurred shadow, opacity or alpha image)")
imgs = subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
bad = [l for l in imgs if " jpeg " not in l]
if bad:
    fails.append(f"{len(bad)} non-JPEG images (draw shapes as SVG/CSS; photos as JPEG with no alpha)")

text = re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>", "", html, flags=re.S))
text = re.sub(r"\s+", " ", text).lower()
for w in banned:
    if re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", text):
        fails.append(f'banned: "{w}"')
br = set(re.findall(r"\[[^\]]{1,40}\]", text)) - allowed
if br:
    fails.append(f"placeholders: {sorted(br)}")

os.makedirs(os.path.join(d, "pages"), exist_ok=True)
subprocess.run(["pdftoppm", "-r", "96", "-png", pdf, os.path.join(d, "pages", "p")])
n = len([f for f in os.listdir(os.path.join(d, "pages")) if f.endswith(".png")])
print("FAIL\n- " + "\n- ".join(fails) if fails else
      f"PASS: fonts, SMask, images, words ({len(banned)} banned). Now look at all {n} images in {os.path.join(d, 'pages')}/.")
sys.exit(1 if fails else 0)
