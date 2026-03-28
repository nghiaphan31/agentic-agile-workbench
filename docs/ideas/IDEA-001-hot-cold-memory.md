---
id: IDEA-001
title: Hot/Cold Memory Architecture
status: ACCEPTED
target_release: v2.0
source: Claude Batch reviews 1+2 (2026-03-28)
source_files:
  - plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md
  - plans/batch-doc6-review/DOC6-REVIEW-RESULTS2.md
captured: 2026-03-28
decided: 2026-03-28
decided_by: Human
---

## Description

Restructure the current flat `memory-bank/` (7 monolithic files always loaded) into a
Hot/Cold architecture:
- `memory-bank/hot-context/` — files the agent reads every session (activeContext, progress, decisionLog, systemPatterns, productContext)
- `memory-bank/archive-cold/sprint-logs/` — completed sprint logs (agent reads via MCP semantic query only)
- `memory-bank/archive-cold/completed-tickets/` — completed ticket history
- `memory-bank/archive-cold/productContext_Master.md` — historical BDD accumulator

A `memory:archive` script rotates hot-context files to cold archive at sprint end.

## Motivation

The current flat structure loads all 7 files into every agent context window simultaneously.
On large projects this causes:
- Context explosion (token cost)
- "Lost in the Middle" errors (agent ignores middle-of-context content)
- No separation between current-sprint context and historical context

## Affected Documents

- DOC-1: No change
- DOC-2: New section — Hot/Cold memory architecture
- DOC-3: New PHASE-A (Hot/Cold memory restructure)
- DOC-4: New section — memory:archive script usage
- .clinerules: New clause — Cold Zone Firewall (agent reads cold archive via MCP only)
- template/: New memory-bank/ subdirectory structure

## Disposition

**Decision:** ACCEPTED for v2.0
**Rationale:** Foundation for all subsequent phases. Calypso orchestration scripts (PHASE-C)
will deposit final_backlog.json into the local environment. The Librarian Agent (PHASE-D)
will read decisionLog.md. The Developer Agent needs a stable, bounded activeContext.md.
If the memory structure is wrong, every subsequent phase is building on sand.
**Implementation reference:** PHASE-A in docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md

## History

- 2026-03-28: Created [IDEA] from batch review findings
- 2026-03-28: Promoted to [ACCEPTED], target v2.0
