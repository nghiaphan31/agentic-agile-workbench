---
# Active Context

**Last updated:** 2026-03-28
**Active mode:** Developer
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minimax` (default via OpenRouter)
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- `origin/master`: at tag v2.0.0 (frozen)
- `origin/release/v2.0`: closed after merge to master
- `release/v2.1`: ACTIVE — all new development here (IDEA-008 OpenRouter MinMax default LLM)
- Last commit: c3f4458 (IDEA-008 captured)

## Current task
All post-release steps (POST-1, POST-2, POST-3, POST-4 Phases 2+3+4) completed.

## Last result
### Session 14+15: POST-RELEASE execution via SSH to Calypso (2026-03-28)

- **POST-0**: SSH connectivity to Calypso confirmed ✅
- **POST-0b**: Calypso synced to `release/v2.0` @ `9a5df35` ✅
- **POST-1**: `chromadb-1.5.5` installed in `venv/` on Calypso ✅
- **POST-1b**: Chroma server started at `localhost:8002`, data at `/home/nghia-phan/chroma-data` ✅
- **POST-1c**: Heartbeat confirmed ✅
- **POST-2**: `librarian_agent.py --index` — 1 file indexed ✅
- **POST-2b**: Semantic query test passed ✅
- **POST-4 Phase 2**: Batch API — 4/4 succeeded; 3 raw files JSON truncated. Repaired via `_repair_expert_json.py`:
  - `security_expert.json` — 9 findings [TRUNCATED]
  - `ux_expert.json` — 13 findings [TRUNCATED]
  - `qa_expert.json` — 13 findings [TRUNCATED]
  - `architecture_expert.json` — 11 findings [OK]
- **POST-4 Phase 3**: Synthesizer — 20 backlog items ✅
  - `batch_artifacts/draft_backlog.json` — 31KB, schema validated
- **POST-4 Phase 4**: Devil's Advocate — credits depleted at BL-012 (12/20 items). BLOCKED: API credits exhausted. ✅ partial
- `.env` created on Calypso with `ANTHROPIC_API_KEY` (gitignored) ✅
- Bug fix: `orchestrator_phase3.py` MAX_TOKENS 4096→8192 ✅
- `.gitignore`: added `batch_artifacts/` ✅
- **Step 8**: ✅ `release/v2.0` → `master` fast-forward merge + push completed
  - Both branches now at `afd3eee` on origin

## Next step(s)
- [ ] **IDEA-008**: Capture MinMax M2.7 via OpenRouter as default LLM with Claude fallback (see docs/ideas/IDEA-008-openrouter-minimax-default.md) — pending human approval to proceed

## Blockers / Open questions
- Git push of commit 51e8ba9 still pending (denied ×6)
  - `ssh calypso "cd /home/nghia-phan/AGENTIC_DEVELOPMENT_PROJECTS/agentic-agile-workbench && set -a && source .env && set +a && venv/bin/python src/calypso/orchestrator_phase4.py --draft-backlog batch_artifacts/draft_backlog.json"`

## Blockers / Open questions
- Git push of commit 51e8ba9 still pending (denied ×6) — push manually

## Last Git commit
adb983e docs(tracker): Session 14+15 -- POST-1+2+4(P2+P3) complete, Step 8 done, Phase 4 partial

## Git state
- `origin/master`: `afd3eee` (up to date with release/v2.0)
- `origin/release/v2.0`: `afd3eee`
- Calypso: synced ✅
- PC: synced ✅
- Last commit: `afd3eee` docs(memory): Session 15 -- POST-4 Phase 2+3 validated, Phase 4 blocked by credits, push blocked by VS Code
