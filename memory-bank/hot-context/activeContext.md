---
# Active Context

**Last updated:** 2026-03-28
**Active mode:** Developer
**Active LLM backend:** MinMax M2.7 via OpenRouter (minimax/minimax-m2.7)
**LLM Backend:** `minimax` (default via OpenRouter)
**Consecutive Errors:** `0`
**Fallback State:** Not triggered

## Git state
- Branch: `release/v2.2` (NEW — active development per ADR-005 GitFlow)
- Base: `master` at v2.1.0 (8218a14)
- `origin/master`: at tag v2.0.0 (frozen — 12 commits behind local master)
- `origin/release/v2.1`: at v2.1.0 (d0c0dcd — closed per ADR-005)
- `origin/release/v2.2`: does not exist yet (needs push)

## Current task
Release v2.1.0 completion — merge release/v2.1 → master, tag v2.1.0, close release/v2.1, create release/v2.2

## Last result
### Release v2.1.0 Merge (Session 17, 2026-03-28)
All steps completed locally:
- [x] `git checkout master` — switched from release/v2.1
- [x] `git merge release/v2.1 --no-ff` — merged 12 commits (IDEA-008 + SP-002 coherence + GitFlow enforcement)
- [x] `git tag -a v2.1.0` — tagged release on master (8218a14)
- [x] `git checkout -b release/v2.2` — created new active development branch
- [x] Temp Python scripts cleaned (_replace_template.py etc.)

Pending (blocked by VS Code security prompt):
- [ ] `git push origin master` — 12 commits + v2.1.0 tag to push
- [ ] `git push origin release/v2.2` — new branch to create

## Next step(s)
- [ ] User approves VS Code security prompt OR manually runs:
  - `git push origin master`
  - `git push origin v2.1.0`
  - `git push origin release/v2.2`

## Blockers / Open questions
- **Git push**: All `git push` commands blocked by VS Code security prompt (×5). User must approve the prompt in VS Code terminal OR push manually via GitHub web UI.

## Last Git commit
`8218a14` Merge release/v2.1 -- v2.1.0 release (IDEA-008, SP-002 coherence fixes)
