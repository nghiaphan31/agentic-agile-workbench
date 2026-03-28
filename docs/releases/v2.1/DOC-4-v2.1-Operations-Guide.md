---
doc_id: DOC-4
release: v2.1
status: Frozen
title: Operations Guide
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v2.0/DOC-4-v2.0-Operations-Guide.md
---

# DOC-4 -- Operations Guide (v2.1)

> **Status: FROZEN** -- This document is read-only. Do not modify.

---

## Delta from v2.0

v2.1 is a **hotfix release**. The Operations Guide from [DOC-4 v2.0](docs/releases/v2.0/DOC-4-v2.0-Operations-Guide.md) applies in full. Only additions are noted here.

---

## New Operations in v2.1

### LLM Backend Fallback (IDEA-008)

When using the workbench, if MinMax M2.7 fails 3 consecutive times, the system automatically switches to Claude Sonnet API. No manual intervention required.

**To force a specific backend:**
- Edit `.clinerules` RULE 5 to adjust the error threshold
- Update `Modelfile` to point to a different OpenRouter model

### SP-002 Coherence Verification

If you modify `.clinerules`, run the sync check:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-prompts-sync.ps1
```

Expected: **6 PASS | 0 FAIL | 1 WARN** (SP-007 is manual).

---

## All v2.0 Operations Preserved

All operations described in [DOC-4 v2.0](docs/releases/v2.0/DOC-4-v2.0-Operations-Guide.md) remain valid, including:
- Memory Bank hot/cold management
- Calypso orchestration pipeline
- Global Brain / Librarian Agent
- deploy-workbench-to-project.ps1
- pre-commit hook

---

*End of DOC-4 v2.1*
