# Release Governance Model â€” Agentic Agile Workbench
## Universal Project Governance: Workbench Core + Application Projects

**Document ID:** PLAN-release-governance
**Version:** 1.0
**Status:** Draft â€” Pending Implementation
**Date:** 2026-03-28
**Author:** Architect mode (claude-sonnet-4-6)
**Branch:** experiment/architecture-v2

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Core Principles](#2-core-principles)
3. [The Two Separate Spaces](#3-the-two-separate-spaces)
4. [The Universal docs/ Structure](#4-the-universal-docs-structure)
5. [The 5 Canonical Documents](#5-the-5-canonical-documents)
6. [Unambiguous Numbering Convention](#6-unambiguous-numbering-convention)
7. [The Idea Lifecycle](#7-the-idea-lifecycle)
8. [The Conversation Log](#8-the-conversation-log)
9. [The Release Lifecycle](#9-the-release-lifecycle)
10. [The Three Execution Tracking Files](#10-the-three-execution-tracking-files)
11. [Git Branching Strategy](#11-git-branching-strategy)
12. [Agent Rules â€” .clinerules Additions](#12-agent-rules--clinerules-additions)
13. [Migration Plan â€” Current Workbench to v2.0](#13-migration-plan--current-workbench-to-v20)
14. [Application to Application Projects](#14-application-to-application-projects)
15. [Implementation Steps](#15-implementation-steps)

---

## 1. Purpose and Scope

### 1.1 The Problem This Solves

Without a formal governance model, the following problems recur:

- **Tangled concerns:** Ideas for the next release contaminate the current release's canonical docs.
- **Ambiguous numbering:** "Part 1 / Phase 2 / Section 3" creates hierarchy confusion â€” readers cannot determine the relationship between levels.
- **No idea capture discipline:** New ideas are either lost or immediately injected into in-progress docs, breaking coherence.
- **No release boundary:** It is unclear when one release ends and the next begins.
- **No conversation traceability:** AI conversations that inform the project are not systematically logged or mined for ideas.
- **Confusion between docs and agent memory:** `memory-bank/` files and `docs/` files serve different masters but are treated as equivalent.

### 1.2 Scope

This governance model applies **universally** to:

1. **The Agentic Agile Workbench** itself (the factory project)
2. **Every application project** initiated and developed using the workbench

The same rules, the same folder structure, the same document IDs, the same release lifecycle apply to both. This universality is what makes the workbench a true reusable factory â€” it ships not just tooling but also the governance process as a template.

### 1.3 What This Document Is Not

This document is **not** a replacement for DOC-1 (PRD) or DOC-2 (Architecture). It is a **process specification** â€” it defines how all canonical documents are created, versioned, and evolved. It belongs in `docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md` as PHASE-0.

---

## 2. Core Principles

### 2.1 One Release = One Git Tag = One Coherent Snapshot

A **release** is a named, versioned snapshot of the **entire project** at a point in time:
- All source code (`src/`)
- All canonical documentation (`docs/releases/vX.Y/`)
- All configuration files (`.clinerules`, `.roomodes`, `Modelfile`, `proxy.py`)
- All scripts (`scripts/`)
- All memory bank files (`memory-bank/`)
- All QA reports (`docs/qa/vX.Y/`)
- All templates (`template/`)

The Git tag `vX.Y.0` captures all of the above atomically. You do not need to copy files â€” the tag IS the release.

### 2.2 Canonical Docs Are Internally Consistent Within a Release

All 5 canonical documents in a release (`DOC-1` through `DOC-5`) must be coherent with each other. You never mix documents from different releases. A reader picking up `DOC-2-v2.0-Architecture.md` must be able to trust that it describes the same system as `DOC-1-v2.0-PRD.md`.

### 2.3 Ideas Are Captured, Not Injected

New ideas that arrive **during** the implementation of release `vX.Y` go into `docs/ideas/IDEAS-BACKLOG.md` â€” they do **not** modify the in-progress `vX.Y` canonical docs. They wait for the next release's scope decision.

### 2.4 The Two Spaces Never Mix

`docs/` (human-authored specifications) and `memory-bank/` (agent runtime context) are completely separate. Agents read `docs/` but write `memory-bank/`. Humans promote `memory-bank/` insights into the next `docs/` at release time.

### 2.5 Finish Before Starting

You do not start writing the next release's canonical docs until the current release is complete **or** you make a conscious decision to abandon/defer it. The only exception: you may draft the next `DOC-1` (PRD) during the final validation phase of the current release, because it is the longest-lead document.

### 2.6 Release Naming

**Format:** `vMAJOR.MINOR` (e.g., `v1.0`, `v2.0`, `v2.1`)

- `MAJOR` bump = fundamental architectural change (e.g., adding the Calypso orchestration tier)
- `MINOR` bump = additive improvement within the same architecture (e.g., adding Hot/Cold memory to an existing system)

Git tags use the full semver format: `v1.0.0`, `v2.0.0`, `v2.1.0`.

---

## 3. The Two Separate Spaces

### 3.1 Comparison Table

| Dimension | `docs/` | `memory-bank/` |
|---|---|---|
| **Written by** | Humans (with AI assistance) | AI agents (automatically) |
| **Read by** | Humans (primary), AI agents (secondary) | AI agents (primary), Humans (audit) |
| **Purpose** | Authoritative specification of WHAT and HOW | Agent runtime context â€” WHERE AM I RIGHT NOW |
| **Lifecycle** | Versioned per release, frozen at Git tag | Continuously overwritten every session |
| **Stability** | Stable â€” changes only at release boundaries | Volatile â€” changes every session |
| **Truth source** | The project's canonical truth | The agent's current working memory |
| **Analogy** | A book in a library | A whiteboard in a meeting room |

### 3.2 The Interaction Points

They interact at exactly two moments:

**Session start:** Agent reads `docs/releases/vX.Y/` to populate `memory-bank/`
- `DOC-1` â†’ informs `memory-bank/productContext.md`
- `DOC-2` â†’ informs `memory-bank/systemPatterns.md`
- `DOC-3` â†’ informs `memory-bank/progress.md`

**Release end:** Human promotes `memory-bank/` insights into next `docs/`
- `memory-bank/systemPatterns.md` â†’ feeds next `DOC-2` (new patterns discovered during implementation)
- `memory-bank/decisionLog.md` â†’ feeds next `DOC-2` ADR section
- `memory-bank/productContext.md` â†’ feeds next `DOC-1` (backlog evolution)

### 3.3 The Three Overlapping Files â€” Explicit Rules

| Overlap | `docs/` file | `memory-bank/` file | Rule |
|---|---|---|---|
| Implementation plan vs. execution state | `DOC-3` (the plan) | `progress.md` (live checkbox state) | `DOC-3` is the map; `progress.md` is the GPS. Agent reads `DOC-3`, writes `progress.md`. |
| Architecture vs. working patterns | `DOC-2` (approved architecture) | `systemPatterns.md` (working copy) | `systemPatterns.md` is a living draft that feeds the next `DOC-2`. Never a substitute for it. |
| Approved ADRs vs. running decisions | `DOC-2` ADR section (frozen) | `decisionLog.md` (running log) | `decisionLog.md` feeds the next `DOC-2` ADR section at release time. |

---

## 4. The Universal `docs/` Structure

This structure is identical for the workbench project and for every application project built with it. It is included in `template/docs/` so every new project starts with it.

```
docs/
â”œâ”€â”€ DOC-1-CURRENT.md              â† Stub pointing to latest approved PRD
â”œâ”€â”€ DOC-2-CURRENT.md              â† Stub pointing to latest approved Architecture
â”œâ”€â”€ DOC-3-CURRENT.md              â† Stub pointing to latest approved Implementation Plan
â”œâ”€â”€ DOC-4-CURRENT.md              â† Stub pointing to latest approved Operations Guide
â”œâ”€â”€ DOC-5-CURRENT.md              â† Stub pointing to latest Release Notes
â”‚
â”œâ”€â”€ releases/
â”‚   â”œâ”€â”€ v1.0/                     â† Frozen at git tag v1.0.0
â”‚   â”‚   â”œâ”€â”€ DOC-1-v1.0-PRD.md
â”‚   â”‚   â”œâ”€â”€ DOC-2-v1.0-Architecture.md
â”‚   â”‚   â”œâ”€â”€ DOC-3-v1.0-Implementation-Plan.md
â”‚   â”‚   â”œâ”€â”€ DOC-4-v1.0-Operations-Guide.md
â”‚   â”‚   â”œâ”€â”€ DOC-5-v1.0-Release-Notes.md
â”‚   â”‚   â””â”€â”€ EXECUTION-TRACKER-v1.0.md
â”‚   â””â”€â”€ v2.0/                     â† In-progress drafts (current release)
â”‚       â”œâ”€â”€ DOC-1-v2.0-PRD.md
â”‚       â”œâ”€â”€ DOC-2-v2.0-Architecture.md
â”‚       â”œâ”€â”€ DOC-3-v2.0-Implementation-Plan.md
â”‚       â”œâ”€â”€ DOC-4-v2.0-Operations-Guide.md
â”‚       â”œâ”€â”€ DOC-5-v2.0-Release-Notes.md
â”‚       â””â”€â”€ EXECUTION-TRACKER-v2.0.md
â”‚
â”œâ”€â”€ qa/
â”‚   â”œâ”€â”€ v1.0/                     â† QA reports for v1.0
â”‚   â”‚   â””â”€â”€ SP-COHERENCE-FINAL-2026-03-24.md
â”‚   â””â”€â”€ v2.0/                     â† QA reports for v2.0 (in progress)
â”‚
â”œâ”€â”€ ideas/                         â† Continuous â€” not per-release
â”‚   â”œâ”€â”€ IDEAS-BACKLOG.md           â† Master registry with status tracking
â”‚   â”œâ”€â”€ IDEA-001-hot-cold-memory.md
â”‚   â”œâ”€â”€ IDEA-002-calypso-orchestration.md
â”‚   â””â”€â”€ IDEA-003-release-governance.md
â”‚
â””â”€â”€ conversations/                 â† Continuous â€” not per-release
    â”œâ”€â”€ README.md                  â† Index: which conversations generated which ideas
    â”œâ”€â”€ 2026-03-27-gemini-doc6-architecture.md
    â””â”€â”€ 2026-03-28-gemini-workbench-explained.md
```

### 4.1 The `DOC-N-CURRENT.md` Stubs

These are lightweight pointer files â€” they tell a reader which version is current without requiring them to navigate the `releases/` folder:

```markdown
# DOC-1 â€” Product Requirements (Current)

**Current release:** v2.0
**File:** [docs/releases/v2.0/DOC-1-v2.0-PRD.md](releases/v2.0/DOC-1-v2.0-PRD.md)
**Status:** In Progress
**Previous release:** [v1.0](releases/v1.0/DOC-1-v1.0-PRD.md)
```

These stubs are updated at each release by the human (or Scrum Master agent).

---

## 5. The 5 Canonical Documents

### 5.1 Document Definitions

| ID | Name | Content | Who authors it | When |
|---|---|---|---|---|
| `DOC-1` | **Product Requirements (PRD)** | What & Why â€” user needs, goals, KPIs, non-functional requirements, scope boundaries | Product Owner (human + PO agent) | Before implementation starts |
| `DOC-2` | **Technical Architecture** | How â€” system design, components, data flows, technology choices, ADRs, security model | Architect (human + Architect agent) | Before implementation starts |
| `DOC-3` | **Implementation Plan** | Phases, steps, validation criteria, sequencing rationale, effort sizing | Architect + Scrum Master | Before implementation starts |
| `DOC-4` | **Operations Guide** | User manual, runbooks, recommended processes, environment setup, troubleshooting | Developer + Scrum Master | Updated at release time |
| `DOC-5` | **Release Notes** | What changed from previous release, migration steps, known issues, deprecations | Scrum Master | At release time |

### 5.2 Document Header Standard

Every canonical document must begin with this header block:

```markdown
---
doc_id: DOC-1
release: v2.0
title: Product Requirements Document
status: Draft | In Review | Approved | Frozen
version: 2.0.0
date: YYYY-MM-DD
authors: [Human name, Agent persona]
previous_release: v1.0
previous_file: docs/releases/v1.0/DOC-1-v1.0-PRD.md
---
```

### 5.3 Frozen vs. In-Progress

- **Frozen** (`status: Frozen`): The document is part of a tagged release. Agents must treat it as read-only. Humans must not modify it â€” create a new version in the next release folder instead.
- **In Progress** (`status: Draft` or `In Review`): The document is being actively developed for the current release. Architect and Product Owner personas may modify it.
- **Approved** (`status: Approved`): The document has been reviewed and approved by the human but the release has not been tagged yet.

---

## 6. Unambiguous Numbering Convention

### 6.1 The Problem with the Current Numbering

The current workbench documentation uses mixed conventions:
- "Part 1", "Part 2", "Part 3", "Part 4" (in DOC6)
- "Phase 1", "Phase 2" (in DOC3 and DOC6 â€” different meanings)
- "Section 3.1", "REQ-2.3" (in DOC1 â€” good, keep this)

A reader cannot determine the hierarchy. "Phase 2" in DOC6 is not the same as "Phase 2" in DOC3.

### 6.2 The Canonical Numbering Hierarchy

| Level | Notation | Scope | Example |
|---|---|---|---|
| Document | `DOC-N` | Project-wide | `DOC-3` = Implementation Plan |
| Section | `DOC-N.S` | Within a document | `DOC-3.2` = Section 2 of Implementation Plan |
| Sub-section | `DOC-N.S.SS` | Within a section | `DOC-3.2.1` = Sub-section 1 of Section 2 |
| Requirement | `REQ-N.S` | Within DOC-1 | `REQ-2.3` = Requirement 3 of Domain 2 (keep existing convention) |
| Phase | `PHASE-N` | Within DOC-3 | `PHASE-0`, `PHASE-A`, `PHASE-1` |
| Step | `PHASE-N.S` | Within a phase | `PHASE-A.1`, `PHASE-A.2` |
| Idea | `IDEA-NNN` | Project-wide | `IDEA-003` = Release governance idea |
| QA Report | `QA-vX.Y-NNN` | Per release | `QA-v2.0-001` = First QA report for v2.0 |

### 6.3 Phase Naming in DOC-3

Phases in the Implementation Plan use **letters** (A, B, C...) for migration/setup phases and **numbers** (1, 2, 3...) for feature development phases. This distinguishes infrastructure work from product work:

- `PHASE-0` = Governance setup (one-time, applies to this project only)
- `PHASE-A` = Foundation work (infrastructure, restructuring)
- `PHASE-B` = Core feature work
- `PHASE-C` = Advanced feature work
- `PHASE-1`, `PHASE-2`... = Sprint-level feature phases (for application projects)

### 6.4 Cross-Reference Format

When referencing another document or section, always use the full qualified ID:

```markdown
See DOC-2.3.1 for the security architecture.
This implements REQ-3.2 from DOC-1.
Blocked by IDEA-004 (deferred to v3.0).
Validated by QA-v2.0-001.
```

---

## 7. The Idea Lifecycle

### 7.1 The IDEAS-BACKLOG.md Master Registry

`docs/ideas/IDEAS-BACKLOG.md` is the single source of truth for all ideas. It is a living document updated by humans at triage sessions.

**Format:**

```markdown
# Ideas Backlog

**Last triage:** YYYY-MM-DD
**Next triage:** At v2.0 release planning

| ID | Title | Source | Captured | Status | Target Release | Disposition |
|---|---|---|---|---|---|---|
| IDEA-001 | Hot/Cold memory architecture | Batch review 1 | 2026-03-28 | [ACCEPTED] | v2.0 | Planned for PHASE-A |
| IDEA-002 | Calypso orchestration scripts | Batch review 2 | 2026-03-28 | [ACCEPTED] | v2.0 | Planned for PHASE-C |
| IDEA-003 | Release governance model | Human 2026-03-28 | 2026-03-28 | [ACCEPTED] | v2.0 | Planned for PHASE-0 |
| IDEA-004 | Gherkin linter integration | Batch review 1 | 2026-03-28 | [DEFERRED] | v3.0 | Too complex for v2.0 |
| IDEA-005 | Multi-developer collaboration | Batch review 2 | 2026-03-28 | [REJECTED] | â€” | Out of scope by design |
```

### 7.2 The 6 Idea Statuses

| Status | Meaning | Who sets it | When |
|---|---|---|---|
| `[IDEA]` | Captured, not yet evaluated | Anyone | At capture time |
| `[ACCEPTED]` | Approved for a specific release | Human (at triage) | At release scope decision |
| `[IMPLEMENTED]` | Built, tested, in a released version | Human | After Git tag is created |
| `[DEFERRED]` | Good idea, but not this release | Human (at triage) | At release scope decision |
| `[REJECTED]` | Will never be implemented, with reason | Human (at triage) | At release scope decision |
| `[SUPERSEDED]` | Replaced by a better idea | Human | When a newer idea makes this one obsolete |

### 7.3 The Individual IDEA-NNN.md File

Each idea has its own file with full audit trail:

```markdown
---
id: IDEA-003
title: Release Governance Model
status: ACCEPTED
target_release: v2.0
source: Human conversation 2026-03-28
source_file: docs/conversations/2026-03-28-human-governance-discussion.md
captured: 2026-03-28
decided: 2026-03-28
decided_by: Human
---

## Description
[What the idea proposes â€” 2-5 sentences]

## Motivation
[Why this is needed â€” the problem it solves]

## Affected Documents
- DOC-1: [No change | Minor update | Major update â€” describe]
- DOC-2: [No change | Minor update | Major update â€” describe]
- DOC-3: [No change | New PHASE-0 â€” describe]
- DOC-4: [No change | New section â€” describe]
- .clinerules: [No change | New RULE 8 â€” describe]

## Disposition
**Decision:** ACCEPTED for v2.0
**Rationale:** [Why accepted/deferred/rejected]
**Implementation reference:** PHASE-0 in docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md

## History
- 2026-03-28: Created [IDEA]
- 2026-03-28: Promoted to [ACCEPTED], target v2.0
- (future) 2026-XX-XX: Marked [IMPLEMENTED], commit abc1234
```

### 7.4 When Triage Happens

**Triage Session 1 â€” Before starting a new release:**
Review all `[IDEA]` and `[DEFERRED]` items. Decide what goes into the next release. This produces the scope for `docs/releases/vX.Y/DOC-1..5`.

**Triage Session 2 â€” After release is tagged:**
Mark all implemented ideas as `[IMPLEMENTED]` with the commit hash. Review `[DEFERRED]` items to see if any should be promoted for the next release.

### 7.5 The Idea Lifecycle Flow

```
New thought / conversation / batch review finding
  â†“
Capture in IDEAS-BACKLOG.md (status: [IDEA])
Create IDEA-NNN.md with description
  â†“
Triage session (at release planning)
  â”œâ”€â”€ Fits this release â†’ [ACCEPTED], target_release: vX.Y
  â”œâ”€â”€ Good but not now â†’ [DEFERRED], target_release: vX.Y+1 or TBD
  â”œâ”€â”€ Out of scope forever â†’ [REJECTED], reason documented
  â””â”€â”€ Replaced by better idea â†’ [SUPERSEDED], reference to newer IDEA
  â†“
Implementation (for ACCEPTED ideas)
  â†“
Release tagged â†’ [IMPLEMENTED], commit hash recorded
```

---

## 8. The Conversation Log

### 8.1 Purpose

AI conversations (Gemini, Claude batch reviews, any significant AI-assisted design session) that inform the project are saved as **first-class artifacts** in `docs/conversations/`. They are:
- **Read-only after creation** â€” never edited
- **Source material** for ideas â€” not canonical docs themselves
- **Audit trail** â€” prove where design decisions came from

### 8.2 The conversations/README.md Index

```markdown
# Conversation Log Index

| Date | Source | File | Ideas Generated | Triage Status |
|---|---|---|---|---|
| 2026-03-27 | Gemini | 2026-03-27-gemini-doc6-architecture.md | IDEA-001, IDEA-002, IDEA-004 | Fully triaged |
| 2026-03-28 | Gemini | 2026-03-28-gemini-workbench-explained.md | IDEA-002 (enriched), IDEA-005 | Fully triaged |
| 2026-03-28 | Claude Batch | ../../plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md | IDEA-001, IDEA-004 | Fully triaged |
| 2026-03-28 | Claude Batch | ../../plans/batch-doc6-review/DOC6-REVIEW-RESULTS2.md | IDEA-002, IDEA-003 | Fully triaged |
```

**Triage Status values:**
- `Not yet triaged` â€” conversation saved but not yet mined for ideas
- `Partially triaged` â€” some findings captured, review incomplete
- `Fully triaged` â€” all significant findings captured as IDEA-NNN entries or explicitly dismissed

### 8.3 Conversation File Naming

`{YYYY-MM-DD}-{source}-{slug}.md`

Examples:
- `2026-03-27-gemini-doc6-architecture.md`
- `2026-03-28-gemini-workbench-explained.md`
- `2026-03-28-claude-batch-doc6-review-1.md`

### 8.4 Note on Batch Review Results

Batch review results in `plans/batch-doc6-review/` are **operational artifacts** (scripts + results), not conversation logs. The `conversations/README.md` references them by relative path. The ideas extracted from them are captured in `docs/ideas/`.

---

## 9. The Release Lifecycle

### 9.1 The Complete Release Process

```
Step 1: Ideas Backlog Triage
  â†’ Review all [IDEA] and [DEFERRED] items
  â†’ Decide scope for vX.Y
  â†’ Update IDEAS-BACKLOG.md (promote to [ACCEPTED] or [DEFERRED])
  â†’ Update each IDEA-NNN.md with decision

Step 2: Draft Canonical Documents
  â†’ Create docs/releases/vX.Y/ folder
  â†’ Draft DOC-1-vX.Y-PRD.md (What & Why)
  â†’ Draft DOC-2-vX.Y-Architecture.md (How)
  â†’ Draft DOC-3-vX.Y-Implementation-Plan.md (Phases & Steps)
  â†’ Create EXECUTION-TRACKER-vX.Y.md (blank, ready for execution)
  â†’ DOC-4 and DOC-5 are drafted last (at release time)

Step 3: Human Approval
  â†’ Review DOC-1, DOC-2, DOC-3 for coherence
  â†’ Update status to Approved in each document header
  â†’ Create release/vX.Y Git branch

Step 4: Implementation
  â†’ Execute DOC-3 phases in order
  â†’ Update EXECUTION-TRACKER-vX.Y.md after each session
  â†’ Update memory-bank/progress.md continuously
  â†’ New ideas â†’ docs/ideas/IDEAS-BACKLOG.md (NOT into vX.Y docs)

Step 5: QA Sign-off
  â†’ QA Engineer runs validation criteria from DOC-3
  â†’ Write QA report to docs/qa/vX.Y/QA-vX.Y-{date}.md
  â†’ All DOC-3 validation criteria must be met

Step 6: Release Finalization
  â†’ Write DOC-4-vX.Y-Operations-Guide.md (or update from previous)
  â†’ Write DOC-5-vX.Y-Release-Notes.md
  â†’ Update all DOC-N-CURRENT.md stubs to point to vX.Y
  â†’ Update CHANGELOG.md with release summary
  â†’ Update VERSION file with vX.Y.0

Step 7: Git Tag
  â†’ git tag vX.Y.0
  â†’ git push origin vX.Y.0
  â†’ All docs in docs/releases/vX.Y/ are now FROZEN (status: Frozen)

Step 8: Branch Merge
  â†’ Merge release/vX.Y into master
  â†’ git push origin master

Step 9: Post-Release Cleanup
  â†’ Mark all implemented ideas as [IMPLEMENTED] in IDEAS-BACKLOG.md
  â†’ Add commit hash to each IDEA-NNN.md
  â†’ Update conversations/README.md triage status
  â†’ Archive EXECUTION-TRACKER-vX.Y.md (it is now frozen)
```

### 9.2 The Baseline Tag Convention

For projects that existed before this governance model was adopted, a **baseline tag** is applied before the first formal release:

```
git tag v1.0.0-baseline
```

This marks "where we started from" without claiming it is a formally validated release. The first formal release tag (`v1.0.0`) is applied after the governance restructure is complete (PHASE-0 of v2.0).

### 9.3 Release Cadence

There is no fixed cadence. A release is complete when:
1. All DOC-3 validation criteria are met
2. QA sign-off is complete
3. DOC-4 and DOC-5 are written
4. Human approves the release

Do not rush a release to meet a calendar date. Do not delay a release because of ideas for the next one.

---

## 10. The Three Execution Tracking Files

### 10.1 The Hierarchy

```
DOC-3-vX.Y-Implementation-Plan.md    â† The plan (what should happen)
  â””â”€â”€ EXECUTION-TRACKER-vX.Y.md      â† The log (what actually happened)
        â””â”€â”€ memory-bank/progress.md  â† The agent's live checkbox state right now
```

### 10.2 DOC-3 â€” The Plan

- Written **before** implementation starts
- Contains phases, steps, validation criteria, sequencing rationale
- **Stable** â€” does not change during implementation (deviations are logged in EXECUTION-TRACKER)
- **Frozen** at Git tag

### 10.3 EXECUTION-TRACKER-vX.Y.md â€” The Log

- Updated **during** implementation, one entry per session
- Contains: steps completed, deviations from DOC-3, blockers, decisions, commit hashes
- Lives in `docs/releases/vX.Y/` alongside DOC-3
- **Frozen** at Git tag â€” becomes a permanent historical record of how the release was built
- Format: same as current `workbench/EXECUTION-TRACKER.md` (session log + blockers + decisions)

### 10.4 memory-bank/progress.md â€” The Live State

- Overwritten by the agent **every session**
- Contains the agent's current view of what is done/in-progress/pending
- References DOC-3 as its source of truth
- **Not frozen** â€” continuously updated
- At release time, should be consistent with EXECUTION-TRACKER

### 10.5 The RESUME-GUIDE

The current `workbench/RESUME-GUIDE.md` is a **DOC-4 companion** â€” operational guidance for resuming work after an interruption. It is merged into `DOC-4-vX.Y-Operations-Guide.md` as a dedicated section: "DOC-4.3 â€” Resuming After an Interruption."

---

## 11. Git Branching Strategy

### 11.1 Branch Structure

```
master                         â† Always = latest complete release (tagged)
â”‚
â”œâ”€â”€ release/v2.0               â† Active development for next release
â”‚   â”œâ”€â”€ feature/phase-0-governance
â”‚   â”œâ”€â”€ feature/phase-a-hot-cold-memory
â”‚   â”œâ”€â”€ feature/phase-b-template-enrichment
â”‚   â””â”€â”€ feature/phase-c-calypso-orchestration
â”‚
â””â”€â”€ experiment/                â† Exploration only
    â””â”€â”€ experiment/architecture-v2   â† Current branch (feeds IDEAS-BACKLOG)
```

### 11.2 Branch Rules

| Branch | Purpose | Merge target | Who creates it |
|---|---|---|---|
| `master` | Latest complete release | â€” | Auto (from release branch) |
| `release/vX.Y` | Active development for release vX.Y | `master` (at tag) | Human at release start |
| `feature/{slug}` | Single feature or phase | `release/vX.Y` | Developer/Scrum Master |
| `experiment/{slug}` | Exploration, ideas, batch reviews | `docs/ideas/` (via triage) | Anyone |

### 11.3 The experiment/ â†’ release/ Transition

`experiment/` branches are **never merged directly into `master`** or `release/`. Their output is:
1. Ideas captured in `docs/ideas/IDEAS-BACKLOG.md`
2. Conversations saved in `docs/conversations/`
3. Batch review results saved in `plans/`

The ideas are then formally accepted into a release via the triage process, and implemented on the `release/vX.Y` branch.

### 11.4 Commit Message Convention

Conventional Commits format (already in use â€” no change):

```
feat(scope): description       â† New feature
fix(scope): description        â† Bug fix
docs(release): description     â† Canonical doc update (DOC-1..5)
docs(ideas): description       â† Idea backlog update
docs(memory): description      â† Memory bank update
docs(conversations): description â† Conversation log addition
chore(config): description     â† Configuration change
chore(governance): description â† Governance process change
refactor(scope): description   â† Refactoring
test(scope): description       â† Tests
```

---

## 12. Agent Rules â€” .clinerules Additions

### 12.1 New RULE 8 â€” Documentation Discipline

The following rule must be added to `.clinerules` (and synchronized to `template/.clinerules` and `prompts/SP-002`):

```
## RULE 8: DOCUMENTATION DISCIPLINE â€” MANDATORY GOVERNANCE PROTOCOL

### 8.1 â€” The Two Spaces
- `docs/releases/vX.Y/` files (FROZEN releases) are READ-ONLY for all agents. Never modify a released canonical doc.
- `docs/releases/vX.Y/` drafts (in-progress release, status: Draft or In Review) may be modified ONLY by the Architect or Product Owner persona.
- `memory-bank/` files are agent-writable â€” update them freely as working memory.

### 8.2 â€” Idea Capture Mandate
When you identify a new requirement, improvement, or architectural change that is NOT part of the current release scope:
1. DO NOT modify the current release's canonical docs (DOC-1..5).
2. ADD an entry to `docs/ideas/IDEAS-BACKLOG.md` with status [IDEA].
3. CREATE `docs/ideas/IDEA-{NNN}-{slug}.md` with description, motivation, and affected documents.
4. INFORM the human that a new idea has been captured.

### 8.3 â€” Conversation Log Mandate
When saving an AI conversation output to the repository:
1. Save it to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`.
2. Add an entry to `docs/conversations/README.md` with triage status "Not yet triaged".
3. Never edit a conversation file after creation.

### 8.4 â€” Release Document References
When referencing canonical documents, always use the full qualified ID:
- Correct: "See DOC-2.3.1 for the security architecture."
- Incorrect: "See the architecture document."

### 8.5 â€” Execution Tracking
After each work session:
1. Update `docs/releases/vX.Y/EXECUTION-TRACKER-vX.Y.md` with the session log entry.
2. Update `memory-bank/progress.md` with the current checkbox state.
3. These two files must be consistent at the end of every session.
```

### 12.2 SP-002 Version Bump

When RULE 8 is added to `.clinerules`, `prompts/SP-002` must be bumped to `v2.3.0` and synchronized to all 4 copies:
- `.clinerules`
- `prompts/SP-002-clinerules-global.md`
- `template/.clinerules`
- `template/prompts/SP-002-clinerules-global.md`

---

## 13. Migration Plan â€” Current Workbench to v2.0

### 13.1 Current State

| Item | Current Location | Status |
|---|---|---|
| DOC1-PRD | `workbench/DOC1-PRD-Workbench-Requirements.md` | v1.0 canonical doc |
| DOC2-ARCH | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | v1.0 canonical doc |
| DOC3-BUILD | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | v1.0 canonical doc |
| DOC4-GUIDE | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | v1.0 canonical doc |
| DOC5-GUIDE | `workbench/DOC5-GUIDE-Project-Development-Process.md` | v1.0 canonical doc (merged into DOC-4) |
| EXECUTION-TRACKER | `workbench/EXECUTION-TRACKER.md` | v1.0 execution log |
| RESUME-GUIDE | `workbench/RESUME-GUIDE.md` | v1.0 operations companion |
| DOC6 (Gemini conv 1) | `workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md` | Conversation log, NOT canonical |
| Gemini conv 2 | `workbench/_Agentic Workbench Architecture Explained .md` | Conversation log, NOT canonical |
| QA reports | `docs/qa/*.md` | v1.0 QA reports (flat, no version subfolder) |
| Git branch | `experiment/architecture-v2` | Exploration branch |
| Git master | `master` | Sessions 1-9, no tag |

### 13.2 PHASE-0 â€” Governance Restructure (First Phase of v2.0)

**Goal:** Establish the governance structure, retroactively document v1.0, and create the foundation for all subsequent v2.0 work.

**Pedagogical justification:** This phase must come first because every subsequent phase depends on the governance structure being in place. Building Hot/Cold memory (PHASE-A) without a proper `docs/releases/v2.0/DOC-3` to track it against would immediately violate the governance model we are trying to establish.

#### PHASE-0.1 â€” Baseline Tag on master

```bash
git checkout master
git tag v1.0.0-baseline
git push origin v1.0.0-baseline
```

This preserves the current `master` state permanently. No restructuring needed yet.

#### PHASE-0.2 â€” Create release/v2.0 Branch

```bash
git checkout experiment/architecture-v2
git checkout -b release/v2.0
git push origin release/v2.0
```

All subsequent v2.0 work happens on `release/v2.0`.

#### PHASE-0.3 â€” Create the docs/ Structure

Create the new folder structure:

```
docs/
â”œâ”€â”€ releases/
â”‚   â”œâ”€â”€ v1.0/
â”‚   â””â”€â”€ v2.0/
â”œâ”€â”€ qa/
â”‚   â””â”€â”€ v1.0/
â”œâ”€â”€ ideas/
â””â”€â”€ conversations/
```

#### PHASE-0.4 â€” Migrate v1.0 Canonical Docs

Move and rename existing workbench docs into `docs/releases/v1.0/`:

| From | To |
|---|---|
| `workbench/DOC1-PRD-Workbench-Requirements.md` | `docs/releases/v1.0/DOC-1-v1.0-PRD.md` |
| `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | `docs/releases/v1.0/DOC-2-v1.0-Architecture.md` |
| `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | `docs/releases/v1.0/DOC-3-v1.0-Implementation-Plan.md` |
| `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` + `DOC5-GUIDE-Project-Development-Process.md` | `docs/releases/v1.0/DOC-4-v1.0-Operations-Guide.md` (merged) |
| `workbench/EXECUTION-TRACKER.md` | `docs/releases/v1.0/EXECUTION-TRACKER-v1.0.md` |
| `workbench/RESUME-GUIDE.md` | Merged into `docs/releases/v1.0/DOC-4-v1.0-Operations-Guide.md` |

Add the standard document header to each migrated file (doc_id, release, status: Frozen).

#### PHASE-0.5 â€” Write DOC-5-v1.0-Release-Notes.md

Create `docs/releases/v1.0/DOC-5-v1.0-Release-Notes.md` documenting what v1.0 delivered:

- 3-mode LLM switcher (Ollama / Gemini proxy / Claude API)
- 4 Agile personas (Product Owner, Scrum Master, Developer, QA Engineer)
- Memory Bank (7 files + `.clinerules` 7 rules)
- Prompts registry (SP-001 to SP-007)
- Pre-commit hook (check-prompts-sync.ps1)
- Project template folder
- Known gaps: Phase 9 RBAC partially validated (1/4 scenarios), SP-007 requires manual Gem Gemini update

#### PHASE-0.6 â€” Migrate QA Reports

Move existing QA reports into the versioned subfolder:

```
docs/qa/SP-COHERENCE-2026-03-24.md       â†’ docs/qa/v1.0/SP-COHERENCE-2026-03-24.md
docs/qa/SP-COHERENCE-FINAL-2026-03-24.md â†’ docs/qa/v1.0/SP-COHERENCE-FINAL-2026-03-24.md
```

#### PHASE-0.7 â€” Create docs/conversations/

Move Gemini conversations out of `workbench/` into `docs/conversations/`:

| From | To |
|---|---|
| `workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md` | `docs/conversations/2026-03-27-gemini-doc6-architecture.md` |
| `workbench/_Agentic Workbench Architecture Explained .md` | `docs/conversations/2026-03-28-gemini-workbench-explained.md` |

Create `docs/conversations/README.md` with the conversation index table.

#### PHASE-0.8 â€” Create docs/ideas/

Create `docs/ideas/IDEAS-BACKLOG.md` with the initial idea registry.

Create the first three idea files:
- `docs/ideas/IDEA-001-hot-cold-memory.md` (from batch review 1 + 2)
- `docs/ideas/IDEA-002-calypso-orchestration.md` (from batch review 2)
- `docs/ideas/IDEA-003-release-governance.md` (this conversation)

#### PHASE-0.9 â€” Create DOC-N-CURRENT.md Stubs

Create the 5 pointer stubs in `docs/`:
- `docs/DOC-1-CURRENT.md` â†’ points to `docs/releases/v1.0/DOC-1-v1.0-PRD.md`
- `docs/DOC-2-CURRENT.md` â†’ points to `docs/releases/v1.0/DOC-2-v1.0-Architecture.md`
- `docs/DOC-3-CURRENT.md` â†’ points to `docs/releases/v1.0/DOC-3-v1.0-Implementation-Plan.md`
- `docs/DOC-4-CURRENT.md` â†’ points to `docs/releases/v1.0/DOC-4-v1.0-Operations-Guide.md`
- `docs/DOC-5-CURRENT.md` â†’ points to `docs/releases/v1.0/DOC-5-v1.0-Release-Notes.md`

#### PHASE-0.10 â€” Eliminate workbench/ Folder

After all files are migrated, delete the `workbench/` folder. Verify no files remain.

#### PHASE-0.11 â€” Add RULE 8 to .clinerules

Add RULE 8 (Documentation Discipline) to `.clinerules`. Bump `prompts/SP-002` to v2.3.0. Synchronize all 4 copies.

#### PHASE-0.12 â€” Tag v1.0.0

```bash
git add .
git commit -m "chore(governance): PHASE-0 complete â€” docs/ restructured, v1.0 retroactively documented"
git tag v1.0.0
git push origin v1.0.0
git push origin release/v2.0
```

#### PHASE-0.13 â€” Update template/ Folder

Add the `docs/` structure to `template/` so every new application project starts with it:

```
template/docs/
â”œâ”€â”€ DOC-1-CURRENT.md    â† Blank stub
â”œâ”€â”€ DOC-2-CURRENT.md    â† Blank stub
â”œâ”€â”€ DOC-3-CURRENT.md    â† Blank stub
â”œâ”€â”€ DOC-4-CURRENT.md    â† Blank stub
â”œâ”€â”€ DOC-5-CURRENT.md    â† Blank stub
â”œâ”€â”€ releases/
â”‚   â””â”€â”€ .gitkeep
â”œâ”€â”€ qa/
â”‚   â””â”€â”€ .gitkeep
â”œâ”€â”€ ideas/
â”‚   â”œâ”€â”€ IDEAS-BACKLOG.md    â† Blank template
â”‚   â””â”€â”€ .gitkeep
â””â”€â”€ conversations/
    â”œâ”€â”€ README.md           â† Blank template
    â””â”€â”€ .gitkeep
```

**PHASE-0 Validation Criteria:**
- [ ] `docs/releases/v1.0/` contains all 5 DOC files + EXECUTION-TRACKER
- [ ] `docs/qa/v1.0/` contains migrated QA reports
- [ ] `docs/conversations/` contains 2 Gemini conversation files + README.md
- [ ] `docs/ideas/` contains IDEAS-BACKLOG.md + IDEA-001..003
- [ ] `docs/DOC-N-CURRENT.md` stubs exist and point to v1.0
- [ ] `workbench/` folder is eliminated
- [ ] RULE 8 is in `.clinerules` and all 4 copies are synchronized
- [ ] Git tag `v1.0.0` exists and is pushed to remote
- [ ] `template/docs/` structure exists with blank stubs

---

## 14. Application to Application Projects

### 14.1 How a New Application Project Starts

When the workbench initiates a new application project (via `deploy-workbench-to-project.ps1` or equivalent):

1. The `template/` folder is copied into the new project repository
2. The `template/docs/` structure is included â€” the project starts with the governance framework already in place
3. The Lead PM Agent (Phase 1 of the Agentic Agile Pipeline) creates `docs/releases/v1.0/DOC-1-v1.0-PRD.md` as its first output
4. The Architect Agent creates `docs/releases/v1.0/DOC-2-v1.0-Architecture.md`
5. The Scrum Master creates `docs/releases/v1.0/DOC-3-v1.0-Implementation-Plan.md`

### 14.2 The Application Project Release Cycle

For application projects, releases map to **product releases** (deployable versions of the application):

- `v1.0` = MVP (Minimum Viable Product)
- `v1.1` = First iteration with user feedback
- `v2.0` = Major feature addition or architectural change

The same governance rules apply: one Git tag per release, 5 canonical docs, ideas backlog, conversation log.

### 14.3 The Workbench as a Meta-Project

The workbench is a **meta-project** â€” it governs itself using the same rules it imposes on application projects. This is the proof of concept: if the governance model works for the workbench, it works for any project.

---

## 15. Implementation Steps

### 15.1 Summary of All Implementation Work

| Step | Phase | Description | Effort |
|---|---|---|---|
| PHASE-0.1 | v2.0 | Baseline tag on master | Small |
| PHASE-0.2 | v2.0 | Create release/v2.0 branch | Small |
| PHASE-0.3 | v2.0 | Create docs/ folder structure | Small |
| PHASE-0.4 | v2.0 | Migrate v1.0 canonical docs | Medium |
| PHASE-0.5 | v2.0 | Write DOC-5-v1.0-Release-Notes.md | Medium |
| PHASE-0.6 | v2.0 | Migrate QA reports to docs/qa/v1.0/ | Small |
| PHASE-0.7 | v2.0 | Create docs/conversations/ | Small |
| PHASE-0.8 | v2.0 | Create docs/ideas/ with IDEA-001..003 | Medium |
| PHASE-0.9 | v2.0 | Create DOC-N-CURRENT.md stubs | Small |
| PHASE-0.10 | v2.0 | Eliminate workbench/ folder | Small |
| PHASE-0.11 | v2.0 | Add RULE 8 to .clinerules + SP-002 v2.3.0 | Medium |
| PHASE-0.12 | v2.0 | Tag v1.0.0 | Small |
| PHASE-0.13 | v2.0 | Update template/ with docs/ structure | Medium |
| PHASE-A | v2.0 | Hot/Cold memory restructure | Large |
| PHASE-B | v2.0 | Template folder enrichment | Medium |
| PHASE-C | v2.0 | Calypso orchestration scripts | Large |
| PHASE-D | v2.0 | Global Brain (Chroma/Mem0, Librarian Agent) | Large |

### 15.2 What Needs to Be Created in docs/releases/v2.0/

Before starting PHASE-A, the following v2.0 canonical docs must be drafted:

- `docs/releases/v2.0/DOC-1-v2.0-PRD.md` â€” Updated PRD incorporating IDEA-001..003 and batch review findings
- `docs/releases/v2.0/DOC-2-v2.0-Architecture.md` â€” Updated architecture (Hot/Cold memory, Calypso tier, Global Brain)
- `docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md` â€” This governance plan + PHASE-A..D
- `docs/releases/v2.0/EXECUTION-TRACKER-v2.0.md` â€” Blank, ready for execution

### 15.3 Dependency Order

```
PHASE-0 (Governance restructure)
  â””â”€â”€ Must complete before any other phase
      â””â”€â”€ PHASE-A (Hot/Cold memory)
            â””â”€â”€ Must complete before PHASE-B
                â””â”€â”€ PHASE-B (Template enrichment)
                      â””â”€â”€ Can run in parallel with PHASE-C
                          â””â”€â”€ PHASE-C (Calypso orchestration)
                                â””â”€â”€ Must complete before PHASE-D
                                    â””â”€â”€ PHASE-D (Global Brain)
```

---

## Appendix A â€” Quick Reference Card

### The 5 Questions to Ask at Any Point

1. **What release am I working on?** â†’ Check `docs/DOC-3-CURRENT.md` and `memory-bank/progress.md`
2. **Is this idea in scope for the current release?** â†’ Check `docs/ideas/IDEAS-BACKLOG.md`
3. **Where does this new idea go?** â†’ `docs/ideas/IDEAS-BACKLOG.md` + new `IDEA-NNN.md`
4. **Is this doc frozen or in-progress?** â†’ Check the `status:` field in the document header
5. **What did the agent do last session?** â†’ Check `docs/releases/vX.Y/EXECUTION-TRACKER-vX.Y.md`

### The 3 Rules That Prevent Most Problems

1. **Never modify a frozen doc.** Create a new version in the next release folder.
2. **Never inject an idea directly into canonical docs.** Always go through `IDEAS-BACKLOG.md` first.
3. **Never mix docs from different releases.** If DOC-1 says v2.0, all other docs must also say v2.0.

---

*End of PLAN-release-governance.md*
*Next action: Review this plan, then switch to Code mode to implement PHASE-0.*
