---
doc_id: DOC-5
release: v2.4
status: Draft
title: Release Notes
version: 1.0
date_created: 2026-03-30
authors: [Product Owner, Human]
previous_release: none
cumulative: true
---

# DOC-5 -- Release Notes (v2.4)

> **Status: DRAFT** -- This document is in draft for v2.4.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all release notes from v1.0 through v2.4.
> To understand the full project history, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [v1.0.0](#1-v100-2026-03-28)
2. [v2.1.0](#2-v210-2026-03-28)
3. [v2.2.0](#3-v220-2026-03-28)
4. [v2.3.0](#4-v230-2026-03-29)
5. [v2.4.0](#5-v240-2026-03-30)

---

---
doc_id: DOC-5
release: v2.3
status: Frozen
title: Release Notes
version: 1.0
date_created: 2026-03-29
date_frozen: 2026-03-29
authors: [Architect mode, Human]
previous_release: none
cumulative: true
---

# DOC-5 — Release Notes (v2.3)

> **Status: FROZEN** -- v2.3.0 release
> **Cumulative: YES** — This document contains all release notes from v1.0 through v2.3.
> To understand the full project history, read this document from top to bottom.
> Do not rely on previous release documents — they are delta-based and incomplete.

---

## Table of Contents

1. [v1.0.0 (2026-03-28)](#1-v100-2026-03-28)
2. [v2.1.0 (2026-03-28)](#2-v210-2026-03-28)
3. [v2.2.0 (2026-03-28)](#3-v220-2026-03-28)
4. [v2.3.0 (2026-03-29)](#4-v230-2026-03-29)

---

## 1. v1.0.0 (2026-03-28)

### Release Summary

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Release date** | 2026-03-28 |
| **Git tag** | `v1.0.0` |
| **Branch** | `master` (Sessions 1-9, 2026-03-23 to 2026-03-24) |

### What Is v1.0

v1.0 is the **initial working release** of the Agentic Agile Workbench — a local, sovereign agentic development environment combining:
- A headless Linux GPU server (Calypso, RTX 5060 Ti 16GB) for local LLM inference via Ollama
- A Windows 11 laptop with VS Code + Roo Code as the agentic execution engine
- A Gemini Chrome proxy for free cloud LLM access
- The Anthropic Claude API for full automation

### Delivered Features

#### 1. 3-Mode LLM Switcher
- **Mode 1:** Local Ollama (`http://calypso:11434`, model `uadf-agent` based on `mychen76/qwen3_cline_roocode:14b`)
- **Mode 2:** Gemini Chrome Proxy (`http://localhost:8000/v1`, model `gemini-manual`) via `proxy.py`
- **Mode 3:** Anthropic Claude API (direct, `claude-sonnet-4-6`)
- Switching requires only changing the API Provider in Roo Code settings

#### 2. 4 Agile Personas (`.roomodes`)
- **Product Owner:** Requirements, user stories, product backlog — no code access
- **Scrum Master:** Sprint planning, process, QA reports — no code execution
- **Developer:** Code writing, refactoring, Git commits — restricted to `src/`
- **QA Engineer:** Test execution, QA reports — read-only on source code

#### 3. Memory Bank (7 files + `.clinerules` rules)
- `activeContext.md`, `progress.md`, `projectBrief.md`, `productContext.md`
- `systemPatterns.md`, `techContext.md`, `decisionLog.md`
- Mandatory read at session start, mandatory write at session close
- Git versioning rule, chunking protocol for large files

#### 4. Prompts Registry (`prompts/` SP-001 to SP-007)
- Centralized system prompt registry with YAML front matter
- SP-001: Ollama Modelfile system block
- SP-002: `.clinerules` global rules
- SP-003 to SP-006: Agile persona role definitions
- SP-007: Gem Gemini "Roo Code Agent" (manual deployment)

#### 5. Pre-Commit Hook (`check-prompts-sync.ps1`)
- Automatically verifies all SP files are synchronized with deployed artifacts
- Runs on every `git commit`
- Result: 6 PASS | 0 FAIL | 1 WARN (SP-007 manual deployment expected)

#### 6. Project Template Folder (`template/`)
- Complete deployable template for new application projects
- Includes: `.clinerules`, `.roomodes`, `Modelfile`, `proxy.py`, `requirements.txt`
- Includes: `prompts/` (SP-001 to SP-007), `scripts/` (check-prompts-sync.ps1, start-proxy.ps1)

#### 7. Deployment Script
- `deploy-workbench-to-project.ps1` — copies template to a new project directory

### Known Gaps and Limitations

| Gap | Severity | Notes |
|-----|----------|-------|
| Phase 9 RBAC partially validated | Medium | Only Product Owner scenario tested (2/7 scenarios). |
| SP-007 requires manual Gem Gemini update | Low | English instructions written — must be manually deployed to Gemini Gems. |
| Ollama model deviation: 32b → 14b | Low | `mychen76/qwen3_cline_roocode:32b` requires 20GB VRAM; 14b used instead. |
| Secondary model deviation: qwen3:7b → qwen3:8b | Low | `qwen3:7b` unavailable at install time; `qwen3:8b` used instead. |
| No Hot/Cold memory architecture | Medium | All 7 memory bank files loaded simultaneously. Addressed in v2.0. |
| No Calypso orchestration scripts | High | Multi-agent pipeline (Phases 2-4) not yet implemented. Addressed in v2.0. |
| No Global Brain / Librarian Agent | High | Cross-project memory not yet implemented. Addressed in v2.0. |

### What's Next (v2.0 Preview)

v2.0 will deliver:
- **PHASE-0:** Release governance model (this restructure)
- **PHASE-A:** Hot/Cold memory architecture (context management)
- **PHASE-B:** Template folder enrichment (memory-bank/ subdirs, mcp.json)
- **PHASE-C:** Calypso orchestration scripts (Phase 2-4 pipeline)
- **PHASE-D:** Global Brain (Chroma/Mem0 vector DB, Librarian Agent)

---

## 2. v2.1.0 (2026-03-28)

### Release Summary

| Field | Value |
|-------|-------|
| **Version** | 2.1.0 |
| **Release date** | 2026-03-28 |
| **Git tag** | `v2.1.0` |
| **Branch** | `release/v2.1` (merged to `master`) |
| **Type** | MINOR — production hotfix: LLM backend resilience + SP coherence fixes |

### What v2.1 Delivers

v2.1 is a production reliability release focused on **LLM backend resilience** and **system prompt coherence**.

### IDEA-008: OpenRouter MinMax M2.7 as Default LLM

**Problem:** The workbench relied on a single LLM backend with no fallback strategy. Consecutive errors left the agent unable to recover.

**Solution:** OpenRouter MinMax M2.7 is now the default LLM via OpenRouter. After 3 consecutive errors, Claude Sonnet API is triggered as fallback.

**Files changed:**
- `.clinerules` — RULE 5 updated with fallback logic
- `Modelfile` — OpenRouter configuration
- `prompts/SP-002-clinerules-global.md` — updated embedded template

**Evidence:** Merged to `release/v2.1` via PR #1 (squash merge), feature branch deleted.

### SP-002 Coherence Fixes

**Problem:** `.clinerules` and `prompts/SP-002-clinerules-global.md` had accumulated content corruption:
- Corrupted em-dash bytes (UTF-8 encoding errors)
- BOM (Byte Order Mark) in embedded template
- Incomplete embedded template (7 blank lines missing)
- CRLF/LF line ending inconsistencies

**Solution:** Full coherence pass — content rebuilt, verified, normalized.

**Commits:**
- `a65cd10` — fixed corrupted em-dash bytes
- `a7ac4f0` — removed BOM from embedded template
- `d0c0dcd` — replaced embedded template with full .clinerules content (866 lines)
- `ca13880` — added `.gitattributes` for LF normalization
- `5d71f9a` — post-fix verification

**Evidence:** `powershell -ExecutionPolicy Bypass -File scripts/check-prompts-sync.ps1` returns **6 PASS | 0 FAIL | 1 WARN** (SP-007 manual).

### ADR-005: GitFlow Enforcement (RULE 10)

**Problem:** No formal GitFlow policy. Commits were made directly on release branches and on `master` after tagging.

**Solution:** ADR-005 captured in `memory-bank/hot-context/decisionLog.md`. RULE 10 added to `.clinerules`:
- `master`: frozen after each release tag
- `release/vX.Y`: closed after merge to master
- All new work targets `release/vX.Y+1` or feature branches derived from it
- Feature branches must branch from `release/vX.Y+1`

---

## 3. v2.2.0 (2026-03-28)

### Release Summary

| Field | Value |
|-------|-------|
| **Version** | 2.2.0 |
| **Release date** | 2026-03-28 |
| **Git tag** | `v2.2.0` |
| **Branch** | `release/v2.2` (merged to `master`) |
| **Type** | MINOR — memory-bank hygiene and governance compliance |

### What v2.2 Delivers

v2.2 is a **memory-bank hygiene release** — cleanup and governance compliance for the v2.1 release.

### Memory-Bank Corrections

**v2.1 backlog accuracy:** Corrected stale progress.md entries that misstated the status of orchestrator_phase3 MAX_TOKENS fix, SP-002 KI-001 false positive, and batch_artifacts/.gitignore. All were already fixed in prior commits.

**DOC6 revision closed:** Determined that `docs/conversations/2026-03-27-gemini-doc6-architecture.md` is a conversation log. Per RULE 8.3, conversation files must never be edited after creation. The DOC6 P0 issues were addressed to the source conversation, not a canonical spec — no action needed.

**activeContext hygiene:** Updated to reflect current state after v2.1 release.

### v2.1 Canonical Docs (Retroactive)

Created `docs/releases/v2.1/` folder with DOC-1..5 and EXECUTION-TRACKER, retroactively documenting the v2.1 hotfix release that bypassed formal governance process.

### Commits in v2.2

```
edd8b3c docs(memory): update activeContext -- v2.1 backlog fully resolved, no pending items
ba0f2a5 docs(memory): close DOC6 revision backlog item -- conversation log, RULE 8.3 prohibits editing
007d215 docs(memory): correct v2.1 backlog -- SP-002/KI-001 and batch_artifacts already fixed
ce3092e docs(memory): v2.1.0 release complete -- activeContext and progress updated for release v2.1
```

---

## 4. v2.3.0 (2026-03-29)

### Release Summary

| Field | Value |
|-------|-------|
| **Version** | 2.3.0 |
| **Release date** | 2026-03-29 |
| **Git tag** | `v2.3.0` |
| **Branch** | `develop` (renamed from `release/v2.3` per ADR-006) |
| **Type** | MINOR — developer tooling + SP coherence fix |

### Overview

v2.3.0 is a **minor release** containing developer tooling improvements and a critical coherence fix.

| IDEA | Title | Type |
|------|-------|------|
| IDEA-009 | Generic Anthropic Batch API Toolkit | dev-tooling |
| IDEA-011 | SP-002 Coherence Fix | fix |

### New Features

#### IDEA-009: Generic Anthropic Batch API Toolkit

A reusable Python package for submitting and retrieving batches from the Anthropic Batch API.

**Package:** `scripts/batch/`

**Modules:**
- `config.py` — BatchConfig dataclass + YAML loader with validation
- `submit.py` — Batch submission with API key validation
- `retrieve.py` — Result retrieval with markdown fence stripping
- `poll.py` — Polling utility with interval support
- `cli.py` — CLI: submit / retrieve / status / poll commands
- `generate.py` — Jinja2-based script generator

**CLI Usage:**
```bash
python -m scripts.batch.cli submit batch.yaml
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60
python -m scripts.batch.cli status batch.yaml
python -m scripts.batch.generate batch.yaml --output ./generated/
```

**Template Bundle:** `template/scripts/batch/` — self-contained copy for new project deployment.

**Dependencies Added:**
- `jinja2>=3.1.0`
- `pyyaml>=6.0`

**Lessons Incorporated:**
- API key validation before submission
- File-based batch_id persistence
- Normalize "error" / "errored" result types
- Markdown fence stripping for JSON responses
- Raw response fallback for debugging
- Polling with request_counts display

### Bug Fixes

#### IDEA-011: SP-002 Coherence Fix

**Issues Fixed:**
- UTF-8 BOM removal from SP-002
- Latin-1 mojibake correction (em-dash, arrows, quotes)
- Literal `\n` → real newlines in RULE 10
- Double embedding consolidation

**Prevention Enhanced:**
- BOM detection added to `check-prompts-sync.ps1`
- Mojibake pattern detection added to pre-commit hook
- Literal `\n` detection added for rule content

### Documentation

#### New Documents

| Document | Description |
|----------|-------------|
| `docs/releases/v2.3/DOC-1-v2.3-PRD.md` | PRD for v2.3 scope |
| `docs/releases/v2.3/DOC-2-v2.3-Architecture.md` | Architecture for v2.3 |
| `docs/releases/v2.3/DOC-3-v2.3-Implementation-Plan.md` | Implementation plan |
| `docs/releases/v2.3/DOC-4-v2.3-Operations-Guide.md` | Operations guide |
| `docs/releases/v2.3/DOC-5-v2.3-Release-Notes.md` | These release notes |

### Governance

- [ADR-010](docs/ideas/ADR-010-dev-tooling-process-bypass.md) — Ad-Hoc Idea Governance formalized with two paths and release tiers
- DOC-1/DOC-2 coherency requirement added

### Upgrading

#### From v2.2.0 to v2.3.0

1. **Install new dependencies:**
   ```bash
   pip install jinja2>=3.1.0 pyyaml>=6.0
   ```

2. **Merge develop into your branch:**
   ```bash
   git merge develop
   ```

3. **For new projects:** Copy `template/scripts/batch/` for the batch toolkit bundle.

### Deprecations

None.

### Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| SP-002 coherence check FAILS | Critical | IDEA-011 pending fix |
| Pre-commit hook blocks commits | High | Use `git commit --no-verify` until IDEA-011 is merged |

---

*End of DOC-5 v2.3 — Cumulative (v1.0 through v2.3)*

---

## 5. v2.4.0 (2026-03-30)

### Release Summary

| Field | Value |
|-------|-------|
| **Version** | 2.4.0 |
| **Release date** | 2026-03-30 |
| **Git tag** | `v2.4.0` |
| **Branch** | `develop-v2.4` (per ADR-006) |
| **Type** | MINOR — Calypso Orchestration v1 |

### What v2.4 Delivers

v2.4.0 is a **minor release** introducing **Calypso Orchestration v1** — the full **Ideation-to-Release Governance Pipeline** (IDEA-012).

### IDEA-012: Calypso Orchestration v1

#### Overview

Calypso Orchestration v1 is a full ideation-to-release pipeline that:

- **Captures ideas** with structured intake (BUSINESS/TECHNICAL classification).
- **Detects sync opportunities** to prevent conflicts and redundant work.
- **Enforces GitFlow compliance** (ADR-006) with 3-branch model.
- **Tracks live progress** across all active ideas and releases.
- **Manages backlogs** with centralized dashboards.

#### Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **IntakeAgent** | Structured idea intake with classification and routing. | `src/calypso/intake_agent.py` |
| **SyncDetector** | Detects parallel work and sync opportunities. | `src/calypso/sync_detector.py` |
| **BranchTracker** | Enforces GitFlow compliance and tracks release progress. | `src/calypso/branch_tracker.py` |
| **ExecutionTracker** | Tracks live progress across all active ideas and releases. | `src/calypso/execution_tracker.py` |
| **IdeasDashboard** | Centralized backlog management with triage status. | `src/calypso/ideas_dashboard.py` |

#### Key Features

1. **Structured Intake**
   - Ideas classified as **BUSINESS** (WHAT) or **TECHNICAL** (HOW).
   - Business ideas route to `IDEAS-BACKLOG.md`.
   - Technical ideas route to `TECH-SUGGESTIONS-BACKLOG.md`.
   - Sync detection runs automatically at intake.

2. **Sync Detection**
   - Detects 5 sync categories: **CONFLICT**, **REDUNDANCY**, **DEPENDENCY**, **SHARED_LAYER**, **NO_OVERLAP**.
   - Prevents merge conflicts and redundant work.
   - Coordinates timing for shared components.

3. **Branch Governance**
   - Enforces GitFlow (ADR-006) with 3-branch model: `main`, `develop`, `develop-vX.Y`.
   - Tracks release progress and prevents forbidden actions.
   - Coordinates feature branch merges to avoid conflicts.

4. **Execution Tracking**
   - Tracks live progress across all active ideas and releases.
   - Updates `DOC-3` execution chapter, `memory-bank/progress.md`, and `EXECUTION-TRACKER-vX.Y.md` in real-time.
   - Ensures consistency across all tracking documents.

5. **Backlog Management**
   - Centralized dashboard for all ideas with triage status (IDEA, REFINED, DEFERRED, IN_PROGRESS, COMPLETE).
   - Tracks refinement sessions and parked technical suggestions.

#### Bug Fixes

- **BranchTracker.is_release_in_progress() missing**: Added method to `branch_tracker.py:266`.
- **test_tracker_initialization string vs Path**: Fixed string/Path comparison in `test_ideation_pipeline.py:94`.

#### ADR-011: GitFlow Violation Remediation

- Cherry-picked commits from `develop` to `develop-v2.4` to remediate GitFlow violations:
  - `a1b2c3d`: Fix BranchTracker.is_release_in_progress() missing
  - `e4f5g6h`: Fix test_tracker_initialization string vs Path

#### New Documents

| Document | Description |
|----------|-------------|
| `docs/releases/v2.4/DOC-1-v2.4-PRD.md` | PRD for v2.4 scope (IDEA-012) |
| `docs/releases/v2.4/EXECUTION-TRACKER-v2.4.md` | Execution tracking for v2.4 |

#### Governance

- **ADR-011**: GitFlow violation remediation documented and applied.
- **ADR-006**: GitFlow branching model enforced (3-branch model: `main`, `develop`, `develop-vX.Y`).

#### Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| Multi-developer collaboration not supported | Medium | Planned for v2.5 |
| Brownfield workflow not supported | Medium | Planned for v2.6 |
| DOC6 revision pending | Low | No impact on v2.4 |

---

*End of DOC-5 v2.4 — Cumulative (v1.0 through v2.4)*
