---
doc_id: DOC-5
release: v1.0
title: Release Notes
status: Frozen
version: 1.0.0
date: 2026-03-28
authors: [Human, Scrum Master agent]
previous_release: none
---

# Release Notes — Agentic Agile Workbench v1.0

**Release date:** 2026-03-28
**Git tag:** `v1.0.0`
**Branch:** `master` (Sessions 1-9, 2026-03-23 to 2026-03-24)

---

## What Is v1.0

v1.0 is the **initial working release** of the Agentic Agile Workbench — a local, sovereign agentic development environment combining:
- A headless Linux GPU server (Calypso, RTX 5060 Ti 16GB) for local LLM inference via Ollama
- A Windows 11 laptop with VS Code + Roo Code as the agentic execution engine
- A Gemini Chrome proxy for free cloud LLM access
- The Anthropic Claude API for full automation

---

## Delivered Features

### 1. 3-Mode LLM Switcher
- **Mode 1:** Local Ollama (`http://calypso:11434`, model `uadf-agent` based on `mychen76/qwen3_cline_roocode:14b`)
- **Mode 2:** Gemini Chrome Proxy (`http://localhost:8000/v1`, model `gemini-manual`) via `proxy.py` v2.8.0
- **Mode 3:** Anthropic Claude API (direct, `claude-sonnet-4-6`)
- Switching requires only changing the API Provider in Roo Code settings

### 2. 4 Agile Personas (`.roomodes`)
- **Product Owner:** Requirements, user stories, product backlog — no code access
- **Scrum Master:** Sprint planning, process, QA reports — no code execution
- **Developer:** Code writing, refactoring, Git commits — restricted to `src/`
- **QA Engineer:** Test execution, QA reports — read-only on source code

### 3. Memory Bank (7 files + `.clinerules` 7 rules)
- `activeContext.md`, `progress.md`, `projectBrief.md`, `productContext.md`
- `systemPatterns.md`, `techContext.md`, `decisionLog.md`
- Mandatory read at session start, mandatory write at session close
- Git versioning rule, chunking protocol for large files

### 4. Prompts Registry (`prompts/` SP-001 to SP-007)
- Centralized system prompt registry with YAML front matter
- SP-001: Ollama Modelfile system block
- SP-002: `.clinerules` global rules
- SP-003 to SP-006: Agile persona role definitions
- SP-007: Gem Gemini "Roo Code Agent" (manual deployment)

### 5. Pre-Commit Hook (`check-prompts-sync.ps1`)
- Automatically verifies all SP files are synchronized with deployed artifacts
- Runs on every `git commit`
- Result: 6 PASS | 0 FAIL | 1 WARN (SP-007 manual deployment expected)

### 6. Project Template Folder (`template/`)
- Complete deployable template for new application projects
- Includes: `.clinerules`, `.roomodes`, `Modelfile`, `proxy.py`, `requirements.txt`
- Includes: `prompts/` (SP-001 to SP-007), `scripts/` (check-prompts-sync.ps1, start-proxy.ps1)

### 7. Deployment Script
- `deploy-workbench-to-project.ps1` — copies template to a new project directory

---

## Known Gaps and Limitations

| Gap | Severity | Notes |
|---|---|---|
| Phase 9 RBAC partially validated | Medium | Only Product Owner scenario tested (2/7 scenarios). Scrum Master, Developer, QA Engineer scenarios pending. |
| SP-007 requires manual Gem Gemini update | Low | English instructions written in `prompts/SP-007-gem-gemini-roo-agent.md` v1.7.0 — must be manually deployed to Gemini Gems. |
| Ollama model deviation: 32b → 14b | Low | `mychen76/qwen3_cline_roocode:32b` requires 20GB VRAM; 14b used instead. Performance impact acceptable. |
| Secondary model deviation: qwen3:7b → qwen3:8b | Low | `qwen3:7b` unavailable at install time; `qwen3:8b` used instead. |
| No Hot/Cold memory architecture | Medium | All 7 memory bank files loaded simultaneously. Context explosion risk on large projects. Addressed in v2.0. |
| No Calypso orchestration scripts | High | Multi-agent pipeline (Phases 2-4) not yet implemented. Addressed in v2.0. |
| No Global Brain / Librarian Agent | High | Cross-project memory not yet implemented. Addressed in v2.0. |

---

## Migration from Previous Version

No previous version exists. This is the initial release.

---

## What's Next (v2.0 Preview)

v2.0 will deliver:
- **PHASE-0:** Release governance model (this restructure)
- **PHASE-A:** Hot/Cold memory architecture (context management)
- **PHASE-B:** Template folder enrichment (memory-bank/ subdirs, mcp.json)
- **PHASE-C:** Calypso orchestration scripts (Phase 2-4 pipeline)
- **PHASE-D:** Global Brain (Chroma/Mem0 vector DB, Librarian Agent)

See `docs/ideas/IDEAS-BACKLOG.md` for the full v2.0 scope.
