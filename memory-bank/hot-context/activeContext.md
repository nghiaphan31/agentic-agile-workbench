---
# Active Context

**Last updated:** 2026-03-28T22:22:00Z
**Active mode:** Code
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minimax` (default via OpenRouter)
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- Branch: `develop` (renamed from `release/v2.3` per ADR-006)
- Base: `master` at v2.2.0 (`f0826b0`)
- `master`: at v2.2.0, frozen
- `origin/master`: at v2.1.0 — needs push (v2.2.0 pending)
- `origin/develop`: does not exist yet — needs push

## Current task
Full Coherence Audit via Anthropic Batch API — batch infrastructure created

## Last result
- Created `plans/batch-full-audit/` with 3 batch scripts + plan + runbook
- 3 submit scripts (governance, crossdocs, template) — ALL PASS syntax check
- 3 retrieve scripts — ALL PASS syntax check
- PLAN-full-coherence-audit.md and RUNBOOK.md created

## Next step(s)
- [ ] Git commit batch-full-audit/ directory
- [ ] Submit 3 batches when ready (python submit_batch{1,2,3}_*.py)
- [ ] Wait 1-4 hours, then retrieve results

## Blockers / Open questions
- None — infrastructure ready

## Last Git commit
`f0826b0` docs(release): add v2.2 canonical docs
