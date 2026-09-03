#!/usr/bin/env python3
"""Consolidate a WILDHOLD book's chapter files into a single reader-facing manuscript.

Usage:
    python3 tools/consolidate.py 1
    python3 tools/consolidate.py 1 --final     # mark complete, add stats footer
    python3 tools/consolidate.py --all
"""
import sys, re, glob, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIES_TITLE = "WILDHOLD"


def find_book(n):
    hits = sorted(glob.glob(os.path.join(ROOT, "series", f"book-{n:02d}-*")))
    return hits[0] if hits else None


def title_from_dir(d):
    slug = os.path.basename(d).split("-", 2)[2]
    return slug.replace("-", " ").title()


def wc(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def consolidate(n, final=False):
    bookdir = find_book(n)
    if not bookdir:
        print(f"  book {n:02d}: no directory")
        return None
    chapters = sorted(glob.glob(os.path.join(bookdir, "chapters", "ch-*.md")))
    if not chapters:
        print(f"  book {n:02d}: no chapters yet")
        return None

    title = title_from_dir(bookdir)
    out = [
        f"# {SERIES_TITLE}",
        f"## Book {n}: {title}",
        "",
        "*A progression fantasy.*",
        "",
        "---",
        "",
    ]
    if not final:
        out += [
            f"> **Work in progress.** {len(chapters)} chapters written so far. "
            f"New chapters are appended as they are finished.",
            "",
            "---",
            "",
        ]

    total = 0
    for path in chapters:
        with open(path, encoding="utf-8") as f:
            body = f.read().strip()
        total += wc(body)
        out.append(body)
        out.append("\n\n---\n")

    if final:
        out.append(f"\n*End of Book {n}: {title}.*\n")
    out.append(
        f"\n<!-- {len(chapters)} chapters · {total:,} words · "
        f"consolidated {datetime.date.today().isoformat()} -->\n"
    )

    safe = title.replace(" ", "-")
    dest = os.path.join(ROOT, "manuscript", f"Book-{n:02d}-{safe}.md")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"  book {n:02d}: {len(chapters):3d} ch · {total:>7,} words -> {os.path.relpath(dest, ROOT)}")
    return (n, title, len(chapters), total)


def write_index(rows):
    lines = [f"# {SERIES_TITLE} — Manuscripts", "",
             "Reader-facing consolidated books. Regenerated automatically as chapters land.",
             "", "| Book | Title | Chapters | Words |", "|---|---|---|---|"]
    grand = 0
    for n, title, ch, words in rows:
        safe = title.replace(" ", "-")
        lines.append(f"| {n} | [{title}](Book-{n:02d}-{safe}.md) | {ch} | {words:,} |")
        grand += words
    lines += ["", f"**Total: {grand:,} words across {len(rows)} book(s).**", ""]
    with open(os.path.join(ROOT, "manuscript", "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    args = sys.argv[1:]
    final = "--final" in args
    args = [a for a in args if not a.startswith("--")]
    if "--all" in sys.argv or not args:
        nums = sorted(int(re.search(r"book-(\d+)-", p).group(1))
                      for p in glob.glob(os.path.join(ROOT, "series", "book-*")))
    else:
        nums = [int(a) for a in args]
    rows = [r for r in (consolidate(n, final) for n in nums) if r]
    all_rows = []
    for p in sorted(glob.glob(os.path.join(ROOT, "series", "book-*"))):
        n = int(re.search(r"book-(\d+)-", p).group(1))
        chs = glob.glob(os.path.join(p, "chapters", "ch-*.md"))
        if chs:
            words = sum(wc(open(c, encoding="utf-8").read()) for c in chs)
            all_rows.append((n, title_from_dir(p), len(chs), words))
    if all_rows:
        write_index(all_rows)
