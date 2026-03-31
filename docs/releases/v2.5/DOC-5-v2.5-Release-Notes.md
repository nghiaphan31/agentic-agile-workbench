---
doc_id: DOC-5
release: v2.5
status: Draft
title: Release Notes
version: 1.0
date_created: 2026-03-31
authors: [Scrum Master mode, Human]
previous_release: v2.4
cumulative: true
---

# DOC-5 -- Release Notes (v2.5)

> **Status: DRAFT** -- This document is in draft for v2.5.0 release. It will be frozen upon release.

---

## Table of Contents

1. [v2.5 Summary](#1-v25-summary)
2. [What's New](#2-whats-new)
3. [Breaking Changes](#3-breaking-changes)
4. [Migration Guide](#4-migration-guide)
5. [Known Issues](#5-known-issues)
6. [Previous Releases](#6-previous-releases)

---

## 1. v2.5 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-03-31 |
| **Type** | Governance Enhancement |
| **Commits** | 2 (ADR-012, ADR-013) |
| **Breaking Changes** | None |

---

## 2. What's New

### ADR-012: Canonical Docs Cumulative + GitFlow Enforcement

This release introduces structural enforcement for canonical documentation governance.

**New Features:**
- **RULE 12 (CANON):** Canonical docs cumulative requirement
  - DOC-1 minimum: 500 lines
  - DOC-2 minimum: 500 lines
  - DOC-3 minimum: 300 lines
  - DOC-4 minimum: 300 lines
  - DOC-5 minimum: 200 lines

- **Git Pre-Receive Hook:** `.githooks/pre-receive`
  - Validates DOC-*-CURRENT.md pointer consistency
  - Checks cumulative nature of canonical docs
  - Enforces feature branch workflow

- **GitHub Actions CI:** `.github/workflows/canonical-docs-check.yml`
  - Runs on PR to `develop`, `develop-v*`, `main`
  - Validates DOC pointer consistency
  - Enforces R-CANON rules

### ADR-013: Squash Merge Prohibition

This release fixes a critical traceability issue by forbidding squash merges.

**Changes:**
- **RULE 10.3 item 4:** Now says "fast-forward merge preferred, NO squash merge"
- **RULE 10.3 item 6:** "NEVER use `--delete-branch` when merging PRs"
- **RULE 10.3 item 7:** "Prefer fast-forward or regular merge over squash merge"

**Impact:** All feature branches are now kept after merge for full commit history traceability.

---

## 3. Breaking Changes

**None.** This release contains only governance improvements with no breaking changes to existing functionality.

---

## 4. Migration Guide

### For Users

No migration required. This is a governance-only release.

### For Developers

If you have pending PRs, please rebase or merge rather than squash:

```bash
# Instead of squash merge
git merge --no-ff feature/your-branch

# Or prefer fast-forward
git merge feature/your-branch
```

---

## 5. Known Issues

| Issue | Status | Workaround |
|-------|--------|------------|
| SP-007 Gem Gemini requires manual deployment | KNOWN | Deploy at https://gemini.google.com > Gems |

---

## 6. Previous Releases

For full history, see:
- [v2.4 Release Notes](v2.4/DOC-5-v2.4-Release-Notes.md)
- [v2.3 Release Notes](v2.3/DOC-5-v2.3-Release-Notes.md)
- [v2.1 Release Notes](v2.1/DOC-5-v2.1-Release-Notes.md)
- [v1.0 Release Notes](v1.0/DOC-5-v1.0-Release-Notes.md)

---

*End of DOC-5-v2.5-Release-Notes.md*
