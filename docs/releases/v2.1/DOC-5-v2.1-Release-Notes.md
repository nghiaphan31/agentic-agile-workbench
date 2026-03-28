---
doc_id: DOC-5
release: v2.1
status: Frozen
title: Release Notes
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v2.0/DOC-5-v2.0-Release-Notes.md
---

# DOC-5 -- Release Notes (v2.1)

> **Status: FROZEN** -- This document is read-only. Do not modify.

---

## Release Summary

| Field | Value |
|-------|-------|
| **Version** | 2.1.0 |
| **Release date** | 2026-03-28 |
| **Git tag** | `v2.1.0` |
| **Branch** | `release/v2.1` (merged to `master`) |
| **Previous release** | v2.0.0 (2026-03-28) |
| **Type** | MINOR — production hotfix: LLM backend resilience + SP coherence fixes |

---

## What v2.1 Delivers

v2.1 is a production reliability release focused on **LLM backend resilience** and **system prompt coherence**.

### IDEA-008: OpenRouter MinMax M2.7 as Default LLM

**Problem:** The workbench relied on a single LLM backend with no fallback strategy. Consecutive errors left the agent unable to recover.

**Solution:** OpenRouter MinMax M2.7 is now the default LLM via OpenRouter. After 3 consecutive errors, Claude Sonnet API is triggered as fallback.

**Files changed:**
- `.clinerules` -- RULE 5 updated with fallback logic
- `Modelfile` -- OpenRouter configuration
- `prompts/SP-002-clinerules-global.md` -- updated embedded template

**Evidence:** Merged to `release/v2.1` via PR #1 (squash merge), feature branch deleted.

---

### SP-002 Coherence Fixes

**Problem:** `.clinerules` and `prompts/SP-002-clinerules-global.md` had accumulated content corruption:
- Corrupted em-dash bytes (UTF-8 encoding errors)
- BOM (Byte Order Mark) in embedded template
- Incomplete embedded template (7 blank lines missing)
- CRLF/LF line ending inconsistencies

**Solution:** Full coherence pass — content rebuilt, verified, normalized.

**Commits:**
- `a65cd10` -- fixed corrupted em-dash bytes
- `a7ac4f0` -- removed BOM from embedded template
- `d0c0dcd` -- replaced embedded template with full .clinerules content (866 lines)
- `ca13880` -- added `.gitattributes` for LF normalization
- `5d71f9a` -- post-fix verification

**Evidence:** `powershell -ExecutionPolicy Bypass -File scripts/check-prompts-sync.ps1` returns **6 PASS | 0 FAIL | 1 WARN** (SP-007 manual).

---

### ADR-005: GitFlow Enforcement (RULE 10)

**Problem:** No formal GitFlow policy. Commits were made directly on release branches and on `master` after tagging.

**Solution:** ADR-005 captured in `memory-bank/hot-context/decisionLog.md`. RULE 10 added to `.clinerules`:
- `master`: frozen after each release tag
- `release/vX.Y`: closed after merge to master
- All new work targets `release/vX.Y+1` or feature branches derived from it
- Feature branches must branch from `release/vX.Y+1`

**Evidence:** `67e332b` -- RULE 10.3 feature branch workflow; `9004a81` -- ADR-005 GitFlow enforcement.

---

## Known Issues

| ID | Severity | Description |
|----|----------|-------------|
| KI-001 | LOW | SP-002 check script false positive (nested code blocks) -- pre-existing, not introduced in v2.1 |
| KI-002 | LOW | Chroma not installed on Calypso -- Global Brain `memory:query` falls back to keyword search |
| KI-003 | LOW | No live end-to-end Calypso pipeline test -- deferred until Anthropic API credits available |

---

## v2.1 Release Notes -- Post-Release

### All POST-release steps from v2.0 completed

The following manual steps (initiated in v2.0 POST phase) were completed during the v2.1 cycle:

| Step | Description | Status |
|------|-------------|--------|
| POST-1 | Chroma installed on Calypso (`chromadb-1.5.5`) | ✅ Complete |
| POST-2 | Cold archive indexed (1 file indexed, Global Brain operational) | ✅ Complete |
| POST-3 | SP-007 Gem Gemini verified (v1.7.0) | ✅ Complete |
| POST-4 | Live Calypso pipeline: Phase 2 (4 expert reports ✅), Phase 3 (20 backlog items ✅), Phase 4 (20/20 ✅ -- 12 GREEN, 8 ORANGE) | ✅ Complete |

---

## Upgrades to v2.1

### From v2.0.0 to v2.1.0

```
git checkout master
git pull origin master
git log v2.0.0..v2.1.0 --oneline
```

**Minimum changes:**
- `.clinerules` -- RULE 5 (LLM fallback), RULE 10 (GitFlow)
- `.gitattributes` -- line ending normalization
- `prompts/SP-002-clinerules-global.md` -- embedded template updated
- `Modelfile` -- OpenRouter configuration
- `memory-bank/hot-context/progress.md` -- updated v2.1 status

---

*End of Release Notes v2.1*
