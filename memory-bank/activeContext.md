---
# Active Context
**Last updated:** 2026-03-28
**Active mode:** Architect / Code
**Active LLM backend:** Claude Sonnet API (claude-sonnet-4-6)

## Current task
Release governance model fully designed and documented in `plans/governance/PLAN-release-governance.md`.

## Last result
### Governance Model Design (Session 2026-03-28)
Designed a universal release governance model applicable to both the workbench project and all
application projects built with it. Key decisions made:

- **Universal docs/ structure**: 5 canonical docs (DOC-1..5) per release, versioned in `docs/releases/vX.Y/`
- **Two separate spaces**: `docs/` (human-authored specs, stable) vs `memory-bank/` (agent runtime, volatile)
- **Idea lifecycle**: IDEAS-BACKLOG.md + IDEA-NNN.md files with 6 statuses ([IDEA] -> [ACCEPTED] -> [IMPLEMENTED] / [DEFERRED] / [REJECTED] / [SUPERSEDED])
- **Conversation log**: `docs/conversations/` with README.md triage index
- **Release = Git tag**: captures everything atomically (code + docs + config + memory bank + QA)
- **Three execution tracking files**: DOC-3 (plan) + EXECUTION-TRACKER-vX.Y.md (log) + memory-bank/progress.md (live state)
- **Unambiguous numbering**: DOC-N.S.SS for sections, PHASE-N.S for steps
- **Migration strategy (Option C)**: baseline tag v1.0.0-baseline on master now, then PHASE-0 of v2.0 restructures docs/ retroactively and tags v1.0.0 properly
- **workbench/ folder eliminated**: contents redistributed into docs/releases/v1.0/, docs/conversations/, docs/qa/v1.0/
- **RULE 8 to add to .clinerules**: Documentation Discipline (read-only frozen docs, idea capture mandate, conversation log mandate)

### Plan document written
- `plans/governance/PLAN-release-governance.md` — 931 lines, 15 sections
  - Sections 1-5: Purpose, Core Principles, Two Spaces, docs/ Structure, 5 Canonical Docs
  - Sections 6-8: Numbering Convention, Idea Lifecycle, Conversation Log
  - Sections 9-11: Release Lifecycle, Three Tracking Files, Git Branching
  - Sections 12-15: Agent Rules (RULE 8), Migration Plan (PHASE-0.1..0.13), Application Projects, Implementation Steps

## Next step(s)
- [ ] Human reviews `plans/governance/PLAN-release-governance.md` and approves
- [ ] PHASE-0.1: `git tag v1.0.0-baseline` on master
- [ ] PHASE-0.2: Create `release/v2.0` branch from `experiment/architecture-v2`
- [ ] PHASE-0.3..0.13: Full governance restructure (docs/ folder, v1.0 retroactive docs, ideas/, conversations/, RULE 8, tag v1.0.0)
- [ ] Draft v2.0 canonical docs (DOC-1..3 for v2.0) before starting PHASE-A
- [ ] PHASE-A: Hot/Cold memory restructure
- [ ] PHASE-B: Template folder enrichment
- [ ] PHASE-C: Calypso orchestration scripts
- [ ] PHASE-D: Global Brain (Chroma/Mem0, Librarian Agent)
- [ ] Manual update of Gem Gemini "Roo Code Agent" with SP-007 v1.7.0 (English)

## Blockers / Open questions
- Human approval of PLAN-release-governance.md required before implementation starts
- P0 unresolved in DOC6: systemPatterns.md genesis, PRD naming collision, conversational framing, missing glossary (to be fixed in v2.0 DOC-1/DOC-2)

## Last Git commit
1bde967 docs(plans): add PLAN-release-governance.md — universal release governance model
---
