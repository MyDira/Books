#!/usr/bin/env python3
"""Mechanical style-quota check for WILDHOLD.

Everything the line-editor agent catches by grep, run locally for free.
Run it every few chapters; run it before every audit; believe the numbers, not your feel.

    python3 tools/tics.py                 # whole series
    python3 tools/tics.py 2               # book 2
    python3 tools/tics.py 2 --from 11     # book 2, chapters 11+
"""
import re, sys, glob, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = lambda t: len(re.findall(r"\b[\w'-]+\b", t))
OK, BAD, WARN = "  ok ", " FAIL", " warn"

# quota, per 1,000 words unless noted
QUOTAS = {
    "em_dash_per_1k": 3.0,
    "which_was_per_book": 30,   # ~1 per 2,500 words. It is the voice; the fault is clustering.
    "awhile_per_book": 60,      # the whole vagueness family; ~1 per 1,200 words is normal prose
    "he_para_pct": 18.0,
}

NUMBER_WORDS = ("one two three four five six seven eight nine ten eleven twelve thirteen "
                "fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty "
                "fifty sixty seventy eighty ninety hundred thousand").split()

LIFESPAN = re.compile(
    r"(for the (?:next|rest of)[^.]{0,40}(?:years|life|his life)"
    r"|when he (?:was|is) (?:a hundred|\w+ty|\w+teen|sixty|eighty|thirty|forty|fifty)"
    r"|would have them at \w+"
    r"|(?:sixty|eighty|three hundred|two hundred) years old"
    r"|for the rest of (?:his|her|their) life)", re.I)


def chapters(book=None, frm=1):
    pat = f"book-{book:02d}-*" if book else "book-*"
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, "series", pat))):
        for c in sorted(glob.glob(os.path.join(d, "chapters", "ch-*.md"))):
            if int(re.search(r"ch-(\d+)", c).group(1)) >= frm:
                out.append(c)
    return out


def run(files):
    if not files:
        print("  no chapters found"); return
    texts = {f: open(f, encoding="utf-8").read() for f in files}
    whole = "\n".join(texts.values())
    words = W(whole)
    print(f"\n  TIC CHECK — {len(files)} chapters · {words:,} words\n  {'='*62}")

    def line(label, val, quota, fmt="{:.2f}", worse_is_higher=True):
        bad = (val > quota) if worse_is_higher else (val < quota)
        flag = BAD if bad else OK
        print(f" [{flag}] {label:<34} {fmt.format(val):>9}   quota {quota}")

    # --- mechanical quotas -------------------------------------------------
    em = whole.count("—")
    line("em-dashes / 1,000 words", em / words * 1000, QUOTAS["em_dash_per_1k"])
    ww = len(re.findall(r", which was", whole))
    line("', which was' (narrator gloss)", ww, QUOTAS["which_was_per_book"], "{:.0f}")
    fam = r"for a while|for a long time|for some time|a long moment|for a moment|for a bit"
    aw = len(re.findall(fam, whole))
    line("time-vagueness family", aw, QUOTAS["awhile_per_book"], "{:.0f}")
    # clustering matters more than the total: flag any chapter carrying >3 of either
    for f_, t_ in texts.items():
        w1 = len(re.findall(r", which was", t_)); w2 = len(re.findall(fam, t_))
        if w1 > 3 or w2 > 3:
            print(f"          cluster: {os.path.basename(f_)}  which-was={w1}  vague={w2}")

    paras = [p for p in re.split(r"\n\s*\n", whole)
             if p.strip() and not p.strip().startswith(("#", ">", "|", "---", "*("))]
    heads = sum(1 for p in paras if re.match(r'^(He|Wick)\b', p.strip()))
    line("paragraphs opening He/Wick  %", heads / max(len(paras), 1) * 100,
         QUOTAS["he_para_pct"], "{:.1f}")

    # --- consecutive He-paragraph runs -------------------------------------
    runs, cur, worst = 0, 0, 0
    for p in paras:
        cur = cur + 1 if re.match(r'^(He|Wick)\b', p.strip()) else 0
        worst = max(worst, cur)
        if cur == 3: runs += 1
    print(f" [{BAD if worst >= 3 else OK}] longest He/Wick paragraph run   {worst:>9}   quota 2")

    # --- similes -----------------------------------------------------------
    tw = len(re.findall(r"the way (?:a|an|the|you|he|she|it|somebody|people)\b", whole))
    lk = len(re.findall(r"\blike (?:a|an|the)\b", whole))
    tot = tw + lk
    if tot:
        print(f" [{BAD if tw/tot > .5 else OK}] similes framed 'the way ___'    "
              f"{tw/tot*100:>8.1f}%   quota 50.0%  ({tw}/{tot})")

    # --- lifespan prolepsis (HARD RULE) ------------------------------------
    hits = []
    for f, t in texts.items():
        for m in LIFESPAN.finditer(t):
            hits.append((os.path.basename(f), m.group(0)[:60]))
    print(f" [{BAD if hits else OK}] lifespan prolepsis (HARD RULE)  {len(hits):>9}   quota 0")
    for f, h in hits[:8]:
        print(f"          {f}: …{h}…")

    # --- default-number detection ------------------------------------------
    counts = collections.Counter()
    for n in NUMBER_WORDS:
        c = len(re.findall(rf"\b{n}\b", whole, re.I))
        if c: counts[n] = c
    top = counts.most_common(6)
    if top:
        lead, n1 = top[0]
        second = top[1][1] if len(top) > 1 else 0
        skew = n1 / max(second, 1)
        print(f" [{WARN if skew > 1.6 else OK}] default-number skew            "
              f"{skew:>8.2f}x   quota 1.60x")
        print("          " + " · ".join(f"{k}:{v}" for k, v in top))

    # --- verbal furniture ownership ----------------------------------------
    print(f"\n  VERBAL FURNITURE (ownership must hold)")
    for tok, owner in (('"Right', "Wick"), ('"Mm', "Gran"), ('"Course you did', "Tam")):
        rows = []
        for f, t in texts.items():
            for m in re.finditer(re.escape(tok) + r'[.,"][^\n]{0,70}', t):
                rows.append((os.path.basename(f), m.group(0)[:72]))
        print(f"   {tok}…' → {owner}: {len(rows)}")
        for f, r in rows:
            speaker = re.search(r'(said|") (\w+)', r)
            print(f"      {f}: {r}")

    # --- per-chapter word counts vs the 2,200 floor ------------------------
    print(f"\n  CHAPTER LENGTHS (floor 2,200 — under means a MISSING BEAT, not missing words)")
    short = []
    for f in files:
        n = W(texts[f])
        tag = "  " if n >= 2200 else "<<"
        if n < 2200: short.append(os.path.basename(f))
        print(f"   {tag} {os.path.basename(f):<12} {n:>6,}")
    if short:
        print(f"   → {len(short)} under floor: {', '.join(short)}")
    print()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    frm = 1
    if "--from" in sys.argv:
        frm = int(sys.argv[sys.argv.index("--from") + 1])
    run(chapters(int(args[0]) if args else None, frm))
