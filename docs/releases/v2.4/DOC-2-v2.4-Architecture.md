---
doc_id: DOC-2
release: v2.4
status: Draft
title: Architecture Document
version: 1.0
date_created: 2026-03-30
authors: [Architect mode, Human]
previous_release: none
cumulative: true
---

# DOC-2 -- Architecture Document (v2.4)

> **Status: DRAFT** -- This document is in draft for v2.4.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all architecture from v1.0 through v2.4.
> To understand the full project architecture, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

---
doc_id: DOC-2
release: v2.3
status: Frozen
title: Architecture Document
version: 1.0
date_created: 2026-03-29
date_frozen: 2026-03-29
authors: [Architect mode, Human]
previous_release: none
cumulative: true
---

# DOC-2 — Architecture Document (v2.3)

> **Status: FROZEN** -- v2.3.0 release
> **Cumulative: YES** — This document contains all architecture from v1.0 through v2.3.
> To understand the full project architecture, read this document from top to bottom.
> Do not rely on previous release documents — they are delta-based and incomplete.

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
9. [Appendices](#9-appendices)

---

## 1. Guiding Principle

**Roo Code is the sole and unique agentic execution engine.** All other components (local LLM engine, clipboard proxy, cloud API, Memory Bank, Agile personas) are **service providers** that interface with Roo Code via standardized protocols.

This principle guarantees that:
- Roo Code's behavior is never modified, regardless of the LLM source used.
- Switching between the three backends (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) is transparent to Roo Code — only the "API Provider" parameter changes.
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
+--------+------------------+    +--------------+------+--------+
|  LINUX SERVER "calypso"   |    |  GEMINI CHROME (Chrome/pc)  |
|  RTX 5060 Ti 16 GB        |    |  (Dedicated Roo Code Gem)   |
|  Ollama + uadf-agent      |    +-----------------------------+
|  + qwen3:8b               |
|  API: calypso:11434       |    +-----------------------+
+---------------------------+    |  ANTHROPIC CLOUD      |
                                  |  api.anthropic.com    |
                                  |  claude-sonnet-4-6    |
                                  +-----------------------+

+-----------------------------------------------------------------------------------+
|                       MEMORY BANK (File System)                                   |
|   Works identically in all 3 modes — Git versioned                                |
|                                                                                   |
|  memory-bank/                                                                     |
|  +-- projectBrief.md      (Vision & Non-Goals)                                    |
|  +-- productContext.md    (User Stories & Business Value)                         |
|  +-- systemPatterns.md    (Architecture & Conventions)                             |
|  +-- techContext.md       (Stack & Commands for all 3 modes)                      |
|  +-- activeContext.md     (Current Task - Working Memory)                         |
|  +-- progress.md          (Phase & Feature Checklist)                             |
|  +-- decisionLog.md       (ADR - Architecture Decision Records)                   |
+-----------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------+
|                       PROMPT REGISTRY (prompts/)                                  |
|   Single source of truth for all system prompts — Git versioned                   |
|                                                                                   |
|  prompts/                                                                         |
|  +-- README.md             (Registry index)                                       |
|  +-- SP-001-ollama-modelfile-system.md   -> Modelfile[SYSTEM]                     |
|  +-- SP-002-clinerules-global.md         -> .clinerules (entire file)             |
|  +-- SP-003-persona-product-owner.md    -> .roomodes[product-owner]              |
|  +-- SP-004-persona-scrum-master.md     -> .roomodes[scrum-master]               |
|  +-- SP-005-persona-developer.md        -> .roomodes[developer]                   |
|  +-- SP-006-persona-qa-engineer.md      -> .roomodes[qa-engineer]                |
|  +-- SP-007-gem-gemini-roo-agent.md     -> gemini.google.com (OUTSIDE GIT)       |
+-----------------------------------------------------------------------------------+
```

---

## 3. Detailed Technical Stack

### 3.1 Interface & Orchestration Layer

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **IDE** | Visual Studio Code | Latest stable | Primary development environment |
| **Agentic Extension** | Roo Code | Latest stable | Agentic execution engine, LLM ↔ file system bridge |
| **Agile Personas** | JSON (`.roomodes`) | — | Definition of the 4 personas and their RBAC permissions |
| **Session Directives** | Markdown (`.clinerules`) | — | Imperative rules injected into each session |

### 3.2 Local LLM Engine Layer (Sovereign Mode — `calypso` Server)

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **Inference Server** | Linux headless `calypso` | Ubuntu/Debian | Ollama host — RTX 5060 Ti 16 GB VRAM |
| **Private Network** | Tailscale | Latest stable | Mesh VPN connecting `pc` (Windows) and `calypso` (Linux) |
| **Inference Engine** | Ollama | Latest stable | VRAM management, weight loading, REST API |
| **Main Model** | `mychen76/qwen3_cline_roocode:14b` | 14B quantized | Main brain, fine-tuned for Roo Code Tool Calling |
| **Secondary Model** | `qwen3:8b` | 8B | Delegated agent for lightweight tasks (Boomerang Tasks) |
| **Model Configuration** | Ollama `Modelfile` | — | Lock T=0.15, Min_P=0.03, num_ctx=131072 |
| **Listening Address** | `calypso:11434` | — | OpenAI-compatible REST API, accessible via Tailscale from `pc` |

### 3.3 Gemini Chrome Proxy Layer (Hybrid Mode)

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.10+ | Proxy server language |
| **Web Framework** | FastAPI | 0.110+ | Lightweight ASGI server, OpenAI API emulation + SSE |
| **ASGI Server** | Uvicorn | 0.29+ | Production server for FastAPI |
| **Clipboard Management** | Pyperclip | 1.8+ | Windows clipboard read/write |
| **Async Management** | asyncio (Python stdlib) | — | Non-blocking polling loop |
| **Streaming** | StreamingResponse (FastAPI) | — | SSE response in a single chunk for Roo Code compatibility |
| **Listening Port** | `localhost:8000` | — | Entry point for Roo Code in proxy mode |
| **Virtual Environment** | venv (Python stdlib) | — | Dependency isolation |

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
| **Endpoint** | `https://api.anthropic.com` | — | Official Anthropic HTTPS entry point |
| **Authentication** | API key (`sk-ant-api03-...`) | — | Stored in VS Code SecretStorage via Roo Code |
| **Roo Code Provider** | "Anthropic" (native) | — | Provider integrated in Roo Code, no middleware |

### 3.7 Prompt Consistency Verification Layer

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Verification script** | PowerShell (`check-prompts-sync.ps1`) | Normalized comparison of canonical SPs vs deployed artifacts |
| **Git Hook** | Shell script (`.git/hooks/pre-commit`) | Automatic script call before each commit |
| **Registry** | `prompts/` directory (Markdown + YAML) | Single source of truth for all system prompts |

---

## 4. Architecture Decisions (v1.0)

### DA-001 — `.roomodes` as central registry of Agile personas

**Decision:** The `.roomodes` file is the central registry of Agile personas. It defines for each role: its unique identifier (`slug`), its display name, its `roleDefinition` (behavioral system prompt), and its permission `groups`. This file is static and versioned in Git.

**Justification:** Clear separation between configuration (`.roomodes`) and behavior (`.clinerules`). The `roleDefinition` is the source of truth for each persona's behavior.

**Requirements addressed:** REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4

### DA-002 — `.clinerules` as universal session trigger

**Decision:** The `.clinerules` file contains imperative rules injected above each user prompt, forcing the agent to follow the CHECK→CREATE→READ→ACT sequence for the Memory Bank, to version under Git, and to maintain prompt registry consistency. These directives are unconditional and apply to all modes.

**Justification:** `.clinerules` is the universal safety net. Even if a persona forgets its own rule, `.clinerules` systematically reminds it at each session.

**Requirements addressed:** REQ-4.2, REQ-4.3, REQ-7.3

### DA-003 — Memory Bank segmented into 7 thematic files

**Decision:** The Memory Bank is segmented into 7 thematic files to avoid contextual pollution and optimize LLM attention. Each file has a unique and non-overlapping responsibility.

**Justification:** A monolithic file would force the LLM to load all memory at each session. Segmentation allows loading only the relevant files according to the task.

**Requirements addressed:** REQ-4.4

### DA-004 — Modelfile with locked determinism parameters

**Decision:** The model `mychen76/qwen3_cline_roocode:14b` is compiled with a custom `Modelfile` locking: `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`, `num_ctx 131072`, `num_gpu 99`, `num_thread 8`. These values cannot be modified at runtime. The Modelfile is compiled on `calypso` via `ollama create uadf-agent -f Modelfile`.

**Justification:** Maximum determinism eliminates hallucinations during code generation. The 128K token window allows simultaneous loading of the project and the Memory Bank. `num_gpu 99` exploits the 16 GB of VRAM of `calypso`'s RTX 5060 Ti.

**Requirements addressed:** REQ-1.2, REQ-1.3

### DA-005 — Boomerang Tasks for delegation to lightweight models

**Decision:** Roo Code's "Boomerang Tasks" workflow is used to delegate repetitive or voluminous tasks (log analysis, unit test generation) to the secondary model `qwen3:8b`, also hosted on `calypso`.

**Justification:** VRAM optimization and acceleration of repetitive cycles. The 14B model remains available for complex decisions. Both models share the same Ollama instance on `calypso`.

**Requirements addressed:** REQ-1.4

> **PROXY MODE LIMITATION:** Boomerang Tasks are not supported in Gemini Proxy Mode.
> The proxy is a single endpoint shared by all Roo Code instances — concurrent requests
> from the main agent and the sub-agent create a clipboard conflict (deadlock).
> **Use Local Mode (Ollama) or Cloud Mode (Claude API) for tasks requiring sub-agents.**

### DA-006 — FastAPI + asyncio for the proxy

**Decision:** FastAPI is chosen over Flask for its native asynchronism management (asyncio), essential for keeping the HTTP connection open while waiting for human intervention (clipboard polling) without blocking the server.

**Justification:** Flask is synchronous by default — it would block the server during polling. FastAPI with asyncio keeps the server responsive (`/health` endpoint responds during polling).

**Requirements addressed:** REQ-2.3.1, REQ-2.1.1

### DA-007 — OpenAI Chat Completions format emulation

**Decision:** The proxy exactly emulates the OpenAI Chat Completions API format (`/v1/chat/completions`). This decision guarantees native compatibility with Roo Code configured in "OpenAI Compatible" mode, without any modification to Roo Code's source code.

**Justification:** Roo Code natively supports the OpenAI format. By emulating this format, the proxy is transparent to Roo Code.

**Requirements addressed:** REQ-2.1.2, REQ-2.4.2

### DA-008 — "Dedicated Gem" mode with system prompt filtering

**Decision:** The proxy implements a `USE_GEM_MODE=true` mode (default) that filters the `system` message when copying to the clipboard. When this mode is active, only `user` and `assistant` messages are transmitted.

**Justification:** Roo Code's system prompt represents several thousand tokens. By storing it in the Gemini Gem (SP-007), we avoid retransmitting it with each request, reducing transfer size by 50%+.

**Requirements addressed:** REQ-2.1.4

### DA-009 — Cleaning of base64 content

**Decision:** The proxy detects and replaces `{"type": "image_url", ...}` elements with the message `[IMAGE OMITTED - Not supported by clipboard proxy]`.

**Justification:** Base64 images can represent hundreds of KB. Their presence in the clipboard would make transfer impossible. Replacing them with a text message preserves context without blocking the flow.

**Requirements addressed:** REQ-2.1.5

### DA-010 — Gemini Gem with integrated Roo Code system prompt

**Decision:** A dedicated "Gem" is created in Gemini Web with the entirety of the Roo Code system prompt (SP-007). This approach avoids retransmitting the system prompt with each request via the clipboard.

**Justification:** The Roo Code system prompt is static and does not change between requests. Storing it in the Gem once is more efficient than retransmitting it with each exchange.

**Requirements addressed:** REQ-5.1, REQ-5.2

### DA-011 — Native Anthropic provider in Roo Code for Cloud Mode

**Decision:** The connection to the Anthropic API uses the native "Anthropic" provider integrated in Roo Code. The reference model is `claude-sonnet-4-6`. The API key is stored in VS Code SecretStorage, never in project files.

**Justification:** The native provider guarantees full compatibility with streaming, vision, and Claude's native tool use.
### DA-012 — Centralized system prompt registry in `prompts/`

**Decision:** A versioned `prompts/` directory contains a canonical copy of each system prompt with YAML metadata (target, version, dependencies, changelog). RULE 6 in `.clinerules` enforces consistency before each commit. SP-007 (Gemini Gem) is marked `hors_git: true` with documented manual deployment procedure.

**Justification:** System prompts are scattered across multiple artifacts (.roomodes JSON, .clinerules text, compiled Modelfile, external Gemini Web). Without a centralized registry, a modification to `.clinerules` can make the Gemini Gem inconsistent without anyone noticing.

**Requirements addressed:** REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5

### DA-013 — Automatic verification via PowerShell script + Git pre-commit hook

**Decision:** A script `scripts/check-prompts-sync.ps1` compares deployed content with canonical SPs via normalized comparison (encoding correction `\r\n`/`\n`, JSON deserialization for `.roomodes`, robust extraction regex). A Git hook `.git/hooks/pre-commit` calls this script automatically and blocks the commit if desynchronization is detected. SP-007 is excluded from automatic verification with a manual verification warning.

**Justification:** RULE 6 being a behavioral directive, it can be ignored by an LLM agent. The pre-commit hook transforms verification into a non-bypassable technical constraint.

**Requirements addressed:** REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4

### DA-014 — SSE streaming in a single chunk for the proxy

**Decision:** The proxy implements SSE (Server-Sent Events) streaming by returning the Gemini response in a single SSE chunk followed by `data: [DONE]`. If the request contains `"stream": false`, a complete non-streamed JSON response is returned. The proxy automatically detects the mode via the `stream` field of the request.

**Justification:** Roo Code can send requests with `stream: true` (default behavior in some versions). Without SSE support, the proxy would return a non-streamed JSON response that Roo Code might reject while expecting SSE format. The single-chunk SSE implementation is transparent to Roo Code regardless of its configuration.

**Requirements addressed:** REQ-2.4.1, REQ-2.4.3

---

## 5. Functional Layer Architecture

### Layer A — Behavioral Orchestration (`.roomodes` & `.clinerules`)

**RBAC Permission Matrix (DA-001):**

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| `read` (read all files) | ✅ | ✅ | ✅ | ✅ |
| `edit` `memory-bank/productContext.md` | ✅ | ✅ | ✅ | ❌ |
| `edit` `memory-bank/*.md` (all) | ❌ | ✅ | ✅ | ❌ |
| `edit` `docs/*.md` (documentation) | ✅ | ✅ | ✅ | ❌ |
| `edit` `docs/qa/*.md` (QA reports) | ❌ | ❌ | ❌ | ✅ |
| `edit` source code (all files) | ❌ | ❌ | ✅ | ❌ |
| `command` general terminal | ❌ | ❌ | ✅ | ❌ |
| `command` Git only | ❌ | ✅ | ✅ | ❌ |
| `command` tests only | ❌ | ❌ | ✅ | ✅ |
| `browser` browser access | ❌ | ❌ | ✅ | ✅ |
| `mcp` MCP access | ❌ | ❌ | ✅ | ❌ |

**Git commands authorized for Scrum Master:** `git add`, `git commit`, `git status`, `git log`
**Test commands authorized for QA Engineer:** `npm test`, `npm run test`, `pytest`, `python -m pytest`, `dotnet test`, `go test`, `git status`, `git log`

---

### Layer B — Memory Bank (Markdown Files)

**Structure and Responsibilities of the 7 Files (DA-003):**

| File | Read Frequency | Write Frequency | Content |
| :--- | :--- | :--- | :--- |
| `projectBrief.md` | Project start | Rare | Vision, objectives, Non-Goals, constraints |
| `productContext.md` | Sprint start | Per sprint | User Stories, business value, backlog |
| `systemPatterns.md` | Before architecture modification | After architecture decision | Folder structure, conventions, patterns |
| `techContext.md` | Before build/test command | After dependency change | Stack, versions, commands, env variables |
| `activeContext.md` | **At each session startup** | **At each task end** | Current task, last result, next action |
| `progress.md` | **At each session startup** | **At each feature validation** | Workbench phase checklist, completed/in-progress features |
| `decisionLog.md` | Before architecture decision | After architecture decision | Timestamped ADRs with context, decision, consequences |

**Mandatory sequence at session startup (DA-002, REQ-4.2):**
```
1. CHECK existence of activeContext.md and progress.md
2. If absent → CREATE from .clinerules templates (immediately)
3. READ activeContext.md then progress.md
4. ACT on the user request
```

---

### Layer C — Local LLM Engine (Ollama + Qwen3)

**`Modelfile` content (DA-004):**
```dockerfile
FROM mychen76/qwen3_cline_roocode:14b

# Determinism parameters (anti-hallucination) — REQ-1.3
PARAMETER temperature 0.15
PARAMETER min_p 0.03
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.1

# Maximum context window (128K tokens) — REQ-1.2
PARAMETER num_ctx 131072

# GPU performance parameters
PARAMETER num_gpu 99
PARAMETER num_thread 8

SYSTEM """
Tu es un agent de developpement logiciel expert integre dans Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank (memory-bank/) avant d'agir.
Tu dois toujours mettre a jour la Memory Bank apres chaque tache.
Apres chaque tache significative, tu dois effectuer un commit Git avec un message descriptif.
"""
```

---

### Layer D — Gemini Chrome Proxy (FastAPI + Pyperclip + SSE)

**Detailed Data Flow:**
```
STEP 1 — RECEPTION (Roo Code -> Proxy)
POST http://localhost:8000/v1/chat/completions
{ "model": "gemini-manual", "messages": [...], "stream": true|false }

STEP 2 — EXTRACTION & FORMATTING
If USE_GEM_MODE=true: ignore role:system
Clean base64 images → [IMAGE OMITTED...]
Format: [USER]\n{content}\n\n---\n\n[ASSISTANT]\n{content}

STEP 3 — UPLINK
pyperclip.copy(formatted_prompt)
hash_initial = md5(formatted_prompt)
Console: numbered instructions for the user

STEP 4 — ASYNCHRONOUS POLLING
while True:
  await asyncio.sleep(1.0)
  if md5(pyperclip.paste()) != hash_initial: break
  if elapsed > 300s: raise HTTP 408

STEP 5 — VALIDATION
Check presence of Roo Code XML tags (warning if absent, non-blocking)

STEP 6 — RE-INJECTION
If stream=true  → SSE: data:{chunk}\n\ndata:{done}\n\ndata:[DONE]\n\n
If stream=false → JSON: {"id":..., "choices":[{"message":{"content":"..."}}]}
```

**Complete `proxy.py` v2.0 code (DA-006, DA-007, DA-008, DA-009, DA-014):**

```python
"""
le workbench Proxy v2.0 — Roo Code <-> Gemini Chrome Bridge
Supports stream=true (SSE) and stream=false (complete JSON).
Requirements: REQ-2.1.1 to REQ-2.4.4
"""
import asyncio, hashlib, json, os, time, uuid
from datetime import datetime
from typing import AsyncGenerator, List, Optional, Union

import pyperclip, uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

USE_GEM_MODE = os.getenv("USE_GEM_MODE", "true").lower() == "true"
POLLING_INTERVAL = float(os.getenv("POLLING_INTERVAL", "1.0"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "300"))
PORT = int(os.getenv("PROXY_PORT", "8000"))

ROO_XML_TAGS = [
    "<write_to_file>", "<read_file>", "<execute_command>",
    "<attempt_completion>", "<ask_followup_question>", "<replace_in_file>",
    "<list_files>", "<search_files>", "<browser_action>", "<new_task>"
]

class MessageContent(BaseModel):
    role: str
    content: Union[str, list]

class ChatRequest(BaseModel):
    model: str
    messages: List[MessageContent]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

app = FastAPI(title="le workbench Proxy", version="2.0.0")

def _hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def _clean_content(content) -> str:
    """Cleans content: removes base64 images. REQ-2.1.5"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif item.get("type") == "image_url":
                    parts.append("[IMAGE OMITTED - Not supported by clipboard proxy]")
                else:
                    parts.append(str(item))
        return "\n".join(parts)
    return str(content)

def _format_prompt(messages: List[MessageContent]) -> str:
    """Formats messages into readable text. REQ-2.1.3, REQ-2.1.4, REQ-2.2.2"""
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if not content.strip():
            continue
        if msg.role == "system":
            if USE_GEM_MODE:
                continue
            parts.append("[SYSTEM PROMPT]\n" + content)
        elif msg.role == "user":
            parts.append("[USER]\n" + content)
        elif msg.role == "assistant":
            parts.append("[ASSISTANT]\n" + content)
    return "\n\n---\n\n".join(parts)

def _validate_response(text: str) -> bool:
    """Checks for presence of Roo Code XML tags. REQ-2.3.4"""
    return any(tag in text for tag in ROO_XML_TAGS)

def _build_json_response(content: str, model: str) -> dict:
    """Builds an OpenAI JSON response. REQ-2.4.2"""
    return {
        "id": "chatcmpl-proxy-" + uuid.uuid4().hex[:8],
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }

async def _stream_response(content: str, model: str) -> AsyncGenerator[str, None]:
    """Generates an SSE response in a single chunk. REQ-2.4.1, DA-014"""
    rid = "chatcmpl-proxy-" + uuid.uuid4().hex[:8]
    ts = int(time.time())
    chunk = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
             "choices": [{"index": 0, "delta": {"role": "assistant", "content": content}, "finish_reason": None}]}
    yield f"data: {json.dumps(chunk)}\n\n"
    done = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}
    yield f"data: {json.dumps(done)}\n\n"
    yield "data: [DONE]\n\n"

async def _wait_clipboard(initial_hash: str, ts: str) -> str:
    """Waits for the Gemini response in the clipboard. REQ-2.3.1, REQ-2.3.2, REQ-2.3.3"""
    start = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)
        current = pyperclip.paste()
        if _hash(current) != initial_hash:
            elapsed = time.time() - start
            print(f"[{ts}] RESPONSE DETECTED! {len(current)} chars in {elapsed:.1f}s")
            if not _validate_response(current):
                print(f"[{ts}] WARNING: No Roo Code XML tags detected.")
            return current
        if time.time() - start > TIMEOUT_SECONDS:
            raise HTTPException(status_code=408, detail="Timeout: Relancez votre requete dans Roo Code.")

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Main entry point. REQ-2.1.1, REQ-2.1.2"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*60}\n[{ts}] REQUEST | model: {request.model} | stream: {request.stream}")
    formatted = _format_prompt(request.messages)
    pyperclip.copy(formatted)
    initial_hash = _hash(formatted)
    print(f"[{ts}] {'GEM MODE' if USE_GEM_MODE else 'FULL MODE'} | {len(formatted)} chars")
    print(f"[{ts}] PROMPT COPIED! ACTION: 1.Chrome 2.Gem 3.Ctrl+V 4.Wait 5.Ctrl+A+C")
    print(f"         Timeout in {TIMEOUT_SECONDS}s...")
    response_text = await _wait_clipboard(initial_hash, ts)
    if request.stream:
        return StreamingResponse(_stream_response(response_text, request.model), media_type="text/event-stream")
    return JSONResponse(content=_build_json_response(response_text, request.model), status_code=200)

@app.get("/v1/models")
async def list_models():
    return JSONResponse({"object": "list", "data": [{"id": "gemini-manual", "object": "model", "created": int(time.time()), "owned_by": "uadf-proxy"}]})

@app.get("/health")
async def health_check():
    return {"status": "ok", "proxy": "le workbench", "version": "2.0.0", "gem_mode": USE_GEM_MODE}

if __name__ == "__main__":
    print(f"{'='*60}\n  le workbench PROXY v2.0 | http://localhost:{PORT}/v1\n  Mode: {'GEM' if USE_GEM_MODE else 'FULL'} | Timeout: {TIMEOUT_SECONDS}s\n{'='*60}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
```

---

### Layer E — Gemini Chrome Configuration (Dedicated Gem)

**Content of the System Prompt for the "Roo Code Agent" Gem (SP-007):**
```
You are the coding agent integrated in Roo Code, an AI assistant expert in software development.

ABSOLUTE AND NON-NEGOTIABLE RULES:
1. You MUST ALWAYS respond using Roo Code XML tags.
2. You must NEVER generate courtesy text, introductions, or conclusions.
3. You must NEVER explain what you are going to do: you do it directly with XML tags.
4. You must treat each message as a direct instruction to execute.
5. If you need additional information, use ask_followup_question.

AVAILABLE XML TAGS:
- write_to_file (path + content): create or write a complete file
- read_file (path): read a file
- execute_command (command): execute a terminal command
- replace_in_file (path + diff): modify part of a file
- list_files (path): list files in a folder
- search_files (path + regex): search in files
- attempt_completion (result): signal task completion
- ask_followup_question (question): ask the user a question

REMINDER: No text before the first XML tag. No text after the last XML tag.
```

---

### Layer F — Prompt Registry (`prompts/`)

| SP File | Deployment Target | Target Field | Outside Git |
| :--- | :--- | :--- | :---: |
| `SP-001-ollama-modelfile-system.md` | `Modelfile` | `SYSTEM """..."""` block | No |
| `SP-002-clinerules-global.md` | `.clinerules` | Entire file | No |
| `SP-003-persona-product-owner.md` | `.roomodes` | `customModes[0].roleDefinition` | No |
| `SP-004-persona-scrum-master.md` | `.roomodes` | `customModes[1].roleDefinition` | No |
| `SP-005-persona-developer.md` | `.roomodes` | `customModes[2].roleDefinition` | No |
| `SP-006-persona-qa-engineer.md` | `.roomodes` | `customModes[3].roleDefinition` | No |
| `SP-007-gem-gemini-roo-agent.md` | `gemini.google.com > Gems > Instructions` | Gem Instructions | **Yes** |
---

## 6. Architecture / Feature / Requirement Traceability Matrix

| Architectural Component | Layer | Feature | Decisions | PRD Requirements |
| :--- | :--- | :--- | :--- | :--- |
| **VS Code + Roo Code** | Interface | Central agentic execution engine | — | REQ-000 |
| **`.roomodes`** | Orchestration | JSON registry of 4 Agile personas with RBAC | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4 |
| **`.clinerules`** | Orchestration | Imperative rules: Memory Bank, Git, Prompt Consistency | DA-002 | REQ-4.2, REQ-4.3, REQ-7.3 |
| **Persona `product-owner`** | Orchestration | User Story writing, doc reading, code refusal | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3 |
| **Persona `scrum-master`** | Orchestration | Agile facilitation, Memory Bank, Git only, no tests | DA-001 | REQ-3.1, REQ-3.2, REQ-3.4 |
| **Persona `developer`** | Orchestration | Full implementation, code + terminal + Git | DA-001 | REQ-3.1, REQ-3.2 |
| **Persona `qa-engineer`** | Orchestration | Tests + QA reports, no source code modification | DA-001 | REQ-3.1, REQ-3.2 |
| **Ollama (Linux daemon `calypso`)** | Local LLM Engine | Private network inference, OpenAI REST API on calypso:11434 (Tailscale) | — | REQ-1.0, REQ-000 |
| **`mychen76/qwen3_cline_roocode:14b`** | Local LLM Engine | Main model fine-tuned for Roo Code Tool Calling | DA-004 | REQ-1.1 |
| **`Modelfile` (T=0.15, num_ctx=131072)** | Local LLM Engine | Determinism + 128K token context window | DA-004 | REQ-1.2, REQ-1.3 |
| **`qwen3:8b` + Boomerang Tasks** | Local LLM Engine | Delegation of lightweight tasks to secondary model | DA-005 | REQ-1.4 |
| **`proxy.py` — POST `/v1/chat/completions`** | Hybrid Proxy | Single entry point, Roo Code request interception | DA-006, DA-007 | REQ-2.1.1, REQ-2.1.2 |
| **`proxy.py` — `_format_prompt()`** | Hybrid Proxy | Payload extraction, system prompt filtering (GEM MODE) | DA-008 | REQ-2.1.3, REQ-2.1.4 |
| **`proxy.py` — `_clean_content()`** | Hybrid Proxy | Base64 image cleaning, replacement with text message | DA-009 | REQ-2.1.5 |
| **`proxy.py` — `pyperclip.copy()`** | Hybrid Proxy | Injection of formatted prompt into Windows clipboard | — | REQ-2.2.1 |
| **`proxy.py` — `[USER]`, `[ASSISTANT]` separators** | Hybrid Proxy | Readable format with explicit separators | DA-008 | REQ-2.2.2 |
| **`proxy.py` — Timestamped console messages** | Hybrid Proxy | User notification with timestamp and 5 instructions | — | REQ-2.2.3 |
| **`proxy.py` — `asyncio` loop + `pyperclip.paste()`** | Hybrid Proxy | Non-blocking asynchronous polling every second | DA-006 | REQ-2.3.1 |
| **`proxy.py` — MD5 hash comparison** | Hybrid Proxy | Clipboard change detection | — | REQ-2.3.2 |
| **`proxy.py` — 300s timeout + HTTP 408** | Hybrid Proxy | Non-response user management | — | REQ-2.3.3 |
| **`proxy.py` — `_validate_response()`** | Hybrid Proxy | Verification of Roo Code XML tag presence (non-blocking warning) | — | REQ-2.3.4 |
| **`proxy.py` — `_stream_response()` (SSE)** | Hybrid Proxy | SSE response in a single chunk if `stream=true` | DA-014 | REQ-2.4.1, REQ-2.4.3 |
| **`proxy.py` — `_build_json_response()`** | Hybrid Proxy | Complete OpenAI JSON response if `stream=false` | DA-007 | REQ-2.4.2, REQ-2.4.3 |
| **`proxy.py` — Raw content transmission** | Hybrid Proxy | Gemini content transmitted as-is without modification | — | REQ-2.4.4 |
| **`memory-bank/`** | Memory | Contextual memory container, integrated with Git | DA-003 | REQ-4.1, REQ-4.5 |
| **`memory-bank/activeContext.md`** | Memory | Session working memory, read and written at each session | DA-002, DA-003 | REQ-4.2, REQ-4.3, REQ-4.4 |
| **`memory-bank/progress.md`** | Memory | Workbench phase and product feature checklist | DA-002, DA-003 | REQ-4.2, REQ-4.3, REQ-4.4 |
| **`memory-bank/projectBrief.md`** | Memory | Vision, objectives, Non-Goals, constraints | DA-003 | REQ-4.4 |
| **`memory-bank/productContext.md`** | Memory | User Stories, business value, backlog | DA-003 | REQ-4.4 |
| **`memory-bank/systemPatterns.md`** | Memory | Architecture, conventions, technical patterns | DA-003 | REQ-4.4 |
| **`memory-bank/techContext.md`** | Memory | Stack, versions, commands, env variables | DA-003 | REQ-4.4 |
| **`memory-bank/decisionLog.md`** | Memory | Timestamped ADRs after each architecture decision | DA-003 | REQ-4.4, REQ-4.5 |
| **Gemini Gem "Roo Code Agent"** | Gemini Config | Dedicated profile with complete Roo Code system prompt (SP-007) | DA-010 | REQ-5.1, REQ-5.2 |
| **Gem instructions (XML tags)** | Gemini Config | Strict rules enforcing XML-only responses, no extraneous text | DA-010 | REQ-5.2 |
| **Conversation history in clipboard** | Gemini Config | Multi-turn history transmission for response coherence | DA-008 | REQ-5.3 |
| **"Anthropic" provider in Roo Code** | Direct Cloud | Direct connection to api.anthropic.com without proxy | DA-011 | REQ-6.3 |
| **Anthropic API key (VS Code SecretStorage)** | Direct Cloud | Anthropic authentication, stored encrypted, never in Git | DA-011 | REQ-6.1, REQ-6.4 |
| **Model `claude-sonnet-4-6`** | Direct Cloud | High-quality Claude Sonnet model, native Roo Code | DA-011 | REQ-6.2 |
| **Roo Code Provider Switcher** | LLM Switcher | Switch between Ollama/Proxy/Anthropic without modifying Roo Code | DA-007, DA-011 | REQ-2.0 |
| **Variable `USE_GEM_MODE`** | Hybrid Proxy | Activates system prompt filtering when Gem is configured | DA-008 | REQ-2.1.4 |
| **`prompts/` directory** | Prompt Registry | Single source of truth for all system prompts | DA-012 | REQ-7.1 |
| **`prompts/SP-XXX-*.md` files** | Prompt Registry | Canonical files with YAML header (id, version, target, changelog) | DA-012 | REQ-7.1, REQ-7.2, REQ-7.4 |
| **`prompts/README.md`** | Prompt Registry | Registry index with ID/file/target/Outside Git table | DA-012 | REQ-7.2 |
| **RULE 6 in `.clinerules`** | Prompt Registry | Imperative directive: verify prompt consistency before commit | DA-012 | REQ-7.3 |
| **Flag `hors_git: true` in SP-007** | Prompt Registry | Manual deployment marker, triggers mandatory commit mention | DA-012 | REQ-7.5 |
| **`scripts/check-prompts-sync.ps1`** | Prompt Verification | Normalized comparison of canonical SPs vs artifacts, PASS/FAIL report with diff | DA-013 | REQ-8.1, REQ-8.3, REQ-8.4 |
| **`.git/hooks/pre-commit`** | Prompt Verification | Git hook calling check-prompts-sync.ps1, blocks commit if desync | DA-013 | REQ-8.2 |

---

## 7. v2.1 Architecture Additions

### 7.1 Delta from v2.0

v2.1 introduces **no architectural changes**. The architecture described in v1.0 above applies in full. This section documents additions made during v2.1.

### 7.2 RULE 10 — GitFlow Enforcement (ADR-006)

v2.1 formalized GitFlow with the following branch lifecycle (previously ad-hoc):

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `main` | Production state — frozen after each release tag | Never commit directly after tag |
| `develop` | Wild mainline — ad-hoc features, experiments, quick fixes | Long-lived, base for `develop-vX.Y` |
| `develop-vX.Y` | Scoped backlog — formal release scope | Created at release planning |
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

1. **IDEA-009 Architecture** — Generic Anthropic Batch API Toolkit (`scripts/batch/`)
2. **Template Bundle** — Self-contained `template/scripts/batch/` for new project deployment
3. **ADR-010 Ad-Hoc Governance** — Lightweight process for reactive ideas

### 8.2 IDEA-009 Architecture: Anthropic Batch API Toolkit

#### 8.2.1 Package Structure

**Location:** `scripts/batch/` (canonical), `template/scripts/batch/` (deployment bundle)

```
scripts/batch/
├── __init__.py           # Public re-exports
├── config.py             # BatchConfig dataclass + YAML loader
├── submit.py             # Batch submission
├── retrieve.py           # Result retrieval + markdown report
├── poll.py               # Polling utility
├── cli.py                # CLI entry point
├── generate.py           # Jinja2 script generator
└── templates/
    ├── batch_submit_script.py.j2
    └── batch_retrieve_script.py.j2
```

#### 8.2.2 Core Dataclass: BatchConfig

```python
@dataclass
class BatchConfig:
    name: str                      # Human-readable batch name
    model: str                     # Anthropic model (e.g., claude-sonnet-4-6)
    max_tokens: int                # Max tokens per response
    temperature: float              # Sampling temperature
    output_dir: pathlib.Path        # Where to save results
    requests: list[RequestSpec]    # List of individual requests
    batch_id_file: pathlib.Path | None = None  # Persistent batch_id
    workspace_root: pathlib.Path                   # For path resolution
```

**RequestSpec:**
```python
@dataclass
class RequestSpec:
    custom_id: str        # Unique identifier for this request
    method: str          # HTTP method (POST)
    url: str             # API endpoint
    headers: dict        # Request headers
    body: dict           # Request body
```

#### 8.2.3 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| YAML-based configuration | Human-readable, version-controllable batch definitions |
| File-based batch_id persistence | Batch ID survives terminal restarts; no in-memory state |
| Markdown fence stripping | API wraps JSON in ```json fences; must strip before parsing |
| Normalize "error" / "errored" | API inconsistency: both appear depending on failure mode |
| Raw response fallback | When text differs after parsing, save raw for debugging |
| CLI-first design | Works standalone without Python import; composable with shell |
| Jinja2 script generation | batch.yaml → submit.py + retrieve.py for repeatable runs |
| Self-contained template bundle | template/scripts/batch/ works independently, no parent delegation |

#### 8.2.4 CLI Commands

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

#### 8.2.5 Data Flow

```
batch.yaml
    └─> config.py (BatchConfig)
            ├─> submit.py --> Anthropic Batch API --> batch_id
            │                                    |
            |                                    v
            |                              batch_id_file
            |                                    |
            |                                    v
            └─> poll.py (loop) --> retrieve.py --> output_dir/
                                                       ├─ {custom_id}_raw.txt
                                                       └─ results.md
```

### 8.3 ADR-010 Ad-Hoc Governance Architecture

#### 8.3.1 Two Paths

| Aspect | [STRUCTURED] | [AD-HOC] |
|--------|-------------|-----------|
| Origin | Formal PRD | Reactive discovery |
| Process | Full DOC-1→DOC-2→DOC-3→Calypso→QA | Lightweight with release tier |
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

## 9. Appendices

### Appendix A — References Table

| Ref. | Type | Title / Identifier | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Internal document | `DOC-1-CURRENT.md` | Product Requirements Document — source of all REQ-xxx requirements |
| [DOC2] | Internal document | `DOC-2-CURRENT.md` | This document — Architecture, Solution and Technical Stack |
| [SP-001] | System Prompt | `prompts/SP-001-ollama-modelfile-system.md` | Ollama Modelfile system prompt — content of the `SYSTEM` block |
| [SP-002] | System Prompt | `prompts/SP-002-clinerules-global.md` | Canonical content of the `.clinerules` file |
| [SP-003] | System Prompt | `prompts/SP-003-persona-product-owner.md` | `roleDefinition` of the Product Owner persona in `.roomodes` |
| [SP-004] | System Prompt | `prompts/SP-004-persona-scrum-master.md` | `roleDefinition` of the Scrum Master persona in `.roomodes` |
| [SP-005] | System Prompt | `prompts/SP-005-persona-developer.md` | `roleDefinition` of the Developer persona in `.roomodes` |
| [SP-006] | System Prompt | `prompts/SP-006-persona-qa-engineer.md` | `roleDefinition` of the QA Engineer persona in `.roomodes` |
| [SP-007] | System Prompt | `prompts/SP-007-gem-gemini-roo-agent.md` | Instructions for the Gemini Gem "Roo Code Agent" — manual deployment outside Git |
| [OLLAMA] | External tool | https://ollama.com | Local LLM inference engine — exposes an OpenAI-compatible REST API on `calypso:11434` |
| [FASTAPI] | Python library | https://fastapi.tiangolo.com | Python ASGI web framework used for the proxy server |
| [UVICORN] | Python library | https://www.uvicorn.org | Production ASGI server for FastAPI |
| [PYPERCLIP] | Python library | https://pypi.org/project/pyperclip | Windows clipboard management from Python |
| [ANTHROPIC] | External API | https://api.anthropic.com | Official Anthropic API — direct connection endpoint for Cloud Mode |
| [GEMINI] | External interface | https://gemini.google.com | Google's Gemini web interface — used in Chrome Proxy Mode |
| [ROOCODE] | VS Code extension | Roo Code (VS Code extension) | Central agentic execution engine — orchestrates all components via XML tags |
| [OPENAI-FMT] | Standard | OpenAI Chat Completions Format v1 | `/v1/chat/completions` API standard emulated by the proxy |
| [ADR-006] | ADR | `memory-bank/hot-context/decisionLog.md` | GitFlow Branch Lifecycle decision record |
| [ADR-010] | ADR | `docs/ideas/ADR-010-dev-tooling-process-bypass.md` | Ad-Hoc Idea Governance decision record |

### Appendix B — Abbreviations Table

| Abbreviation | Full Form | Explanation |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Timestamped record of an architecture decision. Stored in `memory-bank/decisionLog.md`. |
| **API** | Application Programming Interface | Programming interface. Here: Ollama REST API (local), Anthropic HTTPS API (cloud), OpenAI API format (emulated by proxy). |
| **ASGI** | Asynchronous Server Gateway Interface | Python standard for asynchronous web servers. FastAPI + Uvicorn form the proxy's ASGI stack. |
| **DA** | Architecture Decision | Identifier for decisions in this document (DA-001 to DA-014). |
| **GEM** | Gemini Gem | Custom profile in Gemini Web containing a permanent system prompt. |
| **GPU** | Graphics Processing Unit | Graphics processor. `num_gpu 99` in the Modelfile delegates inference to the GPU. |
| **HTTP** | HyperText Transfer Protocol | Communication protocol. The proxy listens on HTTP `localhost:8000`. |
| **JSON** | JavaScript Object Notation | Structured data format. Used for `.roomodes`, OpenAI API responses, and proxy requests. |
| **LAAW** | Local Agentic Agile Workflow | Blueprint source for the segmented Memory Bank and Agile personas. |
| **LLM** | Large Language Model | Large language model. Three instances: Qwen3-14B (local), Gemini Pro (Google cloud), Claude Sonnet (Anthropic cloud). |
| **MCP** | Model Context Protocol | Roo Code extension protocol for external tools. Accessible only to the Developer persona. |
| **MD5** | Message Digest 5 | Hashing algorithm. Used by the proxy to detect clipboard changes. |
| **PRD** | Product Requirements Document | Product requirements document. DOC-1 is the workbench PRD. |
| **RBAC** | Role-Based Access Control | Role-based access control. Matrix defined in Layer A section. |
| **REQ** | Requirement | Identifier for requirements in DOC-1 (e.g.: REQ-2.1.4). |
| **REST** | Representational State Transfer | Web API architectural style. Ollama exposes a REST API on `calypso:11434`. |
| **SP** | System Prompt | Canonical file from the `prompts/` registry with YAML metadata. |
| **SSE** | Server-Sent Events | Server→client HTTP streaming protocol. The proxy returns Gemini responses in SSE when `stream: true`. |
| **VRAM** | Video Random Access Memory | GPU memory. Qwen3-14B requires 8+ GB of VRAM for optimal GPU inference. |
| **YAML** | YAML Ain't Markup Language | Human-readable serialization format. Used for the headers of canonical SP files. |

### Appendix C — Glossary

| Term | Definition |
| :--- | :--- |
| **Workbench** | This repository (`agentic-agile-workbench`). Contains reusable tools, rules, and processes. |
| **Roo Code XML tags** | Roo Code action syntax: `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. |
| **Boomerang Tasks** | Roo Code delegation mechanism: the 14B agent creates a sub-task for the 8B model, retrieves the result and integrates it into its loop. |
| **LLM Switcher** | "API Provider" parameter in Roo Code settings. Switches between Ollama, FastAPI proxy, and Anthropic without modifying Roo Code. |
| **Determinism** | LLM response stability. Achieved via `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` in the Modelfile. |
| **Context window** | Maximum simultaneous processing capacity of an LLM. Fixed at 128K tokens (`num_ctx 131072`) to load code + Memory Bank. |
| **Fine-tuning** | Specialized LLM training. `mychen76/qwen3_cline_roocode:14b` is fine-tuned for Roo Code Tool Calling. |
| **Gemini Gem** | Gemini Web profile with permanent system prompt (SP-007). Avoids retransmitting the system prompt with each request. |
| **Pre-commit hook** | Git script executed before each commit. Calls `check-prompts-sync.ps1` and blocks the commit if desynchronization is detected. |
| **Memory Bank** | 7 Markdown files in `memory-bank/` persisting context between sessions. Segmented by theme to optimize LLM attention. |
| **Modelfile** | Ollama configuration file. Defines the base model, inference parameters, and system prompt. |
| **Cloud Mode** | Roo Code → direct Anthropic API (`claude-sonnet-4-6`). Automated, paid, requires API key in VS Code SecretStorage. |
| **Local Mode** | Roo Code (`pc`) → Ollama `calypso:11434` (Tailscale) → Qwen3-14B. Free, sovereign, private Tailscale network. |
| **Proxy Mode** | Roo Code → FastAPI proxy `localhost:8000` → clipboard → Gemini Web. Free, requires human copy-paste. |
| **Agile Persona** | Roo Code mode simulating a Scrum role. Defined in `.roomodes` with `roleDefinition` (behavior) and `groups` (RBAC permissions). |
| **Polling** | Periodic state checking. The proxy checks the clipboard every second via `asyncio.sleep(1.0)`. |
| **Proxy** | Local FastAPI server (`proxy.py`) intercepting Roo Code requests, relaying them to Gemini Web via clipboard, and returning the response. |
| **Prompt registry** | `prompts/` directory — single source of truth for all system prompts, versioned with YAML metadata. |
| **CHECK→CREATE→READ→ACT sequence** | Mandatory protocol at session startup: check Memory Bank → create if absent → read → act. |
| **SSE (Server-Sent Events)** | Unidirectional HTTP streaming. The proxy returns the Gemini response in a single SSE chunk for compatibility with Roo Code in `stream: true` mode. |
| **Token** | LLM processing unit. The 128K token window allows loading code + Memory Bank simultaneously. |
| **Tool Calling** | LLM capability to call tools via structured requests. Qwen3-14B is fine-tuned for Roo Code Tool Calling (XML tags). |
| **VS Code SecretStorage** | Encrypted VS Code storage for the Anthropic API key. Not accessible from the file system. |

---

---

## 9. v2.4 Architecture Additions

### 9.1 Calypso Orchestration v1 — Ideation-to-Release Pipeline

v2.4 introduces a full ideation-to-release governance pipeline called **Calypso Orchestration v1**.

#### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    IDEATION-TO-RELEASE PIPELINE                  │
│                    (Calypso Orchestration v1)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌────────────┐    ┌───────────┐    ┌─────────┐ │
│  │  Human   │───▶│ IntakeAgent│───▶│SyncDetector│───▶│Backlogs │ │
│  │  Input   │    │ (classify/ │    │(5-category │    │ (IDEAS/ │ │
│  │          │    │  route)    │    │  overlap)  │    │  TECH)  │ │
│  └──────────┘    └────────────┘    └───────────┘    └─────────┘ │
│                                                                  │
│  ┌──────────┐    ┌───────────┐    ┌──────────────────────────┐  │
│  │ GitHub   │───▶│BranchTracker│──▶│ ExecutionTracker         │  │
│  │ (branches)│    │(ADR-006)  │    │ (live progress tracking) │  │
│  └──────────┘    └───────────┘    └──────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              IdeasDashboard                                 │ │
│  │         (triage status, refinement tracking)                │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.1.1 Component Architecture

| Component | Responsibility | Language | Dependencies |
|-----------|---------------|----------|--------------|
| **IntakeAgent** | Idea intake, classification (BUSINESS/TECHNICAL), routing | Python 3.11+ | `jsonschema>=4.23.0` |
| **SyncDetector** | Parallel work detection, 5-category sync analysis | Python 3.11+ | None |
| **BranchTracker** | GitFlow ADR-006 enforcement, release tracking | Python 3.11+ | `GitPython>=3.1.40` |
| **ExecutionTracker** | Live progress tracking across all active work | Python 3.11+ | None |
| **IdeasDashboard** | Centralized backlog management | Python 3.11+ | None |

#### 9.1.2 Data Flow

**Idea Intake Flow:**

```
Human Input
    │
    ▼
IntakeAgent.analyze(raw_text, agent_context)
    │
    ├──▶ Classify: BUSINESS (WHAT) or TECHNICAL (HOW)
    │
    ├──▶ Route: IDEAS-BACKLOG.md or TECH-SUGGESTIONS-BACKLOG.md
    │
    └──▶ SyncDetector.detect(idea_id)
              │
              ├──▶ Read active branch list
              ├──▶ Check for file overlap
              └──▶ Return sync category
```

**Execution Tracking Flow:**

```
Session Start
    │
    ▼
ExecutionTracker.sync()
    │
    ├──▶ Read DOC-3 execution chapter
    ├──▶ Read memory-bank/progress.md
    ├──▶ Read EXECUTION-TRACKER-vX.Y.md
    │
    └──▶ Ensure consistency across all three
```

#### 9.1.3 Storage Architecture

| Data Store | Location | Purpose |
|-----------|----------|---------|
| **IDEAS-BACKLOG** | `docs/ideas/IDEAS-BACKLOG.md` | Business idea backlog (triage status) |
| **TECH-SUGGESTIONS** | `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md` | Technical suggestion backlog |
| **Decision Log** | `memory-bank/hot-context/decisionLog.md` | Architectural decisions |
| **Execution State** | `memory-bank/progress.md` | Current session progress |
| **DOC-3** | `docs/releases/vX.Y/DOC-3-vX.Y-Implementation-Plan.md` | Release execution tracking |

#### 9.1.4 CLI Tool Architecture

All Calypso components are executable as CLI tools via Python module invocation:

| Command | Module |
|---------|--------|
| `python -m src.calypso.intake_agent "text"` | IntakeAgent |
| `python -m src.calypso.sync_detector` | SyncDetector |
| `python -m src.calypso.branch_tracker` | BranchTracker |
| `python -m src.calypso.execution_tracker` | ExecutionTracker |
| `python -m src.calypso.ideas_dashboard` | IdeasDashboard |

#### 9.1.5 ADR-006 GitFlow Enforcement in BranchTracker

The BranchTracker enforces the GitFlow branching model (ADR-006):

| Branch | Purpose | Enforcement |
|--------|---------|-------------|
| `main` | Production state. Frozen. | Cannot commit directly |
| `develop` | Wild mainline. Ad-hoc work. | Long-lived, always ahead of main |
| `develop-vX.Y` | Scoped backlog for vX.Y. | Created at release planning |
| `feature/{IDEA-NNN}-{slug}` | Single feature or fix. | Branch from develop or develop-vX.Y |

**Forbidden actions detected by BranchTracker:**
- Direct commits to `main` after release tag
- Commits on merged branches
- Feature work on release branches (not develop or develop-vX.Y)

#### 9.1.6 Sync Detection Categories

SyncDetector implements 5-category overlap detection:

| Category | Symbol | Meaning | Action |
|----------|--------|---------|--------|
| **CONFLICT** | 🔴 | Mutually exclusive changes | Human must arbitrate |
| **REDUNDANCY** | 🟡 | Same problem solved twice | Merge into single idea |
| **DEPENDENCY** | 🔵 | Idea B needs Idea A first | Reorder, communicate |
| **SHARED_LAYER** | 🟠 | Multiple ideas touch same component | Coordinate timing |
| **NO_OVERLAP** | 🟢 | No conflicts detected | Proceed normally |

---

## 10. v2.4 Functional Layer Additions

### 10.1 New Layer: Orchestration (Layer 7)

v2.4 adds a new **Orchestration Layer** above the existing 6 functional layers:

| Layer | Name | Components |
|-------|------|------------|
| Layer 1 | Infrastructure | Tailscale, calypso server, pc laptop |
| Layer 2 | LLM Inference | Ollama, qwen3-14b, qwen3-8b |
| Layer 3 | Agentic Engine | Roo Code (VS Code extension) |
| Layer 4 | Memory Bank | Hot-context (7 files), Cold archive |
| Layer 5 | Prompt Registry | prompts/SP-001 to SP-010 |
| Layer 6 | Developer Tools | Anthropic Batch API Toolkit, scripts/batch/ |
| **Layer 7** | **Orchestration** | **Calypso: IntakeAgent, SyncDetector, BranchTracker, ExecutionTracker, IdeasDashboard** |

### 10.2 Layer 7 Responsibilities

1. **Intake**: Capture and classify incoming ideas
2. **Routing**: Direct ideas to correct backlogs
3. **Sync**: Detect and prevent conflicts
4. **Governance**: Enforce GitFlow discipline
5. **Tracking**: Monitor live execution progress
6. **Dashboard**: Provide centralized visibility

---

## 11. v2.4 Architecture / Feature / Requirement Traceability

| Feature | Requirement | Architecture Element |
|---------|-------------|---------------------|
| IDEA-012A: IntakeAgent | REQ-012-A1 | `src/calypso/intake_agent.py` |
| IDEA-012A: IntakeAgent | REQ-012-A2 | BUSINESS/TECHNICAL classification |
| IDEA-012B: SyncDetector | REQ-012-B1 | `src/calypso/sync_detector.py` |
| IDEA-012B: SyncDetector | REQ-012-B2 | 5-category sync detection |
| IDEA-012C: BranchTracker | REQ-012-C1 | `src/calypso/branch_tracker.py` |
| IDEA-012C: BranchTracker | REQ-012-C2 | ADR-006 GitFlow enforcement |
| IDEA-012C: ExecutionTracker | REQ-012-C3 | `src/calypso/execution_tracker.py` |
| IDEA-012C: IdeasDashboard | REQ-012-C4 | `src/calypso/ideas_dashboard.py` |

---

## 12. v2.4 Glossary Additions

| Term | Definition |
|------|------------|
| **Calypso Orchestration** | The v2.4 ideation-to-release governance pipeline. Named after the Calypso server. |
| **IntakeAgent** | Component that captures and classifies incoming ideas as BUSINESS or TECHNICAL. |
| **SyncDetector** | Component that detects parallel work overlap and sync opportunities. |
| **BranchTracker** | Component that enforces GitFlow ADR-006 compliance. |
| **ExecutionTracker** | Component that tracks live progress across all active ideas and releases. |
| **IdeasDashboard** | Component that provides centralized backlog management with triage status. |
| **Sync Category** | One of 5 overlap types detected by SyncDetector: CONFLICT, REDUNDANCY, DEPENDENCY, SHARED_LAYER, NO_OVERLAP. |
| **Orchestration Layer** | Layer 7 of the functional stack, added in v2.4 for governance pipeline. |

---

*End of DOC-2 v2.4 -- Cumulative (v1.0 through v2.4)*
