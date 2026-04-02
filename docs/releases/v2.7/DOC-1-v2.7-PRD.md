---
doc_id: DOC-1
release: v2.7
status: Draft
title: Product Requirements Document
version: 1.0
date_created: 2026-04-02
authors: [Architect mode, Human]
previous_release: v2.6
cumulative: true
---

# DOC-1 — Product Requirements Document (v2.7)

> **Status: DRAFT** -- This document is under construction for v2.7 release.
> **Cumulative: YES** -- This document contains ALL requirements from v1.0 through v2.7.
> To understand the complete project requirements, read this document from top to bottom.
> Each section represents a release version. Content grows cumulatively.

---

## Table of Contents

1. [Context and Strategic Vision](#1-context-and-strategic-vision)
2. [v1.0 Requirements](#2-v10-requirements)
3. [v2.0 Requirements](#3-v20-requirements)
4. [v2.1 Requirements](#4-v21-requirements)
5. [v2.2 Requirements](#5-v22-requirements)
6. [v2.3 Requirements](#6-v23-requirements)
7. [v2.4 Requirements](#7-v24-requirements)
8. [v2.5 Requirements](#8-v25-requirements)
9. [v2.6 Requirements](#9-v26-requirements)
10. [v2.7 Requirements](#10-v27-requirements-new)

---

## 1. Context and Strategic Vision

This PRD synthesizes the complete requirements history of the Agentic Agile Workbench project, from initial vision through v2.7.

### 1.1 Project Overview

**Project Name:** Agentic Agile Workbench  
**Version:** v2.7 (Cumulative)  
**Date:** 2026-04-02  
**Status:** Under Development

### 1.2 Core Inspiration Sources

1. **The LAAW Blueprint (mychen76)**: A local, sovereign agentic development environment, orchestrated by specialized AI agents with persistent memory and Agile rituals.

2. **The Gemini Chrome Proxy**: A network-clipboard bridge mechanism allowing Roo Code to leverage the power of Gemini Web for free via minimal human intervention (copy-paste).

### 1.3 Unified System Objective

The objective is to define a **unified and enriched** system that combines:
- Local sovereignty of LAAW with hybrid LLM backend flexibility
- Switchable LLM backends: local Ollama OR Gemini Chrome via proxy OR Claude Sonnet via direct API
- Agile rigor and contextual memory persistence
- Roo Code as central agentic execution engine

### 1.4 System Architecture Summary

| Component | Description |
|-----------|-------------|
| **Roo Code** | Central agentic execution engine (VS Code extension) |
| **Ollama** | Local LLM inference (calypso server via Tailscale) |
| **Gemini Chrome Proxy** | Network-clipboard bridge to Gemini Web |
| **Anthropic API** | Direct Claude Sonnet API access |
| **Memory Bank** | Persistent context across sessions (Git-versioned) |
| **Agile Personas** | RBAC-controlled role simulation |

### 1.5 Three LLM Backend Modes

| Mode | Provider | Cost | Human Intervention | Data Sovereignty |
|------|----------|------|---------------------|------------------|
| **Local Mode** | Ollama (Qwen3-32B) | Free | None | Total (100% local) |
| **Proxy Mode** | Gemini Chrome | Free | Copy-paste | Partial (Google) |
| **Cloud Mode** | Claude Sonnet | Paid | None | Partial (Anthropic) |

---

## 2. v1.0 Requirements

### 2.1 Foundational Requirement (REQ-000)

> **REQ-000 -- Root Requirement of the Unified System**
>
> The overall system must provide an operational agentic development environment on a Windows laptop (`pc`) with VS Code, relying on a dedicated headless Linux server (`calypso`) for local LLM inference, both machines connected via Tailscale. The system must be capable of:
> - Orchestrating specialized AI agents according to Agile roles (Product Owner, Scrum Master, QA Engineer, Developer)
> - Maintaining absolute context continuity between sessions via persistent memory in auditable Markdown files
> - Executing complex development tasks relying on a **switchable** LLM backend: either a local model (Ollama on `calypso` via Tailscale) for total sovereignty, or Gemini Chrome via a local API proxy for free cloud power, or Claude Sonnet via direct Anthropic API for full automation
> - Ensuring that Roo Code remains the central agentic execution engine in all three operating modes, without modification of its native behavior

### 2.2 Domain 1 — Agentic Engine & Foundation Models (REQ-1.x)

#### REQ-1.0 — Local LLM Inference Capability

The system must be capable of executing LLM inferences on the private local network (Tailscale), via Ollama installed on the Linux server `calypso` (RTX 5060 Ti 16 GB).

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-1.1 | Main model optimized for Tool Calling | `mychen76/qwen3_cline_roocode:32b` fine-tuned for Roo Code |
| REQ-1.2 | Minimum context window of 128K tokens | `num_ctx 131072` in Modelfile |
| REQ-1.3 | Inference determinism | `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` |
| REQ-1.4 | Boomerang Tasks delegation | 32B agent delegates to 7B model via sub-task |

### 2.3 Domain 2 — Hybrid LLM Backend & Gemini Chrome Proxy (REQ-2.x)

#### REQ-2.0 — LLM Backend Switchability

The system must allow switching Roo Code's LLM backend between three modes by modifying only the "API Provider" parameter.

##### REQ-2.1 — Local Proxy Server (Interception)

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-2.1.1 | Local FastAPI server on localhost:8000 | `http://localhost:8000/health` returns HTTP 200 |
| REQ-2.1.2 | Exact emulation of OpenAI Chat Completions format | Roo Code connects without error |
| REQ-2.1.3 | Separate extraction of system/user/assistant prompts | Correct identification of message roles |
| REQ-2.1.4 | "Dedicated Gem" mode: system prompt filtering | `USE_GEM_MODE=true` omits system message |
| REQ-2.1.5 | Cleaning of base64 content (images) | Images replaced with `[IMAGE OMITTED]` |

##### REQ-2.2 — Clipboard Transfer (Uplink)

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-2.2.1 | Injection into Windows clipboard in <500ms | Clipboard available within 500ms |
| REQ-2.2.2 | Readable format with explicit separators | Human can identify sections in <5 seconds |
| REQ-2.2.3 | Timestamped console notification | Console shows time, size, actions, timeout |

##### REQ-2.3 — Response Wait and Capture (Downlink)

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-2.3.1 | Asynchronous clipboard polling every second | FastAPI still responds during polling |
| REQ-2.3.2 | Change detection by MD5 hash comparison | Detection within 2 seconds |
| REQ-2.3.3 | Configurable timeout with HTTP 408 response | HTTP 408 after TIMEOUT_SECONDS |
| REQ-2.3.4 | Validation of Roo Code XML tag presence | Warning if no XML tags found |

##### REQ-2.4 — Re-injection to Roo Code

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-2.4.1 | SSE streaming support in a single chunk | Streaming works without error |
| REQ-2.4.2 | Complete OpenAI JSON format for non-streamed response | JSON parseable by Roo Code |
| REQ-2.4.3 | HTTP 200 response with Content-Type application/json | Headers correct in both modes |
| REQ-2.4.4 | Complete preservation of Gemini content | Byte-for-byte identical content |

### 2.4 Domain 3 — Agility & Role Segregation (REQ-3.x)

#### REQ-3.0 — Virtual Agile Team

The system must simulate a complete Scrum team via Roo Code Custom Modes.

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-3.1 | 4 Agile personas in `.roomodes` | `product-owner`, `scrum-master`, `developer`, `qa-engineer` |
| REQ-3.2 | Strict permission segregation (RBAC) | PO cannot create `.py` file |
| REQ-3.3 | Behavioral refusal of out-of-scope actions | Persona refuses and suggests correct persona |
| REQ-3.4 | Scrum Master: pure facilitator | SM can read, write memory-bank/docs, execute Git only |

### 2.5 Domain 4 — Persistence & Memory Bank (REQ-4.x)

#### REQ-4.0 — Persistent Contextual Memory

The system must maintain absolute context continuity between sessions.

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-4.1 | Storage in `memory-bank/` versioned under Git | `git ls-files memory-bank/` lists 7 files |
| REQ-4.2 | Mandatory sequence CHECK → CREATE → READ → ACT | Agent follows sequence at every session |
| REQ-4.3 | Mandatory update before task closure | Git history shows Memory Bank commit before code |
| REQ-4.4 | 7 distinct thematic files | Each file has unique responsibility |
| REQ-4.5 | Git versioning of all Memory Bank modifications | Commit message format: `docs(memory): {description}` |

### 2.6 Domain 5 — Gemini Chrome Configuration (REQ-5.x)

#### REQ-5.0 — Gemini Web Interface Preparation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-5.1 | Dedicated "Roo Code Agent" Gem | Gem exists in Gemini interface |
| REQ-5.2 | Gemini responses exclusively in Roo Code XML tags | 5 test requests produce valid XML only |
| REQ-5.3 | Multi-turn conversation history maintenance | 3 related requests produce coherent responses |

### 2.7 Domain 6 — Direct Cloud Mode via Anthropic API (REQ-6.x)

#### REQ-6.0 — Direct Connection to Anthropic Claude API

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-6.1 | Valid Anthropic API key stored securely | In VS Code SecretStorage only |
| REQ-6.2 | Model `claude-sonnet-4-6` as reference | Connection test successful |
| REQ-6.3 | Connection via Roo Code's native "Anthropic" provider | Direct to `api.anthropic.com` |
| REQ-6.4 | Absolute prohibition on API key versioning | `git grep "sk-ant"` returns zero results |

### 2.8 Domain 7 — Central System Prompt Registry (REQ-7.x)

#### REQ-7.0 — Centralized System Prompt Registry

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-7.1 | 7 canonical SP files in `prompts/` | 8 files total (7 SP + README) |
| REQ-7.2 | Unambiguous identification of deployment target | Developer can deploy without ambiguity |
| REQ-7.3 | Mandatory consistency before commit (RULE 6) | Pre-commit hook blocks desync |
| REQ-7.4 | Semantic versioning of prompts | Changelog maintained |
| REQ-7.5 | Documented manual deployment for SP-007 | `hors_git: true` and manual procedure |

### 2.9 Domain 8 — Automatic Prompt Consistency Verification (REQ-8.x)

#### REQ-8.0 — Automatic Detection of Prompt/Artifact Desynchronization

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-8.1 | PowerShell script `check-prompts-sync.ps1` | Exit code 0 if synced, 1 if desync |
| REQ-8.2 | Blocking Git pre-commit hook | Commit blocked if desync detected |
| REQ-8.3 | Verification report with readable diff | First 200 chars shown for comparison |
| REQ-8.4 | Exclusion of SP-007 from automatic verification | `[MANUAL]` message, exit code 0 |

### 2.10 RBAC Permission Matrix by Persona

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
|-----------|:---:|:---:|:---:|:---:|
| Read all files | ✅ | ✅ | ✅ | ✅ |
| Write `memory-bank/productContext.md` | ✅ | ✅ | ✅ | ❌ |
| Write `memory-bank/*.md` (all) | ❌ | ✅ | ✅ | ❌ |
| Write `docs/*.md` | ✅ | ✅ | ✅ | ❌ |
| Write `docs/qa/*.md` | ❌ | ❌ | ❌ | ✅ |
| Write source code | ❌ | ❌ | ✅ | ❌ |
| General terminal execution | ❌ | ❌ | ✅ | ❌ |
| Execute Git commands only | ❌ | ✅ | ✅ | ❌ |
| Execute test commands | ❌ | ❌ | ✅ | ✅ |
| Browser access | ❌ | ❌ | ✅ | ✅ |
| MCP access | ❌ | ❌ | ✅ | ❌ |

### 2.11 Constraints and Non-Goals

#### Constraints
- Two machines required: Windows laptop `pc` and Linux server `calypso` via Tailscale
- Gemini Chrome proxy requires minimal human intervention (copy-paste)
- Cloud Mode involves per-usage Anthropic API costs
- Ollama model availability on Ollama Hub is installation precondition

#### Non-Goals
- No automation of copy-pasting to Gemini Chrome
- No multi-user project management
- No replacement of real Agile tools (Jira, Linear)
- Proxy Mode does NOT support Boomerang Tasks

---

## 3. v2.0 Requirements

> **v2.0 Release Summary**
> 
> v2.0 introduced the core orchestration infrastructure and major enhancements:
> - IDEA-001: Hot/Cold memory architecture
> - IDEA-002: Calypso orchestration scripts (Phase 2-4 pipeline)
> - IDEA-003: Release governance model
> - IDEA-006: Template enrichment
> - IDEA-007: Global Brain / Librarian Agent

### 3.1 Hot/Cold Memory Architecture (IDEA-001)

#### REQ-HC-1 — Memory Temperature Classification

The system must classify memory into hot and cold zones based on access patterns.

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-HC-1.1 | Hot Zone: frequently accessed files | `memory-bank/hot-context/` contains active session files |
| REQ-HC-1.2 | Cold Zone: archive files | `memory-bank/archive-cold/` contains historical files |
| REQ-HC-1.3 | Automatic temperature detection | System tracks file access frequency |
| REQ-HC-1.4 | Archive promotion/demotion | Files move between zones based on usage |

#### REQ-HC-2 — Archive Management

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-HC-2.1 | Archive integrity | Archived files are immutable and verifiable |
| REQ-HC-2.2 | Archive indexing | Librarian Agent maintains searchable index |
| REQ-HC-2.3 | Archive retrieval | Files can be restored from cold zone |

### 3.2 Calypso Orchestration Scripts (IDEA-002)

#### REQ-CAL-1 — Phase 2-4 Pipeline Automation

The system must provide scripts for orchestrating the ideation-to-release pipeline.

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-CAL-1.1 | Phase 2: Intake orchestration | `orchestrator_phase2.py` processes new ideas |
| REQ-CAL-1.2 | Phase 3: Refinement orchestration | `orchestrator_phase3.py` handles refinement |
| REQ-CAL-1.3 | Phase 4: Implementation orchestration | `orchestrator_phase4.py` tracks implementation |
| REQ-CAL-1.4 | Pipeline status visibility | Dashboard shows current phase and status |

#### REQ-CAL-2 — Calypso Components

| Component | File | Purpose |
|-----------|------|---------|
| Intake Agent | `intake_agent.py` | Initial idea processing and classification |
| Sync Detector | `sync_detector.py` | Overlap detection between ideas |
| Refinement Workflow | `refinement_workflow.py` | Structured refinement process |
| Branch Tracker | `branch_tracker.py` | GitFlow compliance tracking |
| Execution Tracker | `execution_tracker.py` | Implementation progress tracking |
| Ideas Dashboard | `ideas_dashboard.py` | Visual backlog management |

### 3.3 Release Governance Model (IDEA-003)

#### REQ-GOV-1 — Release Process

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-GOV-1.1 | Release planning | vX.Y scope defined before development |
| REQ-GOV-1.2 | Branch naming | `develop-vX.Y` for scoped releases |
| REQ-GOV-1.3 | Release tagging | `vX.Y.0` tag on `develop-vX.Y` at release |
| REQ-GOV-1.4 | Merge to main | Fast-forward merge to main at release |

#### REQ-GOV-2 — ADR Management

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-GOV-2.1 | ADR format | Timestamp, context, decision, consequences |
| REQ-GOV-2.2 | Decision log | `memory-bank/decisionLog.md` contains all ADRs |
| REQ-GOV-2.3 | ADR reference | Decisions referenced in affected code/docs |

### 3.4 Template Enrichment (IDEA-006)

#### REQ-TPL-1 — Template Structure

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-TPL-1.1 | Complete template directory | `template/` contains all workbench files |
| REQ-TPL-1.2 | Template prompts | `template/prompts/` contains all SP files |
| REQ-TPL-1.3 | Template memory bank | `template/memory-bank/` contains structure |
| REQ-TPL-1.4 | Template docs | `template/docs/` contains canonical doc pointers |

### 3.5 Global Brain / Librarian Agent (IDEA-007)

#### REQ-LIB-1 — Librarian Agent Capabilities

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-LIB-1.1 | Archive indexing | Vector database searchable index |
| REQ-LIB-1.2 | Query interface | Semantic search of archived content |
| REQ-LIB-1.3 | Retrieval | Relevant files retrieved on query |
| REQ-LIB-1.4 | SP-010 system prompt | `prompts/SP-010-librarian-agent.md` defines behavior |

---

## 4. v2.1 Requirements

> **v2.1 Release Summary**
>
> v2.1 introduced OpenRouter MinMax M2.7 as the default LLM backend.

### 4.1 OpenRouter MinMax Default (IDEA-008)

#### REQ-OR-1 — OpenRouter Integration

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-OR-1.1 | OpenRouter as default provider | Roo Code configured with OpenRouter |
| REQ-OR-1.2 | MinMax M2.7 model | `minimax/minimax-m2.7` as default model |
| REQ-OR-1.3 | Provider switchability | Can switch between Ollama, OpenRouter, Anthropic |
| REQ-OR-1.4 | API key management | Keys stored securely, not in Git |

### 4.2 Prompt Registry Updates (IDEA-007 continuation)

#### REQ-PR-1 — Registry Maintenance

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PR-1.1 | SP README | `prompts/README.md` index current |
| REQ-PR-1.2 | Version tracking | Each SP has semantic version |
| REQ-PR-1.3 | Change log | Modifications tracked per SP |

---

## 5. v2.2 Requirements

> **v2.2 Release Summary**
>
> v2.2 continued MinMax integration and minor tooling improvements.

### 5.1 MinMax Backend Refinement

#### REQ-MM-1 — Backend Consolidation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-MM-1.1 | Default provider consistency | OpenRouter MinMax as standard default |
| REQ-MM-1.2 | Fallback behavior | Graceful degradation if primary fails |
| REQ-MM-1.3 | Configuration management | Settings in `.roomodes` or environment |

### 5.2 Product Context Updates

#### REQ-PC-1 — Context Maintenance

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PC-1.1 | Product context file | `memory-bank/productContext.md` current |
| REQ-PC-1.2 | Sprint tracking | Active sprint user stories documented |
| REQ-PC-1.3 | Backlog visibility | Upcoming features listed |

---

## 6. v2.3 Requirements

> **v2.3 Release Summary**
>
> v2.3 introduced the generic Anthropic Batch API Toolkit and fixed SP-002 coherence issues.

### 6.1 Batch API Toolkit (IDEA-009)

#### REQ-BATCH-1 — Batch Processing Infrastructure

The system must provide a generic toolkit for submitting and managing Anthropic batch API requests.

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-BATCH-1.1 | Batch submission | `scripts/batch/submit.py` submits batch requests |
| REQ-BATCH-1.2 | Batch polling | `scripts/batch/poll.py` checks batch status |
| REQ-BATCH-1.3 | Batch retrieval | `scripts/batch/retrieve.py` retrieves results |
| REQ-BATCH-1.4 | Batch generation | `scripts/batch/generate.py` creates batch files |
| REQ-BATCH-1.5 | CLI interface | `scripts/batch/cli.py` provides command interface |

#### REQ-BATCH-2 — Batch Configuration

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-BATCH-2.1 | Config management | `scripts/batch/config.py` handles settings |
| REQ-BATCH-2.2 | Template support | Jinja2 templates for batch file generation |
| REQ-BATCH-2.3 | Error handling | Failures reported with actionable messages |

### 6.2 SP-002 Coherence Fix (IDEA-011)

#### REQ-SP2-1 — Persistent Encoding Fix

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-SP2-1.1 | Encoding consistency | UTF-8 encoding enforced |
| REQ-SP2-1.2 | Corruption detection | Pre-commit hook detects encoding issues |
| REQ-SP2-1.3 | Recovery mechanism | Corrupted files can be rebuilt |

### 6.3 Coherence Audit

#### REQ-AUD-1 — Pre-Release Verification

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-AUD-1.1 | Coherence checklist | All requirements verified |
| REQ-AUD-1.2 | Audit documentation | `docs/qa/v2.3/COHERENCE-AUDIT-v2.3.md` exists |
| REQ-AUD-1.3 | Issue tracking | Discrepancies documented and addressed |

---

## 7. v2.4 Requirements

> **v2.4 Release Summary**
>
> v2.4 implemented the full Ideation-to-Release pipeline (PHASE-A, B, C).

### 7.1 Ideation-to-Release PHASE-A Foundation (IDEA-012A)

#### REQ-PHA-1 — Intake Agent Enhancement

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PHA-1.1 | Idea capture | New ideas immediately added to backlog |
| REEA-PHA-1.2 | Classification routing | Business vs Technical routing |
| REQ-PHA-1.3 | TECH-SUGGESTIONS-BACKLOG | Technical suggestions tracked separately |

#### REQ-PHA-2 — RULE 11-14 Implementation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PHA-2.1 | RULE 11: Sync detection | Overlap detection before implementation |
| REQ-PHA-2.2 | RULE 12: Canonical docs | Cumulative doc enforcement |
| REQ-PHA-2.3 | RULE 13: Ideation intake | Mandatory routing for off-topic input |
| REQ-PHA-2.4 | RULE 14: DOC-3 execution | Live execution tracking |

### 7.2 Ideation-to-Release PHASE-B Core Logic (IDEA-012B)

#### REQ-PHB-1 — SyncDetector Implementation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PHB-1.1 | Overlap detection | 5 sync categories identified |
| REQ-PHB-1.2 | Conflict resolution | Human arbitrates conflicts |
| REQ-PHB-1.3 | Redundancy merge | Duplicate ideas combined |
| REQ-PHB-1.4 | Dependency ordering | B depends on A logged |

#### REQ-PHB-2 — RefinementWorkflow Implementation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PHB-2.1 | Structured refinement | 5-phase refinement process |
| REQ-PHB-2.2 | Requirement formalization | Business requirements clearly stated |
| REQ-PHB-2.3 | Feasibility evaluation | Technical suggestions evaluated |

### 7.3 Ideation-to-Release PHASE-C Full Features (IDEA-012C)

#### REQ-PHC-1 — BranchTracker Implementation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PHC-1.1 | GitFlow compliance | Three-branch model enforced |
| REQ-PHC-1.2 | Branch lifecycle | Branches never deleted after merge |
| REQ-PHC-1.3 | Release tracking | `is_release_in_progress()` method |

#### REQ-PHC-2 — ExecutionTracker Implementation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PHC-2.1 | Live progress tracking | Current status per IDEA |
| REQ-PHC-2.2 | Phase awareness | Current phase displayed |
| REQ-PHC-2.3 | Checkpoint updates | Progress.md synchronized |

#### REQ-PHC-3 — IdeasDashboard Implementation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PHC-3.1 | Backlog visualization | All IDEAS with status |
| REQ-PHC-3.2 | Filtering | By status, type, tier, target |
| REQ-PHC-3.3 | Quick actions | Navigate to IDEA details |

### 7.4 DOC-3 Auto-Generation

#### REQ-DOC3-1 — Implementation Plan Automation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-DOC3-1.1 | Template population | DOC-3 populated from IDEA details |
| REQ-DOC3-1.2 | Section structure | Each IDEA gets implementation section |
| REQ-DOC3-1.3 | Status sync | DOC-3 reflects current execution state |

---

## 8. v2.5 Requirements

> **v2.5 Release Summary**
>
> v2.5 completed the ideation-to-release pipeline and added triage dashboard.

### 8.1 TriageDashboard Implementation

#### REQ-TD-1 — Triage Interface

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-TD-1.1 | Triage session UI | Visual dashboard for triage |
| REQ-TD-1.2 | Idea evaluation | Each IDEA reviewed systematically |
| REQ-TD-1.3 | Disposition tracking | ACCEPTED/DEFERRED/REJECTED logged |

### 8.2 FastMCP Server

#### REQ-MCP-1 — Model Context Protocol Server

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-MCP-1.1 | MCP endpoint | `fastmcp_server.py` exposes MCP |
| REQ-MCP-1.2 | Tool registration | Calypso tools registered |
| REQ-MCP-1.3 | Request handling | MCP requests processed correctly |

### 8.3 GitFlow Enforcement ADRs

#### REQ-GF-1 — ADR-010: Dev Tooling Process Bypass

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-GF-1.1 | Process bypass documentation | ADR-010 documents bypass policy |
| REQ-GF-1.2 | Emergency procedure | Defined bypass criteria |

#### REQ-GF-2 — ADR-011: GitFlow Violation Remediation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-GF-2.1 | Violation detection | Cherry-pick remediation applied |
| REQ-GF-2.2 | develop-vX.Y integrity | All fixes merged to correct branch |

### 8.4 ADR-006 GitFlow Documentation

#### REQ-GF-3 — Branch Lifecycle Documentation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-GF-3.1 | Branch definitions | main/develop/develop-vX.Y documented |
| REQ-GF-3.2 | Forbidden actions | Direct commits prohibited |
| REQ-GF-3.3 | Feature branch workflow | Branch/merge/PR lifecycle defined |

---

## 9. v2.6 Requirements

> **v2.6 Release Summary**
>
> v2.6 focused on canonical docs GitFlow enforcement and session checkpoint improvements.

### 9.1 ADR-012: Canonical Docs Cumulative GitFlow Enforcement

#### REQ-ADR12-1 — Cumulative Documentation Requirement

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-ADR12-1.1 | Cumulative docs | DOC-X-vX.Y contains all previous content |
| REQ-ADR12-1.2 | Frozen status | Released docs marked FROZEN |
| REQ-ADR12-1.3 | Draft status | In-progress docs marked DRAFT |
| REQ-ADR12-1.4 | CI enforcement | `canonical-docs-check.yml` validates |

### 9.2 Session Checkpoint Enhancement

#### REQ-SC-1 — Crash Recovery Mechanism

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-SC-1.1 | Session checkpoint file | `memory-bank/hot-context/session-checkpoint.md` exists |
| REQ-SC-1.2 | Heartbeat every 5 minutes | `checkpoint_heartbeat.py` writes periodically |
| REQ-SC-1.3 | Crash detection | If last_heartbeat > 30 minutes, potential crash |

### 9.3 APPEND ONLY Discipline (RULE MB-3)

#### REQ-LOG-1 — Decision Log Integrity

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-LOG-1.1 | APPEND ONLY | New ADRs appended, existing never edited |
| REQ-LOG-1.2 | decisionLog.md integrity | Historical ADRs preserved |

### 9.4 Artifact Identification Schema

#### REQ-ID-1 — Dated Artifact IDs

| ID | Requirement | Format | Example |
|----|-------------|--------|---------|
| REQ-ID-1.1 | Business ideas | `IDEA-YYYY-MM-DD-NNN` | `IDEA-2026-04-01-001` |
| REQ-ID-1.2 | Technical suggestions | `TECH-YYYY-MM-DD-NNN` | `TECH-2026-04-01-001` |
| REQ-ID-1.3 | Architecture decisions | `ADR-YYYY-MM-DD-NNN` | `ADR-2026-04-01-001` |
| REQ-ID-1.4 | Sessions | `sYYYY-MM-DD-{mode}-{NNN}` | `s2026-04-01-developer-001` |
| REQ-ID-1.5 | Enhancements | `ENH-YYYY-MM-DD-NNN` | `ENH-2026-04-01-001` |

### 9.5 Plan-Branch Parity (RULE G-0)

#### REQ-PB-1 — Every Plan Creates a Branch

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-PB-1.1 | Branch naming | `governance/PLAN-{ID}-{slug}` |
| REQ-PB-1.2 | Branch preserved | Branches never deleted after merge |
| REQ-PB-1.3 | PR to target | PRs merge to `develop` or `develop-vX.Y` |

### 9.6 Deferred Enhancement Tracking (RULE D-1)

#### REQ-DE-1 — Future Items Tracked

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-DE-1.1 | ENH IDs | Future items get `ENH-YYYY-MM-DD-NNN` IDs |
| REQ-DE-1.2 | Status tracking | DEFERRED → IN_PROGRESS → COMPLETED |
| REQ-DE-1.3 | Target version | Every enhancement has a target_version |

### 9.7 Coherence Audit v2.6

#### REQ-AUD26-1 — Pre-Release Verification

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-AUD26-1.1 | Audit plan | `docs/qa/v2.6/AUDIT-PLAN-v2.6.md` exists |
| REQ-AUD26-1.2 | Coherence audit | `docs/qa/v2.6/COHERENCE-AUDIT-v2.6.md` exists |
| REQ-AUD26-1.3 | Batch submissions | `docs/qa/v2.6/submit_batch*.py` files exist |

---

## 10. v2.7 Requirements (NEW)

> **v2.7 Release Summary**
>
> v2.7 addresses critical governance issues and introduces new features.

### 10.1 IDEA-013: Batch Toolkit Usability Improvements

#### REQ-BATCH27-1 — Script Usability

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-BATCH27-1.1 | CLI improvements | User-friendly command interface |
| REQ-BATCH27-1.2 | Error messages | Actionable error guidance |
| REQ-BATCH27-1.3 | Documentation | Usage examples provided |

### 10.2 IDEA-014: Canonical Docs Status Governance

#### REQ-DOCGOV-1 — Status Consistency

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-DOCGOV-1.1 | Frozen vs Draft | Clear distinction enforced |
| REQ-DOCGOV-1.2 | Status transitions | DRAFT → IN REVIEW → FROZEN |
| REQ-DOCGOV-1.3 | Gatekeeping | Only PO/Architect can freeze |

### 10.3 IDEA-015: Mandatory Release Coherence Audit

#### REQ-COH-1 — Pre-Release Audit Gate

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-COH-1.1 | Coherence checklist | All items verified before release |
| REQ-COH-1.2 | QA sign-off | Coherence audit passed |
| REQ-COH-1.3 | Audit artifact | Documented in EXECUTION-TRACKER |

### 10.4 IDEA-016: Enrich Docs with Mermaid Diagrams

#### REQ-DIAG-1 — Visual Documentation

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-DIAG-1.1 | Architecture diagrams | Mermaid flowcharts in DOC-2 |
| REQ-DIAG-1.2 | Process diagrams | Mermaid in DOC-3 |
| REQ-DIAG-1.3 | State diagrams | Where applicable |

### 10.5 IDEA-017: Fix Canonical Docs Cumulative Requirement

#### REQ-CUM-1 — Cumulative Documentation Fix

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-CUM-1.1 | All content preserved | DOC-X-v2.7 contains v1.0 through v2.7 |
| REQ-CUM-1.2 | Line count minimums | DOC-1≥500, DOC-2≥500, DOC-3≥300, DOC-4≥300, DOC-5≥200 |
| REQ-CUM-1.3 | Version sections | Each version has its section |
| REQ-CUM-1.4 | CI enforcement | canonical-docs-check.yml passes |

### 10.6 IDEA-018: Make Rules Authoritative and Ensure Coherence

#### REQ-RULES-1 — Rule System Improvement

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-RULES-1.1 | Rule authority | Rules are binding, not suggestions |
| REQ-RULES-1.2 | Contradiction resolution | .clinerules contradictions fixed |
| REQ-RULES-1.3 | Coherence verification | SP-002 matches .clinerules byte-for-byte |

### 10.7 IDEA-019: Implement Conversation Logging Mechanism

#### REQ-CONV-1 — AI Conversation Persistence

| ID | Requirement | Acceptance Criterion |
|----|-------------|---------------------|
| REQ-CONV-1.1 | Logging trigger | All AI conversations logged |
| REQ-CONV-1.2 | File naming | `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md` |
| REQ-CONV-1.3 | README index | `docs/conversations/README.md` updated |
| REQ-CONV-1.4 | Non-editable | Conversations never modified after creation |

---

## Appendix A: Requirements Traceability Matrix

| Requirement | Domain | Priority | Version Introduced | Status |
|-------------|--------|----------|-------------------|--------|
| REQ-000 | Foundational | CRITICAL | v1.0 | IMPLEMENTED |
| REQ-1.x | Local Engine | HIGH | v1.0 | IMPLEMENTED |
| REQ-2.x | Hybrid Proxy | CRITICAL | v1.0 | IMPLEMENTED |
| REQ-3.x | Agility | HIGH | v1.0 | IMPLEMENTED |
| REQ-4.x | Memory | HIGH | v1.0 | IMPLEMENTED |
| REQ-5.x | Gemini Config | HIGH | v1.0 | IMPLEMENTED |
| REQ-6.x | Direct Cloud API | HIGH | v1.0 | IMPLEMENTED |
| REQ-7.x | Prompt Registry | HIGH | v1.0 | IMPLEMENTED |
| REQ-8.x | Consistency Verification | HIGH | v1.0 | IMPLEMENTED |
| REQ-HC-x | Hot/Cold Memory | HIGH | v2.0 | IMPLEMENTED |
| REQ-CAL-x | Calypso Orchestration | HIGH | v2.0 | IMPLEMENTED |
| REQ-GOV-x | Release Governance | HIGH | v2.0 | IMPLEMENTED |
| REQ-OR-x | OpenRouter | MEDIUM | v2.1 | IMPLEMENTED |
| REQ-BATCH-x | Batch API | MEDIUM | v2.3 | IMPLEMENTED |
| REQ-SP2-x | SP-002 Coherence | HIGH | v2.3 | IMPLEMENTED |
| REQ-PHA-x | PHASE-A | MEDIUM | v2.4 | IMPLEMENTED |
| REQ-PHB-x | PHASE-B | MEDIUM | v2.4 | IMPLEMENTED |
| REQ-PHC-x | PHASE-C | MEDIUM | v2.4 | IMPLEMENTED |
| REQ-ADR12-x | Canonical Docs | CRITICAL | v2.6 | IMPLEMENTED |
| REQ-CUM-x | Cumulative Docs | CRITICAL | v2.7 | IN PROGRESS |

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **ADR** | Architecture Decision Record - timestamped decision documentation |
| **Calypso** | Orchestration scripts for ideation-to-release pipeline |
| **CI/CD** | Continuous Integration/Continuous Deployment |
| **GitFlow** | Branching strategy: main/develop/feature/hotfix |
| **IDEA** | Business requirement item |
| **Librarian Agent** | AI agent managing cold archive |
| **MCP** | Model Context Protocol |
| **PHASE-A/B/C** | Phases of ideation-to-release pipeline |
| **RBAC** | Role-Based Access Control |
| **SP** | System Prompt - canonical prompt definition |
| **TECH** | Technical suggestion item |

---

*DOC-1-v2.7-PRD.md — Cumulative Product Requirements Document v2.7*
*Status: DRAFT — Under construction for v2.7 release*
