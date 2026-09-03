---
name: close-book
description: Finish a WILDHOLD book - run the full audit battery, consolidate the reader-facing manuscript, and open the next book. Use at the end of any book.
---

# CLOSE-BOOK

## STEP 1 — FULL AUDIT BATTERY
Spawn all four in parallel, each scoped to this book's chapters:
- `continuity-auditor` — canon violations across the whole book
- `power-auditor` — progression pacing vs. the declared budget
- `line-editor` — prose quality, repetition, voice drift, tic detection
- `reader-advocate` — is it *fun*; where did attention drop; is the ending satisfying

Write all findings to `series/book-XX-<slug>/AUDIT.md`.

## STEP 2 — TRIAGE AND FIX
- **Blocking** (canon contradiction, broken progression math, character acting against
  established self, unpaid promise that was due): fix now, in place.
- **Should-fix** (repetition, a flat chapter, a rushed fight): fix now if under ~30 min.
- **Noted** (taste, could-be-better): record in AUDIT.md, carry into the next book's plan.

Re-run `continuity-auditor` if fixes were structural.

## STEP 3 — CONSOLIDATE
```bash
python3 tools/consolidate.py <book-number> --final
```
Produces `manuscript/Book-XX-<Title>.md` with title page, chapter breaks, and a word
count. Verify it opens and reads clean.

## STEP 4 — CANON ROLL-UP
- Prune `canon/STATE.md` back toward 200 lines. Roll resolved detail into the log.
- Move closed threads to the CLOSED table in `canon/threads.md`.
- Mark paid promises in `canon/promises.md`.
- Append a **book summary block** (10–15 lines) to `canon/book-summaries.md` — this is
  what future books use instead of rereading. Include: what happened, who joined, what
  Wick gained, what changed in the world, what was left open.
- Update `series/arc-map.md` with what actually happened and what it implies.

## STEP 5 — OPEN THE NEXT BOOK
Run skill `plan-book`. Update `canon/STATE.md` POSITION + NEXT ACTION.

## STEP 6 — SHIP
```bash
git add -A
git commit -m "Book XX complete: <Title> (NN chapters, ~NNk words)"
git push -u origin claude/litrpg-25-book-series-nekk0e
```
Then tell the user, in two lines: book done, word count, where to read it, what's next.
