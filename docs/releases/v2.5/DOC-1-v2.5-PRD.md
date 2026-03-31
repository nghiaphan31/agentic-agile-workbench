---
doc_id: DOC-1
release: v2.5
status: Draft
title: Product Requirements Document
version: 1.0
date_created: 2026-03-31
authors: [Architect mode, Human]
previous_release: v2.4
cumulative: true
---

# DOC-1 — Product Requirements Document (v2.5)

> **Status: DRAFT** -- This document is in draft for v2.5.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all requirements from v1.0 through v2.5.
> To understand the full project requirements, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [Context and Strategic Vision](#1-context-and-strategic-vision)
2. [v1.0 Requirements](#2-v10-requirements)
3. [v2.1 Requirements](#3-v21-requirements)
4. [v2.2 Requirements](#4-v22-requirements)
5. [v2.3 Requirements](#5-v23-requirements)
6. [v2.4 Requirements](#6-v24-requirements)
7. [v2.5 Requirements](#7-v25-requirements)
8. [All Previous Workflows Preserved](#8-all-previous-workflows-preserved)

---

## 1. Context and Strategic Vision

This PRD synthesizes two complementary sources of inspiration:

1. **The LAAW Blueprint (mychen76)**: A local, sovereign agentic development environment, orchestrated by specialized AI agents with persistent memory and Agile rituals.
2. **The Gemini Chrome Proxy**: A network-clipboard bridge mechanism allowing Roo Code to leverage the power of Gemini Web for free via minimal human intervention (copy-paste).

The objective is to define a **unified and enriched** system that combines the local sovereignty of LAAW with the flexibility of a hybrid LLM backend (local Ollama OR Gemini Chrome via proxy OR Claude Sonnet via direct API), while maintaining Agile rigor and contextual memory persistence.

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

---

### 2.2 Domain 1 -- Agentic Engine & Foundation Models (REQ-1.x)

#### REQ-1.0 -- Local LLM Inference Capability

The system must be capable of executing LLM inferences on the private local network (Tailscale), via Ollama installed on the Linux server `calypso` (RTX 5060 Ti 16 GB). The Ollama API is accessible from the laptop `pc` at `http://calypso:11434` via the Tailscale network.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-1.1** | **Main model optimized for Tool Calling** | The Ollama model used as the main agent must be `mychen76/qwen3_cline_roocode:14b`, specifically fine-tuned for Roo Code tool calling. | The agent emits valid JSON requests to the Roo Code API without syntax or formatting errors on 10 consecutive test requests. |
| **REQ-1.2** | **Minimum context window of 128K tokens** | The `num_ctx` parameter in the Ollama Modelfile must be configured to exactly `131072` (128K tokens). | `ollama show uadf-agent --modelfile` displays `PARAMETER num_ctx 131072`. |
| **REQ-1.3** | **Inference determinism** | Generation parameters must be locked in the Modelfile: `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`. These values cannot be modified at runtime. | `ollama show uadf-agent --modelfile` displays the 4 parameters with the exact values above. |
| **REQ-1.4** | **Boomerang Tasks delegation** | The system must allow the main agent (14B) to delegate sub-tasks to a lightweight secondary model (`qwen3:8b`) via Roo Code's "Boomerang Tasks" workflow. | The 14B agent can create a Boomerang sub-task, the 8B model executes it, and the result is returned to the 14B agent without human intervention. |

---

### 2.3 Domain 2 -- Hybrid LLM Backend & Gemini Chrome Proxy (REQ-2.x)

#### REQ-2.0 -- LLM Backend Switchability

The system must allow the user to switch Roo Code's LLM backend between three modes (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) by modifying only the "API Provider" parameter in Roo Code settings, without modifying Roo Code's behavior or the Memory Bank structure.

#### REQ-2.1 -- Sub-domain: Local Proxy Server (Interception)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.1** | **Local SSE proxy server** | A Python proxy server (`proxy.py`) must run on port 8080 of the laptop `pc`, intercepting Roo Code's API requests and forwarding them to the configured backend (Ollama or Gemini). | `curl http://localhost:8080/v1/models` returns a valid OpenAI-compatible models list. |
| **REQ-2.2** | **Gemini API key injection** | The proxy must read the Gemini API key from a `.env` file at startup and inject it into outgoing requests to the Gemini API. | The proxy logs "Gemini API key loaded" at startup without exposing the key in logs. |
| **REQ-2.3** | **Request routing** | The proxy must route requests to the appropriate backend based on the API endpoint: Ollama at `http://calypso:11434` or Gemini at `generativelanguage.googleapis.com`. | A request to `localhost:8080/v1/chat/completions` with model `gemini-2.0-flash` is forwarded to Gemini; with model `uadf-agent` is forwarded to Ollama. |

#### REQ-2.2 -- Sub-domain: Gemini Chrome Integration

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.4** | **Chrome tab interception** | The proxy must be capable of intercepting requests from a Chrome browser tab running Gemini, by configuring Chrome to use `http://localhost:8080/proxy` as its API endpoint. | With proxy running and Chrome configured, Gemini web UI makes requests through the proxy. |
| **REQ-2.5** | **SSE response streaming** | The proxy must forward SSE (Server-Sent Events) responses from Gemini to Roo Code in real-time, without buffering the full response. | A streaming chat completion through the proxy delivers tokens to Roo Code within 500ms of Gemini generating them. |

---

### 2.4 Domain 3 -- Persistent Memory & Memory Bank (REQ-3.x)

#### REQ-3.0 -- Memory Bank Structure

The system must maintain a **Memory Bank** directory (`memory-bank/`) in the project root, containing Markdown files that persist all agent session context.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-3.1** | **Memory Bank location** | The Memory Bank must be located at `memory-bank/` in the project root, version-controlled in Git. | `ls memory-bank/` lists at least 5 Markdown files. |
| **REQ-3.2** | **Session continuity** | At session start, the agent must read `memory-bank/` files to restore full project context before taking any action. | After a clean restart, the agent can answer "What was the last thing we worked on?" without human input. |
| **REQ-3.3** | **Audit trail** | All significant decisions, tool usages, and task completions must be logged in `memory-bank/` with timestamps and rationale. | `memory-bank/` contains a dated entry for every significant action in the previous session. |

---

### 2.5 Domain 4 -- Agile Process & Role Orchestration (REQ-4.x)

#### REQ-4.0 -- Agile Roles

The system must support four Agile roles: Product Owner, Scrum Master, QA Engineer, Developer. Each role has a distinct system prompt defining its responsibilities.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-4.1** | **Role switcher** | A `.roomodes` file in the project root defines the four role prompts. The active role is switched by the human via a Roo Code configuration parameter. | Changing the "Roo Code Mode" in VS Code settings loads the corresponding role prompt. |
| **REQ-4.2** | **Product Owner role** | The Product Owner prompt must define the agent's responsibility for requirements elaboration, prioritization, and stakeholder communication. | The Product Owner agent produces a well-structured PRD from a human's raw idea. |
| **REQ-4.3** | **Scrum Master role** | The Scrum Master prompt must define the agent's responsibility for process facilitation, ceremony scheduling, and impediment removal. | The Scrum Master agent identifies blockers and suggests concrete removal actions. |
| **REQ-4.4** | **QA Engineer role** | The QA Engineer prompt must define the agent's responsibility for test strategy, acceptance criteria, and quality gates. | The QA Engineer agent produces a test plan from a user story with given acceptance criteria. |
| **REQ-4.5** | **Developer role** | The Developer prompt must define the agent's responsibility for implementation, code quality, and technical debt management. | The Developer agent implements a feature branch from a user story with acceptance criteria. |

---

### 2.6 Domain 5 -- Security & Sovereignty (REQ-5.x)

#### REQ-5.0 -- Network Isolation

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-5.1** | **Tailscale network** | The laptop `pc` and server `calypso` must be connected via Tailscale, forming a private network. | `ping calypso` from `pc` resolves to a Tailscale IP address (100.x.x.x). |
| **REQ-5.2** | **No exposure to public internet** | Ollama on `calypso` must be configured to listen only on the Tailscale IP, not on all interfaces. | `curl http://calypso:11434` from `pc` succeeds; `curl http://0.0.0.0:11434` from an external network fails. |
| **REQ-5.3** | **API key isolation** | The Gemini API key must never be committed to Git or stored in files outside `memory-bank/`. | `.gitignore` excludes `.env`; `git log` on `.env` files returns empty. |

---

## 3. v2.1 Requirements

### 3.1 Anthropic Claude API Integration (REQ-6.x)

v2.1 introduced direct Anthropic Claude API integration as a third LLM backend option.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-6.1** | **Claude API direct access** | The system must support direct API access to Anthropic's Claude models (Claude 3.5 Sonnet) via the proxy. | Roo Code can make requests to `localhost:8080/v1/chat/completions` with `claude-3-5-sonnet-20241022` model and receive valid responses. |
| **REQ-6.2** | **API key management** | Claude API key must be stored in `.env` and loaded by the proxy at startup. | Proxy logs confirm Claude API key is loaded without exposing the key value. |
| **REQ-6.3** | **OpenRouter abstraction** | OpenRouter is used as the unified gateway for Claude access, providing fallback and routing. | Requests to OpenRouter API succeed with valid credentials. |

### 3.2 GitHub Actions CI/CD (REQ-7.x)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-7.1** | **Prompt coherence check** | A GitHub Actions workflow must verify that all system prompts (SP-001 through SP-007) remain coherent with their source files. | Push to `develop` triggers coherence check; failure blocks merge. |
| **REQ-7.2** | **Canonical docs enforcement** | A GitHub Actions workflow must enforce cumulative and coherent canonical docs per release. | CI checks that DOC-*-CURRENT.md pointers are consistent and DOC files meet minimum line counts. |

---

## 4. v2.2 Requirements

### 4.1 Memory Architecture (REQ-8.x)

v2.2 introduced the Hot/Cold memory architecture.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-8.1** | **Hot memory** | `memory-bank/hot-context/` contains active session files: `activeContext.md`, `progress.md`, `decisionLog.md`, `systemPatterns.md`, `productContext.md`. | All hot-context files exist and are regularly updated. |
| **REQ-8.2** | **Cold memory** | `memory-bank/archive-cold/` contains historical, infrequently accessed files organized by category. | Archive structure exists with `.gitkeep` for empty directories. |
| **REQ-8.3** | **Librarian Agent** | SP-010 defines the Librarian Agent responsible for archiving and indexing cold memory. | Librarian Agent can query cold archive via MCP tool. |

---

## 5. v2.3 Requirements

### 5.1 Anthropic Batch API Toolkit (REQ-9.x)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-9.1** | **Batch CLI** | `scripts/batch/cli.py` provides a CLI for submitting, retrieving, and polling batch jobs. | `python scripts/batch/cli.py --help` displays submit/retrieve/status/poll commands. |
| **REQ-9.2** | **Jinja2 templates** | Batch scripts are generated from Jinja2 templates in `scripts/batch/templates/`. | Templates produce valid Python scripts for batch submission/retrieval. |
| **REQ-9.3** | **Config management** | `scripts/batch/config.py` provides `BatchConfig` dataclass and YAML configuration. | Config loads from `config.yaml` without hardcoded values. |

### 5.2 Governance Refinements (REQ-10.x)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-10.1** | **Ideation intake** | RULE 11 mandates routing off-topic inputs to the Orchestrator Agent. | Any agent can route an idea to the intake process. |
| **REQ-10.2** | **Sync detection** | RULE 12 mandates checking for parallel work before implementation. | SyncDetector identifies overlapping file changes. |
| **REQ-10.3** | **DOC-3 execution tracking** | RULE 13 mandates live execution tracking in DOC-3. | DOC-3 execution chapter is updated at end of each session. |

---

## 6. v2.4 Requirements

### 6.1 Calypso Orchestration (REQ-11.x)

v2.4 introduced the Calypso Orchestration tier for multi-agent coordination.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-11.1** | **Phase 2: Expert Reports** | Calypso Phase 2 generates expert reports for each backlog item. | 4 expert reports generated and stored in `src/calypso/schemas/`. |
| **REQ-11.2** | **Phase 3: Triage** | Calypso Phase 3 applies triage classification to backlog items. | 20 backlog items classified with status and priority. |
| **REQ-11.3** | **Phase 4: Orchestration** | Calypso Phase 4 executes the orchestration workflow. | 20/20 items processed (12 GREEN, 8 ORANGE). |
| **REQ-11.4** | **FastMCP server** | `src/calypso/fastmcp_server.py` provides MCP tools for Calypso operations. | MCP server starts and registers all tools. |
| **REQ-11.5** | **Global Brain** | ChromaDB-based vector store indexes cold archive for semantic search. | Librarian Agent can query cold archive via `memory:query()`. |

### 6.2 Agent System Prompts (REQ-12.x)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-12.1** | **Synthesizer Agent** | SP-008 defines the Synthesizer Agent for cross-expert synthesis. | Synthesizer produces consolidated analysis from multiple expert reports. |
| **REQ-12.2** | **Devil's Advocate Agent** | SP-009 defines the Devil's Advocate Agent for critical review. | DAA identifies weaknesses and risks in proposals. |
| **REQ-12.3** | **Librarian Agent** | SP-010 defines the Librarian Agent for memory archive management. | Librarian can archive and query cold memory. |

---

## 7. v2.5 Requirements

### 7.1 Canonical Docs GitFlow Enforcement (REQ-13.x)

v2.5 introduces ADR-012: Canonical Docs Cumulative + GitFlow Enforcement.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-13.1** | **Cumulative docs** | All canonical docs (DOC-1 through DOC-5) must be cumulative, containing complete state from all previous releases. | Each release doc in `docs/releases/vX.Y/` meets minimum line count (DOC-1: 500+, DOC-2: 500+, DOC-3: 300+, DOC-4: 300+, DOC-5: 200+). |
| **REQ-13.2** | **GitFlow enforcement** | RULE 12 (CANON) enforces canonical docs workflow: feature branches, no direct commits to frozen folders. | Pre-receive hook at `.githooks/pre-receive` rejects non-compliant pushes. |
| **REQ-13.3** | **CI validation** | GitHub Actions workflow at `.github/workflows/canonical-docs-check.yml` validates doc coherence. | CI passes on PR to `develop-vX.Y` with consistent DOC pointers. |
| **REQ-13.4** | **DOC-*-CURRENT.md consistency** | All five `DOC-*-CURRENT.md` pointer files must point to the same release version. | CI check confirms all five files reference the same vX.Y version. |

### 7.2 Squash Merge Prohibition (REQ-14.x)

v2.5 introduces ADR-013: Squash Merge Prohibition for traceability.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-14.1** | **No squash merges** | RULE 10.3 forbids squash merges to preserve full commit history on feature branches. | Feature branches retain complete commit history after merge. |
| **REQ-14.2** | **No branch deletion** | RULE 10.3 item 6 forbids `--delete-branch` when merging PRs. | All merged feature branches remain in the repository for traceability. |
| **REQ-14.3** | **Fast-forward preferred** | RULE 10.3 prefers fast-forward or regular merge over squash. | Merge strategy documented and enforced in `.clinerules`. |

---

## 8. All Previous Workflows Preserved

All workflows and processes defined in v1.0 through v2.4 remain valid and are not superseded by this document unless explicitly noted.

---

*End of DOC-1-v2.5-PRD.md*
