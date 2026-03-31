---
doc_id: DOC-2
release: v2.5
status: Draft
title: Architecture Document
version: 1.0
date_created: 2026-03-31
authors: [Architect mode, Human]
previous_release: v2.4
cumulative: true
---

# DOC-2 -- Architecture Document (v2.5)

> **Status: DRAFT** -- This document is in draft for v2.5.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all architecture from v1.0 through v2.5.
> To understand the full project architecture, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [Guiding Principle](#1-guiding-principle)
2. [Global Architecture Diagram](#2-global-architecture-diagram)
3. [Detailed Technical Stack](#3-detailed-technical-stack)
4. [Architecture Decisions](#4-architecture-decisions)
5. [Functional Layer Architecture](#5-functional-layer-architecture)
6. [Architecture / Feature / Requirement Traceability Matrix](#6-architecture-feature--requirement-traceability-matrix)
7. [v2.5 Architecture Additions](#7-v25-architecture-additions)
8. [Appendices](#8-appendices)

---

## 1. Guiding Principle

**Roo Code is the sole and unique agentic execution engine.** All other components (local LLM engine, clipboard proxy, cloud API, Memory Bank, Agile personas) are **service providers** that interface with Roo Code via standardized protocols.

This principle guarantees that:
- Roo Code's behavior is never modified, regardless of the LLM source used.
- Switching between the three backends (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) is transparent to Roo Code -- only the "API Provider" parameter changes.
- The Memory Bank and Agile personas function identically in all three modes.

---

## 2. Global Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|              WINDOWS LAPTOP "pc" (VS Code + Roo Code + Chrome)                    |
|                                                                                   |
|  +--------------------------------------------------------------------------+    |
|  |                      ROO CODE (VS Code Extension)                        |    |
|  |                                                                          |    |
|  |  +-------------+  +--------------+  +----------------------------+      |    |
|  |  |  .roomodes  |  | .clinerules  |  |   Memory Bank Reader       |      |    |
|  |  |  (4 Agile   |  |  (Imperative  |   (Read/Write .md)         |      |    |
|  |  |   Personas) |  |   Rules)     |  |                            |      |    |
|  |  +-------------+  +--------------+  +----------------------------+      |    |
|  |                                                                          |    |
|  |    OpenAI-Compatible API (HTTP)         Anthropic API (HTTPS)            |    |
|  +------------------+-----------------------+----------------+--------------+    |
|                     |                                        |                   |
|         +-----------+------------+                          |                   |
|         |    LLM SWITCHER        |  (Provider Parameter     |                   |
|         |    (3 modes)           |   in Roo Code)           |                   |
|         +-----------+------------+                          |                   |
|                     |                                        |                   |
|       +-------------+-------------+                         |                   |
|       |                           |                         |                   |
|  +----+----------+   +------------+----------+   +-----------+-----------+       |
|  | MODE 1        |   | MODE 2                |   | MODE 3                |       |
|  | LOCAL         |   | GEMINI PROXY          |   | DIRECT CLOUD          |       |
|  | (Tailscale)   |   |                       |   |                       |       |
|  |               |   | proxy.py              |   | Anthropic API         |       |
|  | calypso:11434 |   | localhost:8000        |   | api.anthropic.com     |       |
|  +---------------+   +----------------------+   +-----------------------+       |
|                                                                                   |
+-----------------------------------------------------------------------------------+
                                    |
                                    | Tailscale VPN
                                    |
+-----------------------------------------------------------------------------------+
|                        LINUX SERVER "calypso"                                    |
|                                                                                   |
|  +---------------------------+   +---------------------------------------------+  |
|  |      OLLAMA               |   |              CHROMA SERVER                  |  |
|  |  (Local LLM Inference)    |   |         (Vector Store for Memory)          |  |
|  |                           |   |                                             |  |
|  |  uadf-agent (14B)        |   |  Port 8002                                  |  |
|  |  qwen3:8b (lightweight)  |   |  /home/nghia-phan/chroma-data             |  |
|  |                           |   |                                             |  |
|  +---------------------------+   +---------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Detailed Technical Stack

### 3.1 Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| Agentic Engine | Roo Code (VS Code extension) | Central execution engine |
| Local LLM | Ollama on `calypso` | Sovereign inference |
| LLM Proxy | `proxy.py` (Python) | Multi-backend routing |
| Cloud LLM | Anthropic Claude API / Gemini | Scalable inference |
| Persistent Memory | Markdown files (`memory-bank/`) | Session continuity |
| Vector Memory | ChromaDB on `calypso` | Semantic search |
| VPN | Tailscale | Secure network connectivity |

### 3.2 Project Structure

```
agentic-agile-workbench/
├── .clinerules              # Global imperative rules for all agents
├── .roomodes                # Agile persona system prompts
├── Modelfile                # Ollama model configuration
├── proxy.py                 # LLM proxy server
├── memory-bank/             # Agent working memory
│   ├── hot-context/         # Active session files
│   │   ├── activeContext.md
│   │   ├── progress.md
│   │   ├── decisionLog.md
│   │   ├── systemPatterns.md
│   │   └── productContext.md
│   └── archive-cold/        # Historical files
├── docs/                    # Canonical documentation
│   ├── DOC-*-CURRENT.md     # Release pointers
│   ├── releases/
│   │   └── vX.Y/           # Frozen release docs
│   └── ideas/               # Idea backlog
├── src/calypso/             # Orchestration scripts
│   ├── fastmcp_server.py    # MCP server
│   ├── orchestrator_*.py   # Phase implementations
│   └── librarian_agent.py   # Memory management
├── scripts/                 # Utility scripts
│   └── batch/               # Batch API toolkit
└── template/                # Project template
```

---

## 4. Architecture Decisions

### ADR-001: Roo Code as Sole Agentic Engine

**Context:** Multiple agent frameworks exist (LangChain, AutoGen, etc.)

**Decision:** Use Roo Code exclusively as the agentic execution engine.

**Consequences:**
- Positive: Single integration point, no framework lock-in
- Negative: Tied to VS Code ecosystem

### ADR-006: Three-Branch GitFlow Model

**Context:** Need clear separation between wild development and release preparation.

**Decision:** Adopt `main` + `develop` + `develop-vX.Y` branching model.

| Branch | Purpose | Lifecycle |
|--------|---------|-----------|
| `main` | Production frozen | Never direct commits |
| `develop` | Wild mainline | Long-lived, base for scoped branches |
| `develop-vX.Y` | Scoped release | Created at release planning |

### ADR-012: Canonical Docs Cumulative + GitFlow Enforcement

**Context:** Previous releases used delta-based docs, causing coherence issues.

**Decision:** All canonical docs must be cumulative (contain full state) and enforced via Git hooks + CI.

**Rules:**
- R-CANON-0: Each doc is fully self-contained cumulative
- R-CANON-1..3: GitFlow enforcement for canonical docs
- R-CANON-5..7: Consistency rules for coordinated releases

### ADR-013: Squash Merge Prohibition

**Context:** Squash merges destroy feature branch commit history.

**Decision:** Forbid squash merges to preserve full traceability.

**Rules:**
- RULE 10.3: Prefer fast-forward or regular merge
- RULE 10.3 item 6: Never use `--delete-branch`
- Feature branches kept after merge for traceability

---

## 5. Functional Layer Architecture

### 5.1 LLM Switcher Layer

The `proxy.py` routes requests to the appropriate backend based on model name:

| Model Pattern | Backend | Endpoint |
|---------------|---------|----------|
| `gemini-*` | Google Gemini API | `generativelanguage.googleapis.com` |
| `claude-*` | Anthropic API | `api.anthropic.com` |
| `anthropic/*` | Anthropic via OpenRouter | `openrouter.ai` |
| `uadf-agent` | Local Ollama | `http://calypso:11434` |
| `qwen3:8b` | Local Ollama | `http://calypso:11434` |

### 5.2 Memory Architecture

```
memory-bank/
├── hot-context/           # MCP-accessible, frequently updated
│   ├── activeContext.md    # Current session state
│   ├── progress.md        # Feature checkbox tracking
│   ├── decisionLog.md     # ADR decisions
│   ├── systemPatterns.md  # Working patterns
│   └── productContext.md  # Product knowledge
└── archive-cold/          # Historical, vector-indexed
    ├── productContext_Master.md
    ├── completed-tickets/
    └── sprint-logs/
```

**Access Pattern:**
- Hot memory: Direct file read/write
- Cold memory: Via `memory:query()` MCP tool → Librarian Agent → ChromaDB

### 5.3 Calypso Orchestration Tier

```
Human Input
    │
    ▼
┌─────────────────┐
│ Intake Agent    │ ──► IDEAS-BACKLOG.md
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Sync Detector   │ ──► Overlap analysis
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Refinement      │ ──► Requirements
│ Workflow        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Expert Reports  │ ──► Phase 2
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Triage          │ ──► Phase 3
│ Dashboard       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execution       │ ──► Phase 4
│ Tracker         │
└─────────────────┘
```

---

## 6. Architecture / Feature / Requirement Traceability Matrix

| Feature | REQ | Implementation | Status |
|---------|-----|----------------|--------|
| LLM Switcher | REQ-2.x | `proxy.py` | Implemented |
| Memory Bank | REQ-3.x | `memory-bank/` | Implemented |
| Agile Personas | REQ-4.x | `.roomodes` | Implemented |
| Claude API | REQ-6.x | `proxy.py` + OpenRouter | Implemented |
| GitHub Actions | REQ-7.x | `.github/workflows/` | Implemented |
| Hot/Cold Memory | REQ-8.x | `memory-bank/` + ChromaDB | Implemented |
| Batch API Toolkit | REQ-9.x | `scripts/batch/` | Implemented |
| Sync Detection | REQ-10.2 | `src/calypso/sync_detector.py` | Implemented |
| Calypso Orchestration | REQ-11.x | `src/calypso/` | Implemented |
| Canonical Docs GitFlow | REQ-13.x | `.githooks/` + CI | Implemented |
| Squash Merge Prohibition | REQ-14.x | `.clinerules` RULE 10.3 | Implemented |

---

## 7. v2.5 Architecture Additions

### 7.1 Canonical Docs Governance

v2.5 introduces structural enforcement for canonical documentation:

**Git Pre-Receive Hook (`.githooks/pre-receive`):**
- Validates DOC-*-CURRENT.md pointer consistency
- Checks cumulative nature (minimum line counts)
- Enforces feature branch workflow for canonical docs

**GitHub Actions CI (`.github/workflows/canonical-docs-check.yml`):**
- Runs on PR to `develop`, `develop-v*`, `main`
- Checks DOC pointer consistency
- Validates cumulative nature of docs
- Enforces R-CANON rules

**Template Deployment (`deploy-workbench-to-project.ps1`):**
- Copies `.githooks/pre-receive` to new projects
- Copies `.github/workflows/canonical-docs-check.yml`
- Ensures governance follows the template

### 7.2 Branch Lifecycle Rules

**Feature Branch Workflow (RULE 10.3):**
1. Branch from `develop` (ad-hoc) or `develop-vX.Y` (scoped)
2. Develop and test on feature branch
3. Commit results to feature branch
4. Merge via PR (fast-forward preferred, NO squash merge)
5. **Keep** feature branch after merge (traceability)
6. **Never** use `--delete-branch` when merging PRs
7. Prefer fast-forward or regular merge

---

## 8. Appendices

### A. Port Reference

| Service | Port | Location |
|---------|------|----------|
| Ollama API | 11434 | `calypso` |
| Chroma Server | 8002 | `calypso` |
| LLM Proxy | 8000 | `pc` |
| Tailscale | 443 | Both |

### B. Environment Variables

| Variable | Purpose | Location |
|----------|---------|----------|
| `GEMINI_API_KEY` | Gemini access | `.env` (not git-committed) |
| `ANTHROPIC_API_KEY` | Claude access | `.env` (not git-committed) |
| `OPENROUTER_API_KEY` | OpenRouter access | `.env` (not git-committed) |

### C. Git Reference

| Branch | Purpose | Created From |
|--------|---------|--------------|
| `master` | Production frozen | Tag vX.Y.0 |
| `develop` | Wild mainline | `master` |
| `develop-vX.Y` | Scoped release | `develop` |
| `feature/*` | Single feature | `develop` or `develop-vX.Y` |
| `hotfix/*` | Emergency fix | `master` tag |

---

*End of DOC-2-v2.5-Architecture.md*
