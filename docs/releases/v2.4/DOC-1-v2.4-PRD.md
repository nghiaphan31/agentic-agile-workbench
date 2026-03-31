---
doc_id: DOC-1
release: v2.4
status: Draft
title: Product Requirements Document
version: 1.0
date_created: 2026-03-30
authors: [Architect mode, Human]
previous_release: none
cumulative: true
---

# DOC-1 — Product Requirements Document (v2.4)

> **Status: DRAFT** -- This document is in draft for v2.4.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** — This document contains all requirements from v1.0 through v2.4.
> To understand the full project requirements, read this document from top to bottom.
> Do not rely on previous release documents — they are delta-based and incomplete.

---

## Table of Contents

1. [Context and Strategic Vision](#1-context-and-strategic-vision)
2. [v1.0 Requirements](#2-v10-requirements)
3. [v2.1 Requirements](#3-v21-requirements)
4. [v2.2 Requirements](#4-v22-requirements)
5. [v2.3 Requirements](#5-v23-requirements)
6. [v2.4 Requirements](#6-v24-requirements)
7. [All Previous Workflows Preserved](#7-all-previous-workflows-preserved)

---

## 1. Context and Strategic Vision

This PRD synthesizes two complementary sources of inspiration:

1. **The LAAW Blueprint (mychen76)**: A local, sovereign agentic development environment, orchestrated by specialized AI agents with persistent memory and Agile rituals.
2. **The Gemini Chrome Proxy**: A network-clipboard bridge mechanism allowing Roo Code to leverage the power of Gemini Web for free via minimal human intervention (copy-paste).

The objective is to define a **unified and enriched** system that combines the local sovereignty of LAAW with the flexibility of a hybrid LLM backend (local Ollama OR Gemini Chrome via proxy OR Claude Sonnet via direct API), while maintaining Agile rigor and contextual memory persistence.

---

## 2. v1.0 Requirements

### 2.1 Foundational Requirement (REQ-000)

> **REQ-000 — Root Requirement of the Unified System**
>
> The overall system must provide an operational agentic development environment on a Windows laptop (`pc`) with VS Code, relying on a dedicated headless Linux server (`calypso`) for local LLM inference, both machines connected via Tailscale. The system must be capable of:
> - Orchestrating specialized AI agents according to Agile roles (Product Owner, Scrum Master, QA Engineer, Developer)
> - Maintaining absolute context continuity between sessions via persistent memory in auditable Markdown files
> - Executing complex development tasks relying on a **switchable** LLM backend: either a local model (Ollama on `calypso` via Tailscale) for total sovereignty, or Gemini Chrome via a local API proxy for free cloud power, or Claude Sonnet via direct Anthropic API for full automation
> - Ensuring that Roo Code remains the central agentic execution engine in all three operating modes, without modification of its native behavior

---

### 2.2 Domain 1 — Agentic Engine & Foundation Models (REQ-1.x)

#### REQ-1.0 — Local LLM Inference Capability

The system must be capable of executing LLM inferences on the private local network (Tailscale), via Ollama installed on the Linux server `calypso` (RTX 5060 Ti 16 GB). The Ollama API is accessible from the laptop `pc` at `http://calypso:11434` via the Tailscale network.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-1.1** | **Main model optimized for Tool Calling** | The Ollama model used as the main agent must be `mychen76/qwen3_cline_roocode:14b`, specifically fine-tuned for Roo Code tool calling. | The agent emits valid JSON requests to the Roo Code API without syntax or formatting errors on 10 consecutive test requests. |
| **REQ-1.2** | **Minimum context window of 128K tokens** | The `num_ctx` parameter in the Ollama Modelfile must be configured to exactly `131072` (128K tokens). | `ollama show uadf-agent --modelfile` displays `PARAMETER num_ctx 131072`. |
| **REQ-1.3** | **Inference determinism** | Generation parameters must be locked in the Modelfile: `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`. These values cannot be modified at runtime. | `ollama show uadf-agent --modelfile` displays the 4 parameters with the exact values above. |
| **REQ-1.4** | **Boomerang Tasks delegation** | The system must allow the main agent (14B) to delegate sub-tasks to a lightweight secondary model (`qwen3:8b`) via Roo Code's "Boomerang Tasks" workflow. | The 14B agent can create a Boomerang sub-task, the 8B model executes it, and the result is returned to the 14B agent without human intervention. |

---

### 2.3 Domain 2 — Hybrid LLM Backend & Gemini Chrome Proxy (REQ-2.x)

#### REQ-2.0 — LLM Backend Switchability

The system must allow the user to switch Roo Code's LLM backend between three modes (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) by modifying only the "API Provider" parameter in Roo Code settings, without modifying Roo Code's behavior or the Memory Bank structure.

##### REQ-2.1 — Sub-domain: Local Proxy Server (Interception)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.1.1** | **Local FastAPI server on localhost:8000** | A local Python web server (FastAPI + uvicorn) must listen on `localhost:8000`. It must start in less than 3 seconds after executing `python proxy.py`. | `Invoke-WebRequest http://localhost:8000/health` returns HTTP 200 with `{"status":"ok"}` within 3 seconds of startup. |
| **REQ-2.1.2** | **Exact emulation of OpenAI Chat Completions format** | The proxy must expose the `POST /v1/chat/completions` and `GET /v1/models` endpoints in OpenAI format. | Roo Code configured in "OpenAI Compatible" mode with `Base URL: http://localhost:8000/v1` must connect without error. |
| **REQ-2.1.3** | **Separate extraction of system prompt and user prompt** | The proxy must parse the `messages` array and extract separately: (a) the `system` role message, (b) `user` role messages, (c) `assistant` role messages. | For a `messages` array of 10 elements, the 3 categories are correctly identified and separated. |
| **REQ-2.1.4** | **"Dedicated Gem" mode: system prompt filtering** | When `USE_GEM_MODE=true` (default), the proxy must omit the `system` role message when copying to the clipboard. | With `USE_GEM_MODE=true`, the text copied to the clipboard contains no content from the `system` message. |
| **REQ-2.1.5** | **Cleaning of base64 content (images)** | The proxy must detect any `content` element of type `array` containing `{"type": "image_url", ...}` objects and replace them with: `[IMAGE OMITTED - Not supported by clipboard proxy]`. | A request containing a base64 image is processed without error. |

##### REQ-2.2 — Sub-domain: Clipboard Transfer (Uplink)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.2.1** | **Injection into Windows clipboard in less than 500ms** | After receiving the request from Roo Code, the proxy must copy the formatted text to the Windows system clipboard via `pyperclip.copy()`. | The delay between receiving the HTTP request and the text being available in the clipboard is less than 500ms. |
| **REQ-2.2.2** | **Readable format with explicit separators** | The text copied to the clipboard must use: `[SYSTEM PROMPT]\n{content}` (if `USE_GEM_MODE=false`), `[USER]\n{content}`, `[ASSISTANT]\n{content}`. Sections separated by `\n\n---\n\n`. | A human can visually identify the system/user/assistant sections in the clipboard in less than 5 seconds. |
| **REQ-2.2.3** | **Timestamped console notification** | The proxy must display: (a) time in `HH:MM:SS`, (b) prompt size in characters, (c) 5 numbered action instructions, (d) remaining timeout delay. | The console displays these 4 elements for each request received. |

##### REQ-2.3 — Sub-domain: Response Wait and Capture (Downlink)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.3.1** | **Asynchronous clipboard polling every second** | The proxy must monitor the clipboard via an `asyncio` loop with `await asyncio.sleep(POLLING_INTERVAL)` (default: 1.0 second). The loop must not block the main FastAPI thread. | During polling, the FastAPI server still responds to `GET /health` without delay. |
| **REQ-2.3.2** | **Change detection by MD5 hash comparison** | The proxy must calculate `MD5(initial_copied_content)` at the time of copying, then compare with `MD5(current_clipboard_content)` at each polling iteration. | Detection occurs within 2 seconds of the user copying the Gemini response. |
| **REQ-2.3.3** | **Configurable timeout with HTTP 408 response** | If no clipboard change is detected within `TIMEOUT_SECONDS` (default: 300 seconds), the proxy must return HTTP 408 with: `"Timeout: Relancez votre requete dans Roo Code."` | With `TIMEOUT_SECONDS=5`, the proxy returns HTTP 408 after 5 seconds. |
| **REQ-2.3.4** | **Validation of Roo Code XML tag presence** | After detecting a clipboard change, the proxy must verify the presence of at least one Roo Code XML tag (`<write_to_file>`, `<execute_command>`, `<attempt_completion>`, etc.). If no tag is present, a warning is displayed (non-blocking). | With a valid Gemini response, no warning. With text without XML tags, the warning is displayed but the response is still transmitted. |

##### REQ-2.4 — Sub-domain: Re-injection to Roo Code

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.4.1** | **SSE streaming support in a single chunk** | The proxy must detect if the request contains `"stream": true` and return SSE format with: (1) content chunk, (2) end chunk with `finish_reason: "stop"`, (3) `data: [DONE]`. If `stream: false`, return complete non-streamed JSON. | Both streaming and non-streaming modes work correctly with Roo Code. |
| **REQ-2.4.2** | **Complete OpenAI JSON format for non-streamed response** | The non-streamed JSON response must contain: `id` (format `chatcmpl-proxy-{8 hex chars}`), `object`, `created`, `model`, `choices[0].index` (0), `choices[0].message.role` ("assistant"), `choices[0].message.content`, `choices[0].finish_reason` ("stop"), `usage` (all zeros). | The JSON response is parseable by Roo Code without deserialization error. |
| **REQ-2.4.3** | **HTTP 200 response with correct Content-Type** | HTTP 200 OK with `Content-Type: application/json` for non-streamed, `Content-Type: text/event-stream` for SSE. | Response headers are correct in both modes. |
| **REQ-2.4.4** | **Complete preservation of Gemini content** | The content of the Gemini response (including Roo Code XML tags) must be transmitted as-is in `choices[0].message.content`, without any modification. | The content is identical (byte-for-byte) to the content copied from Gemini. |

---

### 2.4 Domain 3 — Agility & Role Segregation (REQ-3.x)

#### REQ-3.0 — Virtual Agile Team

The system must simulate a complete Scrum team via Roo Code Custom Modes, each with distinct and non-overlapping responsibilities, behaviors, and access permissions.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-3.1** | **Product Owner Mode** | A `.roomodes` entry with `slug: product-owner`. Restricted to: (a) reading files in `docs/`, `memory-bank/`, and `prompts/`, (b) writing to `memory-bank/productContext.md`, `memory-bank/decisionLog.md`, and `docs/releases/`. Unable to read or write to `src/`. | Switching to Product Owner mode and attempting to read `src/hello.py` returns an access denied error. |
| **REQ-3.2** | **Scrum Master Mode** | A `.roomodes` entry with `slug: scrum-master`. Restricted to: (a) reading all files, (b) writing to `docs/qa/`, `memory-bank/activeContext.md`, and `memory-bank/progress.md`. Unable to write to `src/` or modify `memory-bank/projectBrief.md`. | Switching to Scrum Master mode and attempting to write to `src/hello.py` returns an access denied error. |
| **REQ-3.3** | **Developer Mode** | A `.roomodes` entry with `slug: developer`. Restricted to: (a) reading and writing to `src/` exclusively, (b) reading `docs/releases/`, `memory-bank/`, and `prompts/`. Unable to write to `memory-bank/` files (only `read` allowed). | Switching to Developer mode and attempting to write to `memory-bank/activeContext.md` returns an access denied error. Writing to `src/hello.py` succeeds. |
| **REQ-3.4** | **QA Engineer Mode** | A `.roomodes` entry with `slug: qa-engineer`. Restricted to: (a) reading all files in `src/`, `docs/`, `memory-bank/`, and `prompts/`, (b) writing to `docs/qa/` exclusively. Unable to write to `src/`, `memory-bank/`, or `prompts/`. | Switching to QA Engineer mode and attempting to write to `src/hello.py` returns an access denied error. Writing to `docs/qa/QA-REPORT.md` succeeds. |

#### REQ-3.5 — Agile Ceremony Support

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-3.5.1** | **Sprint Planning** | In Scrum Master mode, the agent must be capable of generating a sprint backlog from `memory-bank/productContext.md`. | A prompt "plan a sprint" in Scrum Master mode produces a sprint backlog document in `docs/releases/vX.Y/`. |
| **REQ-3.5.2** | **Daily Standup** | In Scrum Master mode, the agent must be capable of generating a daily standup summary by reading `memory-bank/activeContext.md` and `memory-bank/progress.md`. | A prompt "daily standup" in Scrum Master mode produces a summary of what was done, what will be done, and blockers. |

---

### 2.5 Domain 4 — Persistent Memory & Versioning (REQ-4.x)

#### REQ-4.0 — Memory Bank as Single Source of Truth

The Memory Bank (7 `.md` files in `memory-bank/`) is the **single source of truth** for all project context.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-4.1** | **Memory Bank directory structure** | The `memory-bank/` directory must contain exactly 7 files: `projectBrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`, `decisionLog.md`. | All 7 files exist. Each file's first line is a heading that matches its filename. |
| **REQ-4.2** | **Session Start: Mandatory Read** | At the start of every session, every agent must read ALL 7 Memory Bank files before taking any action. The CHECK→CREATE→READ→ACT sequence is mandatory. | Attempting to take any action before reading all 7 files produces a reminder message. |
| **REQ-4.3** | **Session End: Mandatory Write** | Before closing any session (before `attempt_completion`), every agent must update: `memory-bank/activeContext.md` and `memory-bank/progress.md`. | Closing a session without updating these files produces a warning. |
| **REQ-4.4** | **Git versioning** | Every modification to `memory-bank/` must be committed to Git with a meaningful commit message. The pre-commit hook must verify that `memory-bank/` modifications are committed before allowing the commit. | A direct `git commit` of a `memory-bank/` modification without adding the file to staging produces an error. |
| **REQ-4.5** | **File format: Human-readable Markdown** | All Memory Bank files must be written in Markdown format. No binary formats, no JSON, no YAML. | Opening any Memory Bank file in a text editor displays formatted Markdown. |

---

### 2.6 Domain 5 — Gemini Chrome Integration (REQ-5.x)

#### REQ-5.0 — Gemini Chrome as Free Cloud LLM

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-5.1** | **Dedicated Gem Profile** | A Gemini Gem named "Roo Code Agent" must be configured with a system prompt that positions Gemini as an expert developer assistant. | The Gem is accessible at gemini.google.com > Gems. |
| **REQ-5.2** | **Clipboard-only data transfer** | All data transfer between Roo Code and Gemini Chrome must occur via the Windows clipboard. No network connections, no browser automation. | A network trace during a proxy-mode session shows no connections to Google servers from Roo Code. |
| **REQ-5.3** | **5-step action protocol** | The proxy must display 5 numbered action instructions after each request, guiding the user through the copy-paste flow. | The console output after each request displays 5 numbered steps. |

---

### 2.7 Domain 6 — Claude API Direct Mode (REQ-6.x)

#### REQ-6.0 — Anthropic Claude API as Fully Automated Backend

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-6.1** | **Native Anthropic Provider** | Roo Code must be configurable with the "Anthropic" provider and API key. The connection must be direct HTTPS to `api.anthropic.com`, with no intermediate proxy. | Roo Code in Anthropic mode successfully executes a task without any clipboard interaction. |
| **REQ-6.2** | **Model: claude-sonnet-4-6** | The Claude Sonnet 4 model must be used for all direct API calls. | API logs show `claude-sonnet-4-6` as the model for all requests. |
| **REQ-6.3** | **Streaming support** | The direct API connection must support streaming mode (`"stream": true`) identical to the Ollama backend. | Roo Code configured for streaming with Anthropic provider receives streaming responses without error. |
| **REQ-6.4** | **Tool calling compatibility** | The Anthropic API connection must support Roo Code's XML tool calling format natively. | A series of 10 tool calls via the Anthropic API succeeds with correct JSON formatting. |

---

### 2.8 Domain 7 — Prompt Registry (REQ-7.x)

#### REQ-7.0 — Centralized System Prompt Management

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-7.1** | **Prompts directory structure** | The `prompts/` directory must contain: `README.md` (index), `SP-001` through `SP-007`. | All 8 files exist. |
| **REQ-7.2** | **YAML front matter** | Each SP file must contain YAML front matter with: `doc_id`, `version`, `date_created`, `authors`, `purpose`. | Each SP file begins with a YAML block that can be parsed. |
| **REQ-7.3** | **Deployment verification** | A `check-prompts-sync.ps1` script must verify that each deployed artifact exactly matches the corresponding canonical SP in `prompts/`. | Running `check-prompts-sync.ps1` produces a report: X PASS, Y FAIL, Z WARN. |
| **REQ-7.4** | **Pre-commit hook** | The `check-prompts-sync.ps1` script must run automatically on every `git commit` via a Git hook. If any SP fails, the commit is blocked. | A commit with a modified `.clinerules` that diverges from `SP-002` is blocked by the pre-commit hook. |
| **REQ-7.5** | **SP-007 external deployment** | SP-007 (Gem Gemini) must be manually deployed to gemini.google.com > Gems. A warning is displayed if the deployed Gem version differs from the canonical. | The pre-commit hook reports SP-007 status as WARN (manual deployment required). |

---

### 2.9 Domain 8 — Validation & Testing (REQ-8.x)

#### REQ-8.0 — End-to-End Validation

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-8.1** | **Self-contained Git test** | A test that initializes a new Git repository, makes a commit, and verifies the pre-commit hook runs and passes — all without network access. | The test completes in < 30 seconds and reports PASS. |
| **REQ-8.2** | **Proxy mode end-to-end test** | A test that sends a request to the proxy, simulates clipboard copy-paste, and verifies the response is correctly formatted. | The test completes in < 60 seconds and reports PASS. |
| **REQ-8.3** | **Memory Bank integrity test** | A test that verifies all 7 Memory Bank files are readable, have valid Markdown headers, and satisfy size constraints. | The test reports: 7/7 files valid. |
| **REQ-8.4** | **LLM backend switch test** | A test that switches between all 3 LLM backends and verifies connectivity for each. | All 3 backends report CONNECTED within 10 seconds each. |

---

## 3. v2.1 Requirements

### 3.1 Overview

v2.1 is a **production hotfix release** addressing two critical quality concerns:

1. **LLM backend resilience** -- OpenRouter MinMax M2.7 as default with Claude fallback
2. **System prompt coherence** -- `.clinerules` and `SP-002` synchronization fixes

### 3.2 Scope of v2.1

| IDEA | Title | Type | Status |
|------|-------|------|--------|
| IDEA-008 | OpenRouter MinMax M2.7 as default LLM + Claude fallback | feat | [IMPLEMENTED] |
| SP-002 Coherence | .clinerules content corruption fixes | fix | [IMPLEMENTED] |
| ADR-005 | GitFlow enforcement (RULE 10) | chore | [IMPLEMENTED] |

### 3.3 IDEA-008: OpenRouter MinMax M2.7 as Default LLM

**Solution:** OpenRouter provides access to MinMax M2.7 as a default LLM backend with automatic Claude Sonnet fallback:

```
Default:  minimax/minimax-m2.7  (via OpenRouter)
Fallback: claude-sonnet-4-6     (after 3 consecutive errors)
```

### 3.4 RULE 10 — GitFlow Enforcement (ADR-006)

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `main` | Production state — frozen after each release tag | Never commit directly after tag |
| `develop` | Wild mainline — ad-hoc features, experiments, quick fixes | Long-lived, base for `develop-vX.Y` |
| `develop-vX.Y` | Scoped backlog — formal release scope | Created at release planning |
| `feature/{slug}` | Single feature or fix | Branch from `develop` or `develop-vX.Y` |
| `hotfix/vX.Y.Z` | Emergency production fix | Branch from production tag, merge to main + develop |

### 3.5 SP-002 Coherence Fix (v2.1)

The `.clinerules` file suffered from encoding corruption (em-dash mojibake, BOM bytes). The fix:
- Rewrote `.clinerules` with correct UTF-8 encoding
- Synchronized with `prompts/SP-002-clinerules-global.md`
- Pre-commit hook validates coherence on every commit

---

## 4. v2.2 Requirements

### 4.1 Overview

v2.2 is a **memory-bank hygiene release** — corrections and governance compliance.

**No new features.** All v1.0 and v2.1 functionality is preserved unchanged.

### 4.2 Scope of v2.2

| Item | Type | Status |
|------|------|--------|
| v2.1 backlog accuracy corrections | docs | [IMPLEMENTED] |
| DOC6 revision close (RULE 8.3) | docs | [IMPLEMENTED] |
| activeContext hygiene | docs | [IMPLEMENTED] |
| v2.1 canonical docs (retroactive) | docs | [IMPLEMENTED] |

---

## 5. v2.3 Requirements

### 5.1 Overview

v2.3 is a **minor release** capturing:
1. **IDEA-009** — Generic Anthropic Batch API Toolkit (developer tooling, ad-hoc)
2. **IDEA-011** — SP-002 Coherence Fix (bug fix, ad-hoc)

### 5.2 Scope of v2.3

| IDEA | Title | Type | Tier | Status |
|------|-------|------|------|--------|
| IDEA-009 | Generic Anthropic Batch API Toolkit | dev-tooling | Minor | [IMPLEMENTED] |
| IDEA-011 | SP-002 Coherence Fix | fix | Minor | [IMPLEMENTED] |

### 5.3 IDEA-009: Generic Anthropic Batch API Toolkit

**Package:** `scripts/batch/`

| Module | Purpose |
|--------|---------|
| `config.py` | BatchConfig dataclass + YAML loader with validation |
| `submit.py` | Batch submission with ANTHROPIC_API_KEY validation |
| `retrieve.py` | Result retrieval with markdown fence stripping + raw fallback |
| `poll.py` | Polling utility with interval support and request_counts display |
| `cli.py` | CLI: submit / retrieve / status / poll commands |
| `generate.py` | Jinja2-based script generator from batch.yaml |

**Template Bundle:** `template/scripts/batch/` — self-contained copy for new project deployment.

**CLI Usage:**
```bash
python -m scripts.batch.cli submit batch.yaml
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60
python -m scripts.batch.cli status batch.yaml
```

**Requirements:** Python 3.11+, `anthropic>=0.49.0`, `jsonschema>=4.23.0`, `jinja2>=3.1.0`, `pyyaml>=6.0`

### 5.4 IDEA-011: SP-002 Coherence Fix

**Issues Fixed:**
- UTF-8 BOM at start of file
- Latin-1 mojibake (em-dash → Ã©, arrow → â†', etc.)
- Literal `\n` in RULE 10 instead of real newlines
- Double embedding of SP-002 in itself

**Prevention:** Enhanced `scripts/check-prompts-sync.ps1` with BOM/mojibake/literal-\n detection.

---

## 6. v2.4 Requirements

### 6.1 Overview

v2.4 is a **minor release** capturing **IDEA-012**: **Ideation-to-Release Governance Pipeline** (Calypso Orchestration v1).

This release formalizes the full ideation-to-release pipeline with:
- **SyncDetector** (parallel work detection)
- **BranchTracker** (GitFlow compliance)
- **ExecutionTracker** (live progress tracking)
- **IntakeAgent** (structured idea intake)
- **IdeasDashboard** (centralized backlog management)

### 6.2 Scope of v2.4

| IDEA | Title | Type | Tier | Status |
|------|-------|------|------|--------|
| IDEA-012 | Ideation-to-Release Governance Pipeline | feature | Minor | [IMPLEMENTED] |

### 6.3 IDEA-012: Ideation-to-Release Governance Pipeline

#### Problem Statement

The current ideation process lacks:
- **Structured intake**: Ideas are captured ad-hoc without classification or routing.
- **Sync detection**: Parallel work is not detected, leading to merge conflicts and redundant effort.
- **Branch governance**: GitFlow compliance is manual and error-prone.
- **Execution tracking**: Progress is not tracked in real-time, leading to blind spots.
- **Backlog management**: Ideas are scattered across documents, making prioritization difficult.

#### Solution

**Calypso Orchestration v1** — A full ideation-to-release pipeline with:

| Component | Purpose | Location |
|-----------|---------|----------|
| **IntakeAgent** | Structured idea intake with classification (BUSINESS/TECHNICAL) and routing to the correct backlog. | `src/calypso/intake_agent.py` |
| **SyncDetector** | Detects parallel work and sync opportunities (CONFLICT, REDUNDANCY, DEPENDENCY, SHARED_LAYER, NO_OVERLAP). | `src/calypso/sync_detector.py` |
| **BranchTracker** | Enforces GitFlow compliance (ADR-006) and tracks release progress. | `src/calypso/branch_tracker.py` |
| **ExecutionTracker** | Tracks live progress across all active ideas and releases. | `src/calypso/execution_tracker.py` |
| **IdeasDashboard** | Centralized backlog management with triage status and refinement tracking. | `src/calypso/ideas_dashboard.py` |

#### Key Features

1. **Structured Intake**
   - Ideas are classified as **BUSINESS** (WHAT) or **TECHNICAL** (HOW).
   - Business ideas route to `IDEAS-BACKLOG.md`.
   - Technical ideas route to `TECH-SUGGESTIONS-BACKLOG.md`.
   - Sync detection runs automatically at intake.

2. **Sync Detection**
   - Detects 5 sync categories: **CONFLICT**, **REDUNDANCY**, **DEPENDENCY**, **SHARED_LAYER**, **NO_OVERLAP**.
   - Prevents merge conflicts and redundant work.
   - Coordinates timing for shared components.

3. **Branch Governance**
   - Enforces GitFlow (ADR-006) with 3-branch model: `main`, `develop`, `develop-vX.Y`.
   - Tracks release progress and prevents forbidden actions (e.g., committing directly to `main`).
   - Coordinates feature branch merges to avoid conflicts.

4. **Execution Tracking**
   - Tracks live progress across all active ideas and releases.
   - Updates `DOC-3` execution chapter, `memory-bank/progress.md`, and `EXECUTION-TRACKER-vX.Y.md` in real-time.
   - Ensures consistency across all tracking documents.

5. **Backlog Management**
   - Centralized dashboard for all ideas with triage status (IDEA, REFINED, DEFERRED, IN_PROGRESS, COMPLETE).
   - Tracks refinement sessions and parked technical suggestions.

#### Requirements

- Python 3.11+
- `GitPython>=3.1.40` (for BranchTracker)
- `jsonschema>=4.23.0` (for intake validation)

#### CLI Usage

```bash
# Intake a new idea
python -m src.calypso.intake_agent "New feature request: Add dark mode support"

# Run sync detection
python -m src.calypso.sync_detector

# Check GitFlow compliance
python -m src.calypso.branch_tracker

# Track execution progress
python -m src.calypso.execution_tracker

# View ideas dashboard
python -m src.calypso.ideas_dashboard
```

#### Out of Scope for v2.4

- Multi-developer collaboration (planned for v2.5).
- Brownfield workflow (planned for v2.6).
- DOC6 revision (pending).

---

## 7. All Previous Workflows Preserved

All v1.0, v2.1, v2.2, and v2.3 features and workflows remain unchanged:

- Hot/Cold memory architecture
- Template folder enrichment
- Calypso orchestration scripts (Phase 2, 3, 4)
- Global Brain / Librarian Agent
- 4 Agile personas (.roomodes)
- Memory Bank (7 files in hot-context/)
- ADR-010 governance (two paths: structured vs ad-hoc)
- GitFlow branching model (ADR-006)
- 3-Mode LLM Switcher (Ollama, Gemini Proxy, Anthropic direct)
- Prompt Registry with pre-commit validation
- Anthropic Batch API Toolkit
- Ideation-to-Release Governance Pipeline

---

## Out of Scope for v2.4

- New Calypso phases beyond v1.
- Multi-developer collaboration features.
- Brownfield workflow.
- DOC6 revision.

---

## DOC-1 / DOC-2 Coherency (ADR-010)

Per ADR-010, this DOC-1 and the corresponding DOC-2 must be coherent:
- All requirements in DOC-1 have a corresponding architecture element in DOC-2
- All architecture elements in DOC-2 support a requirement in DOC-1
- No blind spots: anything not in DOC-1 is not required; anything not in DOC-2 is not architecture

---

*End of DOC-1 v2.4 — Cumulative (v1.0 through v2.4)*
