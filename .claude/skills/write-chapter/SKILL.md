---
name: write-chapter
description: Write the next chapter of the WILDHOLD series and update all canon state. Use whenever continuing the series, writing a chapter, or resuming work after a session restart. This is the core production loop.
---

# WRITE-CHAPTER — the core loop

Run this once per chapter. It is deliberately mechanical. Do not improvise the process;
improvise inside it.

---

## STEP 0 — LOAD (cheap, always the same four reads)

```bash
cat canon/STATE.md
cat series/book-$BK-*/OUTLINE.md
tail -n 60 canon/continuity-log.md
```
Plus the **previous chapter file** only if the new chapter continues a scene directly.
(The `LAST CHAPTER SUMMARY` in STATE.md is usually sufficient. Prefer it — it exists to
save context.)

Load on demand, only if the chapter touches them:
- `canon/characters/<name>.md` for any POV or major-speaking character
- `bible/01-magic-system.md` if the chapter has an advancement or a new working
- `bible/04-bestiary.md` if a Wildborn appears
- `bible/06-style-guide.md` **if this is the first chapter of a session** (voice reset)

## STEP 1 — BRIEF

From STATE.md's `NEXT CHAPTER BRIEF` plus the book OUTLINE, write yourself a 5-line brief
before drafting. It must name:
1. The chapter's **question** (what the reader wants to know for these 2,800 words)
2. The **turn** it ends on
3. Which of {progress · cost · revelation · relationship-change} it delivers (≥1, ideally 2)
4. Any **system fact** it establishes
5. Any **promise** it plants or pays

If the brief has no turn, the chapter is not ready. Fix the brief, not the prose.

## STEP 2 — DRAFT

Write to `series/book-XX-<slug>/chapters/ch-NNN.md`.

**Header format (exact):**
```markdown
# Chapter N — Title
```
No front matter in chapter files. Nothing but the story.

**Targets:** 2,200–3,200 words. Open in motion or on a question. Close on the turn.

**Non-negotiables while drafting:**
- Voice per `bible/06-style-guide.md`. Short sentences. Dry warmth. No purple.
- Nobody gets stronger off-page.
- Terrain named as landscape, never as "powers."
- If a fight: run the five-beat house method (problem → terrain → cost → adaptation →
  diagrammable resolution).
- Invent freely — but everything invented is written down in STEP 4.

## STEP 2.5 — RUN THE TOOL
```bash
python3 tools/tics.py <book> --from <last audited chapter>
```
Free, instant, and it catches what your ear will not: em-dash density, gloss and
time-vagueness clustering, He/Wick paragraph runs, default-number skew, lifespan prolepsis
(a hard rule), verbal-furniture theft, and chapters under the 2,200 floor. Fix what it flags
before Step 3.

**If you edit prose to fix a finding: explicit old → new pairs only, one per instance, after
reading the sentence. Never a blind regex.** Then re-run the integrity check:
`grep -o '[a-z]\. [a-z]' series/book-*/chapters/ch-0*.md | wc -l` must be 0.

## STEP 3 — SELF-CHECK (before touching canon)

Read your own chapter and answer, honestly, in one line each:
- Does it contain a real turn, or does it merely continue?
- Would a reader skim any paragraph? Cut those paragraphs.
- Is every number consistent with `power-ledger.md`?
- Did anyone act out of character to make the plot work? (This is the most common failure.)
- Ratchet check: has there been progress within the last 3 chapters? If not, add some now.

Fix what fails. Do not proceed with known defects.

## STEP 4 — RECORD (mandatory, same session, no exceptions)

This step is what makes 25 books possible. Never skip it, never defer it.

1. **`canon/continuity-log.md`** — append a block:
   ```
   ## B01 c007 — "Title"  [Y-812, Green 14, afternoon]
   - Facts: ...
   - New terms coined: ...
   - Injuries/objects/promises: ...
   - Present: ...
   ```
2. **`canon/glossary.md`** — add every coined term, alphabetically.
3. **`canon/power-ledger.md`** — add a row for ANY change to anyone's numbers, terrain,
   or workings, citing the deed.
4. **`canon/threads.md`** — open new threads; update statuses.
5. **`canon/promises.md`** — log new setups; mark payoffs.
6. **`bible/04-bestiary.md`** — any new Wildborn.
7. **`canon/characters/<name>.md`** — create for any new named character with lines.
8. **`canon/STATE.md`** — rewrite these sections:
   - `POSITION` (chapter count, story date)
   - `WHERE EVERYONE IS, RIGHT NOW`
   - `POWER LEDGER — LIVE`
   - `OPEN THREADS — TOP 7`
   - `LAST CHAPTER SUMMARY` (3–5 sentences)
   - `NEXT CHAPTER BRIEF` (specific — this is the handoff to a possibly-fresh session)
   Keep STATE.md under 250 lines. Prune.

## STEP 5 — CONSOLIDATE & COMMIT

```bash
python3 tools/consolidate.py <book-number>
git add -A && git commit -m "B01 c007: <title>"
```
Push every 5 chapters (or at any book boundary):
```bash
git push -u origin claude/litrpg-25-book-series-nekk0e
```

## STEP 6 — AUDIT CADENCE

- **Every 8 chapters** → run skill `continuity-audit`, **scoped to those 8 chapters only**
  (auditor + line-editor). Scoping keeps the cost sustainable across 25 books; the canon
  files carry the earlier history so the agents do not need the earlier prose.
- **Every 16 chapters / at every book close** → additionally spawn `power-auditor` and
  `reader-advocate`.
- **Book boundaries** → run skill `close-book`.

Act on audit findings *before* writing the next chapter. Findings are not suggestions;
a confirmed continuity break is fixed immediately, in the chapter where it occurred.

---

## FAILURE MODES TO WATCH FOR
| Symptom | Fix |
|---|---|
| Chapters getting longer and mushier | Hard-cap at 3,200. Cut the second-best scene. |
| No advancement for 4+ chapters | Insert a ratchet. Readers feel the stall before you do. |
| Everyone sounds the same | Re-read the dialogue section of the style guide. |
| Power creep — fights got easy | Run `power-auditor`. Probably a Seed was too generous. |
| Drifting toward grimdark | Re-read `bible/00-premise.md`. Put a joke back in. |
| Forgetting a character exists | That is what `WHERE EVERYONE IS` is for. Read it. |
