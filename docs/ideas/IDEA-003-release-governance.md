---
id: IDEA-003
title: Release Governance Model
status: IMPLEMENTED
target_release: v2.0
source: Human conversation 2026-03-28
source_files: []
captured: 2026-03-28
decided: 2026-03-28
decided_by: Human
implemented: 2026-03-28
implementation_commit: 1bde967
---

## Description

A universal release governance model applicable to both the Agentic Agile Workbench and
all application projects built with it. Key components:

- **Universal docs/ structure**: 5 canonical docs (DOC-1..5) per release, versioned in `docs/releases/vX.Y/`
- **Two separate spaces**: `docs/` (human-authored specs) vs `memory-bank/` (agent runtime)
- **Idea lifecycle**: IDEAS-BACKLOG.md + IDEA-NNN.md with 6 statuses
- **Conversation log**: `docs/conversations/` with triage tracking
- **Release = Git tag**: captures everything atomically
- **Three execution tracking files**: DOC-3 (plan) + EXECUTION-TRACKER (log) + progress.md (live)
- **Unambiguous numbering**: DOC-N.S.SS for sections, PHASE-N.S for steps
- **RULE 8**: Documentation Discipline added to .clinerules

## Motivation

Without a formal governance model:
- Ideas for the next release contaminate current release docs
- Ambiguous numbering (Part 1 / Phase 2 / Section 3) creates hierarchy confusion
- No idea capture discipline — ideas are lost or injected directly into docs
- No clear release boundary
- Confusion between docs/ and memory-bank/ purposes

## Affected Documents

- DOC-1: No change
- DOC-2: New section — governance model overview
- DOC-3: PHASE-0 (this restructure)
- DOC-4: New section — release process, idea capture workflow
- .clinerules: RULE 8 (Documentation Discipline)
- template/: New docs/ subdirectory structure

## Disposition

**Decision:** ACCEPTED for v2.0, implemented in PHASE-0
**Rationale:** Foundational process improvement needed before any feature work. Must be
the first phase of v2.0 because every subsequent phase depends on the governance structure.
**Implementation reference:** PHASE-0 in docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md

## History

- 2026-03-28: Created [IDEA] from human governance discussion
- 2026-03-28: Promoted to [ACCEPTED], target v2.0
- 2026-03-28: Marked [IMPLEMENTED], commit 1bde967 (PLAN-release-governance.md)
- 2026-03-28: PHASE-0 execution in progress (this restructure)
