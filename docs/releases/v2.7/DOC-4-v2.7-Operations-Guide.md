---
doc_id: DOC-4
release: v2.7
status: Draft
title: Operations Guide
version: 1.0
date_created: 2026-04-02
authors: [Developer mode, Human]
previous_release: v2.6
cumulative: true
---

# DOC-4 — Operations Guide (v2.7)

> **Status: DRAFT** -- This document is in draft for v2.7.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all operations guidance from v1.0 through v2.7.
> To understand the full project operations history, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [Workbench Deployment Guide](#1-workbench-deployment-guide)
2. [Session Checkpoint Operations](#2-session-checkpoint-operations)
3. [Heartbeat Script Usage](#3-heartbeat-script-usage)
4. [ADR Management](#4-adr-management)
5. [Artifact ID Generation](#5-artifact-id-generation)
6. [Canonical Docs Operations](#6-canonical-docs-operations)
7. [Prompt Registry Operations](#7-prompt-registry-operations)

---

## 1. Workbench Deployment Guide

### 1.1 Understanding What This Repository Is (and Is Not)

```
agentic-agile-workbench/   ← YOU ARE HERE
│                                     This is the WORKBENCH
│
│  docs/           ← The workbench documentation (DOC1-5)
│  prompts/        ← The workbench tools (system prompts SP-001 to SP-010)
│  proxy.py        ← A workbench machine (Roo Code <-> Gemini Chrome bridge)
│  .roomodes       ← The workbench worker roles (4 Agile personas)
│  .clinerules     ← The workbench rulebook (15 mandatory rules)
│  scripts/        ← The workbench utility scripts
│
└── It produces PROJECTS (separate repositories, in other folders)
```

**This repository contains no application code.** It contains the rules, tools, processes and system prompts that enable developing any project in an agentic, agile and versioned manner.

### 1.2 Deployment Checklist

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Clone repository to local machine | `git clone <repo-url>` |
| 2 | Install Python 3.10+ dependencies | `pip install -r requirements.txt` |
| 3 | Copy template to new project | `.\deploy-workbench-to-project.ps1 -TargetPath ./my-project` |
| 4 | Initialize Git in target project | `cd ./my-project && git init` |
| 5 | Configure Roo Code in VS Code | Install Roo Code extension, configure API provider |
| 6 | Verify Memory Bank structure | `ls memory-bank/hot-context/` shows 6 files |
| 7 | Test pre-commit hook | `git commit` triggers prompt sync check |

---

## 2. Session Checkpoint Operations

### 2.1 Starting a Session

At session start, the agent MUST:
1. Read `memory-bank/hot-context/session-checkpoint.md`
2. Check `last_heartbeat` timestamp
3. If `last_heartbeat > 30 minutes`, report crash detection
4. Offer recovery options: continue from checkpoint or start fresh

### 2.2 Crash Detection Logic

```
IF session-checkpoint.last_heartbeat > NOW - 30 minutes:
    → Session is ACTIVE
ELSE:
    → Session was INTERRUPTED
    → Report: "Crash detected. Last heartbeat X minutes ago."
    → Offer: [Continue] [Start Fresh]
```

### 2.3 Session ID Format

Sessions use the format: `s{YYYY-MM-DD}-{mode}-{NNN}`

Examples:
- `s2026-04-02-developer-001`
- `s2026-04-02-scrum-master-002`
- `s2026-04-02-qa-engineer-001`

---

## 3. Heartbeat Script Usage

### 3.1 Commands

| Command | Description |
|---------|-------------|
| `--start` | Start 5-minute heartbeat loop (runs continuously) |
| `--stop` | Stop heartbeat loop |
| `--once` | Write single heartbeat and exit |
| `--status` | Show current checkpoint status |

### 3.2 Examples

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

### 3.3 RULE MB-2: Session Checkpoint

Every 5 minutes during active work:
1. Update `session-checkpoint.md.last_heartbeat`
2. Update `session-checkpoint.md.git_state`
3. Update `session-checkpoint.md.current_task`

---

## 4. ADR Management

### 4.1 RULE MB-3: APPEND ONLY for ADRs

`decisionLog.md` is **APPEND ONLY**:
- Never overwrite existing ADRs
- Never delete entries
- Archive old entries to cold only when file > 500 lines

### 4.2 Creating New ADRs

Format:
```markdown
## ADR-{YYYY-MM-DD}-{NNN}

**Date:** {YYYY-MM-DD}
**Status:** {PROPOSED | ACCEPTED | REJECTED | SUPERSEDED}
**Superseded by:** {ADR-ID if applicable}

### Context
[What problem or decision prompted this ADR?]

### Decision
[What is the decision made?]

### Consequences
[What are the consequences of this decision?]
```

### 4.3 ADR ID Format

Architecture Decisions use: `ADR-{YYYY-MM-DD}-{NNN}`

Examples:
- `ADR-2026-03-23-001` (DA-001 in DOC-2)
- `ADR-2026-04-01-001`

---

## 5. Artifact ID Generation

### 5.1 All Artifact ID Formats

| Type | Format | Example |
|------|--------|---------|
| Business Idea | `IDEA-{YYYY-MM-DD}-{NNN}` | `IDEA-2026-04-01-001` |
| Technical Suggestion | `TECH-{YYYY-MM-DD}-{NNN}` | `TECH-2026-04-01-001` |
| Architecture Decision | `ADR-{YYYY-MM-DD}-{NNN}` | `ADR-2026-04-01-001` |
| Session | `s{YYYY-MM-DD}-{mode}-{NNN}` | `s2026-04-01-developer-001` |
| Refinement Session | `REF-{YYYY-MM-DD}-{NNN}` | `REF-2026-04-01-001` |
| Conversation | `{YYYY-MM-DD}-{source}-{slug}` | `2026-04-01-gemini-workbench` |
| Batch Job | `BATCH-{YYYY-MM-DD}-{NNNN}` | `BATCH-2026-04-01-0001` |
| Expert Report | `RPT-{YYYY-MM-DD}-{NNNN}` | `RPT-2026-04-01-0001` |
| Enhancement | `ENH-{YYYY-MM-DD}-{NNN}` | `ENH-2026-04-01-001` |
| Checkpoint | `CHECKPOINT-{YYYY-MM-DD}-{NNN}` | `CHECKPOINT-2026-04-01-001` |

### 5.2 Plan-Branch Parity (RULE G-0)

Every plan creates a branch:
- Plan ID: `PLAN-{YYYY-MM-DD}-{NNN}` or `PLAN-{slug}`
- Branch name: `feature/{slug}` or `governance/PLAN-{slug}`
- Branch preserved after merge (never deleted for traceability)

---

## 6. Canonical Docs Operations

### 6.1 The Two Spaces

| Space | Location | Status | Rules |
|-------|----------|--------|-------|
| **Frozen** | `docs/releases/vX.Y/*.md` with `status: Frozen` | READ-ONLY | Never modify |
| **Draft** | `docs/releases/vX.Y/*.md` with `status: Draft` | Modifiable | Only Architect/PO |
| **Working** | `memory-bank/*.md` | Agent-writable | Update freely |

### 6.2 Canonical Docs Minimum Line Counts

| Doc | Minimum | Purpose |
|-----|---------|---------|
| DOC-1 | 500 lines | Product Requirements Document |
| DOC-2 | 500 lines | Technical Architecture |
| DOC-3 | 300 lines | Implementation Plan |
| DOC-4 | 300 lines | Operations Guide |
| DOC-5 | 200 lines | Release Notes |

### 6.3 Creating New Release Docs

When creating vX.Y canonical docs:
1. Create `docs/releases/vX.Y/` directory
2. Create all 5 DOC-*-vX.Y-*.md files
3. Set `cumulative: true` front matter
4. Set `status: Draft`
5. Ensure line counts meet minimums
6. Update `DOC-*-CURRENT.md` pointers after freeze

### 6.4 Idea Capture Mandate

When identifying a new requirement NOT in current release scope:
1. DO NOT modify current release's canonical docs
2. ADD entry to `docs/ideas/IDEAS-BACKLOG.md` with status [IDEA]
3. CREATE `docs/ideas/IDEA-{NNN}-{slug}.md`
4. INFORM human that new idea has been captured

### 6.5 Conversation Log Mandate

When saving AI conversation output:
1. Save to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`
2. Add entry to `docs/conversations/README.md` with triage status
3. Never edit a conversation file after creation

---

## 7. Prompt Registry Operations

### 7.1 Registry Structure

```
prompts/
├── README.md                    # Registry index
├── SP-001-ollama-modelfile-system.md
├── SP-002-clinerules-global.md
├── SP-003-persona-product-owner.md
├── SP-004-persona-scrum-master.md
├── SP-005-persona-developer.md
├── SP-006-persona-qa-engineer.md
├── SP-007-gem-gemini-roo-agent.md (hors_git: true)
├── SP-008-synthesizer-agent.md
├── SP-009-devils-advocate-agent.md
└── SP-010-librarian-agent.md
```

### 7.2 SP Metadata Format

```yaml
---
sp_id: SP-XXX
version: 1.0
target: .roomodes | .clinerules | Modelfile | Gemini Gem
dependencies: [SP-XXX if any]
changelog:
  - YYYY-MM-DD: Initial version
  - YYYY-MM-DD: Updated description
---
```

### 7.3 Pre-Commit Verification

Before each commit:
1. `scripts/check-prompts-sync.ps1` runs automatically via Git hook
2. Compares canonical SPs vs deployed artifacts
3. Reports PASS/FAIL for each SP
4. SP-007 excluded (manual deployment required)
5. Commit blocked if desynchronization detected

### 7.4 SP-007 Manual Deployment

SP-007 (Gemini Gem) requires manual deployment:
1. Read `prompts/SP-007-gem-gemini-roo-agent.md`
2. Copy content to Gemini Gem at gemini.google.com
3. Save and activate
4. Verify manually

---

## Appendix: RULE Quick Reference

| RULE | Domain | Title |
|------|--------|-------|
| RULE 1 | Memory Bank | CHECK→CREATE→READ→ACT sequence |
| RULE 2 | Memory Bank | Write at close of each task |
| RULE 3 | Memory Bank | Contextual read based on task |
| RULE 4 | Memory Bank | No exceptions to Rules 1-3 |
| RULE 5 | Git | Versioning mandatory |
| RULE 6 | Prompts | Prompt registry consistency |
| RULE 7 | Large Files | Chunking protocol (>500 lines) |
| RULE 8 | Docs | Documentation discipline |
| RULE 9 | Memory | Cold zone firewall |
| RULE 10 | Git | GitFlow enforcement |
| RULE 11 | Sync | Synchronization awareness |
| RULE 12 | Docs | Canonical docs cumulative |
| RULE 13 | Ideas | Ideation intake |
| RULE 14 | Ideas | DOC-3 execution chapter |
| RULE 15 | Tech | Technical suggestions backlog |
| MB-2 | Memory | Session checkpoint (5-min heartbeat) |
| MB-3 | Memory | APPEND ONLY for ADRs |
| G-0 | Git | Plan-branch parity |
