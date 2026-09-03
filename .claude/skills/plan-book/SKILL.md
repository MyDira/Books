---
name: plan-book
description: Plan and open a new book in the WILDHOLD series - build its outline, escalation, antagonist, and progression budget. Use when starting any new book in the series.
---

# PLAN-BOOK

Run once per book, before its first chapter.

## STEP 1 — READ
`canon/STATE.md`, `series/arc-map.md`, `canon/threads.md`, `canon/promises.md`,
`bible/08-cosmology-and-endgame.md`, and the previous book's `AUDIT.md`.

## STEP 2 — THE FIVE QUESTIONS
Answer before outlining. A book that cannot answer these is not a book.

1. **What does Wick want, concretely, that he cannot have on page one?**
   (Physical, checkable, and *not* "get stronger.")
2. **Who or what is in the way, and why can't he just out-level it?**
3. **What is the new system idea?** Every book must teach the reader one genuinely new
   thing about how the world works. List it as one sentence.
4. **What is the progression budget?** (See below.)
5. **What does the crew look like at the end that it didn't at the start?**

## STEP 3 — PROGRESSION BUDGET
Decide, *in advance*, exactly what Wick gains. Write it down. Do not exceed it.

Template:
```
RANK:        start <X> → end <Y>          (books 1-6: ~1 rank; 7-15: ~1 sub-rank; 16+: fractional)
ACREAGE:     start <n> → end <n>          (each gain must name its deed)
WEIGHT:      start <n> → end <n>
COHERENCE:   start <g> → end <g>
TERRAIN:     N new plants, named, with the Seed source for each
WORKINGS:    N new, with the terrain each comes from
LAW WORK:    none / notion forming / notion / law
CREW:        who joins, who is tested, who is lost
```
The budget is a contract with the reader's sense of pace. Under-delivering is boring;
over-delivering is why series die at book nine.

## STEP 4 — THE STORY-ARCHITECT PASS (mandatory)
Spawn the `story-architect` agent with the five answers and the budget. It will stress
the shape: is the midpoint a real reversal? Does the climax test the thing the book
taught? Is the antagonist an *argument* rather than an obstacle?

Revise. Then spawn it once more only if the shape changed materially.

## STEP 5 — OUTLINE
Write `series/book-XX-<slug>/OUTLINE.md`:

```markdown
# Book XX — <Title>
**Logline:** one sentence.
**New system idea:** one sentence.
**Progression budget:** (paste from step 3)
**Antagonist:** who, what they want, why they are right about something.
**Setting:** where, and why here.

## Act structure
- **Act I (ch 1–8):** ...
- **Turn 1 (ch 8):** ...
- **Act II-a (ch 9–15):** ...
- **Midpoint reversal (ch 16):** ...
- **Act II-b (ch 17–24):** ...
- **Turn 2 / low point (ch 24):** ...
- **Act III (ch 25–31):** ...
- **Climax (ch 29–31):** ...
- **Landing (ch 32):** the advancement, the cost, the new question.

## Chapter grid
| # | Working title | Purpose | Ratchet | POV |
|---|---|---|---|---|
| 1 | | | | Wick |
...(all 32 rows; keep them loose — the grid is a trellis, not a track)

## Threads this book opens / pays
## Promises this book plants / pays
## Ending state: where everyone must be for Book XX+1
```

**Length target:** 30–34 chapters, ~85,000 words.

## STEP 6 — SCAFFOLD
```bash
mkdir -p series/book-XX-<slug>/chapters
touch series/book-XX-<slug>/{NOTES.md,AUDIT.md}
```
Update `canon/STATE.md` POSITION and NEXT ACTION. Update `series/arc-map.md`.
Commit.

## RULES
- **Never plan more than one book ahead in detail.** The arc-map holds the loose shape;
  the reader (and the author) is better served by discovery. Books 2+ are outlined only
  when Book N-1 closes.
- The outline is a trellis. Deviating is fine and expected; deviating *silently* is not —
  update the outline when the book turns.
- Each book must be readable standalone by someone who forgot the previous one, without
  a recap chapter. Re-establish through action.

## AGENT INVOCATION — IMPORTANT
The role briefs live in `.claude/agents/*.md`. They register as real subagent types only
when a session *starts* with them already on disk. In a session where they are not
registered (e.g. the session that created them), invoke `general-purpose` instead and
point it at the brief:

```
subagent_type: general-purpose  (or the named agent if it is registered)
prompt: "Working directory: /home/user/Books. Read .claude/agents/<agent>.md and follow
         that role brief exactly. Scope: <files>. Also read: <canon files>."
```
Always try the named agent first; fall back to `general-purpose` on 'agent type not found'.
