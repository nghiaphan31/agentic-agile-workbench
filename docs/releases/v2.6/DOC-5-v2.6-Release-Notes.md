---
doc_id: DOC-5
release: v2.6
status: Draft
title: Release Notes
version: 1.0
date_created: 2026-04-01
authors: [Developer mode, Human]
previous_release: v2.5
cumulative: true
---

# DOC-5 -- Release Notes (v2.6)

> **Status: DRAFT** -- This document is in draft for v2.6.0 release. It will be frozen upon release.

---

## Table of Contents

1. [v2.6 Summary](#1-v26-summary)
2. [What's New](#2-whats-new)
3. [Breaking Changes](#3-breaking-changes)
4. [Migration Guide](#4-migration-guide)
5. [Known Issues](#5-known-issues)
6. [Previous Releases](#6-previous-releases)

---

## 1. v2.6 Summary

| Item | Details |
|------|---------|
| **Release Date** | 2026-04-01 |
| **Type** | Governance Enhancement |
| **Commits** | 8 (Phases 1-2 of PLAN-2026-04-01-001) |
| **Breaking Changes** | None |

---

## 2. What's New

### PLAN-2026-04-001: Governance Enhancement

This release implements the first two phases of PLAN-2026-04-01-001, bringing Memory Bank best practices and session crash recovery to the workbench.

#### Phase 1: Memory Bank Enhancements

**New Features:**

- **RULE MB-2 (Session Checkpoint):** Crash recovery checkpoint
  - New file: `memory-bank/hot-context/session-checkpoint.md`
  - Read at session start for crash recovery
  - Written every 5 minutes during active work

- **RULE MB-3 (APPEND ONLY for ADRs):** Decision log safety
  - `decisionLog.md` is now APPEND ONLY
  - Never overwrite, never delete existing ADRs
  - To update status, append a new entry

- **Artifact Identification Schema:** Part 0 of governance plan
  - All artifacts now use `TYPE-YYYY-MM-DD-NNN` format
  - Example: `IDEA-2026-04-01-001`, `ADR-2026-04-01-001`
  - Session IDs: `sYYYY-MM-DD-{mode}-{NNN}`

- **Plan-to-Branch Lifecycle:** RULE G-0
  - Every plan creates a branch
  - Branch naming: `governance/PLAN-{ID}-{slug}`
  - Branches preserved after merge (no deletion)

#### Phase 2: Heartbeat Script

**New Features:**

- **scripts/checkpoint_heartbeat.py:** 5-minute heartbeat automation
  - `python checkpoint_heartbeat.py --start` — Start heartbeat loop
  - `python checkpoint_heartbeat.py --stop` — Stop heartbeat loop
  - `python checkpoint_heartbeat.py --once` — Write single heartbeat
  - `python checkpoint_heartbeat.py --status` — Show checkpoint status

- Captures Git state (branch, commit, files) in checkpoint

### New Governance Rules

| Rule | Description |
|------|-------------|
| **RULE MB-1** | Memory Bank as Cognitive Prosthetic |
| **RULE MB-2** | Session Checkpoint (Crash Recovery) |
| **RULE MB-3** | APPEND ONLY for ADRs |
| **RULE MB-4** | File Size Rotation |
| **RULE G-0** | Plan-Branch Parity |
| **RULE D-1** | Deferred Enhancement Tracking |

### New Artifact Schema

| Type | Format | Example |
|------|--------|---------|
| Business Idea | `IDEA-{YYYY-MM-DD}-{NNN}` | `IDEA-2026-04-01-001` |
| Technical Suggestion | `TECH-{YYYY-MM-DD}-{NNN}` | `TECH-2026-04-01-001` |
| Architecture Decision | `ADR-{YYYY-MM-DD}-{NNN}` | `ADR-2026-04-01-001` |
| Session | `s{YYYY-MM-DD}-{mode}-{NNN}` | `s2026-04-01-developer-001` |
| Enhancement | `ENH-{YYYY-MM-DD}-{NNN}` | `ENH-2026-04-01-001` |

### Deferred Enhancements (Tracked)

| ID | Enhancement | Status | Target |
|----|--------------|--------|--------|
| ENH-2026-04-01-001 | MCP Memory Server Integration | DEFERRED | v3.0 |
| ENH-2026-04-01-002 | Semantic Cold Archive Query | DEFERRED | v3.0 |

---

## 3. Breaking Changes

**None.** This release contains only governance improvements with no breaking changes to existing functionality.

---

## 4. Migration Guide

### For Users

No migration required. This is a governance-only release.

### For Developers

1. **New session-checkpoint.md** will be created automatically on first heartbeat
2. **decisionLog.md** should now be treated as APPEND ONLY — do not edit or delete existing entries
3. **Branches are preserved** after merge — no need to clean up feature branches

### Using the Heartbeat Script

```bash
# Start automatic 5-minute heartbeat
python scripts/checkpoint_heartbeat.py --start

# Write a single heartbeat
python scripts/checkpoint_heartbeat.py --once

# Check current status
python scripts/checkpoint_heartbeat.py --status

# Stop heartbeat when done
python scripts/checkpoint_heartbeat.py --stop
```

---

## 5. Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| PRs merged to `master` instead of `develop` | Low | Fast-forwarded `develop` manually |

---

## 6. Previous Releases

- [DOC-5-v2.5-Release-Notes.md](../v2.5/DOC-5-v2.5-Release-Notes.md) (v2.5.0)
- [DOC-5-v2.4-Release-Notes.md](../v2.4/DOC-5-v2.4-Release-Notes.md) (v2.4.0)
- [DOC-5-v2.3-Release-Notes.md](../v2.3/DOC-5-v2.3-Release-Notes.md) (v2.3.0)
- [DOC-5-v2.2-Release-Notes.md](../v2.2/DOC-5-v2.2-Release-Notes.md) (v2.2.0)
- [DOC-5-v2.1-Release-Notes.md](../v2.1/DOC-5-v2.1-Release-Notes.md) (v2.1.0)
- [DOC-5-v2.0-Release-Notes.md](../v2.0/DOC-5-v2.0-Release-Notes.md) (v2.0.0)
