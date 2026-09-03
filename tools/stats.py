#!/usr/bin/env python3
"""Progress report for WILDHOLD."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wc = lambda t: len(re.findall(r"\b[\w'-]+\b", t))

books = sorted(glob.glob(os.path.join(ROOT, "series", "book-*")))
print(f"\n  WILDHOLD — progress\n  {'='*46}")
gw = gc = 0
for b in books:
    n = re.search(r"book-(\d+)-", b).group(1)
    title = os.path.basename(b).split("-", 2)[2].replace("-", " ").title()
    chs = sorted(glob.glob(os.path.join(b, "chapters", "ch-*.md")))
    words = sum(wc(open(c, encoding="utf-8").read()) for c in chs)
    gw += words; gc += len(chs)
    bar = "#" * min(30, len(chs)) + "." * max(0, 30 - len(chs))
    print(f"  {n}. {title:<24} [{bar}] {len(chs):>2}ch {words:>7,}w")
print(f"  {'='*46}")
print(f"  {len(books)}/25 books · {gc} chapters · {gw:,} words")
if gc:
    print(f"  avg chapter: {gw//gc:,} words")
print(f"  series target: ~2,125,000 words ({gw/2125000*100:.1f}% complete)\n")
