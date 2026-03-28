---
doc_id: DOC-1
release: v2.1
status: Frozen
title: Product Requirements Document
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v2.0/DOC-1-v2.0-PRD.md
---

# DOC-1 -- Product Requirements Document (v2.1)

> **Status: FROZEN** -- This document is read-only. Do not modify.

---

## Overview

v2.1 is a **production hotfix release** addressing two critical quality concerns:

1. **LLM backend resilience** -- OpenRouter MinMax M2.7 as default with Claude fallback
2. **System prompt coherence** -- `.clinerules` and `SP-002` synchronization fixes

This is not a feature release. The v2.0 workflow remains unchanged.

---

## Scope of v2.1

| IDEA | Title | Type | Status |
|------|-------|------|--------|
| IDEA-008 | OpenRouter MinMax M2.7 as default LLM + Claude fallback | feat | [IMPLEMENTED] |
| SP-002 Coherence | .clinerules content corruption fixes | fix | [IMPLEMENTED] |
| ADR-005 | GitFlow enforcement (RULE 10) | chore | [IMPLEMENTED] |

---

## Out of Scope for v2.1

- New phases (PHASE-E, PHASE-F, etc.)
- DOC6 revision (conversation log, out of scope)
- Brownfield workflow
- Multi-developer collaboration

---

## v2.0 Workflow Preserved

All v2.0 features and workflows remain unchanged and are carried forward:

- Hot/Cold memory architecture (PHASE-A)
- Template folder enrichment (PHASE-B)
- Calypso orchestration scripts (PHASE-C)
- Global Brain / Librarian Agent (PHASE-D)
- 4 Agile personas (.roomodes)
- Memory Bank (7 files)
- pre-commit hook (check-prompts-sync.ps1)

---

*End of DOC-1 v2.1*
