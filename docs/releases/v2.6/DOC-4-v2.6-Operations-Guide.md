---
doc_id: DOC-4
release: v2.6
status: Draft
title: Operations Guide
version: 1.0
date_created: 2026-04-01
authors: [Developer mode, Human]
previous_release: v2.5
cumulative: true
---

# DOC-4 — Operations Guide (v2.6)

> **Status: DRAFT** -- This document is in draft for v2.6.0 release.
> **Cumulative: YES** -- This document contains all operations guidance from v1.0 through v2.6.

---

## Table of Contents

1. [Session Checkpoint Operations](#1-session-checkpoint-operations)
2. [Heartbeat Script Usage](#2-heartbeat-script-usage)
3. [ADR Management](#3-adr-management)
4. [Artifact ID Generation](#4-artifact-id-generation)

---

## 1. Session Checkpoint Operations

### 1.1 Starting a Session

At session start, read the checkpoint:

```bash
# Check current checkpoint status
python scripts/checkpoint_heartbeat.py --status
```

### 1.2 Crash Detection

If `last_heartbeat > 30 minutes`, the session was likely interrupted.

Recovery options:
- Continue from last checkpoint
- Start fresh (context may be lost)

---

## 2. Heartbeat Script Usage

### 2.1 Commands

| Command | Description |
|---------|-------------|
| `--start` | Start 5-minute heartbeat loop |
| `--stop` | Stop heartbeat loop |
| `--once` | Write single heartbeat and exit |
| `--status` | Show current checkpoint status |

### 2.2 Examples

```bash
# Start heartbeat for active work session
python scripts/checkpoint_heartbeat.py --start

# Write a manual heartbeat
python scripts/checkpoint_heartbeat.py --once

# Check status
python scripts/checkpoint_heartbeat.py --status

# Stop when done
python scripts/checkpoint_heartbeat.py --stop
```

---

## 3. ADR Management

### 3.1 APPEND ONLY Rule

**decisionLog.md is APPEND ONLY**

- Never edit existing ADRs
- Never delete ADRs
- Append new ADRs at the bottom

### 3.2 Adding an ADR

```markdown
## ADR-NEW: Your Decision Title
**Date:** 2026-04-01
**Status:** Accepted

**Context:**
What was the situation?

**Decision:**
What was decided?

**Consequences:**
What are the outcomes?
```

---

## 4. Artifact ID Generation

### 4.1 Daily Sequential Counter

IDs reset at midnight UTC each day:

| Day | Sequence |
|-----|----------|
| 2026-04-01 | IDEA-2026-04-01-001, IDEA-2026-04-01-002, ... |
| 2026-04-02 | IDEA-2026-04-02-001, IDEA-2026-04-02-002, ... |

### 4.2 Quick Reference

| Type | Format | Example |
|------|--------|---------|
| Idea | `IDEA-YYYY-MM-DD-NNN` | `IDEA-2026-04-01-001` |
| ADR | `ADR-YYYY-MM-DD-NNN` | `ADR-2026-04-01-001` |
| Tech | `TECH-YYYY-MM-DD-NNN` | `TECH-2026-04-01-001` |
| Session | `sYYYY-MM-DD-{mode}-NNN` | `s2026-04-01-developer-001` |
| Enhancement | `ENH-YYYY-MM-DD-NNN` | `ENH-2026-04-01-001` |
