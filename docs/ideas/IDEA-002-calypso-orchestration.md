---
id: IDEA-002
title: Calypso Orchestration Scripts (Phase 2-4 Pipeline)
status: ACCEPTED
target_release: v2.0
source: Claude Batch reviews 1+2 + Gemini conversations (2026-03-28)
source_files:
  - plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md
  - plans/batch-doc6-review/DOC6-REVIEW-RESULTS2.md
  - docs/conversations/2026-03-27-gemini-doc6-architecture.md
  - docs/conversations/2026-03-28-gemini-workbench-explained.md
captured: 2026-03-28
decided: 2026-03-28
decided_by: Human
---

## Description

Build the Calypso (Tier 2) orchestration layer for the multi-agent pipeline:

- `orchestrator_phase2.py` — packages PRD into JSONL, dispatches to Anthropic Batch API (Committee of Experts: Architecture, Security, UX/UI, QA agents)
- `check_batch_status.py` — polls Anthropic Batch API, validates JSON schemas, saves consolidated expert reports
- `orchestrator_phase3.py` — runs Synthesizer Agent against expert reports + PRD, produces `draft_backlog.json`
- `orchestrator_phase4.py` — runs Devil's Advocate micro-loop (MAX_ATTEMPTS=2), produces `final_backlog.json` with GREEN/ORANGE classification
- `triage_dashboard.py` — parses `final_backlog.json`, generates `triage_dashboard.md` for human arbitration
- `apply_triage.py` — reads human checkbox decisions, updates `systemPatterns.md`, populates project `productContext.md`
- `fastmcp_server.py` — FastMCP server exposing `launch_factory()`, `check_batch_status()`, `retrieve_backlog()` to local IDE

## Motivation

The current workbench has no automated multi-agent pipeline. All analysis is done manually
or via ad-hoc batch scripts. The Calypso orchestration layer is the core of the
"Asynchronous Factory" concept — it enables the human to disconnect after Phase 1 (ideation)
and let the factory run Phases 2-4 autonomously.

## Affected Documents

- DOC-1: No change
- DOC-2: New section — Calypso Tier 2 architecture, FastMCP server, orchestration scripts
- DOC-3: New PHASE-C (Calypso orchestration)
- DOC-4: New section — running the factory pipeline, monitoring batch status
- template/: New mcp.json template with Calypso FastMCP server entry

## Disposition

**Decision:** ACCEPTED for v2.0
**Rationale:** Core capability of the target architecture. Must come after PHASE-A (Hot/Cold
memory) and PHASE-B (template enrichment) to ensure the local execution environment is
stable before the factory feeds it work at scale.
**Implementation reference:** PHASE-C in docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md

## History

- 2026-03-28: Created [IDEA] from batch review + Gemini conversation findings
- 2026-03-28: Promoted to [ACCEPTED], target v2.0
