---
# Active Context
**Last updated:** 2026-03-28
**Active mode:** Code
**Active LLM backend:** Claude Sonnet API (claude-sonnet-4-6)

## Current task
PHASE-B: Template folder enrichment — complete. Ready to commit and proceed to PHASE-C.

## Last result
### PHASE-A: Hot/Cold Memory Architecture (Session 2026-03-28)

Completed on `release/v2.0` branch (commit bd1bf7d):

- **`memory-bank/hot-context/`** created with 5 migrated files (git mv)
- **`memory-bank/archive-cold/`** created with sprint-logs/, completed-tickets/, productContext_Master.md
- **RULE 9** (Cold Zone Firewall) added to `.clinerules` and `template/.clinerules`
- **RULE 1** updated to reference `hot-context/` paths
- **`scripts/memory-archive.ps1`** created (sprint archival script)
- **SP-002** bumped to v2.4.0

### PHASE-B: Template Folder Enrichment (Session 2026-03-28)

All deliverables created (pending commit):

- **`template/memory-bank/hot-context/`** — 5 blank stubs:
  - `activeContext.md` (from prior session)
  - `progress.md`
  - `decisionLog.md`
  - `systemPatterns.md`
  - `productContext.md`
- **`template/memory-bank/archive-cold/`** — directory structure:
  - `sprint-logs/.gitkeep`
  - `completed-tickets/.gitkeep`
  - `productContext_Master.md` (blank stub)
- **`template/mcp.json`** — Calypso FastMCP server config template
- **`deploy-workbench-to-project.ps1`** — updated:
  - Added `mcp.json` to `$FilesToCopy`
  - Added `docs`, `memory-bank` to `$FoldersToCopy`
  - Replaced old 7-file Memory Bank creation block with new Hot/Cold-aware block
  - Updated "Next steps" to reference `hot-context/productContext.md`

## Next step(s)
- [ ] PHASE-B.4: Commit and push (feat(template): PHASE-B complete)
- [ ] PHASE-C: Calypso orchestration scripts
  - C.1: Create src/calypso/ directory structure
  - C.2: Write orchestrator_phase2.py
  - C.3: Write check_batch_status.py
  - C.4: Write orchestrator_phase3.py
  - C.5: Write orchestrator_phase4.py
  - C.6: Write triage_dashboard.py
  - C.7: Write apply_triage.py
  - C.8: Write fastmcp_server.py
  - C.9: Write SP-008 (Synthesizer Agent)
  - C.10: Write SP-009 (Devil's Advocate Agent)
  - C.11: End-to-end test
- [ ] PHASE-D: Global Brain / Librarian Agent
- [ ] PHASE-E: v2.0 release finalization

## Blockers / Open questions
- SP-002 check script regex issue (nested code blocks) — low priority, non-blocking
- Chroma vector DB installation on Calypso required for PHASE-D (manual step)
- SP-008, SP-009, SP-010 system prompts to be written during PHASE-C and PHASE-D

## Last Git commit
bd1bf7d feat(memory): PHASE-A complete -- Hot/Cold memory architecture
---
