---
name: continuity-audit
description: Run the WILDHOLD checks-and-balances battery over recent chapters using editorial subagents. Use every 4 chapters, at book boundaries, or whenever something feels off in the series.
---

# CONTINUITY-AUDIT — the checks and balances

The author (me) is the least reliable judge of my own drift. This skill exists because
across 25 books, drift is guaranteed and invisible from the inside.

## SCOPE
Default: the last 4 chapters. At a book boundary: the whole book.

## THE BATTERY

Spawn in parallel (they do not depend on each other). Each gets: the chapter files in
scope, `canon/STATE.md`, and whichever canon files its brief names.

| Agent | Asks | Spawn when |
|---|---|---|
| `continuity-auditor` | Does this contradict anything established? | every 4 ch |
| `line-editor` | Is the prose doing its job? Tics? Repetition? Voice drift? | every 4 ch |
| `power-auditor` | Is progression honest, paced, and un-crept? | every 8 ch |
| `reader-advocate` | Is this *fun*? Where would I skim? | every 8 ch |
| `story-architect` | Is the shape working? Are threads paying? | book boundaries |

**Prompt template for each:**
```
You are auditing WILDHOLD, a 25-book progression fantasy.
Read: series/book-XX-<slug>/chapters/ch-0NN.md through ch-0NN.md
Also read: canon/STATE.md, <plus files per your role>
Your role brief is in .claude/agents/<agent>.md — follow it exactly.
Report findings in the format your brief specifies. Be specific and cite
file:line. Do not rewrite prose; report.
```

## HANDLING FINDINGS

Findings land in `series/book-XX-<slug>/AUDIT.md` under a dated heading.

**Severity ladder:**
- **BREAK** — a hard contradiction with canon, or broken progression math.
  → Fix immediately, in the offending chapter, before writing anything new. Then log the
  fix in `canon/continuity-log.md`.
- **DRIFT** — voice, pacing, or characterisation sliding. → Fix in the next chapter and
  note the correction in the style guide if it is a recurring tendency.
- **NOTE** — taste. → Record; decide at book close.

**A BREAK is never resolved by retconning canon** unless the retcon *improves* the
series and is written up explicitly in `canon/continuity-log.md` under a `RETCON` heading
with the reasoning and every affected chapter listed and amended.

## THE HONEST-CRITIC RULE
Agents that report "looks great" on a 4-chapter batch are not being useful. Each brief
requires a minimum of two substantive findings or an explicit statement of what was
checked and found genuinely clean. Do not paper over. The whole point of this machinery
is to catch what I cannot see.
