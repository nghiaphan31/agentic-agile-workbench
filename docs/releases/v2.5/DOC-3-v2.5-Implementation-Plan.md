---
doc_id: DOC-3
release: v2.5
status: Draft
title: Implementation Plan
version: 1.0
date_created: 2026-03-31
authors: [Scrum Master mode, Human]
previous_release: v2.4
cumulative: true
---

# DOC-3 -- Implementation Plan (v2.5)

> **Status: DRAFT** -- This document is in draft for v2.5.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all implementation tracking from v1.0 through v2.5.
> To understand the full implementation history, read this document from top to bottom.

---

## Table of Contents

1. [v2.5 Scope](#1-v25-scope)
2. [v2.5 Execution Tracker](#2-v25-execution-tracker)
3. [v2.4 Execution Summary](#3-v24-execution-summary)
4. [v2.3 Execution Summary](#4-v23-execution-summary)
5. [Previous Releases](#5-previous-releases)

---

## 1. v2.5 Scope

### ADR-012: Canonical Docs Cumulative + GitFlow Enforcement

| IDEA | Title | Status | Notes |
|------|-------|--------|-------|
| IDEA-NNN | Canonical Docs GitFlow | IMPLEMENTED | ADR-012 |

**Key Deliverables:**
- RULE 12: Canonical docs cumulative requirement (DOC-1..DOC-5 min line counts)
- RULE 12: GitFlow enforcement for canonical docs (feature branch workflow)
- Git pre-receive hook at `.githooks/pre-receive`
- GitHub Actions CI at `.github/workflows/canonical-docs-check.yml`
- Template deployment script updated

### ADR-013: Squash Merge Prohibition

**Key Deliverables:**
- RULE 10.3 updated to forbid squash merge
- RULE 10.3 item 6: Never use `--delete-branch`
- Feature branches kept after merge for traceability

---

## 2. v2.5 Execution Tracker

### Session Log

| Date | Commit | Action | Status |
|------|--------|--------|--------|
| 2026-03-31 | cb06d10 | Created develop-v2.5 branch | DONE |
| 2026-03-31 | -- | Created DOC-1-v2.5-PRD.md | DONE |
| 2026-03-31 | -- | Created DOC-2-v2.5-Architecture.md | DONE |
| 2026-03-31 | -- | Created DOC-3-v2.5-Implementation-Plan.md | IN PROGRESS |
| 2026-03-31 | -- | Created DOC-4-v2.5-Operations-Guide.md | PENDING |
| 2026-03-31 | -- | Created DOC-5-v2.5-Release-Notes.md | PENDING |
| 2026-03-31 | -- | QA pass | PENDING |
| 2026-03-31 | -- | Human approval | PENDING |
| 2026-03-31 | -- | Tag v2.5.0 | PENDING |
| 2026-03-31 | -- | Merge to master | PENDING |

---

## 3. v2.4 Execution Summary

### Epic 1: Agentic Agile Workbench Architecture (DOC6)

| Feature | Status | Notes |
|---------|--------|-------|
| DOC6-PRD-AGENTIC-AGILE-PROCESS.md | CLOSED | First Gemini conversation |
| _Agentic Workbench Architecture Explained | CLOSED | Second Gemini conversation |
| Batch 1 -- DOC6 Expert Review | CLOSED | Submitted + retrieved |
| Batch 2 -- Second-Pass Vision Analysis | CLOSED | Submitted + retrieved |
| Migration Phase A: Hot/Cold memory | CLOSED | ADR-001 implemented |
| Migration Phase B: Template enrichment | CLOSED | Template folder completed |
| Migration Phase C: Calypso scripts | CLOSED | Phase 2-4 implemented |
| Migration Phase D: Global Brain | CLOSED | ChromaDB + Librarian Agent |
| SP-008 Synthesizer Agent | CLOSED | Implemented |
| SP-009 Devil's Advocate Agent | CLOSED | Implemented |
| SP-010 Librarian Agent | CLOSED | Implemented |

### Epic 2: Calypso Orchestration v1

| Feature | Status | Notes |
|---------|--------|-------|
| Phase 2: Expert Reports | CLOSED | 4 expert reports generated |
| Phase 3: Triage | CLOSED | 20 backlog items classified |
| Phase 4: Orchestration | CLOSED | 20/20 items processed |

---

## 4. v2.3 Execution Summary

### IDEA-009: Generic Anthropic Batch API Toolkit

| Feature | Status | Notes |
|---------|--------|-------|
| scripts/batch/ CLI | CLOSED | 8 modules + 2 templates |
| template/scripts/batch/ | CLOSED | 7 modules + 2 templates |
| config.py | CLOSED | BatchConfig + YAML loader |
| submit.py | CLOSED | Batch submission |
| retrieve.py | CLOSED | Result retrieval |
| poll.py | CLOSED | Polling utility |
| cli.py | CLOSED | CLI with commands |
| generate.py | CLOSED | Jinja2 generator |

### IDEA-011: SP-002 Coherence Fix

| Feature | Status | Notes |
|---------|--------|-------|
| BOM/mojibake detection | CLOSED | UTF-8 BOM, Latin-1 mojibake fixed |
| SP-002 synchronization | CLOSED | 6 PASS, 0 FAIL |

---

## 5. Previous Releases

See `docs/releases/v1.0/DOC-3-v1.0-Implementation-Plan.md` through `docs/releases/v2.4/DOC-3-v2.4-Implementation-Plan.md` for earlier implementation history.

---

*End of DOC-3-v2.5-Implementation-Plan.md*
