---
doc_id: DOC-2
release: v2.7
status: Draft
title: Architecture Document
version: 1.0
date_created: 2026-04-02
authors: [Architect mode, Human]
previous_release: v2.6
cumulative: true
---

# DOC-2 â€” Architecture Document (v2.7)

> **Status: DRAFT** -- This document is in draft for v2.7.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all architecture from v1.0 through v2.7.
> To understand the full project architecture, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [Guiding Principle](#1-guiding-principle)
2. [Global Architecture Diagram](#2-global-architecture-diagram)
3. [Detailed Technical Stack](#3-detailed-technical-stack)
4. [Architecture Decisions (v1.0)](#4-architecture-decisions-v10)
5. [Functional Layer Architecture](#5-functional-layer-architecture)
6. [Architecture / Feature / Requirement Traceability Matrix](#6-architecture-feature--requirement-traceability-matrix)
7. [v2.1 Architecture Additions](#7-v21-architecture-additions)
8. [v2.3 Architecture Additions](#8-v23-architecture-additions)
9. [v2.4 Architecture Additions](#9-v24-architecture-additions)
10. [v2.5 Architecture Additions](#10-v25-architecture-additions)
11. [v2.6 Architecture Additions](#11-v26-architecture-additions)
12. [v2.7 Architecture Additions](#12-v27-architecture-additions)
13. [Appendices](#13-appendices)

---

## 1. Guiding Principle

**Roo Code is the sole and unique agentic execution engine.** All other components (local LLM engine, clipboard proxy, cloud API, Memory Bank, Agile personas) are **service providers** that interface with Roo Code via standardized protocols.

This principle guarantees that:
- Roo Code's behavior is never modified, regardless of the LLM source used.
- Switching between the three backends (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) is transparent to Roo Code â€” only the "API Provider" parameter changes.
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
|  |  |  (4 Agile   |  |  (6 Imperative  |   (Read/Write .md)         |      |    |
|  |  |   Personas) |  |   Rules)     |  |                            |      |    |
|  |  +-------------+  +--------------+  +----------------------------+      |    |
|  |                                                                          |    |
|  |    OpenAI-Compatible API (HTTP)         Anthropic API (HTTPS)            |    |
|  +------------------+-----------------------+----------------+--------------+    |
|                     |                                        |                   |
|         +-----------+------------+                           |                   |
|         |    LLM SWITCHER        |  (Provider Parameter      |                   |
|         |    (3 modes)           |   in Roo Code)            |                   |
|         +-----------+------------+                           |                   |
|                     |                                        |                   |
|       +-------------+-------------+                          |                   |
|       |                           |                          |                   |
|  +----+----------+   +------------+----------+   +-----------+-----------+       |
|  | MODE 1        |   | MODE 2                |   | MODE 3                |       |
|  | LOCAL         |   | GEMINI PROXY          |   | DIRECT CLOUD          |       |
|  | (Tailscale)   |   |                       |   |                       |       |
|  |               |   | proxy.py              |   | Anthropic API         |       |
|  | calypso:11434 |   | localhost:8000        |   | api.anthropic.com     |       |
|  | (via Tailscale|   | (FastAPI + SSE)       |   | (native HTTPS)        |       |
|  |  private net) |   |         |             |   |                       |       |
|  | uadf-agent    |   | Windows |             |   | claude-sonnet-4-6     |       |
|  | (Qwen3-32B    |   | Clip-   |             |   | (Anthropic Provider   |       |
|  |  T=0.15)      |   | board   |             |   |  native Roo Code)     |       |
|  |               |   |         |             |   |                       |       |
|  | Free          |   | Free    |             |   | Paid per usage        |       |
|  | Private net   |   | Copy-   |             |   | Fully automated       |       |
|  | Tailscale     |   | paste   |             |   | Connection required   |       |
|  +---------------+   +----+----+             +-----------------------+---+       |
|                           |                                                       |
|                  +--------+---------+                                             |
|                  |  HUMAN           |                                             |
|                  |  INTERVENTION    |                                             |
|                  |  (Ctrl+V/Ctrl+C) |                                             |
|                  +--------+---------+                                             |
|                           |                                                       |
+---------------------------+-------------------+------+----------------------------+
          |  Tailscale VPN    |                   |      |
          v  (private net)    |                   |      |
+---------------------------+    +--------------+------+--------+
|  LINUX SERVER "calypso"   |    |  GEMINI CHROME (Chrome/pc)  |
|  RTX 5060 Ti 16 GB        |    +-----------------------------+
|  Ollama + uadf-agent      |    +-----------------------+
|  + qwen3:7b               |    |  ANTHROPIC CLOUD      |
|  API: calypso:11434       |    |  api.anthropic.com    |
+---------------------------+    |  claude-sonnet-4-6    |
                                  +-----------------------+

+-----------------------------------------------------------------------------------+
|                       MEMORY BANK (File System)                                   |
|   Works identically in all 3 modes â€” Git versioned                                |
|                                                                                   |
|  memory-bank/                                                                     |
|  +-- hot-context/           (Read at session start)                              |
|  |   +-- activeContext.md   (Current task - Working Memory)                      |
|  |   +-- progress.md         (Phase & Feature Checklist)                          |
|  |   +-- decisionLog.md      (ADR - Architecture Decision Records, APPEND ONLY)   |
|  |   +-- systemPatterns.md   (Architecture & Conventions)                         |
|  |   +-- productContext.md   (User Stories & Business Value)                     |
|  |   +-- session-checkpoint.md (CRASH RECOVERY, 5-min heartbeat)                 |
|  +-- projectBrief.md         (Vision & Non-Goals)                                |
|  +-- techContext.md          (Stack & Commands for all 3 modes)                  |
|  +-- archive-cold/           (MCP ONLY access)                                   |
|  +-- batch_artifacts/         (Anthropic Batch API outputs)                       |
+-----------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------+
|                       PROMPT REGISTRY (prompts/)                                  |
|   Single source of truth for all system prompts â€” Git versioned                   |
|                                                                                   |
|  prompts/                                                                         |
|  +-- README.md             (Registry index)                                       |
|  +-- SP-001-ollama-modelfile-system.md   -> Modelfile[SYSTEM]                     |
|  +-- SP-002-clinerules-global.md         -> .clinerules (entire file)             |
|  +-- SP-003-persona-product-owner.md    -> .roomodes[product-owner]               |
|  +-- SP-004-persona-scrum-master.md     -> .roomodes[scrum-master]                |
|  +-- SP-005-persona-developer.md        -> .roomodes[developer]                   |
|  +-- SP-006-persona-qa-engineer.md     -> .roomodes[qa-engineer]                  |
|  +-- SP-007-gem-gemini-roo-agent.md    -> gemini.google.com (OUTSIDE GIT)         |
+-----------------------------------------------------------------------------------+
```

---

## 3. Detailed Technical Stack

### 3.1 Interface & Orchestration Layer

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **IDE** | Visual Studio Code | Latest stable | Primary development environment |
| **Agentic Extension** | Roo Code | Latest stable | Agentic execution engine, LLM â†” file system bridge |
| **Agile Personas** | JSON (`.roomodes`) | â€” | Definition of the 4 personas and their RBAC permissions |
| **Session Directives** | Markdown (`.clinerules`) | â€” | 6 imperative rules injected into each session |

### 3.2 Local LLM Engine Layer (Sovereign Mode â€” `calypso` Server)

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **Inference Server** | Linux headless `calypso` | Ubuntu/Debian | Ollama host â€” RTX 5060 Ti 16 GB VRAM |
| **Private Network** | Tailscale | Latest stable | Mesh VPN connecting `pc` (Windows) and `calypso` (Linux) |
| **Inference Engine** | Ollama | Latest stable | VRAM management, weight loading, REST API |
| **Main Model** | `mychen76/qwen3_cline_roocode:32b` | 32B quantized | Main brain, fine-tuned for Roo Code Tool Calling |
| **Secondary Model** | `qwen3:7b` | 7B | Delegated agent for lightweight tasks (Boomerang Tasks) |
| **Model Configuration** | Ollama `Modelfile` | â€” | Lock T=0.15, Min_P=0.03, num_ctx=131072 |
| **Listening Address** | `calypso:11434` | â€” | OpenAI-compatible REST API, accessible via Tailscale from `pc` |

### 3.3 Gemini Chrome Proxy Layer (Hybrid Mode)

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.10+ | Proxy server language |
| **Web Framework** | FastAPI | 0.110+ | Lightweight ASGI server, OpenAI API emulation + SSE |
| **ASGI Server** | Uvicorn | 0.29+ | Production server for FastAPI |
| **Clipboard Management** | Pyperclip | 1.8+ | Windows clipboard read/write |
| **Async Management** | asyncio (Python stdlib) | â€” | Non-blocking polling loop |
| **Streaming** | StreamingResponse (FastAPI) | â€” | SSE response in a single chunk for Roo Code compatibility |
| **Listening Port** | `localhost:8000` | â€” | Entry point for Roo Code in proxy mode |
| **Virtual Environment** | venv (Python stdlib) | â€” | Dependency isolation |

### 3.4 Persistent Memory Layer

| Component | Technology | Role |
| :--- | :--- | :--- |
| **File System** | NTFS Windows (laptop `pc`) | Physical storage of `.md` files |
| **Data Format** | Markdown (`.md`) | Human readability, Git compatibility |
| **Versioning** | Git | Traceability of Memory Bank modifications |
| **Directory** | `memory-bank/` (project root) | Container for all contextual memory |

### 3.5 Gemini Chrome Interface Layer

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Web Interface** | Gemini Chrome (gemini.google.com) | Free cloud LLM, generation engine |
| **Dedicated Profile** | Gemini Gem "Roo Code Agent" | Contains the Roo Code system prompt (SP-007) |
| **Browser** | Google Chrome | Access to the Gemini Web interface |

### 3.6 Direct Cloud LLM Engine Layer (Claude API Mode)

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **API Provider** | Anthropic API | v1 (stable) | Official cloud API, direct connection without proxy |
| **Model** | `claude-sonnet-4-6` | Latest stable Sonnet | High-quality model, native Roo Code, integrated tool use |
| **Endpoint** | `https://api.anthropic.com` | â€” | Official Anthropic HTTPS entry point |
| **Authentication** | API key (`sk-ant-api03-...`) | â€” | Stored in VS Code SecretStorage via Roo Code |
| **Roo Code Provider** | "Anthropic" (native) | â€” | Provider integrated in Roo Code, no middleware |

### 3.7 Prompt Consistency Verification Layer

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Verification script** | PowerShell (`check-prompts-sync.ps1`) | Normalized comparison of canonical SPs vs deployed artifacts |
| **Git Hook** | Shell script (`.git/hooks/pre-commit`) | Automatic script call before each commit |
| **Registry** | `prompts/` directory (Markdown + YAML) | Single source of truth for all system prompts |

---

## 4. Architecture Decisions (v1.0)

### DA-001 â€” `.roomodes` as central registry of Agile personas

**Decision:** The `.roomodes` file is the central registry of Agile personas. It defines for each role: its unique identifier (`slug`), its display name, its `roleDefinition` (behavioral system prompt), and its permission `groups`. This file is static and versioned in Git.

**Justification:** Clear separation between configuration (`.roomodes`) and behavior (`.clinerules`). The `roleDefinition` is the source of truth for each persona's behavior.

**Requirements addressed:** REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4

### DA-002 â€” `.clinerules` as universal session trigger

**Decision:** The `.clinerules` file contains 6 imperative rules injected above each user prompt, forcing the agent to follow the CHECKâ†’CREATEâ†’READâ†’ACT sequence for the Memory Bank, to version under Git, and to maintain prompt registry consistency. These directives are unconditional and apply to all modes.

**Justification:** `.clinerules` is the universal safety net. Even if a persona forgets its own rule, `.clinerules` systematically reminds it at each session.

**Requirements addressed:** REQ-4.2, REQ-4.3, REQ-7.3

### DA-003 â€” Memory Bank segmented into 7 thematic files

**Decision:** The Memory Bank is segmented into 7 thematic files to avoid contextual pollution and optimize LLM attention. Each file has a unique and non-overlapping responsibility.

**Justification:** A monolithic file would force the LLM to load all memory at each session. Segmentation allows loading only the relevant files according to the task.

**Requirements addressed:** REQ-4.4

### DA-004 â€” Modelfile with locked determinism parameters

**Decision:** The model `mychen76/qwen3_cline_roocode:32b` is compiled with a custom `Modelfile` locking: `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`, `num_ctx 131072`, `num_gpu 99`, `num_thread 8`. These values cannot be modified at runtime. The Modelfile is compiled on `calypso` via `ollama create uadf-agent -f Modelfile`.

**Justification:** Maximum determinism eliminates hallucinations during code generation. The 128K token window allows simultaneous loading of the project and the Memory Bank. `num_gpu 99` exploits the 16 GB of VRAM of `calypso`'s RTX 5060 Ti.

**Requirements addressed:** REQ-1.2, REQ-1.3

### DA-005 â€” Boomerang Tasks for delegation to lightweight models

**Decision:** Roo Code's "Boomerang Tasks" workflow is used to delegate repetitive or voluminous tasks (log analysis, unit test generation) to the secondary model `qwen3:7b`, also hosted on `calypso`.

**Justification:** VRAM optimization and acceleration of repetitive cycles. The 32B model remains available for complex decisions. Both models share the same Ollama instance on `calypso`.

**Requirements addressed:** REQ-1.4

> âš ï¸ **PROXY MODE LIMITATION:** Boomerang Tasks are not supported in Gemini Proxy Mode.
> The proxy is a single endpoint shared by all Roo Code instances â€” concurrent requests
> from the main agent and the sub-agent create a clipboard conflict (deadlock).
> **Use Local Mode (Ollama) or Cloud Mode (Claude API) for tasks requiring sub-agents.**

### DA-006 â€” FastAPI + asyncio for the proxy

**Decision:** FastAPI is chosen over Flask for its native asynchronism management (asyncio), essential for keeping the HTTP connection open while waiting for human intervention (clipboard polling) without blocking the server.

**Justification:** Flask is synchronous by default â€” it would block the server during polling. FastAPI with asyncio keeps the server responsive (`/health` endpoint responds during polling).

**Requirements addressed:** REQ-2.3.1, REQ-2.1.1

### DA-007 â€” OpenAI Chat Completions format emulation

**Decision:** The proxy exactly emulates the OpenAI Chat Completions API format (`/v1/chat/completions`). This decision guarantees native compatibility with Roo Code configured in "OpenAI Compatible" mode, without any modification to Roo Code's source code.

**Justification:** Roo Code natively supports the OpenAI format. By emulating this format, the proxy is transparent to Roo Code.

**Requirements addressed:** REQ-2.1.2, REQ-2.4.2

### DA-008 â€” "Dedicated Gem" mode with system prompt filtering

**Decision:** The proxy implements a `USE_GEM_MODE=true` mode (default) that filters the `system` message when copying to the clipboard. When this mode is active, only `user` and `assistant` messages are transmitted.

**Justification:** Roo Code's system prompt represents several thousand tokens. By storing it in the Gemini Gem (SP-007), we avoid retransmitting it with each request, reducing transfer size by 50%+.

**Requirements addressed:** REQ-2.1.4

### DA-009 â€” Cleaning of base64 content

**Decision:** The proxy detects and replaces `{"type": "image_url", ...}` elements with the message `[IMAGE OMITTED - Not supported by clipboard proxy]`.

**Justification:** Base64 images can represent hundreds of KB. Their presence in the clipboard would make transfer impossible. Replacing them with a text message preserves context without blocking the flow.

**Requirements addressed:** REQ-2.1.5

### DA-010 â€” Gemini Gem with integrated Roo Code system prompt

**Decision:** A dedicated "Gem" is created in Gemini Web with the entirety of the Roo Code system prompt (SP-007). This approach avoids retransmitting the system prompt with each request via the clipboard.

**Justification:** The Roo Code system prompt is static and does not change between requests. Storing it in the Gem once is more efficient than retransmitting it with each exchange.

**Requirements addressed:** REQ-5.1, REQ-5.2

### DA-011 â€” Native Anthropic provider in Roo Code for Cloud Mode

**Decision:** The connection to the Anthropic API uses the native "Anthropic" provider integrated in Roo Code. The reference model is `claude-sonnet-4-6`. The API key is stored in VS Code SecretStorage, never in project files.

**Justification:** The native provider guarantees full compatibility with streaming, vision, and Claude's native tool use. VS Code SecretStorage is encrypted and not accessible from the file system, guaranteeing API key security.

**Requirements addressed:** REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4

### DA-012 â€” Centralized system prompt registry in `prompts/`

**Decision:** A versioned `prompts/` directory contains a canonical copy of each system prompt with YAML metadata (target, version, dependencies, changelog). RULE 6 in `.clinerules` enforces consistency before each commit. SP-007 (Gemini Gem) is marked `hors_git: true` with documented manual deployment procedure.

**Justification:** System prompts are scattered across multiple artifacts (.roomodes JSON, .clinerules text, compiled Modelfile, external Gemini Web). Without a centralized registry, a modification to `.clinerules` can make the Gemini Gem inconsistent without anyone noticing.

**Requirements addressed:** REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5

### DA-013 â€” Automatic verification via PowerShell script + Git pre-commit hook

**Decision:** A script `scripts/check-prompts-sync.ps1` compares deployed content with canonical SPs via normalized comparison (encoding correction `\r\n`/`\n`, JSON deserialization for `.roomodes`, robust extraction regex). A Git hook `.git/hooks/pre-commit` calls this script automatically and blocks the commit if desynchronization is detected. SP-007 is excluded from automatic verification with a manual verification warning.

**Justification:** RULE 6 being a behavioral directive, it can be ignored by an LLM agent. The pre-commit hook transforms verification into a non-bypassable technical constraint.

**Requirements addressed:** REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4

### DA-014 â€” SSE streaming in a single chunk for the proxy

**Decision:** The proxy implements SSE (Server-Sent Events) streaming by returning the Gemini response in a single SSE chunk followed by `data: [DONE]`. If the request contains `"stream": false`, a complete non-streamed JSON response is returned. The proxy automatically detects the mode via the `stream` field of the request.

**Justification:** Roo Code can send requests with `stream: true` (default behavior in some versions). Without SSE support, the proxy would return a non-streamed JSON response that Roo Code might reject while expecting SSE format. The single-chunk SSE implementation is transparent to Roo Code regardless of its configuration.

**Requirements addressed:** REQ-2.4.1, REQ-2.4.3

---

## 5. Functional Layer Architecture

### Layer A â€” Behavioral Orchestration (`.roomodes` & `.clinerules`)

**RBAC Permission Matrix (DA-001):**

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| `read` (read all files) | âœ… | âœ… | âœ… | âœ… |
| `edit` `memory-bank/productContext.md` | âœ… | âœ… | âœ… | âŒ |
| `edit` `memory-bank/*.md` (all) | âŒ | âœ… | âœ… | âŒ |
| `edit` `docs/*.md` (documentation) | âœ… | âœ… | âœ… | âŒ |
| `edit` `docs/qa/*.md` (QA reports) | âŒ | âŒ | âŒ | âœ… |
| `edit` source code (all files) | âŒ | âŒ | âœ… | âŒ |
| `command` general terminal | âŒ | âŒ | âœ… | âŒ |
| `command` Git only | âŒ | âœ… | âœ… | âŒ |
| `command` tests only | âŒ | âŒ | âœ… | âœ… |
| `browser` browser access | âŒ | âŒ | âœ… | âœ… |
| `mcp` MCP access | âŒ | âŒ | âœ… | âŒ |

**Git commands authorized for Scrum Master:** `git add`, `git commit`, `git status`, `git log`
**Test commands authorized for QA Engineer:** `npm test`, `npm run test`, `pytest`, `python -m pytest`, `dotnet test`, `go test`, `git status`, `git log`

---

### Layer B â€” Memory Bank (Markdown Files)

**Structure and Responsibilities of the 7 Files (DA-003):**

| File | Read Frequency | Write Frequency | Content |
| :--- | :--- | :--- | :--- |
| `projectBrief.md` | Project start | Rare | Vision, objectives, Non-Goals, constraints |
| `productContext.md` | Sprint start | Per sprint | User Stories, business value, backlog |
| `systemPatterns.md` | Per feature | Per feature | Architecture conventions, patterns, anti-patterns |
| `techContext.md` | Per task | Per change | Stack, commands, CLI, IDE configuration |
| `activeContext.md` | Every task | Every task | Current task, session state, next step |
| `progress.md` | Weekly | Weekly | Phase & feature checklist, blockers |
| `decisionLog.md` | Weekly | Weekly | Architecture decisions, ADR records |

**Hot/Cold Separation (v2.6+):**

```
memory-bank/
â”œâ”€â”€ hot-context/           # Read directly at session start
â”‚   â”œâ”€â”€ activeContext.md   # Current task, session state
â”‚   â”œâ”€â”€ progress.md        # Checkbox tracking
â”‚   â”œâ”€â”€ decisionLog.md     # ADRs (APPEND ONLY!)
â”‚   â”œâ”€â”€ systemPatterns.md  # Architecture conventions
â”‚   â”œâ”€â”€ productContext.md  # Backlog, user stories
â”‚   â””â”€â”€ session-checkpoint.md  # CRASH RECOVERY
â”œâ”€â”€ projectBrief.md        # Vision (root, rarely changes)
â”œâ”€â”€ techContext.md         # Stack, commands (root)
â”œâ”€â”€ archive-cold/          # MCP ONLY access
â””â”€â”€ batch_artifacts/       # Anthropic Batch API outputs
```

---

### Layer C â€” Anthropic Batch API Toolkit

**Package Structure:**

```
scripts/batch/
â”œâ”€â”€ __init__.py           # Public re-exports
â”œâ”€â”€ config.py             # BatchConfig dataclass + YAML loader
â”œâ”€â”€ submit.py             # Batch submission
â”œâ”€â”€ retrieve.py           # Result retrieval + markdown report
â”œâ”€â”€ poll.py               # Polling utility
â”œâ”€â”€ cli.py                # CLI entry point
â”œâ”€â”€ generate.py           # Jinja2 script generator
â””â”€â”€ templates/
    â”œâ”€â”€ batch_submit_script.py.j2
    â””â”€â”€ batch_retrieve_script.py.j2
```

**Core Dataclass: BatchConfig:**

```python
@dataclass
class BatchConfig:
    name: str                      # Human-readable batch name
    model: str                     # Anthropic model (e.g., claude-sonnet-4-6)
    max_tokens: int                # Max tokens per response
    temperature: float             # Sampling temperature
    output_dir: pathlib.Path        # Where to save results
    requests: list[RequestSpec]    # List of individual requests
    batch_id_file: pathlib.Path | None = None  # Persistent batch_id
    workspace_root: pathlib.Path   # For path resolution
```

**CLI Commands:**

```bash
# Submit a batch
python -m scripts.batch.cli submit batch.yaml

# Retrieve results (with optional polling)
python -m scripts.batch.cli retrieve batch.yaml --poll --interval 60

# Check batch status
python -m scripts.batch.cli status batch.yaml

# Generate scripts from YAML
python -m scripts.batch.generate batch.yaml --output ./generated/
```

---

## 6. Architecture / Feature / Requirement Traceability Matrix

| Component | Architecture Decision | Requirement |
|-----------|----------------------|-------------|
| **Local Ollama Server** | Ollama on `calypso` | REQ-1.1 |
| **Custom Modelfile** | DA-004 | REQ-1.2, REQ-1.3 |
| **Boomerang Tasks** | DA-005 | REQ-1.4 |
| **proxy.py** | DA-006, DA-007 | REQ-2.0 |
| **Gemini Gem SP-007** | DA-010 | REQ-2.1.3, REQ-5.1, REQ-5.2 |
| **SSE streaming** | DA-014 | REQ-2.4.1, REQ-2.4.3 |
| **base64 cleaning** | DA-009 | REQ-2.1.5 |
| **USE_GEM_MODE flag** | DA-008 | REQ-2.1.4 |
| **`.roomodes`** | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4 |
| **`.clinerules`** | DA-002 | REQ-4.1, REQ-4.2, REQ-4.3, REQ-4.5 |
| **Memory Bank 7-file** | DA-003 | REQ-4.4 |
| **Roo Code Provider Switcher** | DA-007, DA-011 | REQ-2.0 |
| **Variable `USE_GEM_MODE`** | DA-008 | REQ-2.1.4 |
| **`prompts/` directory** | DA-012 | REQ-7.1 |
| **`prompts/SP-XXX-*.md` files** | DA-012 | REQ-7.1, REQ-7.2, REQ-7.4 |
| **`prompts/README.md`** | DA-012 | REQ-7.2 |
| **RULE 6 in `.clinerules`** | DA-012 | REQ-7.3 |
| **Flag `hors_git: true` in SP-007** | DA-012 | REQ-7.5 |
| **`scripts/check-prompts-sync.ps1`** | DA-013 | REQ-8.1, REQ-8.3, REQ-8.4 |
| **`.git/hooks/pre-commit`** | DA-013 | REQ-8.2 |
---

## 7. v2.1 Architecture Additions

### 7.1 Delta from v2.0

v2.1 introduces **no architectural changes**. The architecture described in v1.0 above applies in full. This section documents additions made during v2.1.

### 7.2 RULE 10 â€” GitFlow Enforcement (ADR-006)

v2.1 formalized GitFlow with the following branch lifecycle:

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `main` | Production state â€” frozen after each release tag | Never commit directly after tag |
| `develop` | Wild mainline â€” ad-hoc features, experiments, quick fixes | Long-lived, base for `develop-vX.Y` |
| `develop-vX.Y` | Scoped backlog â€” formal release scope | Created at release planning |
| `feature/{slug}` | Single feature or fix | Branch from `develop` or `develop-vX.Y` |
| `hotfix/vX.Y.Z` | Emergency production fix | Branch from production tag, merge to main + develop |

**Key rule:** All development commits must be on a feature branch. Governance-only commits (ADRs, RULE additions) may be committed directly on `develop`.

### 7.3 LLM Backend Resilience (IDEA-008)

The 3-tier architecture is unchanged. The Tier-1 LLM routing now includes:

```
Default:  minimax/minimax-m2.7  (via OpenRouter)
Fallback: claude-sonnet-4-6     (after 3 consecutive errors)
```

This provides automatic fallback without human intervention.

### 7.4 SP-002 Coherence Fix

The `.clinerules` encoding issues were resolved:
- UTF-8 BOM removed
- Latin-1 mojibake corrected (em-dash, arrows, quotes)
- Literal `\n` replaced with real newlines
- Double embedding consolidated

Prevention: `scripts/check-prompts-sync.ps1` enhanced with BOM/mojibake detection.

---

## 8. v2.3 Architecture Additions

### 8.1 Delta from v2.1 and v2.2

v2.2 introduced no architectural changes. v2.3 adds:
1. **IDEA-009 Architecture** â€” Generic Anthropic Batch API Toolkit (`scripts/batch/`)
2. **Template Bundle** â€” Self-contained `template/scripts/batch/` for new project deployment
3. **ADR-010 Ad-Hoc Governance** â€” Lightweight process for reactive ideas

### 8.2 IDEA-009 Architecture: Anthropic Batch API Toolkit

#### 8.2.1 Package Structure

**Location:** `scripts/batch/` (canonical), `template/scripts/batch/` (deployment bundle)

#### 8.2.2 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| YAML-based configuration | Human-readable, version-controllable batch definitions |
| File-based batch_id persistence | Batch ID survives terminal restarts; no in-memory state |
| Markdown fence stripping | API wraps JSON in ```json fences; must strip before parsing |
| Normalize "error" / "errored" | API inconsistency: both appear depending on failure mode |
| Raw response fallback | When text differs after parsing, save raw for debugging |
| CLI-first design | Works standalone without Python import; composable with shell |
| Jinja2 script generation | batch.yaml â†’ submit.py + retrieve.py for repeatable runs |
| Self-contained template bundle | template/scripts/batch/ works independently, no parent delegation |

#### 8.2.5 Data Flow

```
batch.yaml
    â””â”€> config.py (BatchConfig)
            â”œâ”€> submit.py --> Anthropic Batch API --> batch_id
            â”‚                                    |
            |                                    v
            |                              batch_id_file
            |                                    |
            |                                    v
            â””â”€> poll.py (loop) --> retrieve.py --> output_dir/
                                                       â”œâ”€ {custom_id}_raw.txt
                                                       â””â”€ results.md
```

### 8.3 ADR-010 Ad-Hoc Governance Architecture

#### 8.3.1 Two Paths

| Aspect | [STRUCTURED] | [AD-HOC] |
|--------|-------------|-----------|
| Origin | Formal PRD | Reactive discovery |
| Process | Full DOC-1â†’DOC-2â†’DOC-3â†’Calypsoâ†’QA | Lightweight with release tier |
| Branch | `develop-vX.Y` | `develop` or `feature/IDEA-NNN-slug` |
| Calypso | Yes | Optional (Minor skip) |
| Release tier | N/A | Minor / Medium / Major |

#### 8.3.2 Release Tier Criteria

| Tier | Trigger | Process |
|------|---------|---------|
| Minor | Bug fixes, dev-tooling, low-risk | Skip Calypso; lightweight docs; unit+integration tests |
| Medium | New features, moderate scope | Partial/full Calypso; full DOC-1/2/3; QA review |
| Major | Architectural, epic-level | Full process; stakeholder sign-off |

---

## 9. v2.4 Architecture Additions

### 9.1 Delta from v2.3

v2.4 introduces the **ideation-to-release pipeline** (PHASE-A â†’ PHASE-B â†’ PHASE-C) with formal governance.

### 9.2 Ideation Pipeline Architecture

```
PHASE-A: Intake & Triage
    â”‚
    â”œâ”€> Human input (idea/request/remark)
    â”œâ”€> Orchestrator detects off-topic input (RULE 13)
    â”œâ”€> Assigns IDEA/TECH ID
    â”œâ”€> Classifies: BUSINESS (What) â†’ IDEAS-BACKLOG
    â”‚               TECHNICAL (How) â†’ TECH-SUGGESTIONS-BACKLOG
    â””â”€> Sync detection: NO_OVERLAP / REDUNDANCY / DEPENDENCY / CONFLICT / SHARED_LAYER

PHASE-B: Refinement & Approval
    â”‚
    â”œâ”€> Structured requirement/feasibility session
    â”œâ”€> Impact analysis (RULE 11 synchronization awareness)
    â”œâ”€> Human chooses: [A] Refine now / [B] Park for later / [C] Sync first
    â””â”€> Status transitions: IDEA â†’ REFINED / DEFERRED / INTEGRATED

PHASE-C: Execution & Release
    â”‚
    â”œâ”€> Feature branch from develop or develop-vX.Y
    â”œâ”€> Calypso orchestration (4-agent pipeline)
    â”œâ”€> QA validation
    â””â”€> Merge via PR (fast-forward preferred, branch preserved)
```

### 9.3 Calypso Orchestration Scripts

**4-Agent Pipeline:**

```
Orchestrator
    â”‚
    â”œâ”€> Librarian Agent (SP-010) â€” Cold archive indexing
    â”œâ”€> Product Owner Agent (SP-003) â€” Requirements refinement
    â”œâ”€> Developer Agent (SP-005) â€” Implementation
    â””â”€> QA Engineer Agent (SP-006) â€” Validation
```

**Scripts location:** `scripts/calypso/` (or `src/calypso/`)

### 9.4 RULE 13 â€” Ideation Intake

Every human input outside the current task MUST be routed to Orchestrator:
- Detection: If human expresses idea/request/remark outside scope
- Routing: Raw idea text + agent context + exact words
- Acknowledgment: Orchestrator handles
- Intake: Assigns IDEA/TECH ID, classifies, adds to backlog, runs sync detection

---

## 10. v2.5 Architecture Additions

### 10.1 Delta from v2.4

v2.5 introduces **canonical docs status governance** (RULE 8) and **release coherence audit** (IDEA-015).

### 10.2 RULE 8 â€” Documentation Discipline

#### 10.2.1 The Two Spaces

- **docs/releases/vX.Y/** files with status **Frozen** are **READ-ONLY** for all agents
- **docs/releases/vX.Y/** files with status **Draft** or **In Review** may be modified ONLY by Architect or Product Owner persona
- **memory-bank/** files are agent-writable â€” update freely as working memory

#### 10.2.2 Idea Capture Mandate

When identifying a new requirement/improvement NOT in current release scope:
1. DO NOT modify current release's canonical docs
2. ADD entry to `docs/ideas/IDEAS-BACKLOG.md` with status [IDEA]
3. CREATE `docs/ideas/IDEA-{NNN}-{slug}.md` with description, motivation, affected documents
4. INFORM human that new idea has been captured

#### 10.2.3 Conversation Log Mandate

When saving AI conversation output:
1. Save to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`
2. Add entry to `docs/conversations/README.md` with triage status "Not yet triaged"
3. Never edit a conversation file after creation

### 10.3 IDEA-015 â€” Release Coherence Audit

**Frequency:** Pre-release (5 days before target)

**Audit Checklist:**
- Scope freeze (all ideas not REFINED deferred)
- Documentation coherence (DOC-1..DOC-5 aligned)
- Code coherence (all branches merged, full QA pass)
- Dry run release (RC1 tag, full test suite)
- Final review (human approves, vX.Y.0 tag applied)

---

## 11. v2.6 Architecture Additions

### 11.1 Delta from v2.5

v2.6 introduces **session checkpoint** (crash recovery), **APPEND ONLY for ADRs**, and **artifact ID schema**.

### 11.2 Session Checkpoint Architecture

**Location:** `memory-bank/hot-context/session-checkpoint.md`

**Required Metadata:**

```yaml
---
artifact_id: CHECKPOINT-YYYY-MM-DD-NNN
session_id: sYYYY-MM-DD-{mode}-{NNN}
status: ACTIVE | CLOSED | CRASHED
created: YYYY-MM-DDTHH:MM:SSZ
modified: YYYY-MM-DDTHH:MM:SSZ
last_heartbeat: YYYY-MM-DDTHH:MM:SSZ
---
```

**RULE MB-2: Session Checkpoint**

Every 5 minutes during active work:
1. Update `session-checkpoint.md.last_heartbeat`
2. Update `session-checkpoint.md.git_state`
3. Update `session-checkpoint.md.current_task`

At session start:
- IF `session-checkpoint.last_heartbeat > 30 minutes`
- â†’ Report crash detection
- â†’ Offer recovery options

### 11.3 RULE MB-3: APPEND ONLY for ADRs

`decisionLog.md` is **APPEND ONLY**:
- Never overwrite existing ADRs
- Never delete entries
- Archive old entries to cold only when file > 500 lines

### 11.4 Artifact Identification Schema

| Artifact Type | ID Format | Example |
|--------------|-----------|---------|
| **Business Idea** | `IDEA-{YYYY-MM-DD}-{NNN}` | `IDEA-2026-04-01-001` |
| **Technical Suggestion** | `TECH-{YYYY-MM-DD}-{NNN}` | `TECH-2026-04-01-001` |
| **Architecture Decision** | `ADR-{YYYY-MM-DD}-{NNN}` | `ADR-2026-04-01-001` |
| **Session** | `s{YYYY-MM-DD}-{mode}-{NNN}` | `s2026-04-01-developer-001` |
| **Refinement Session** | `REF-{YYYY-MM-DD}-{NNN}` | `REF-2026-04-01-001` |
| **Conversation** | `{YYYY-MM-DD}-{source}-{slug}` | `2026-04-01-gemini-workbench` |
| **Batch Job** | `BATCH-{YYYY-MM-DD}-{NNNN}` | `BATCH-2026-04-01-0001` |
| **Expert Report** | `RPT-{YYYY-MM-DD}-{NNNN}` | `RPT-2026-04-01-0001` |
| **Enhancement** | `ENH-{YYYY-MM-DD}-{NNN}` | `ENH-2026-04-01-001` |

### 11.5 RULE G-0: Plan-Branch Parity

Every plan creates a branch. Branch is preserved after merge (never deleted for traceability).

---

## 12. v2.7 Architecture Additions

### 12.1 Delta from v2.6

v2.7 addresses **IDEA-017** â€” canonical docs must be cumulative and self-contained.

### 12.2 RULE 12 â€” Canonical Docs Cumulative Requirement

**R-CANON-0:** Each canonical doc in `docs/releases/vX.Y/` is **fully self-contained and cumulative** â€” it contains the complete state of that document for the entire project history up to vX.Y.

**Canonical docs:**
- DOC-1: Product Requirements Document (PRD)
- DOC-2: Technical Architecture
- DOC-3: Implementation Plan
- DOC-4: Operations Guide
- DOC-5: Release Notes

**Minimum line counts for cumulative docs:**
- DOC-1 >= 500 lines
- DOC-2 >= 500 lines
- DOC-3 >= 300 lines
- DOC-4 >= 300 lines
- DOC-5 >= 200 lines

### 12.3 RULE 12.2 â€” GitFlow Rules for Canonical Docs

**R-CANON-1:** Canonical docs on `develop`: Only via feature branch (`feature/canon-doc-*`)

**R-CANON-2:** Canonical docs on `develop-vX.Y`: Only via feature branch scoped to that release

**R-CANON-3:** Direct commits on `develop` or `develop-vX.Y` to canonical docs are **FORBIDDEN**

**R-CANON-4:** Exception: Governance-only commits (ADRs, RULE additions) MAY be committed directly per RULE 10.3 exception

### 12.4 RULE 12.3 â€” Consistency Rules

**R-CANON-5:** All 5 canonical docs MUST be updated together for any release

**R-CANON-6:** When merging to `develop-vX.Y`, all 5 DOC-*-vX.Y-*.md files must exist and be consistent

**R-CANON-7:** The `DOC-*-CURRENT.md` pointer files MUST all point to the same release version

### 12.5 Enforcement

Canonical docs enforcement is enforced by:
- **Git pre-receive hook** at `.githooks/pre-receive`
- **GitHub Actions CI** at `.github/workflows/canonical-docs-check.yml`

### 12.6 Idea Enrichment (IDEA-016)

Canonical docs should be enriched with **diagrams** (Mermaid, ASCII art) where text alone is insufficient:
- Architecture diagrams in DOC-2
- Workflow diagrams in DOC-3
- Sequence diagrams for complex interactions

### 12.7 Conversation Logging Enhancement (IDEA-019)

New enhancement tracking:
- Enhancement ID format: `ENH-{YYYY-MM-DD}-{NNN}`
- Tracked in `docs/ideas/ENH-*.md`
- Logged in `docs/conversations/README.md` with triage status

---

## 13. Appendices

### Appendix A â€” References Table

| Ref. | Type | Title / Identifier | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Internal document | `DOC-1-CURRENT.md` | Product Requirements Document â€” source of all REQ-xxx requirements |
| [DOC2] | Internal document | `DOC-2-CURRENT.md` | This document â€” Architecture, Solution and Technical Stack |
| [SP-001] | System Prompt | `prompts/SP-001-ollama-modelfile-system.md` | Ollama Modelfile system prompt â€” content of the `SYSTEM` block |
| [SP-002] | System Prompt | `prompts/SP-002-clinerules-global.md` | Canonical content of the `.clinerules` file |
| [SP-003] | System Prompt | `prompts/SP-003-persona-product-owner.md` | `roleDefinition` of the Product Owner persona in `.roomodes` |
| [SP-004] | System Prompt | `prompts/SP-004-persona-scrum-master.md` | `roleDefinition` of the Scrum Master persona in `.roomodes` |
| [SP-005] | System Prompt | `prompts/SP-005-persona-developer.md` | `roleDefinition` of the Developer persona in `.roomodes` |
| [SP-006] | System Prompt | `prompts/SP-006-persona-qa-engineer.md` | `roleDefinition` of the QA Engineer persona in `.roomodes` |
| [SP-007] | System Prompt | `prompts/SP-007-gem-gemini-roo-agent.md` | Instructions for the Gemini Gem "Roo Code Agent" â€” manual deployment outside Git |
| [SP-008] | System Prompt | `prompts/SP-008-synthesizer-agent.md` | Synthesizer Agent for complex multi-perspective analysis |
| [SP-009] | System Prompt | `prompts/SP-009-devils-advocate-agent.md` | Devil's Advocate Agent for challenging assumptions |
| [SP-010] | System Prompt | `prompts/SP-010-librarian-agent.md` | Librarian Agent for cold archive indexing |
| [OLLAMA] | External tool | https://ollama.com | Local LLM inference engine â€” exposes an OpenAI-compatible REST API on `calypso:11434` |
| [FASTAPI] | Python library | https://fastapi.tiangolo.com | Python ASGI web framework used for the proxy server |
| [UVICORN] | Python library | https://www.uvicorn.org | Production ASGI server for FastAPI |
| [PYPERCLIP] | Python library | https://pypi.org/project/pyperclip | Windows clipboard management from Python |
| [ANTHROPIC] | External API | https://api.anthropic.com | Official Anthropic API â€” direct connection endpoint for Cloud Mode |
| [GEMINI] | External interface | https://gemini.google.com | Google's Gemini web interface â€” used in Chrome Proxy Mode |
| [ROOCODE] | VS Code extension | Roo Code (VS Code extension) | Central agentic execution engine â€” orchestrates all components via XML tags |
| [OPENROUTER] | External service | https://openrouter.ai | LLM routing service for minimax default backend |

### Appendix B â€” RBAC Permission Matrix (Complete)

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| `read` (read all files) | âœ… | âœ… | âœ… | âœ… |
| `edit` `memory-bank/productContext.md` | âœ… | âœ… | âœ… | âŒ |
| `edit` `memory-bank/*.md` (all) | âŒ | âœ… | âœ… | âŒ |
| `edit` `docs/releases/*.md` (Frozen) | âŒ | âŒ | âŒ | âŒ |
| `edit` `docs/releases/vX.Y/*.md` (Draft) | âœ… | âŒ | âŒ | âŒ |
| `edit` `docs/ideas/*.md` | âœ… | âœ… | âœ… | âŒ |
| `edit` `docs/qa/*.md` (QA reports) | âŒ | âŒ | âŒ | âœ… |
| `edit` source code (all files) | âŒ | âŒ | âœ… | âŒ |
| `command` general terminal | âŒ | âŒ | âœ… | âŒ |
| `command` Git only | âŒ | âœ… | âœ… | âŒ |
| `command` tests only | âŒ | âŒ | âœ… | âœ… |
| `browser` browser access | âŒ | âŒ | âœ… | âœ… |
| `mcp` MCP access | âŒ | âŒ | âœ… | âŒ |

### Appendix C â€” GitFlow Branch Summary

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `main` | Production state. **Frozen.** Only receives merge commits from develop-vX.Y at release time. Tags mark releases. | Never deleted. Never committed to directly. |
| `develop` | **Wild mainline.** Ad-hoc features, experiments, quick fixes. No formal scope. | Long-lived. Never deleted. Always the base for develop-vX.Y. |
| `develop-vX.Y` | **Scoped backlog.** Created when IDEAs are formally triaged for vX.Y. All release-scope work lands here. | Created at release planning. Never deleted after merge â€” kept for traceability. |
| `feature/{IDEA-NNN}-{slug}` | Single feature or fix. | Branch from develop or develop-vX.Y, merge back via PR. Never deleted â€” kept for traceability. |
| `hotfix/vX.Y.Z` | Emergency production fix. | Branched from production tag on main. Merged to main and develop. Never deleted â€” kept for traceability. |

### Appendix D â€” RULE Summary

| RULE | Domain | Title |
|------|--------|-------|
| RULE 1 | Memory Bank | CHECKâ†’CREATEâ†’READâ†’ACT sequence |
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
| R-CANON-* | Docs | Canonical docs GitFlow rules |

### Appendix E â€” Artifact ID Reference

| Type | Format | Example |
|------|--------|---------|
| Business Idea | `IDEA-{YYYY-MM-DD}-{NNN}` | IDEA-2026-04-01-001 |
| Technical Suggestion | `TECH-{YYYY-MM-DD}-{NNN}` | TECH-2026-04-01-001 |
| Architecture Decision | `ADR-{YYYY-MM-DD}-{NNN}` | ADR-2026-04-01-001 |
| Session | `s{YYYY-MM-DD}-{mode}-{NNN}` | s2026-04-01-developer-001 |
| Refinement Session | `REF-{YYYY-MM-DD}-{NNN}` | REF-2026-04-01-001 |
| Conversation | `{YYYY-MM-DD}-{source}-{slug}` | 2026-04-01-gemini-workbench |
| Batch Job | `BATCH-{YYYY-MM-DD}-{NNNN}` | BATCH-2026-04-01-0001 |
| Expert Report | `RPT-{YYYY-MM-DD}-{NNNN}` | RPT-2026-04-01-0001 |
| Enhancement | `ENH-{YYYY-MM-DD}-{NNN}` | ENH-2026-04-01-001 |
| Checkpoint | `CHECKPOINT-{YYYY-MM-DD}-{NNN}` | CHECKPOINT-2026-04-01-001 |
