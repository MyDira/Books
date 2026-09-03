---
name: resume
description: Resume work on the WILDHOLD series after a session restart or context loss. Use at the start of any fresh session, or when asked to continue writing the series.
---

# RESUME — cold-start protocol

You are continuing a 25-book progression fantasy series. You may have no memory of it.
That is fine; the repository is designed for exactly this.

## DO THIS, IN THIS ORDER

```bash
cat canon/STATE.md                    # position, cast, power, threads, next brief
cat bible/00-premise.md               # what this series is
cat bible/06-style-guide.md           # the voice contract — do not skip
ls series/                            # which books exist
tail -40 canon/continuity-log.md      # recent established facts
cat series/book-*/OUTLINE.md | head -80   # current book's plan  (pick the current one)
```

That is roughly 900 lines and it is enough. **Do not read old chapters to "catch up."**
The state files exist so you never have to. Reading manuscripts burns the context you
need for writing.

## THEN
`canon/STATE.md` has a `NEXT ACTION` line. Do it.

- If it says write a chapter → invoke skill `write-chapter`.
- If it says a book is finished → invoke skill `close-book`.
- If it says a book needs planning → invoke skill `plan-book`.
- If it says an audit is due → invoke skill `continuity-audit`.

## STANDING ORDERS
The user has asked for **continuous autonomous work**. They do not want to supervise,
do not want to be asked what happens next, and do not want to know the story in advance.

- Do not ask the user for plot decisions. Decide, and use the editorial agents as your
  check on that decision.
- Keep working through chapters and books until you run out of budget.
- **Consolidate as you go** so the user can read finished books at any moment:
  `python3 tools/consolidate.py <book>` after every chapter.
- Commit every chapter. Push every 5 chapters and at every book boundary.
- When you are near the end of available budget, make sure `canon/STATE.md` is current
  and everything is committed and pushed. That is the handoff.

## THE ONE RULE THAT MATTERS
Never write prose without updating canon in the same session. A chapter written and not
recorded is a landmine for every future session.
