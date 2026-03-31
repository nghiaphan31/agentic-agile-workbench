---
doc_id: DOC-1
release: v2.3
status: Frozen
title: Product Requirements Document
version: 1.0
date_created: 2026-03-29
date_frozen: 2026-03-29
authors: [Architect mode, Human]
previous_release: none
cumulative: true
---

# DOC-1 — Product Requirements Document (v2.3)

> **Status: FROZEN** -- v2.3.0 release
> **Cumulative: YES** — This document contains all requirements from v1.0 through v2.3.
> To understand the full project requirements, read this document from top to bottom.
> Do not rely on previous release documents — they are delta-based and incomplete.

---

## Table of Contents

1. [Context and Strategic Vision](#1-context-and-strategic-vision)
2. [v1.0 Requirements](#2-v10-requirements)
3. [v2.1 Requirements](#3-v21-requirements)
4. [v2.2 Requirements](#4-v22-requirements)
5. [v2.3 Requirements](#5-v23-requirements)
6. [All Previous Workflows Preserved](#6-all-previous-workflows-preserved)

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
| **REQ-1.1** | **Main model optimized for Tool Calling** | The Ollama model used as the main agent must be `mychen76/qwen3_cline_roocode:32b`, specifically fine-tuned for Roo Code tool calling. No fallback model is planned — model availability on Ollama Hub is an installation precondition. | The agent emits valid JSON requests to the Roo Code API without syntax or formatting errors on 10 consecutive test requests. |
| **REQ-1.2** | **Minimum context window of 128K tokens** | The `num_ctx` parameter in the Ollama Modelfile must be configured to exactly `131072` (128K tokens). This value is non-negotiable: it allows simultaneous loading of the project source code AND the 7 Memory Bank files into the agent's context. | `ollama show uadf-agent --modelfile` displays `PARAMETER num_ctx 131072`. |
| **REQ-1.3** | **Inference determinism** | Generation parameters must be locked in the Modelfile to eliminate hallucinations during code generation: `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`. These values are fixed and cannot be modified by the user at runtime. | `ollama show uadf-agent --modelfile` displays the 4 parameters with the exact values above. |
| **REQ-1.4** | **Boomerang Tasks delegation** | The system must allow the main agent (32B) to delegate sub-tasks to a lightweight secondary model (`qwen3:7b`) via Roo Code's "Boomerang Tasks" workflow, then integrate the output into its own decision loop. | The 32B agent can create a Boomerang sub-task, the 7B model executes it, and the result is returned to the 32B agent without human intervention. |

---

### 2.3 Domain 2 — Hybrid LLM Backend & Gemini Chrome Proxy (REQ-2.x)

#### REQ-2.0 — LLM Backend Switchability

The system must allow the user to switch Roo Code's LLM backend between the three modes (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) by modifying only the "API Provider" parameter in Roo Code settings, without modifying Roo Code's behavior or the Memory Bank structure.

##### REQ-2.1 — Sub-domain: Local Proxy Server (Interception)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.1.1** | **Local FastAPI server on localhost:8000** | A local Python web server (FastAPI + uvicorn) must listen on `localhost:8000`. It must start in less than 3 seconds after executing `python proxy.py`. | `Invoke-WebRequest http://localhost:8000/health` returns HTTP 200 with `{"status":"ok"}` within 3 seconds of startup. |
| **REQ-2.1.2** | **Exact emulation of OpenAI Chat Completions format** | The proxy must expose the `POST /v1/chat/completions` and `GET /v1/models` endpoints in OpenAI format. Roo Code configured in "OpenAI Compatible" mode with `Base URL: http://localhost:8000/v1` must connect without error. | Roo Code sends a request to the proxy and receives a response without connection or format error messages. |
| **REQ-2.1.3** | **Separate extraction of system prompt and user prompt** | The proxy must parse the `messages` array from the JSON request and extract separately: (a) the `system` role message, (b) `user` role messages, (c) `assistant` role messages (history). This extraction must work even if the array contains a multi-turn history of N messages. | For a `messages` array of 10 elements (1 system + 4 user + 5 assistant), the 3 categories are correctly identified and separated. |
| **REQ-2.1.4** | **"Dedicated Gem" mode: system prompt filtering** | When the environment variable `USE_GEM_MODE=true` (default value), the proxy must omit the `system` role message when copying to the clipboard. Only `user` and `assistant` messages are transmitted. | With `USE_GEM_MODE=true`, the text copied to the clipboard contains no content from the `system` message. The size reduction is measurable (≥ 50% for a standard Roo Code system prompt). |
| **REQ-2.1.5** | **Cleaning of base64 content (images)** | The proxy must detect any `content` element of type `array` containing `{"type": "image_url", ...}` objects and replace them with the exact literal string: `[IMAGE OMITTED - Not supported by clipboard proxy]`. | A request containing a base64 image is processed without error. The clipboard contains the replacement message instead of the image. |

##### REQ-2.2 — Sub-domain: Clipboard Transfer (Uplink)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.2.1** | **Injection into Windows clipboard in less than 500ms** | After receiving and processing the request from Roo Code, the proxy must copy the formatted text to the Windows system clipboard via `pyperclip.copy()`. | The delay between receiving the HTTP request and the text being available in the clipboard is less than 500ms (measured by `Get-Clipboard` immediately after). |
| **REQ-2.2.2** | **Readable format with explicit separators** | The text copied to the clipboard must use the following separators: `[SYSTEM PROMPT]\n{content}` (if `USE_GEM_MODE=false`), `[USER]\n{content}`, `[ASSISTANT]\n{content}`. Sections are separated by `\n\n---\n\n`. | A human can visually identify the system/user/assistant sections in the clipboard in less than 5 seconds. |
| **REQ-2.2.3** | **Timestamped console notification** | The proxy must display in the console: (a) the time in `HH:MM:SS` format, (b) the prompt size in characters, (c) the 5 numbered action instructions for the user, (d) the remaining timeout delay. | The console displays these 4 elements for each request received. |

##### REQ-2.3 — Sub-domain: Response Wait and Capture (Downlink)

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.3.1** | **Asynchronous clipboard polling every second** | The proxy must monitor the clipboard via an `asyncio` loop with `await asyncio.sleep(POLLING_INTERVAL)` (default: 1.0 second). The loop must not block the main FastAPI thread. | During polling, the FastAPI server still responds to `GET /health` without delay. |
| **REQ-2.3.2** | **Change detection by MD5 hash comparison** | The proxy must calculate `MD5(initial_copied_content)` at the time of copying, then compare with `MD5(current_clipboard_content)` at each polling iteration. Detection is triggered as soon as the two hashes differ. | Detection occurs within 2 seconds of the user copying the Gemini response (maximum 1 polling cycle). |
| **REQ-2.3.3** | **Configurable timeout with HTTP 408 response** | If no clipboard change is detected within the `TIMEOUT_SECONDS` delay (default: 300 seconds), the proxy must return an HTTP 408 (Request Timeout) response to Roo Code with the message: `"Timeout: Relancez votre requête dans Roo Code."` | With `TIMEOUT_SECONDS=5` (test), the proxy returns HTTP 408 after 5 seconds without user action. |
| **REQ-2.3.4** | **Validation of Roo Code XML tag presence** | After detecting a clipboard change, the proxy must verify the presence of at least one of the following Roo Code XML tags in the captured content: `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, `<ask_followup_question>`, `<replace_in_file>`, `<list_files>`, `<search_files>`, `<browser_action>`, `<new_task>`. If no tag is present, a warning is displayed in the console (non-blocking). | With a valid Gemini response, no warning. With text without XML tags, the warning is displayed but the response is still transmitted to Roo Code. |

##### REQ-2.4 — Sub-domain: Re-injection to Roo Code

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-2.4.1** | **SSE streaming support in a single chunk** | The proxy must detect if the request contains `"stream": true` and return a Server-Sent Events (SSE) format response with: (1) a content chunk, (2) an end chunk with `"finish_reason": "stop"`, (3) the `data: [DONE]` line. If `"stream": false`, return a complete non-streamed JSON response. | Roo Code configured with streaming enabled receives the response without error. Roo Code configured without streaming also receives the response without error. |
| **REQ-2.4.2** | **Complete OpenAI JSON format for non-streamed response** | The non-streamed JSON response must contain exactly the fields: `id` (format `chatcmpl-proxy-{8 hex chars}`), `object` (`"chat.completion"`), `created` (Unix timestamp), `model` (value of the `model` field from the request), `choices[0].index` (`0`), `choices[0].message.role` (`"assistant"`), `choices[0].message.content` (raw Gemini content), `choices[0].finish_reason` (`"stop"`), `usage.prompt_tokens` (`0`), `usage.completion_tokens` (`0`), `usage.total_tokens` (`0`). | The JSON response is parseable by Roo Code without deserialization error. |
| **REQ-2.4.3** | **HTTP 200 response with Content-Type application/json** | The HTTP response must have status 200 OK and the `Content-Type: application/json` header for the non-streamed response, or `Content-Type: text/event-stream` for the SSE response. | Response headers are correct in both modes. |
| **REQ-2.4.4** | **Complete preservation of Gemini content** | The content of the Gemini response (including Roo Code XML tags) must be transmitted as-is in `choices[0].message.content`, without any modification, deletion, addition, or character transformation. | The content in `choices[0].message.content` is identical (byte-for-byte) to the content copied from Gemini. |

---

### 2.4 Domain 3 — Agility & Role Segregation (REQ-3.x)

#### REQ-3.0 — Virtual Agile Team

The system must simulate a complete Scrum team via Roo Code Custom Modes, each with distinct and non-overlapping responsibilities, behaviors, and access permissions.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-3.1** | **Product Owner Mode** | A `.roomodes` entry with `slug: product-owner`. Its `roleDefinition` must restrict it to: (a) reading files in `docs/`, `memory-bank/`, and `prompts/`, (b) writing to `memory-bank/productContext.md`, `memory-bank/decisionLog.md`, and `docs/releases/`. It must be unable to read or write to `src/`. | Switching to Product Owner mode and attempting to read `src/hello.py` returns an access denied error. Attempting to write to `memory-bank/productContext.md` succeeds. |
| **REQ-3.2** | **Scrum Master Mode** | A `.roomodes` entry with `slug: scrum-master`. Its `roleDefinition` must restrict it to: (a) reading all files, (b) writing to `docs/qa/`, `memory-bank/activeContext.md`, and `memory-bank/progress.md`. It must be unable to write to `src/` or modify `memory-bank/projectBrief.md`. | Switching to Scrum Master mode and attempting to write to `src/hello.py` returns an access denied error. Writing to `docs/qa/QA-REPORT.md` succeeds. |
| **REQ-3.3** | **Developer Mode** | A `.roomodes` entry with `slug: developer`. Its `roleDefinition` must restrict it to: (a) reading and writing to `src/` exclusively, (b) reading `docs/releases/`, `memory-bank/`, and `prompts/`. It must be unable to write to `memory-bank/` files (only `read` allowed). | Switching to Developer mode and attempting to write to `memory-bank/activeContext.md` returns an access denied error. Writing to `src/hello.py` succeeds. |
| **REQ-3.4** | **QA Engineer Mode** | A `.roomodes` entry with `slug: qa-engineer`. Its `roleDefinition` must restrict it to: (a) reading all files in `src/`, `docs/`, `memory-bank/`, and `prompts/`, (b) writing to `docs/qa/` exclusively. It must be unable to write to `src/`, `memory-bank/`, or `prompts/`. | Switching to QA Engineer mode and attempting to write to `src/hello.py` returns an access denied error. Writing to `docs/qa/QA-REPORT.md` succeeds. |

#### REQ-3.5 — Agile Ceremony Support

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-3.5.1** | **Sprint Planning** | In Scrum Master mode, the agent must be capable of generating a sprint backlog from `memory-bank/productContext.md`, including: (a) prioritization of user stories by business value, (b) effort estimation, (c) sprint goal statement. | A prompt "plan a sprint" in Scrum Master mode produces a sprint backlog document in `docs/releases/vX.Y/`. |
| **REQ-3.5.2** | **Daily Standup** | In Scrum Master mode, the agent must be capable of generating a daily standup summary by reading `memory-bank/activeContext.md` and `memory-bank/progress.md`. | A prompt "daily standup" in Scrum Master mode produces a summary of: what was done yesterday, what will be done today, and blockers. |

---

### 2.5 Domain 4 — Persistent Memory & Versioning (REQ-4.x)

#### REQ-4.0 — Memory Bank as Single Source of Truth

The Memory Bank (7 `.md` files in `memory-bank/`) is the **single source of truth** for all project context. No information is stored outside these files. All LLM agents must read from and write to these files exclusively.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-4.1** | **Memory Bank directory structure** | The `memory-bank/` directory must contain exactly 7 files: `projectBrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`, `decisionLog.md`. Each file has a specific purpose documented in its header. | All 7 files exist. Each file's first line is a heading that matches its filename. |
| **REQ-4.2** | **Session Start: Mandatory Read** | At the start of every session, every agent (regardless of mode) must read ALL 7 Memory Bank files before taking any action. The CHECK→CREATE→READ→ACT sequence is mandatory. | Attempting to take any action (including asking questions) before reading all 7 files produces a reminder message. |
| **REQ-4.3** | **Session End: Mandatory Write** | Before closing any session (before `attempt_completion`), every agent must update: `memory-bank/activeContext.md` (current state), `memory-bank/progress.md` (checklist state). | Closing a session without updating these files produces a warning. |
| **REQ-4.4** | **Git versioning** | Every modification to `memory-bank/` must be committed to Git with a meaningful commit message. The pre-commit hook must verify that `memory-bank/` modifications are committed before allowing the commit. | A direct `git commit` of a `memory-bank/` modification without adding the file to staging produces an error. |
| **REQ-4.5** | **File format: Human-readable Markdown** | All Memory Bank files must be written in Markdown format, readable by humans without tooling. No binary formats, no JSON, no YAML. | Opening `memory-bank/activeContext.md` in a text editor displays formatted Markdown. |

---

### 2.6 Domain 5 — Gemini Chrome Integration (REQ-5.x)

#### REQ-5.0 — Gemini Chrome as Free Cloud LLM

The system must leverage Gemini Chrome (gemini.google.com) as a free cloud LLM backend via the clipboard proxy mechanism described in REQ-2.x.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-5.1** | **Dedicated Gem Profile** | A Gemini Gem named "Roo Code Agent" must be configured with a system prompt that positions Gemini as an expert developer assistant. The Gem ID must be stored in the Memory Bank. | The Gem is accessible at gemini.google.com > Gems. The system prompt is visible in the Gem settings. |
| **REQ-5.2** | **Clipboard-only data transfer** | All data transfer between Roo Code and Gemini Chrome must occur via the Windows clipboard. No network connections, no browser automation, no external services. | A network trace during a proxy-mode session shows no connections to Google servers from Roo Code. |
| **REQ-5.3** | **5-step action protocol** | The proxy must display 5 numbered action instructions after each request, guiding the user through the copy-paste flow: (1) Ctrl+A in Gemini response, (2) Ctrl+C to copy, (3) wait for proxy detection, (4) Ctrl+V in Roo Code, (5) verify response. | The console output after each request displays 5 numbered steps. |

---

### 2.7 Domain 6 — Claude API Direct Mode (REQ-6.x)

#### REQ-6.0 — Anthropic Claude API as Fully Automated Backend

The system must allow Roo Code to connect directly to the Anthropic Claude API for fully automated operation without human clipboard intervention.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-6.1** | **Native Anthropic Provider** | Roo Code must be configurable with the "Anthropic" provider and API key (`sk-ant-api03-...`). The connection must be direct HTTPS to `api.anthropic.com`, with no intermediate proxy. | Roo Code in Anthropic mode successfully executes a task without any clipboard interaction. |
| **REQ-6.2** | **Model: claude-sonnet-4-6** | The Claude Sonnet 4 model must be used for all direct API calls. | API logs show `claude-sonnet-4-6` as the model for all requests. |
| **REQ-6.3** | **Streaming support** | The direct API connection must support streaming mode (`"stream": true`) identical to the Ollama backend. | Roo Code configured for streaming with Anthropic provider receives streaming responses without error. |
| **REQ-6.4** | **Tool calling compatibility** | The Anthropic API connection must support Roo Code's XML tool calling format natively (no translation layer). | A series of 10 tool calls via the Anthropic API succeeds with correct JSON formatting. |

---

### 2.8 Domain 7 — Prompt Registry (REQ-7.x)

#### REQ-7.0 — Centralized System Prompt Management

All system prompts must be centralized in a `prompts/` directory with a strict synchronization discipline.

| ID | Requirement | Detailed Description | Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **REQ-7.1** | **Prompts directory structure** | The `prompts/` directory must contain: `README.md` (index), `SP-001-ollama-modelfile-system.md`, `SP-002-clinerules-global.md`, `SP-003-persona-product-owner.md`, `SP-004-persona-scrum-master.md`, `SP-005-persona-developer.md`, `SP-006-persona-qa-engineer.md`, `SP-007-gem-gemini-roo-agent.md`. | All 8 files exist. |
| **REQ-7.2** | **YAML front matter** | Each SP file must contain YAML front matter with: `doc_id`, `version`, `date_created`, `authors`, `purpose`. | Each SP file begins with a YAML block that can be parsed. |
| **REQ-7.3** | **Deployment verification** | A `check-prompts-sync.ps1` script must verify that each deployed artifact (`.roomodes`, `.clinerules`, `Modelfile`) exactly matches the corresponding canonical SP in `prompts/`. | Running `check-prompts-sync.ps1` produces a report: X PASS, Y FAIL, Z WARN. |
| **REQ-7.4** | **Pre-commit hook** | The `check-prompts-sync.ps1` script must run automatically on every `git commit` via a Git hook. If any SP fails, the commit is blocked. | A commit with a modified `.clinerules` that diverges from `SP-002` is blocked by the pre-commit hook. |
| **REQ-7.5** | **SP-007 external deployment** | SP-007 (Gem Gemini) must be manually deployed to gemini.google.com > Gems. The canonical source is `prompts/SP-007-gem-gemini-roo-agent.md`. A warning is displayed if the deployed Gem version differs from the canonical. | The pre-commit hook reports SP-007 status as WARN (manual deployment required). |

---

### 2.9 Domain 8 — Validation & Testing (REQ-8.x)

#### REQ-8.0 — End-to-End Validation

The system must include automated validation tests to verify all requirements are met.

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

This is not a feature release. The v1.0 workflow remains unchanged.

### 3.2 Scope of v2.1

| IDEA | Title | Type | Status |
|------|-------|------|--------|
| IDEA-008 | OpenRouter MinMax M2.7 as default LLM + Claude fallback | feat | [IMPLEMENTED] |
| SP-002 Coherence | .clinerules content corruption fixes | fix | [IMPLEMENTED] |
| ADR-005 | GitFlow enforcement (RULE 10) | chore | [IMPLEMENTED] |

### 3.3 IDEA-008: OpenRouter MinMax M2.7 as Default LLM

#### Problem Statement

The v1.0 system relied on local Ollama exclusively (Mode 1) or Gemini Chrome via clipboard (Mode 2). Neither is fully reliable for all use cases:
- Ollama requires the `calypso` server to be available on the Tailscale network
- Gemini Chrome requires manual clipboard intervention

#### Solution

OpenRouter provides access to MinMax M2.7 as a default LLM backend with automatic Claude Sonnet fallback:

```
Default:  minimax/minimax-m2.7  (via OpenRouter)
Fallback: claude-sonnet-4-6     (after 3 consecutive errors)
```

**Implementation:**
- OpenRouter API key configured in environment or `.env`
- LLM routing implemented in the agent configuration
- Automatic fallback triggered after 3 consecutive API errors
- All 3 original modes (Ollama, Gemini, Anthropic direct) remain available

### 3.4 RULE 10 — GitFlow Enforcement (ADR-005, ADR-006)

#### Branch Lifecycle

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `main` | Production state — frozen after each release tag | Never commit directly after tag |
| `develop` | Wild mainline — ad-hoc features, experiments, quick fixes | Long-lived, base for `develop-vX.Y` |
| `develop-vX.Y` | Scoped backlog — formal release scope | Created at release planning |
| `feature/{slug}` | Single feature or fix | Branch from `develop` or `develop-vX.Y` |
| `hotfix/vX.Y.Z` | Emergency production fix | Branch from production tag, merge to main + develop |

#### Forbidden Actions

- **NEVER** commit directly on `main` after a release tag
- **NEVER** commit on a branch that has been merged to `main`
- **NEVER** commit feature work directly on a release or main branch
- **ALL** new development MUST target `develop`, `develop-vX.Y`, or a feature branch

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

### 4.3 What Was Preserved

All v1.0 and v2.1 features and workflows remain unchanged:
- 3-Mode LLM Switcher (Ollama, Gemini Proxy, Anthropic direct)
- 4 Agile Personas (.roomodes)
- Memory Bank (7 files)
- Prompt Registry (prompts/ SP-001 to SP-007)
- Pre-commit hook (check-prompts-sync.ps1)
- GitFlow branching model (ADR-006)

---

## 5. v2.3 Requirements

### 5.1 Overview

v2.3 is a **minor release** capturing:
1. **IDEA-009** — Generic Anthropic Batch API Toolkit (developer tooling, ad-hoc)
2. **IDEA-011** — SP-002 Coherence Fix (bug fix, ad-hoc)

Both ideas emerged ad-hoc during the v2.3 coherence audit (IDEA-009) and ongoing operations (IDEA-011).

This release follows the [AD-HOC] lightweight process per [ADR-010](docs/ideas/ADR-010-dev-tooling-process-bypass.md).

### 5.2 Scope of v2.3

| IDEA | Title | Type | Tier | Status |
|------|-------|------|------|--------|
| IDEA-009 | Generic Anthropic Batch API Toolkit | dev-tooling | Minor | [IMPLEMENTED] |
| IDEA-011 | SP-002 Coherence Fix | fix | Minor | [IMPLEMENTED] |

### 5.3 IDEA-009: Generic Anthropic Batch API Toolkit

#### Problem Statement

During the v2.3 coherence audit, we submitted 3 batches to the Anthropic Batch API (BATCH1-GOVERNANCE, BATCH2-CROSSDOCS, BATCH3-TEMPLATE). The submission and retrieval process required multiple fixing cycles due to:
- API key friction (no validation before submission)
- No polling mechanism (manual status checks)
- JSON fence parsing issues (markdown fences around JSON responses)
- Inconsistent result types ("error" vs "errored")
- No structured batch_id persistence

These issues were solved ad-hoc during the audit. IDEA-009 extracts these lessons into a reusable toolkit.

#### Solution

A generic, reusable Python package for submitting and retrieving batches from the Anthropic Batch API:

**Package:** `scripts/batch/`

| Module | Purpose |
|--------|---------|
| `config.py` | BatchConfig dataclass + YAML loader with validation |
| `submit.py` | Batch submission with ANTHROPIC_API_KEY validation |
| `retrieve.py` | Result retrieval with markdown fence stripping + raw fallback |
| `poll.py` | Polling utility with interval support and request_counts display |
| `cli.py` | CLI: submit / retrieve / status / poll commands |
| `generate.py` | Jinja2-based script generator from batch.yaml |

**CLI Usage:**
```bash
python -m scripts.batch.cli submit batch.yaml
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60
python -m scripts.batch.cli status batch.yaml
```

**Template Bundle:** `template/scripts/batch/` — self-contained copy for new project deployment.

#### Requirements

- Python 3.11+
- `anthropic>=0.49.0`
- `jsonschema>=4.23.0`
- `jinja2>=3.1.0`
- `pyyaml>=6.0`

### 5.4 IDEA-011: SP-002 Coherence Fix

#### Problem Statement

SP-002 (.clinerules) consistently fails the pre-commit coherence check:
- **UTF-8 BOM** at start of file
- **Latin-1 mojibake** (em-dash → Ã©, arrow → â†', etc.)
- **Literal `\n`** in RULE 10 instead of real newlines
- **Double embedding** of SP-002 in itself

Root cause: files saved as UTF-8 but read through a Latin-1/Windows-1252 pipeline.

#### Solution

1. Investigate source vs deployment corruption
2. Fix SP-002 and template/SP-002: remove BOM, correct mojibake, fix literal \n
3. Add BOM/mojibake detection to pre-commit hook
4. Consolidate SP-002 double-embedding

#### Prevention

Enhanced `scripts/check-prompts-sync.ps1`:
- BOM detection (byte scan for EF BB BF)
- Mojibake pattern detection (Ã©, â†', â€œ, â€")
- Literal `\n` detection in rule content

---

## 6. All Previous Workflows Preserved

All v1.0, v2.1, and v2.2 features and workflows remain unchanged:

- Hot/Cold memory architecture
- Template folder enrichment
- Calypso orchestration scripts (Phase 2, 3, 4)
- Global Brain / Librarian Agent
- 4 Agile personas (.roomodes)
- Memory Bank (7 files in hot-context/)
- ADR-010 governance (two paths: structured vs ad-hoc)
- GitFlow branching model (ADR-006)
- 3-Mode LLM Switcher
- Prompt Registry with pre-commit validation
- Anthropic Batch API Toolkit

---

## Out of Scope for v2.3

- New Calypso phases
- Multi-developer collaboration features
- Brownfield workflow
- DOC6 revision (still pending)

---

## DOC-1 / DOC-2 Coherency (ADR-010)

Per ADR-010, this DOC-1 and the corresponding DOC-2 must be coherent:
- All requirements in DOC-1 have a corresponding architecture element in DOC-2
- All architecture elements in DOC-2 support a requirement in DOC-1
- No blind spots: anything not in DOC-1 is not required; anything not in DOC-2 is not architecture

---

*End of DOC-1 v2.3 — Cumulative (v1.0 through v2.3)*
