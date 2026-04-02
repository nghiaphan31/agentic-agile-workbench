---
doc_id: DOC-3
release: v2.7
status: Draft
title: Implementation Plan
version: 1.0
date_created: 2026-04-02
authors: [Scrum Master mode, Human]
previous_release: v2.6
cumulative: true
---

# DOC-3 — Implementation Plan (v2.7)

> **Status: DRAFT** -- This document is in draft for v2.7.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all implementation guidance from v1.0 through v2.7.
> To understand the full project implementation history, read this document from top to bottom.
> Do not rely on previous release documents -- they are delta-based and incomplete.

---

## Table of Contents

1. [v1.0 Implementation Phases](#1-v10-implementation-phases)
2. [v2.1 Implementation Summary](#2-v21-implementation-summary)
3. [v2.2 Implementation Summary](#3-v22-implementation-summary)
4. [v2.3 Implementation Summary](#4-v23-implementation-summary)
5. [v2.4 Implementation Summary](#5-v24-implementation-summary)
6. [v2.5 Implementation Summary](#6-v25-implementation-summary)
7. [v2.6 Implementation Summary](#7-v26-implementation-summary)
8. [v2.7 Implementation Summary](#8-v27-implementation-summary)
9. [Execution Tracking](#9-execution-tracking)

---

## 1. v1.0 Implementation Phases

### Phase Overview

```
PHASE 0  : Clean Base — VS Code + Roo Code Cleanup and Reinstallation
PHASE 1  : System Infrastructure (Ollama + LLM Models)
PHASE 2  : Creation of the le workbench Git Repository
PHASE 3  : Modelfile and Custom Ollama Model
PHASE 4  : Agile Personas (.roomodes) with Git Rules
PHASE 5  : Memory Bank (.clinerules with 7 Rules + 7 .md files)
PHASE 6  : Gemini Chrome Proxy (proxy.py v2.0 with SSE)
PHASE 7  : Gemini Chrome Configuration (Dedicated Gem)
PHASE 8  : Roo Code Configuration (3-Mode LLM Switcher)
PHASE 9  : End-to-End Validation Tests
PHASE 10 : Direct Cloud Mode — Anthropic Claude Sonnet API
PHASE 11 : Central System Prompts Registry (prompts/)
PHASE 12 : Automatic Prompt Consistency Verification
```

### Phase / PRD Requirements Mapping Table

| Phase | Description | PRD Requirements |
| :--- | :--- | :--- |
| Phase 0 | Clean VS Code + Roo Code base | REQ-000 |
| Phase 1 | Ollama + models installation | REQ-1.0, REQ-1.1, REQ-1.2 |
| Phase 2 | Git repository + complete .gitignore | REQ-000, REQ-4.1, REQ-4.5 |
| Phase 3 | Custom Modelfile + commit | REQ-1.2, REQ-1.3 |
| Phase 4 | Agile personas .roomodes + Git rules | REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4 |
| Phase 5 | .clinerules (7 rules) + 7 Memory Bank files | REQ-4.1 to REQ-4.5 |
| Phase 6 | proxy.py v2.0 (SSE + JSON) + scripts/ | REQ-2.1.1 to REQ-2.4.4 |
| Phase 7 | Gemini Chrome Gem + Memory Bank doc | REQ-5.1, REQ-5.2, REQ-5.3 |
| Phase 8 | Roo Code 3-mode LLM switcher | REQ-2.0, REQ-6.0 |
| Phase 9 | End-to-end tests (including self-contained Git test) | REQ-000 |
| Phase 10 | Anthropic Claude Sonnet API (claude-sonnet-4-6) | REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4 |
| Phase 11 | Central prompts registry (prompts/) | REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5 |
| Phase 12 | Automatic prompt consistency verification (script + pre-commit hook) | REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4 |

---

### PHASE 0: Clean Base — VS Code + Roo Code Cleanup and Reinstallation

**Objective:** Start from a clean VS Code and Roo Code environment, free from previous configuration pollution.
**Requirements addressed:** REQ-000

**Steps:**
1. Uninstall existing Roo Code extension from VS Code
2. Close all VS Code windows
3. Delete extension storage: `%USERPROFILE%\.vscode\extensions\` (Roo Code folder)
4. Delete VS Code settings: `%APPDATA%\Code\User\settings.json`
5. Delete Roo Code global storage: `%USERPROFILE%\.roocode\` (if exists)
6. Reinstall Roo Code from the VS Code Marketplace
7. Restart VS Code

**Verification:**
- Run `git --version` in PowerShell
- Run `git status` in the project directory — should show clean or properly initialized repo

---

### PHASE 1: System Infrastructure — Ollama + LLM Models

**Objective:** Install and configure Ollama on `calypso` (Linux server) with the required models.
**Requirements addressed:** REQ-1.0, REQ-1.1

**Prerequisites:**
- Tailscale VPN connected between `pc` and `calypso`
- SSH access to `calypso`

**Steps:**
1. SSH into `calypso`: `ssh user@calypso`
2. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
3. Pull the main model: `ollama pull mychen76/qwen3_cline_roocode:32b`
4. Pull the secondary model: `ollama pull qwen3:7b`
5. Create the compiled model: `ollama create uadf-agent -f /path/to/Modelfile`
6. Start Ollama as a service: `systemctl enable ollama`
7. Configure Ollama to listen on all interfaces: add `OLLAMA_HOST=0.0.0.0` to the service environment
8. Verify: `curl http://calypso:11434/api/tags` should return model list

**Verification:**
- `curl http://calypso:11434/api/tags` shows both models
- `ollama list` shows `uadf-agent` as available

---

### PHASE 2: Git Repository Initialization

**Objective:** Create the workbench Git repository with a complete .gitignore and initial structure.
**Requirements addressed:** REQ-000, REQ-4.1, REQ-4.5

**Steps:**
1. Initialize Git repo: `git init`
2. Create comprehensive `.gitignore` (venv/, .env, __pycache__/, *.log, etc.)
3. Create initial directory structure:
   ```
   ./
   ├── memory-bank/
   │   ├── hot-context/
   │   └── archive-cold/
   ├── prompts/
   ├── scripts/
   ├── src/
   ├── docs/
   │   ├── ideas/
   │   ├── qa/
   │   └── releases/
   ├── plans/
   └── template/
   ```
4. Create `.gitattributes` for Git LFS if needed
5. Initial commit: `git add . && git commit -m "chore: initial project structure"`

**Verification:**
- `git status` shows clean working directory
- `.gitignore` properly excludes venv/, .env, __pycache__/, *.log

---

### PHASE 3: Modelfile and Custom Ollama Model

**Objective:** Create and compile a custom Modelfile that locks all determinism parameters.
**Requirements addressed:** REQ-1.2, REQ-1.3

**Modelfile Parameters (locked):**
```
PARAMETER temperature 0.15
PARAMETER min_p 0.03
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 131072
PARAMETER num_gpu 99
PARAMETER num_thread 8
```

**Steps:**
1. Create `Modelfile` in project root with locked parameters
2. Commit to Git: `git add Modelfile && git commit -m "feat: add custom Modelfile with locked determinism parameters"`
3. Deploy to calypso: copy Modelfile to server
4. Compile on calypso: `ollama create uadf-agent -f Modelfile`
5. Verify: `curl http://calypso:11434/api/show -d '{"name":"uadf-agent"}'`

**Verification:**
- `ollama show uadf-agent` displays locked parameters
- Temperature, min_p, top_p, repeat_penalty, num_ctx all match specification

---

### PHASE 4: Agile Personas (.roomodes) with Git Rules

**Objective:** Define the 4 Agile personas (Product Owner, Scrum Master, Developer, QA Engineer) with RBAC permissions.
**Requirements addressed:** REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4

**Steps:**
1. Create `.roomodes` with 4 personas:
   - `product-owner`: Backlog management, requirement prioritization
   - `scrum-master`: Process facilitation, Git commits, ceremony facilitation
   - `developer`: Code implementation, terminal commands, Git operations
   - `qa-engineer`: Test execution, QA reports, bug identification
2. Define RBAC groups for each persona
3. Commit to Git: `git add .roomodes && git commit -m "feat: add .roomodes with 4 Agile personas and RBAC"`

**RBAC Matrix:**

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| read (all files) | ✅ | ✅ | ✅ | ✅ |
| edit memory-bank/productContext.md | ✅ | ✅ | ✅ | ❌ |
| edit memory-bank/*.md | ❌ | ✅ | ✅ | ❌ |
| edit docs/*.md | ✅ | ✅ | ✅ | ❌ |
| edit docs/qa/*.md | ❌ | ❌ | ❌ | ✅ |
| edit source code | ❌ | ❌ | ✅ | ❌ |
| command (general) | ❌ | ❌ | ✅ | ❌ |
| command (Git only) | ❌ | ✅ | ✅ | ❌ |
| command (tests only) | ❌ | ❌ | ✅ | ✅ |
| browser access | ❌ | ❌ | ✅ | ✅ |
| MCP access | ❌ | ❌ | ✅ | ❌ |

**Verification:**
- `.roomodes` file exists and is valid JSON
- All 4 personas have defined roleDefinitions

---

### PHASE 5: Memory Bank (.clinerules + 7 .md files)

**Objective:** Set up the Memory Bank with 6 imperative rules and 7 thematic files.
**Requirements addressed:** REQ-4.1 to REQ-4.5

**Steps:**
1. Create `.clinerules` with 6 mandatory rules (CHECK→CREATE→READ→ACT sequence)
2. Create the 7 Memory Bank files:
   - `projectBrief.md`: Vision, objectives, Non-Goals
   - `productContext.md`: User Stories, business value, backlog
   - `systemPatterns.md`: Architecture conventions, patterns
   - `techContext.md`: Stack, commands, CLI configuration
   - `activeContext.md`: Current task, session state
   - `progress.md`: Phase & feature checklist
   - `decisionLog.md`: Architecture decisions, ADR records
3. Commit: `git add .clinerules memory-bank/ && git commit -m "feat: add Memory Bank with 6 mandatory rules and 7 files"`

**Verification:**
- `.clinerules` exists with all 6 rules
- All 7 Memory Bank files exist with proper structure

---

### PHASE 6: Gemini Chrome Proxy (proxy.py)

**Objective:** Deploy proxy.py for Gemini Chrome mode with SSE streaming.
**Requirements addressed:** REQ-2.1.1 to REQ-2.4.4

**Features:**
- FastAPI-based proxy server
- OpenAI Chat Completions API emulation
- SSE streaming support
- Clipboard management (pyperclip)
- System prompt filtering (USE_GEM_MODE)
- base64 image cleaning

**Steps:**
1. Create `proxy.py` with FastAPI + SSE
2. Create `requirements.txt` with fastapi, uvicorn, pyperclip, asyncio
3. Create venv: `python -m venv venv`
4. Install dependencies: `.\venv\Scripts\pip install -r requirements.txt`
5. Test locally: `.\venv\Scripts\python proxy.py`
6. Commit: `git add proxy.py requirements.txt && git commit -m "feat: add Gemini Chrome proxy with SSE streaming"`

**Verification:**
- `GET http://localhost:8000/health` returns 200 OK
- Proxy accepts OpenAI-format requests and returns Gemini responses

---

### PHASE 7: Gemini Chrome Configuration (Dedicated Gem)

**Objective:** Configure the Gemini "Roo Code Agent" Gem with the system prompt.
**Requirements addressed:** REQ-5.1, REQ-5.2, REQ-5.3

**Steps:**
1. Create a Google Gemini account if not exists
2. Create a new Gem named "Roo Code Agent"
3. Copy SP-007 content into the Gem's system prompt
4. Save and activate the Gem
5. Document the Gem ID in `prompts/SP-007-gem-gemini-roo-agent.md`

**Verification:**
- Gem exists at gemini.google.com with correct name
- System prompt matches SP-007

---

### PHASE 8: Roo Code 3-Mode LLM Switcher

**Objective:** Configure Roo Code with three LLM provider modes.
**Requirements addressed:** REQ-2.0, REQ-6.0

**Modes:**
1. **Local (Ollama)**: `http://calypso:11434` — sovereign mode
2. **Proxy (Gemini)**: `http://localhost:8000` — hybrid mode
3. **Cloud (Anthropic)**: `api.anthropic.com` — direct cloud mode

**Steps:**
1. Configure Roo Code's "OpenAI Compatible" provider for Local and Proxy modes
2. Configure Roo Code's native "Anthropic" provider for Cloud mode
3. Test each mode independently
4. Commit configuration notes to `memory-bank/techContext.md`

**Verification:**
- All 3 modes respond correctly to test prompts
- Mode switching works via Roo Code provider parameter

---

### PHASE 9: End-to-End Validation Tests

**Objective:** Validate the complete system with end-to-end tests.
**Requirements addressed:** REQ-000

**Tests:**
1. Git test (self-contained): Verify Git operations in isolated environment
2. Memory Bank test: Verify CHECK→CREATE→READ→ACT cycle
3. LLM mode tests: Test all 3 modes (Local, Proxy, Cloud)
4. Prompt registry test: Verify SP consistency

**Verification:**
- All tests pass without manual intervention
- Self-contained Git test runs in clean environment

---

### PHASE 10: Direct Cloud Mode — Anthropic Claude Sonnet API

**Objective:** Configure direct Anthropic API connection.
**Requirements addressed:** REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4

**Steps:**
1. Obtain Anthropic API key (`sk-ant-api03-...`)
2. Store API key in VS Code SecretStorage via Roo Code
3. Configure Roo Code with "Anthropic" provider
4. Test with `claude-sonnet-4-6` model
5. Commit: `git commit -m "feat: add Anthropic Claude API configuration"`

**Verification:**
- Cloud mode responds to test prompts
- API key stored securely (not in project files)

---

### PHASE 11: Central System Prompts Registry (prompts/)

**Objective:** Create centralized prompt registry with YAML metadata.
**Requirements addressed:** REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5

**Registry Structure:**
```
prompts/
├── README.md                    # Registry index
├── SP-001-ollama-modelfile-system.md
├── SP-002-clinerules-global.md
├── SP-003-persona-product-owner.md
├── SP-004-persona-scrum-master.md
├── SP-005-persona-developer.md
├── SP-006-persona-qa-engineer.md
└── SP-007-gem-gemini-roo-agent.md (hors_git: true)
```

**YAML Metadata for each SP:**
```yaml
---
sp_id: SP-XXX
version: 1.0
target: .roomodes | .clinerules | Modelfile | Gemini Gem
changelog:
  - YYYY-MM-DD: Initial version
---
```

**Verification:**
- `prompts/README.md` lists all SPs with targets
- All SPs have valid YAML metadata

---

### PHASE 12: Automatic Prompt Consistency Verification

**Objective:** Deploy pre-commit hook and verification script.
**Requirements addressed:** REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4

**Components:**
1. `scripts/check-prompts-sync.ps1`: PowerShell script for normalized comparison
2. `.git/hooks/pre-commit`: Git hook that blocks commits on desync

**Verification:**
- Pre-commit hook triggers on `git commit`
- Script reports PASS/FAIL for each SP
- SP-007 excluded with manual verification warning

---

## 2. v2.1 Implementation Summary

### Ideation-to-Release Pipeline (PHASE-A → PHASE-B → PHASE-C)

v2.1 formalized the governance pipeline:

**PHASE-A: Intake & Triage**
- Human input routed to Orchestrator
- IDEA/TECH ID assignment
- Classification: BUSINESS → IDEAS-BACKLOG, TECHNICAL → TECH-SUGGESTIONS-BACKLOG
- Sync detection

**PHASE-B: Refinement & Approval**
- Structured requirement/feasibility session
- Human chooses: [A] Refine now / [B] Park for later / [C] Sync first

**PHASE-C: Execution & Release**
- Feature branch from develop or develop-vX.Y
- Calypso orchestration
- QA validation
- Merge via PR (branch preserved)

---

## 3. v2.2 Implementation Summary

v2.2 introduced **ADR-011 GitFlow Violation Remediation**:
- Clarified feature branch lifecycle
- Added hotfix branch definition
- Documented branch preservation requirement

---

## 4. v2.3 Implementation Summary

v2.3 introduced **IDEA-009: Anthropic Batch API Toolkit**:
- Created `scripts/batch/` package
- Implemented BatchConfig dataclass
- Added CLI entry point
- Created Jinja2 template generator
- Self-contained `template/scripts/batch/` bundle

---

## 5. v2.4 Implementation Summary

v2.4 formalized **ADR-010 Ad-Hoc Governance**:
- Two paths: STRUCTURED vs AD-HOC
- Release tier criteria (Minor/Medium/Major)
- Calypso orchestration scripts

---

## 6. v2.5 Implementation Summary

v2.5 introduced **RULE 8 Documentation Discipline**:
- The Two Spaces (Frozen vs Draft)
- Idea Capture Mandate
- Conversation Log Mandate
- Release Document References (DOC-X.Y.Z format)

---

## 7. v2.6 Implementation Summary

v2.6 introduced **Session Checkpoint** and **APPEND ONLY for ADRs**:

### Session Checkpoint Implementation
- Created `memory-bank/hot-context/session-checkpoint.md`
- Created `scripts/checkpoint_heartbeat.py`
- RULE MB-2: 5-minute heartbeat
- Crash detection at session start (>30 min)

### APPEND ONLY for ADRs
- RULE MB-3: decisionLog.md is APPEND ONLY
- Never overwrite or delete existing ADRs
- Archive to cold only when >500 lines

### Artifact ID Schema
- All artifacts use `TYPE-YYYY-MM-DD-NNN` format
- Session IDs: `sYYYY-MM-DD-{mode}-{NNN}`

### Plan-Branch Parity
- RULE G-0: Every plan creates a branch
- Branch preserved after merge

---

## 8. v2.7 Implementation Summary

v2.7 addresses **IDEA-017: Canonical Docs Cumulative Requirement**:

### RULE 12 — Canonical Docs Cumulative Requirement

**R-CANON-0:** Each canonical doc is fully self-contained and cumulative.

**Minimum line counts:**
- DOC-1 >= 500 lines
- DOC-2 >= 500 lines
- DOC-3 >= 300 lines
- DOC-4 >= 300 lines
- DOC-5 >= 200 lines

**R-CANON-1 to R-CANON-4:** GitFlow rules for canonical docs:
- Only via feature branch on develop/develop-vX.Y
- Direct commits forbidden
- Exception: governance-only commits

**R-CANON-5 to R-CANON-7:** Consistency rules:
- All 5 docs updated together
- All DOC-*-vX.Y-*.md must exist
- DOC-*-CURRENT.md must point to same release

### Enforcement
- Git pre-receive hook at `.githooks/pre-receive`
- GitHub Actions CI at `.github/workflows/canonical-docs-check.yml`

---

## 9. Execution Tracking

### IDEA-017 Remediation

| Item | Status | Details |
|------|--------|---------|
| **IDEA-017** | In Progress | Canonical docs cumulative fix |
| DOC-1-v2.7-PRD.md | ✅ Complete | 10 sections, v1.0-v2.7 |
| DOC-2-v2.7-Architecture.md | ✅ Complete | 903 lines, exceeds 500 minimum |
| DOC-3-v2.7-Implementation-Plan.md | ✅ Complete | All phases v1.0-v2.7 |
| DOC-4-v2.7-Operations-Guide.md | ⏳ Pending | Pending |
| DOC-5-v2.7-Release-Notes.md | ⏳ Pending | Pending |
| Audit verification | ⏳ Pending | Pending |

### Commit History for IDEA-017

| Commit | Description | Artifact |
|--------|-------------|----------|
| TBD | feat(docs): build DOC-1-v2.7-PRD.md cumulative | DOC-1-v2.7-PRD.md |
| TBD | feat(docs): build DOC-2-v2.7-Architecture.md cumulative | DOC-2-v2.7-Architecture.md |
| TBD | feat(docs): build DOC-3-v2.7-Implementation-Plan.md cumulative | DOC-3-v2.7-Implementation-Plan.md |
| TBD | feat(docs): build DOC-4-v2.7-Operations-Guide.md cumulative | DOC-4-v2.7-Operations-Guide.md |
| TBD | feat(docs): build DOC-5-v2.7-Release-Notes.md cumulative | DOC-5-v2.7-Release-Notes.md |
