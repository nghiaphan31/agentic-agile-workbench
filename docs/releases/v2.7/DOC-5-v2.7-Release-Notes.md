---
doc_id: DOC-5
release: v2.7
status: Draft
title: Release Notes
version: 1.0
date_created: 2026-04-02
authors: [Scrum Master mode, Human]
previous_release: v2.6
cumulative: true
---

# DOC-5 — Release Notes (v2.7)

> **Status: DRAFT** -- This document is in draft for v2.7.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all release notes from v1.0 through v2.7.

---

## Table of Contents

1. [v2.7 Summary](#1-v27-summary)
2. [What's New in v2.7](#2-whats-new-in-v27)
3. [Breaking Changes](#3-breaking-changes)
4. [Migration Guide](#4-migration-guide)
5. [Known Issues](#5-known-issues)
6. [Previous Releases](#6-previous-releases)

---

## 1. v2.7 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-04-02 |
| **Type** | Critical Bug Fix — Canonical Docs |
| **IDEA** | IDEA-017: Canonical docs must be cumulative/self-contained |
| **Commits** | Multiple (DOC-1 through DOC-5 rebuilt) |
| **Breaking Changes** | None |
| **Minimum Line Counts** | Enforced via GitHub Actions CI |

### v2.7 Highlights

- **RULE 12 Enforcement**: Canonical docs now properly cumulative with GitHub Actions CI validation
- **DOC-1**: 10 sections (v1.0-v2.7), comprehensive PRD with RBAC matrix
- **DOC-2**: 903 lines, full architecture from all versions
- **DOC-3**: 536 lines, complete implementation plan
- **DOC-4**: 321 lines, comprehensive operations guide
- **DOC-5**: Consolidated release notes

---

## 2. What's New in v2.7

### IDEA-017: Canonical Docs Cumulative Requirement

This release addresses a critical (P0) issue where canonical docs were NOT properly cumulative/self-contained as required by RULE 12.

#### The Problem

Previous v2.6 docs claimed `cumulative: true` but:
- v2.6 DOC-1 had only 120 lines (needs 500+)
- v2.6 DOC-2 had only 148 lines (needs 500+)
- v2.6 DOC-3 had only 166 lines (needs 300+)
- v2.6 DOC-4 had only 128 lines (needs 300+)
- v2.6 DOC-5 had only 165 lines (needs 200+)
- Missing intermediate version sections (v2.1-v2.5)

#### The Solution

v2.7 canonical docs are **properly cumulative**:
- All content from v1.0 through v2.7 included
- Each version has its own section
- Minimum line counts verified by GitHub Actions CI
- Front matter `cumulative: true` is accurate

#### GitHub Actions CI Enforcement

New workflow at `.github/workflows/canonical-docs-check.yml` validates:
1. All 5 DOC-*-vX.Y.md files exist for each release
2. All DOC-*-vX.Y.md have `cumulative: true` front matter
3. All DOC-*-vX.Y.md meet minimum line counts:
   - DOC-1 >= 500 lines
   - DOC-2 >= 500 lines
   - DOC-3 >= 300 lines
   - DOC-4 >= 300 lines
   - DOC-5 >= 200 lines

---

## 3. Breaking Changes

None. This release only fixes documentation compliance.

---

## 4. Migration Guide

No migration needed. v2.7 docs are drop-in replacements for v2.6 docs.

**Action Required:**
1. Pull latest changes
2. Review DOC-1 through DOC-5 for v2.7 updates
3. No code or configuration changes needed

---

## 5. Known Issues

None reported.

---

## 6. Previous Releases

### v2.6 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-04-01 |
| **Type** | Governance Enhancement |
| **Commits** | 8 (Phases 1-2 of PLAN-2026-04-01-001) |

**New Features:**
- RULE MB-2: Session Checkpoint (crash recovery)
- RULE MB-3: APPEND ONLY for ADRs
- Artifact Identification Schema (TYPE-YYYY-MM-DD-NNN)
- Plan-Branch Parity (RULE G-0)
- `scripts/checkpoint_heartbeat.py` for 5-minute heartbeat

---

### v2.5 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-30 |
| **Type** | Documentation Governance |

**New Features:**
- RULE 8: Documentation Discipline (The Two Spaces)
- Idea Capture Mandate
- Conversation Log Mandate
- IDEA-014: Canonical docs status governance
- IDEA-015: Release coherence audit

---

### v2.4 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-30 |
| **Type** | Ideation-to-Release Governance |

**New Features:**
- ADR-010: Ad-Hoc Governance (two paths: STRUCTURED vs AD-HOC)
- Release tier criteria (Minor/Medium/Major)
- Calypso orchestration scripts
- 4-agent pipeline: intake → triage → refinement → execution

---

### v2.3 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-29 |
| **Type** | Anthropic Batch API Toolkit |

**New Features:**
- IDEA-009: Generic Anthropic Batch API Toolkit (`scripts/batch/`)
- BatchConfig dataclass + YAML loader
- CLI entry point (`python -m scripts.batch.cli`)
- Jinja2 script generator
- Self-contained `template/scripts/batch/` bundle

---

### v2.2 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-28 |
| **Type** | GitFlow Clarification |

**Changes:**
- ADR-011: GitFlow Violation Remediation
- Clarified feature branch lifecycle
- Added hotfix branch definition
- Branch preservation requirement documented

---

### v2.1 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-27 |
| **Type** | Ideation Pipeline Formalization |

**New Features:**
- Ideation-to-Release Pipeline (PHASE-A → PHASE-B → PHASE-C)
- RULE 10: GitFlow Enforcement (ADR-006)
- IDEA-008: LLM Backend Resilience (minimax fallback)
- SP-002 Coherence Fix (encoding issues resolved)

---

### v2.0 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-26 |
| **Type** | Major Refactor |

**Changes:**
- 3-Mode LLM Switcher (Local/Proxy/Cloud)
- Boomerang Tasks for lightweight model delegation
- Anthropic Batch API integration
- Enhanced prompt registry

---

### v1.0 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-23 |
| **Type** | Initial Working Release |

**Delivered Features:**

1. **3-Mode LLM Switcher**
   - Mode 1: Local Ollama (calypso:11434)
   - Mode 2: Gemini Chrome Proxy (localhost:8000)
   - Mode 3: Anthropic Claude API

2. **4 Agile Personas (.roomodes)**
   - Product Owner, Scrum Master, Developer, QA Engineer
   - RBAC permissions defined

3. **Memory Bank (7 files + .clinerules 7 rules)**
   - activeContext.md, progress.md, projectBrief.md, productContext.md
   - systemPatterns.md, techContext.md, decisionLog.md
   - Mandatory read/write cycle

4. **Prompts Registry (prompts/ SP-001 to SP-007)**
   - Centralized system prompt registry with YAML metadata
   - Pre-commit hook for consistency verification

5. **Project Template Folder (template/)**
   - Complete deployable template for new projects
   - deploy-workbench-to-project.ps1 script

---

## Appendix: Release Tag Reference

| Tag | Date | Key Feature |
|-----|------|-------------|
| v1.0.0 | 2026-03-28 | Initial working release |
| v2.0.0 | 2026-03-26 | Major refactor (3-mode switcher) |
| v2.1.0 | 2026-03-27 | Ideation pipeline |
| v2.2.0 | 2026-03-28 | GitFlow clarification |
| v2.3.0 | 2026-03-29 | Batch API toolkit |
| v2.4.0 | 2026-03-30 | Ad-hoc governance |
| v2.5.0 | 2026-03-30 | Documentation governance |
| v2.6.0 | 2026-04-01 | Session checkpoint |
| v2.7.0 | 2026-04-02 | Canonical docs fix |
