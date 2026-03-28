---
doc_id: DOC-3
release: v2.1
status: Frozen
title: Implementation Plan
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md
---

# DOC-3 -- Implementation Plan (v2.1)

> **Status: FROZEN** -- This document is read-only. Do not modify.

---

## Delta from v2.0

v2.1 is a **hotfix release** -- no new phases or implementation steps. The implementation plan from [DOC-3 v2.0](docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md) applies in full for all v2.0 features.

---

## v2.1 Implementation Summary

v2.1 was implemented in a single session on `release/v2.1` branch (later merged to `master`).

### Steps Executed

| Step | Description | Commit |
|------|-------------|--------|
| 1 | Capture IDEA-008 in `docs/ideas/IDEAS-BACKLOG.md` | `c3f4458` |
| 2 | Implement OpenRouter MinMax M2.7 default + Claude fallback | `42845ab` |
| 3 | Add GitFlow enforcement (ADR-005, RULE 10) | `67e332b`, `9004a81` |
| 4 | Fix .clinerules em-dash corruption | `a65cd10` |
| 5 | Fix SP-002 embedded template BOM | `a7ac4f0` |
| 6 | Fix SP-002 embedded template content (866 lines) | `d0c0dcd` |
| 7 | Add .gitattributes for LF normalization | `ca13880` |
| 8 | QA: check-prompts-sync.ps1 6 PASS | `5d71f9a` |
| 9 | Merge release/v2.1 → master, tag v2.1.0 | `8218a14` |

---

## Deviations from v2.0 Process

v2.1 bypassed the formal release governance process (no `docs/releases/v2.1/` folder created at start). This was a production hotfix execution. Governance compliance restored retroactively by creating these canonical docs after the fact.

---

## Validation

| Criterion | Result |
|-----------|--------|
| `scripts/check-prompts-sync.ps1` | 6 PASS \| 0 FAIL \| 1 WARN |
| Git tag | `v2.1.0` on `master` |
| All v2.0 features preserved | ✅ |

---

*End of DOC-3 v2.1*
