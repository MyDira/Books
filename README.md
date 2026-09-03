# WILDHOLD
**A 25-book progression fantasy series, written and maintained by an autonomous system.**

Everyone on the Sill has a country inside them. At fourteen you light it, a clerk
measures it, and that measurement is your life. Wick Alder lights his and gets forty-one
acres of cold salt flat under a starless sky — the largest Hold in the province and the
emptiest. Weight: zero. Rank: unrankable.

He just has to fill it. One monster at a time.

---

## 📖 READ IT HERE → [`manuscript/`](manuscript/)
Books are consolidated after every chapter, so finished books — and partial ones —
are always readable while work continues.

---

## HOW THIS REPOSITORY WORKS

This is a **context-management system for writing a very long series across many
sessions**, plus the series itself. The problem it solves: no single session can hold
2,000,000 words of continuity, so continuity lives in files, not in memory.

### The layers

| Layer | Changes | Purpose |
|---|---|---|
| [`bible/`](bible/) | rarely | Canon. Magic system, world, factions, style contract, long arc. |
| [`canon/`](canon/) | every chapter | Live state. The "save file." Power ledger, threads, promises, glossary, continuity log. |
| [`series/`](series/) | per book | Outlines, working chapter files, audit results. |
| [`manuscript/`](manuscript/) | every chapter | Reader-facing consolidated books. |
| [`.claude/`](.claude/) | rarely | The system itself — skills and editorial agents. |

### The single most important file
[`canon/STATE.md`](canon/STATE.md) — position, where every character is, live power
numbers, top threads, and a specific brief for the next chapter. A session that reads
STATE.md plus the current outline can write the next chapter correctly with no other
context. It is rewritten at the end of every chapter.

### The production loop (skill: `write-chapter`)
```
load state → brief → draft → self-check → record to canon → consolidate → commit
                                    ↑                                        │
                                    └──────── audit every 4 chapters ────────┘
```

### Checks and balances (skill: `continuity-audit`)
The author is the worst judge of their own drift. Five editorial subagents run on a
cadence and their findings are binding:

| Agent | Job | Cadence |
|---|---|---|
| [`continuity-auditor`](.claude/agents/continuity-auditor.md) | Contradictions, numbers, timeline, geography | every 4 ch |
| [`line-editor`](.claude/agents/line-editor.md) | Voice drift, verbal tics (with real grep counts), skimmable paragraphs | every 4 ch |
| [`power-auditor`](.claude/agents/power-auditor.md) | Progression pacing, power creep, rank-gap integrity, threat scaling | every 8 ch |
| [`reader-advocate`](.claude/agents/reader-advocate.md) | *Is it fun?* Where did I skim? Would I keep reading? | every 8 ch |
| [`story-architect`](.claude/agents/story-architect.md) | Structure, thread payoff, 25-book runway, corner risks | book boundaries |

Findings are triaged **BREAK / DRIFT / NOTE**. A BREAK is fixed before another word is
written.

### Skills
| Skill | Use |
|---|---|
| [`resume`](.claude/skills/resume/SKILL.md) | Cold-start a session. Read this first if you are a fresh session. |
| [`write-chapter`](.claude/skills/write-chapter/SKILL.md) | The core loop. Once per chapter. |
| [`plan-book`](.claude/skills/plan-book/SKILL.md) | Open a book: five questions, progression budget, outline. |
| [`close-book`](.claude/skills/close-book/SKILL.md) | Full audit battery, consolidate, roll up canon, open next book. |
| [`continuity-audit`](.claude/skills/continuity-audit/SKILL.md) | Run the editorial battery. |

### Tools
```bash
python3 tools/consolidate.py 1          # rebuild Book 1 manuscript
python3 tools/consolidate.py --all      # rebuild everything + index
python3 tools/stats.py                  # progress report
```

---

## DESIGN PRINCIPLES

1. **Nobody gets stronger off-page.** Every advancement cites the deed or Seed that
   earned it, in `canon/power-ledger.md`.
2. **Everything invented is recorded in the same session it is invented.** This single
   rule is what makes book 25 possible.
3. **Only one book is planned in detail at a time.** The long arc is a gravity well,
   not a track. The story is discovered, then audited.
4. **State files are read; manuscripts are not.** Catching up by rereading is how a
   session runs out of context before it writes anything.
5. **The audit agents are not optional and are not flattering.** They are required to
   produce substantive findings or explicitly justify a clean bill.

## STATUS
See [`canon/STATE.md`](canon/STATE.md) for live position.
