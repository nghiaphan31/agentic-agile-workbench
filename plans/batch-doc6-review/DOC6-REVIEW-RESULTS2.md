# Agentic Workbench Vision Analysis — Second-Pass Results

**Source documents:**
- [`workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md`](../../workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md) — First Gemini conversation
- [`workbench/_Agentic Workbench Architecture Explained .md`](../../workbench/_Agentic%20Workbench%20Architecture%20Explained%20.md) — Second Gemini conversation
- [`plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md`](DOC6-REVIEW-RESULTS.md) — Previous expert review

**Batch ID:** `msgbatch_01X6jHRi8tHAh3fadCpsZq1s`
**Retrieved at:** 2026-03-28 09:36 UTC
**Model:** `claude-sonnet-4-6`
**Total tokens:** 217,032 input / 12,288 output

---

## Table of Contents

1. [Vision Coherence & Synthesis Review](#analysis-1-vision-coherence--synthesis-review)
2. [Core Workbench vs. Application Template Taxonomy](#analysis-2-core-workbench-vs-application-template-taxonomy)
3. [Migration Plan — Current → Target](#analysis-3-migration-plan--current-workbench--target-vision)

---

## 🔭 Analysis 1: Vision Coherence & Synthesis Review
**Expert persona:** Senior Technical Architect & Documentation Strategist

*Tokens: 72,187 input / 4,096 output*

# Vision Coherence Review: Agentic Agile Workbench

---

## 1. Executive Summary

- **The two Gemini conversations are substantially coherent and additive rather than contradictory.** Document B is a direct continuation and enrichment of Document A, drilling deeper into implementation details (Calypso scripts, Librarian Agent, Global Brain, Hot/Cold memory) that were conceptually present but unimplemented in Document A. No fundamental architectural reversals occur.

- **A Phase 7 (Retrospective/Global Brain) emerges exclusively in Document B** and represents the most significant architectural extension — it transforms the system from a stateless per-project pipeline into a compounding, cross-project learning ecosystem. This is architecturally significant and has no equivalent in Document A.

- **The previous expert review (Document C) is only partially addressed by Document B.** Several P0 issues from Document C — notably missing `systemPatterns.md` genesis, undefined SP-04x agent identifiers, missing `mcp.json`, and the non-existent model identifier — remain unresolved. However, Document B materially resolves a number of P1 issues by providing concrete Python scripts, artifact templates, and the taxonomy matrix.

- **The Workbench/Template boundary, left entirely implicit in Document A, is now explicitly defined in Document B** through the Summary Matrix and the `.clinerules`/`systemPatterns.md` templates. However, the boundary definition itself contains ambiguities (e.g., the Hot/Cold memory split and archive rotation are defined conceptually but not reconciled with the existing workbench state).

- **The unified vision is that of a 3-tier, 7-phase, dual-mode (Greenfield/Brownfield) Agentic Agile pipeline** — a cognitive assembly line that enforces strict separation between asynchronous upstream intelligence generation (Phases 1-4 on Calypso/Cloud) and synchronous downstream surgical execution (Phases 5-6 on local Tier 1), with a periodic retrospective loop (Phase 7) that compounds cross-project knowledge into a Global Brain on Calypso.

---

## 2. Vision Evolution Analysis

### New Concepts Introduced in Document B (Absent or Implicit in Document A)

| Concept | Status in Doc A | Status in Doc B |
|:---|:---|:---|
| **Phase 7: Retrospective / Global Brain** | Completely absent | Fully defined with actors, trigger, flow, Librarian Agent, and promotion mechanism |
| **Librarian Agent** | Not mentioned | Fully specified including system prompt (`prompt_agent_librarian.md`), JSON schema (`proposed_promotions_schema.json`), and Human Gate triage |
| **Cross-Project Memory Taxonomy (4 Pillars)** | Absent | Explicitly defined: Developer Persona, Core Engineering Standards, Infrastructure & Blueprints, Post-Mortem Archive |
| **Hot/Cold Memory Split with archive rotation** | Mentioned as a concept in Part 4 MCP section | Fully operationalized: directory structure (`/hot-context/` vs `/archive-cold/`), rotation trigger (sprint end), `memory:archive` script, `.clinerules` Cold Zone Firewall |
| **Workbench Core vs. Application Template Boundary** | Entirely implicit — reader must infer | Explicitly documented with a Summary Matrix (6 rows) and rationale per item |
| **Calypso Python Orchestration Scripts** | Mentioned as needed, never implemented | 5 complete scripts provided: `orchestrator_phase2.py`, `check_batch_status.py`, `orchestrator_phase3.py`, `orchestrator_phase4.py`, `triage_dashboard.py`, `apply_triage.py` |
| **`.clinerules` canonical content** | Referenced as existing but not specified | Full content provided with 5 mandatory sections |
| **`systemPatterns.md` template** | Ghost artifact — used but never created | Full structural template provided with 6 sections mapping to Priority Matrix (P0-P3) |
| **`decisionLog.md` template** | Referenced but never specified | ADR template provided with context, decision, consequences, and Librarian Tags fields |
| **Human Gate triage UI** (`triage_dashboard.md`) | Described abstractly in Phase 5 | Fully specified as a generated Markdown file with checkbox-based arbitration and three resolution paths |
| **`apply_triage.py` companion script** | Described procedurally | Complete Python implementation provided |
| **Promotion Triage (Approve/Reject/Refine)** | Absent | Three-option arbitration workflow with system consequences per choice fully documented |
| **7-Phase End-to-End Operational Runbook** | Absent | Complete runbook with hardware tier, actor, and tool per step |
| **Exhaustive Component Taxonomy Matrix** | Absent | Full matrix across Scope, Mode, Type, Environment, and Actor for ~30 system items |
| **Cognitive Garbage Collection / Log Rotation** | Mentioned as Hot/Cold concept | Operationalized as directory structure + `.clinerules` Cold Zone Firewall + sprint-end archive script |

### Concepts That Evolved or Were Refined

| Concept | Doc A Version | Doc B Evolution |
|:---|:---|:---|
| **Phase 1 character** | Described as Synchronous Ideation Workshop — primarily a procedural definition | Same core, but now grounded in operational examples (the "referral system" runbook) and fully connected to Tier 1 workflow |
| **`systemPatterns.md`** | Ghost artifact — referenced as Phase 3 input, never created | Now has a canonical 6-section template. Creation genesis remains partially ambiguous (see Section 3) |
| **Memory Bank files** | 7 files referenced but only 4 (Phase 1 ideation) templated | `systemPatterns.md`, `decisionLog.md` fully templated; `productContext.md` partially defined via `apply_triage.py` output |
| **Calypso role** | "Orchestrator / Router" — abstract description | Concretized: receives PRD, manages Devil's Advocate loop, runs routing models, manages vectorization, hosts FastMCP server, runs Librarian Agent |
| **MCP ecosystem** | 7 server recommendations with brief descriptions | Maintained as recommendations; production-readiness is discussed but not formally assessed (Doc C's critique not explicitly addressed) |
| **Hot/Cold memory** | Architectural principle stated | Operationalized as filesystem structure with `.clinerules` enforcement |
| **Brownfield workflow** | Described with same depth as Greenfield but without implementation artifacts | Analyst Agent prompt provided; otherwise no deeper artifacts; the asymmetry noted in Doc C persists |

### What Contradicts Between Conversations

No direct contradictions of substance exist. Document B supersedes Document A's abstract descriptions with concrete implementations throughout. The only tension points are:

1. **Phase 1 Environment:** Doc A states "Local (Your machine) -> Cloud" for Phase 1. Doc B's runbook places Phase 1 exclusively at Tier 1 (Windows Laptop) without cloud dependency. This is a minor refinement, not a contradiction.

2. **`systemPatterns.md` creation genesis:** Doc A implies it pre-exists as a project prerequisite. Doc B's template makes it something the Phase 2 Architecture Agent populates — but the script `orchestrator_phase3.py` reads it as a pre-existing file. Neither document fully resolves when and how this file is first created for a new Greenfield project.

### The Final, Authoritative Vision Emerging from Both Together

The Agentic Agile Workbench is a **7-phase, 3-tier, dual-mode cognitive assembly line** for AI-assisted software development. It enforces a strict architectural separation between:

- **Upstream intelligence generation** (Phases 1-4): Human-initiated business extraction (Phase 1, Tier 1) feeding into asynchronous multi-agent analysis, synthesis, and feasibility filtering (Phases 2-4, Tier 2/3), producing a classified backlog
- **Downstream surgical execution** (Phases 5-6): Human triage of escalated conflicts (Phase 5, Tier 1) feeding into TDD-driven code generation with mandatory tunnel vision (Phase 6, Tier 1)
- **Cross-project intelligence compounding** (Phase 7): Sprint retrospective via Librarian Agent (Tier 2) extracting universal patterns for the Global Brain

The system operates on a **Glass Box** transparency principle: all agent memory is human-readable Markdown versioned in Git, with vector databases serving only as retrieval indexes over these source files, never as opaque primary stores.

---

## 3. Consistency Audit

### Terminology Inconsistencies

| Inconsistency | Doc A Usage | Doc B Usage | Resolution Needed |
|:---|:---|:---|:---|
| **"Book of Laws"** | Used as informal synonym for `systemPatterns.md` in Phase 4 | Used in orchestrator scripts as `systemPatterns.md` path argument; informal name drops away | Formally equate in glossary: *"Book of Laws = `systemPatterns.md`"* |
| **"Memory Bank"** | Refers to the local project file set | Also applied to the global Calypso vector store in some passages | Define two distinct terms: *"Local Memory Bank"* (project files) vs. *"Global Brain"* (Calypso vector DB) |
| **"Asynchronous Factory"** | Used to denote Phases 2-4 collectively | Used consistently — no drift | No action needed |
| **Agent identifiers (SP-004, SP-005, SP-006)** | Used in Phase 5/6 without definition | Replaced by descriptive names (Lead PM Agent, Developer Agent, QA Agent) | Doc B's naming convention is superior; SP codes should be formally mapped or retired |
| **"PRD"** | Ambiguous — sometimes refers to `draft_prd.md`, sometimes to the "final PRD" presented at Scope Lock Gate | Doc B adds further confusion: the PRD is also described as "a massive, ultra-structured JSON or Markdown document" in Phase 1's output | **Critical gap** — see below |

### Architectural Contradictions

**Contradiction 1: `systemPatterns.md` Genesis (P0)**

This is the most consequential unresolved contradiction across both documents.

- In `orchestrator_phase3.py` (Doc B), the script calls `load_file("./memory-bank/systemPatterns.md")` as a pre-existing input to Phase 3.
- In `orchestrator_phase2.py`, the PRD and lexicon are sent to expert agents — but the Architecture Agent's output is described as informing the system architecture. The document never specifies that Phase 2 *creates or writes* `systemPatterns.md`.
- The `systemPatterns.md` template provided in Doc B shows it as a file to be *populated* by the factory, yet the factory reads it before populating it.
- **Resolution required:** Define `systemPatterns.md` as a *two-lifecycle file*: (a) a blank-but-structured template initialized at project creation (from the Project Template Folder), and (b) progressively populated/updated by the Phase 2 Architecture Agent output (injected during Phase 5 triage via `apply_triage.py`). This requires an explicit `initialize_project.py` script or a `memory:init` command.

**Contradiction 2: PRD Artifact Identity (P0)**

Across both documents, "the PRD" refers to at least three distinct artifacts:

- `draft_prd.md`: The working PRD built incrementally during Phase 1 ideation
- `projectBrief.md`: The high-level constitution (Elevator Pitch, KPIs)
- The "PRD payload sent to Phase 2": Described in both docs as the frozen artifact submitted to the Asynchronous Factory — but which file? `draft_prd.md`? A merged artifact?

The `orchestrator_phase2.py` script reads `./ideation_board/draft_prd.md`, which confirms `draft_prd.md` is the Phase 2 input — but Phase 1's Passing Criterion mentions "the final PRD" is presented to the human for approval, and Doc A's Phase 1 output lists both `projectBrief.md` and "the PRD payload". These need to be definitively reconciled.

**Contradiction 3: Cold Zone Firewall vs. MCP Semantic Query**

Doc B's `.clinerules` states the Developer Agent must use `query_semantic_memory` MCP tool to retrieve cold archive content. But Doc B also states the Semantic MCP server is hosted on Calypso. This means Phase 6 (local Tier 1 execution) requires a live network connection to Calypso for historical context retrieval — contradicting the goal of isolated local execution and creating a hard dependency that could block development if Calypso is offline.

**Contradiction 4: Batch API vs. Synchronous API for Phase 3**

Doc A specifies Phase 3 as "Cloud (Batch API). Asynchronous Process." Doc B's `orchestrator_phase3.py` uses `client.messages.create()` — the synchronous API — with a comment explaining this is for "complex reasoning." This is a reasonable design decision but contradicts the Phase 3 header description. The runbook in Doc B treats Phase 3 as part of the "Asynchronous Factory" sequence on Calypso, which obscures this distinction.

### Scope Creep and Undefined Boundaries

**The `/ideation_board/` folder placement is undefined in the context of the Workbench/Template split.** Doc B's scripts read from `./ideation_board/draft_prd.md` and `./memory-bank/systemPatterns.md` — suggesting they co-exist in the same working directory. But the taxonomy matrix places ideation files in "Workbench Core" and memory bank files in "Application Project." The actual filesystem path relationship between these two conceptual zones is never specified.

**The `projectBrief.md` is listed as both a Workbench Core output (generated in Phase 1) and an Application Project Template file** (appears in the template folder list in Doc B). This dual-placement is logical (it's generated once and then lives in the project), but the transition moment is not documented.

---

## 4. Integration with Previous Review (Document C)

### P0 Issues from Document C — Status After Document B

| Issue | Doc C P0 ID | Resolution Status | Evidence |
|:---|:---|:---|:---|
| Conversational framing ("your machine," etc.) | P0-1 | ❌ **Unresolved** | Doc B repeats conversational framing throughout; no formal document header added |
| Missing templates for `systemPatterns.md`, `productContext.md`, `progress.md`, `decisionLog.md` | P0-2 | ✅ **Substantially Resolved** | Doc B provides `systemPatterns.md` template (6 sections), `decisionLog.md` ADR template; `productContext.md` is now generated by `apply_triage.py` |
| PRD naming collision (`projectBrief.md` vs `draft_prd.md`) | P0-3 | ❌ **Unresolved** | Both docs still use "the PRD" ambiguously; `orchestrator_phase2.py` clarifies the input file but the Phase 1 output remains ambiguous |
| Undefined SP-004, SP-005, SP-006 and GAP-001, GAP-002 | P0-4 | 🟡 **Partially Resolved** | Doc B uses descriptive agent names (Lead PM Agent, Developer Agent, etc.), effectively obsoleting SP codes; GAP-001/002 remain undefined but are contextually addressable via MCP section |
| `systemPatterns.md` has no defined creation point | P0-5 | ❌ **Unresolved** | Doc B provides a template but still reads it as a pre-existing file in Phase 3 script; genesis moment not defined |
| Missing Glossary | P0-6 | ❌ **Unresolved** | No glossary added in Doc B; informal definitions scattered throughout |

**P0 Score: 1 fully resolved, 1 partially resolved, 4 unresolved**

### P1 Issues from Document C — Status After Document B

| Issue | Doc C P1 ID | Resolution Status | Evidence |
|:---|:---|:---|:---|
| Missing Table of Contents | P1-1 | ❌ **Unresolved** | No TOC in Doc B |
| Missing Architecture Overview diagram | P1-2 | ❌ **Unresolved** | No Mermaid or diagram added |
| Devil's Advocate loop underspecified | P1-3 | ✅ **Resolved** | `orchestrator_phase4.py` provides complete Python implementation with bounded retry loop (MAX_ATTEMPTS=2), attack/defense pattern, and graceful degradation |
| Missing Failure and Recovery section | P1-4 | ❌ **Unresolved** | Scripts have basic try/except but no system-level recovery protocol |
| Brownfield

---

## 🗂️ Analysis 2: Core Workbench vs. Application Template Taxonomy
**Expert persona:** Principal Platform Architect

*Tokens: 72,271 input / 4,096 output*

# Definitive Taxonomy: Core Workbench vs. Application Project Template

---

## 1. Executive Summary

- **The fundamental separation principle is deployment scope**: items that operate *on* projects (the factory, orchestration, cross-project intelligence) belong to the Core Workbench; items that operate *within* a project (the local execution environment, per-project memory, application code) belong to the Application Project Template.
- **The Memory Bank is split**: the hot-context files (`activeContext.md`, `systemPatterns.md`, `productContext.md`, `progress.md`, `decisionLog.md`, `projectBrief.md`) belong in the Project Template because they are project-specific artifacts versioned alongside application code; the Cold/Archive rotation mechanism belongs to the Workbench because it is a cross-project service.
- **All Python orchestration scripts** (`orchestrator_phase2.py`, `check_batch_status.py`, `orchestrator_phase3.py`, `orchestrator_phase4.py`, `triage_dashboard.py`, `apply_triage.py`) belong exclusively to the Core Workbench on Calypso/Tier-2; they must never appear in application repositories.
- **Agent system prompts are dual-homed**: upstream factory prompts (Lead PM, Expert Committee, Synthesizer, Devil's Advocate, Librarian) belong to the Core Workbench; local execution prompts (Developer Agent `.clinerules`, QA Agent rules, persona `.roomodes`) belong to the Project Template.
- **The user's explicit Git co-versioning requirement** resolves all ambiguity for memory artifacts: any file that must be versioned alongside application source code — including the full human-readable archive (`/memory-bank/archive-cold/`) — belongs in the Project Template, not the Workbench Core.

---

## 2. The Separation Principle

### The Testable Criterion

> **An item belongs to the Core Workbench if and only if it would be IDENTICAL (or intentionally shared) across two completely different application projects running simultaneously.**
>
> **An item belongs to the Application Project Template if it must be COPIED, INSTANTIATED, and INDEPENDENTLY EVOLVED for each new project.**

### Operationalized as Three Tests

**Test 1 — The "Two Projects" Test:**
If you ran Project A (a fintech app) and Project B (a CMS) in parallel, would this item be shared between them or separate? If shared → Core Workbench. If separate → Project Template.

**Test 2 — The "Git Repository" Test:**
Should this item appear in the application's Git commit history, readable by a developer who joins the project six months later? If yes → Project Template. If no (it's infrastructure) → Core Workbench.

**Test 3 — The "Factory vs. Product" Test:**
Does this item *produce* the project (factory tooling, orchestration, cross-project intelligence) or does it *constitute* the project (memory, code, tests, per-project rules)? Factory → Core Workbench. Product → Project Template.

---

## 3. Core Workbench Items (Complete Inventory)

### 3A. AI Agents (Upstream Factory Agents)

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|
| Lead PM Agent | Orchestration Script / AI Agent Prompt | Tier 1 Local → Cloud API | AI Agent | Synchronous | AI Agent Prompt | Operates across all projects; extracts business intent before a project repository exists |
| Analyst Agent (Reverse-Engineer) | AI Agent Prompt | Tier 1 Local → Cloud API | AI Agent | Synchronous | AI Agent Prompt | Cross-project capability; reads spaghetti codebases from any project to extract PRD |
| Architecture Agent (Expert Committee) | AI Agent Prompt | Cloud Tier 3 (Anthropic Batch) | AI Agent | Asynchronous | AI Agent Prompt | Factory-tier agent; operates on PRD before project Memory Bank exists |
| Security Agent (Expert Committee) | AI Agent Prompt | Cloud Tier 3 (Anthropic Batch) | AI Agent | Asynchronous | AI Agent Prompt | Factory-tier agent; compliance analysis independent of any specific codebase |
| UX/UI Agent (Expert Committee) | AI Agent Prompt | Cloud Tier 3 (Anthropic Batch) | AI Agent | Asynchronous | AI Agent Prompt | Factory-tier agent; journey-to-interface translation at PRD level |
| QA Agent (Expert Committee) | AI Agent Prompt | Cloud Tier 3 (Anthropic Batch) | AI Agent | Asynchronous | AI Agent Prompt | Factory-tier agent; business rule flaws hunted before code exists |
| Synthesizer Agent | AI Agent Prompt | Cloud Tier 3 (Anthropic API) | AI Agent | Asynchronous | AI Agent Prompt | Applies Priority Matrix across expert reports; factory-level reasoning |
| Devil's Advocate Agent | AI Agent Prompt | Cloud Tier 3 (Anthropic API) | AI Agent | Asynchronous | AI Agent Prompt | Validates feasibility against `systemPatterns.md`; factory-level architectural guard |
| Librarian Agent | AI Agent Prompt | Tier 2 Calypso (Headless Linux) | AI Agent | Asynchronous | AI Agent Prompt | Cross-project retrospective; reads local project logs to promote global rules |
| `prompt_agent_analyste.md` | AI Agent Prompt | Tier 2 Calypso / Tier 1 Local | AI Agent | Synchronous | AI Agent Prompt | System directive file for Analyst Agent; workbench-level configuration |
| `prompt_agent_librarian.md` | AI Agent Prompt | Tier 2 Calypso | AI Agent | Asynchronous | AI Agent Prompt | System directive file for Librarian Agent; factory-level configuration |

### 3B. Orchestration Scripts (Calypso Tier 2)

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|
| `orchestrator_phase2.py` | Orchestration Script | Tier 2 Calypso (Headless Linux) | Human-triggered | Synchronous trigger → Async batch | Actual Code | Packages PRD into JSONL, dispatches to Anthropic Batch API; purely factory infrastructure |
| `check_batch_status.py` | Orchestration Script | Tier 2 Calypso (Headless Linux) | Human or Cron | Synchronous polling | Actual Code | Polls Anthropic Batch API, validates JSON schemas, saves consolidated expert reports |
| `orchestrator_phase3.py` | Orchestration Script | Tier 2 Calypso (Headless Linux) | Human-triggered | Synchronous | Actual Code | Runs Synthesizer Agent against expert reports + PRD; produces `draft_backlog.json` |
| `orchestrator_phase4.py` | Orchestration Script | Tier 2 Calypso (Headless Linux) | Human-triggered | Synchronous (iterative loop) | Actual Code | Runs Devil's Advocate micro-loop; produces `final_backlog.json` with GREEN/ORANGE classification |
| `triage_dashboard.py` | Orchestration Script | Tier 1 Local (Windows) | Human-triggered | Synchronous | Actual Code | Parses `final_backlog.json`, generates `triage_dashboard.md` for human arbitration |
| `apply_triage.py` | Orchestration Script | Tier 1 Local (Windows) | Human-triggered | Synchronous | Actual Code | Reads human checkbox decisions, updates `systemPatterns.md`, populates project `productContext.md` |
| Custom FastMCP Server on Calypso | Infrastructure | Tier 2 Calypso (Headless Linux) | AI Agent (remote tool call) | Asynchronous | Infrastructure | Exposes `launch_factory()`, `check_batch_status()`, `retrieve_backlog()` to local IDE; purely workbench infrastructure |
| `memory:archive` rotation script | Orchestration Script | Tier 1 Local (Windows) | Human-triggered (end of sprint) | Synchronous | Actual Code | Moves hot-context files to cold archive; triggers Calypso vectorization; operates on project but is workbench tooling |

### 3C. Upstream Ideation Artifacts (Pre-Project, Factory-Scoped)

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|
| `/ideation_board/` folder | Configuration | Tier 1 Local (Windows) | Lead PM Agent + Human | Synchronous | Data Artifact | Pre-project workspace; exists before any application repo is created; must not pollute project Git |
| `ideation_state.md` | Data Artifact | Tier 1 Local (`/ideation_board/`) | Lead PM Agent | Synchronous | Documentation | Resumption marker for ideation sessions; workbench-level session state, not project-level |
| `draft_prd.md` (in `/ideation_board/`) | Data Artifact | Tier 1 Local (`/ideation_board/`) | Lead PM Agent + Human | Synchronous | Documentation | Working PRD under construction; becomes input to factory, not the project's own artifact |
| `domain_lexicon.md` | Data Artifact | Tier 1 Local (`/ideation_board/`) | Lead PM Agent + Human | Synchronous | Documentation | Business dictionary for the ideation phase; feeds Phase 2 but lives in factory space |
| `tech_parking_lot.md` | Data Artifact | Tier 1 Local (`/ideation_board/`) | Lead PM Agent | Synchronous | Documentation | Technical dump excluded from PRD; factory artifact, not application artifact |
| `draft_backlog.json` | Data Artifact | Tier 2 Calypso | Synthesizer Agent | Asynchronous | Data Artifact | Intermediate factory payload between Phase 3 and 4; never enters application repository |
| `final_backlog.json` | Data Artifact | Tier 2 Calypso → Tier 1 Local | Devil's Advocate Agent | Asynchronous | Data Artifact | Factory output payload; consumed by triage scripts, then dissolved into project `productContext.md` |
| `triage_dashboard.md` | Data Artifact | Tier 1 Local (Windows) | Generated by script, edited by Human | Synchronous | Documentation | Temporary arbitration UI; created and deleted by workbench scripts; not part of project history |
| `phase2_batch_payload.jsonl` | Data Artifact | Tier 2 Calypso | Orchestration Script | Asynchronous | Data Artifact | Anthropic Batch API payload; purely factory infrastructure artifact |
| `consolidated_experts_{job_id}.json` | Data Artifact | Tier 2 Calypso | `check_batch_status.py` | Asynchronous | Data Artifact | Aggregated expert reports; intermediate factory state |
| `error_synthesizer_dump.txt` | Data Artifact | Tier 2 Calypso | `orchestrator_phase3.py` | Asynchronous | Data Artifact | Debug artifact from Synthesizer failures; factory-level error handling |

### 3D. Cross-Project Global Brain (Calypso Tier 2)

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|
| Global Brain Vector Database (Chroma/Mem0) | Infrastructure | Tier 2 Calypso (Headless Linux) | Librarian Agent (writes), Developer Agent (queries) | Asynchronous | Infrastructure | Cross-project semantic memory; shared by all projects; cannot live in any single repository |
| `proposed_promotions_schema.json` | Configuration | Tier 2 Calypso | Human (defines once) | N/A (Static) | Configuration | JSON Schema governing Librarian Agent output; workbench-level data contract |
| Pillar 1: Developer Persona (profile) | Configuration | Tier 2 Calypso / Global System Prompt | Human (defines), all agents (read) | N/A (Static) | Configuration | Cross-project operator preferences; injected universally into all local agents |
| Pillar 2: Core Engineering Standards | Configuration | Tier 2 Calypso Vector DB | Librarian Agent (writes), Devil's Advocate (reads) | Asynchronous | Configuration | Cross-project non-negotiable technical laws; shared across all projects |
| Pillar 3: Infrastructure & Blueprints | Configuration | Tier 2 Calypso Vector DB | Librarian Agent (writes), Architecture Agent (reads) | Asynchronous | Documentation | Reusable boilerplate and CI/CD templates; cross-project factory resource |
| Pillar 4: Post-Mortem Archive | Configuration | Tier 2 Calypso Vector DB | Librarian Agent (writes), all agents (query) | Asynchronous | Documentation | De-contextualized lessons from past projects; cross-project intelligence |
| `proposed_promotions.json` (runtime) | Data Artifact | Tier 2 Calypso → Tier 1 Local | Librarian Agent | Asynchronous | Data Artifact | Promotion proposals awaiting human triage; transient factory artifact |

### 3E. Global MCP Infrastructure

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|
| Global `mcp.json` (Calypso-facing) | Configuration | Tier 2 Calypso | Human (configures) | N/A (Static) | Configuration | Connects Calypso to Anthropic API, vector databases, semantic MCP servers; workbench infrastructure |
| `mcp-server-memory` / Chroma MCP / Mem0 MCP | Infrastructure | Tier 2 Calypso | Librarian Agent, factory agents | Asynchronous | Infrastructure | Global semantic memory servers; cross-project; not per-project |
| Semantic Code Parser MCP (Sourcegraph/Tree-sitter) | Infrastructure | Tier 2 Calypso | Analyst Agent | Asynchronous | Infrastructure | Reads entire codebases for brownfield analysis; workbench-level tool |
| `mermaid-mcp-server` / `excalidraw-architect-mcp` | Infrastructure | Tier 2 Calypso | Architecture Agent | Asynchronous | Infrastructure | Architecture diagramming; factory-level visualization |
| `github-mcp-server` / `mcp-server-git` (global) | Infrastructure | Tier 2 Calypso | Factory agents | Async | Infrastructure | Global repository management; workbench-level Git operations |
| `mcp-server-jest` / `mcp-server-pytest` (global) | Infrastructure | Tier 2 Calypso | Devil's Advocate Agent | Asynchronous | Infrastructure | Batch-phase test feasibility validation; factory-level |

### 3F. Workbench Documentation & Process

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|
| DOC1–DOC6 (workbench documentation series) | Documentation | Tier 1 Local (`/workbench/`) | Human | N/A | Documentation | Workbench architecture specifications; not application-specific |
| EXECUTION-TRACKER.md | Documentation | Tier 1 Local (`/workbench/`) | Human | N/A | Documentation | Workbench operational log; tracks workbench build progress |
| RESUME-GUIDE.md | Documentation | Tier 1 Local (`/workbench/`) | Human | N/A | Documentation | Workbench onboarding guide; factory-level |
| Batch review plans (`/plans/`) | Documentation | Tier 1 Local | Human + Claude API | Asynchronous | Data Artifact | Batch API review submissions for workbench documents; factory-level |
| Operational Runbook (end-to-end pipeline) | Documentation | Tier 1 Local (`/workbench/`) | Human | N/A | Documentation | Describes the factory pipeline; not application-specific |

### 3G. Workbench Infrastructure (Current State Items)

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|
| `proxy.py` v2.8.0 (Gemini Chrome proxy) | Infrastructure | Tier 1 Local (Windows) | Human-started, all agents use | Synchronous (SSE) | Actual Code | Routes all local agent traffic; workbench-level network infrastructure |
| `start-proxy.ps1` | Orchestration Script | Tier 1 Local (Windows) | Human | Synchronous | Actual Code | Workbench startup script; not

---

## 🗺️ Analysis 3: Migration Plan — Current Workbench → Target Vision
**Expert persona:** Senior Engineering Lead & Technical Program Manager

*Tokens: 72,574 input / 4,096 output*

# Agentic Agile Workbench: Detailed Migration Plan

## 1. Executive Summary

- **The migration is fundamentally a layered enrichment, not a replacement.** The current workbench is a solid, working foundation (Memory Bank, 3-mode LLM switcher, template folder, Git discipline). Every phase of this migration builds *on top of* what exists rather than tearing it down, which eliminates big-bang risk.
- **The single most critical gap is the Hot/Cold memory architecture.** The current flat `memory-bank/` structure with 7 monolithic files will eventually cause context explosion. Solving this first, before adding Calypso orchestration scripts, ensures the agent execution environment is stable before the factory feeds it work at scale.
- **The template/ folder needs surgical enrichment, not reconstruction.** It already has `.clinerules`, `.roomodes`, and `prompts/` — but it lacks the `memory-bank/` subdirectory structure, the Hot/Cold split, the `systemPatterns.md` template, and the `decisionLog.md` ADR format. These are additions, not overwrites.
- **Calypso orchestration is the last thing to build, not the first.** The four Python orchestration scripts (Phase 2–4) and the FastMCP server are only valuable once the local execution environment (Phase 6 in the target vision) is reliable and the template produces stable Memory Banks. Building Calypso first would be building a factory with no quality-controlled assembly line at the other end.
- **Every phase gate in this migration plan is a working, demoable system state.** A developer can stop at the end of any phase and have a coherent, functional workbench — just with fewer capabilities than the final vision.

---

## 2. Current State Assessment

### What Is Already Implemented and Working

| Component | Status | Notes |
|---|---|---|
| `.clinerules` (core workbench) | ✅ Working | 6 rules, Memory Bank read/write mandate, Git versioning, chunking protocol |
| `.roomodes` (4 personas) | ✅ Working | product-owner, scrum-master, developer, qa-engineer |
| `memory-bank/` (7 files) | ✅ Working | activeContext, progress, projectBrief, productContext, systemPatterns, techContext, decisionLog — flat structure |
| `proxy.py` v2.8.0 | ✅ Working | Gemini Chrome proxy, SSE, FastAPI |
| 3-mode LLM switcher | ✅ Working | Ollama (Calypso/Tailscale), Gemini proxy, Claude API |
| `template/` folder | ✅ Working | Has .clinerules, .roomodes, Modelfile, proxy.py, requirements.txt, prompts/, scripts/ |
| `prompts/` SP-001 to SP-007 | ✅ Working | System prompt registry |
| `scripts/` | ✅ Working | check-prompts-sync.ps1, start-proxy.ps1 |
| Pre-commit hook | ✅ Working | Runs check-prompts-sync.ps1 |
| Git repository | ✅ Working | Branch experiment/architecture-v2 |
| Anthropic Claude API | ✅ Working | Phase 10 marked complete in practice |
| `plans/batch-doc6-review/` | ✅ Working | Submit scripts and results exist — proves Batch API is operational |

### What Is Partially Implemented

| Component | Gap | Location |
|---|---|---|
| Memory Bank structure | Flat (no Hot/Cold split). All 7 files always loaded. No archive rotation. | `memory-bank/` |
| Template folder | Missing `memory-bank/` subdirectory, Hot/Cold structure, `systemPatterns.md` template, ADR format for `decisionLog.md`, `triage_dashboard`-related files | `template/` |
| `.clinerules` in template | Exists but does not enforce Hot/Cold perimeter, Cold Zone Firewall, or semantic memory query instructions | `template/.clinerules` |
| Agent personas | 4 personas exist but no Librarian Agent, no Lead PM Agent, no Synthesizer, no Devil's Advocate | `.roomodes` / `prompts/` |
| `systemPatterns.md` | Exists as a populated file but no canonical blank template in the template folder | `memory-bank/systemPatterns.md` |

### What Is Completely Missing Relative to the Target Vision

| Missing Component | Target Location | Priority |
|---|---|---|
| Hot/Cold memory directory split | Core workbench + template | P0 |
| `archive-cold/` rotation script (`memory:archive`) | Core workbench scripts | P0 |
| `decisionLog.md` ADR format template | Template folder | P0 |
| `systemPatterns.md` blank template | Template folder | P0 |
| Calypso FastMCP server (`orchestration/fastmcp_server.py`) | Calypso (Tier 2) | P1 |
| `orchestrator_phase2.py` | Calypso | P1 |
| `check_batch_status.py` | Calypso | P1 |
| `orchestrator_phase3.py` | Calypso | P1 |
| `orchestrator_phase4.py` | Calypso | P1 |
| `triage_dashboard.py` | Core workbench (Tier 1) | P1 |
| `apply_triage.py` | Core workbench (Tier 1) | P1 |
| Ideation Memory Bank (`/ideation_board/`) | Core workbench | P1 |
| Lead PM Agent system prompt (SP-008) | Core workbench `prompts/` | P1 |
| Analyst Agent prompt (SP-009, Brownfield) | Core workbench `prompts/` | P2 |
| Librarian Agent system prompt (SP-010) | Calypso | P2 |
| `proposed_promotions_schema.json` | Calypso | P2 |
| Global Brain vector database (Chroma/Mem0) | Calypso | P2 |
| Cross-Project Memory taxonomy (4 pillars) | Calypso | P2 |
| `triage_promotions.md` generation logic | Calypso + Tier 1 | P2 |
| Local `mcp.json` template | Template folder | P1 |
| Context management clause in `.clinerules` | Template folder | P0 |
| Cold Zone Firewall instruction | Template folder `.clinerules` | P0 |
| `check-prompts-sync.ps1` update for Hot/Cold | Core workbench scripts | P1 |
| `memory:archive` npm/shell script | Core workbench scripts | P1 |
| Gherkin linter integration | Core workbench | P2 |
| Schema validation script for Phase 2-4 JSON | Core workbench | P1 |

---

## 3. Target State Description

### What Will Exist in the Core Workbench

The core workbench is the **factory engine** and the **global configuration layer**. It lives on the Windows 11 laptop (Tier 1) and on Calypso (Tier 2). It is **never committed into an application project's Git repository**.

```
/workbench-core/                        ← Lives on Windows 11 laptop
├── .clinerules                         ← Global workbench agent rules (NOT the app template version)
├── .roomodes                           ← 9 personas: 4 existing + Lead PM, Analyst, Librarian, Synthesizer, DevilsAdvocate
├── proxy.py                            ← Gemini proxy (existing)
├── Modelfile                           ← uadf-agent definition (existing)
│
├── ideation_board/                     ← Phase 1 artifacts (NEW)
│   ├── ideation_state.md
│   ├── draft_prd.md
│   ├── domain_lexicon.md
│   └── tech_parking_lot.md
│
├── memory-bank/                        ← Workbench-level hot context (RESTRUCTURED)
│   ├── hot-context/                    ← Agent reads ONLY this
│   │   ├── activeContext.md
│   │   ├── progress.md               ← Current sprint only
│   │   └── decisionLog.md            ← Current sprint only
│   └── archive-cold/                  ← Human log, Git-versioned, agent reads via MCP only
│       ├── sprint-logs/
│       └── completed-tickets/
│
├── prompts/                            ← Extended (NEW prompts added)
│   ├── SP-001 to SP-007               ← Existing
│   ├── SP-008-lead-pm-agent.md        ← NEW
│   ├── SP-009-analyst-agent.md        ← NEW (Brownfield)
│   └── SP-010-librarian-agent.md      ← NEW (Retrospective)
│
├── scripts/                            ← Extended
│   ├── check-prompts-sync.ps1         ← Updated for Hot/Cold
│   ├── start-proxy.ps1                ← Existing
│   ├── memory_archive.py              ← NEW: Hot→Cold rotation
│   ├── triage_dashboard.py            ← NEW: Phase 5 HITL dashboard
│   └── apply_triage.py               ← NEW: Phase 5 triage execution
│
├── plans/                              ← Existing
│   └── batch-doc6-review/             ← Existing proof-of-concept
│
└── workbench/                          ← Existing documentation
    └── DOC1-DOC6, EXECUTION-TRACKER, RESUME-GUIDE
```

### What Will Exist in the Application Project Template

The template is what gets copied into every new application Git repository. It is the **local execution environment** for the Developer Agent (Phase 6). It contains only what the coding agent needs.

```
/template/                              ← Copied into every new app repo
├── .clinerules                         ← UPDATED: Hot/Cold perimeter + Cold Zone Firewall
├── .roomodes                           ← UPDATED: developer + qa-engineer personas only
├── Modelfile                           ← Existing
├── proxy.py                            ← Existing
├── requirements.txt                    ← Existing
│
├── memory-bank/                        ← NEW directory structure in template
│   ├── hot-context/
│   │   ├── activeContext.md            ← Blank (filled per ticket)
│   │   ├── progress.md                 ← Blank
│   │   ├── decisionLog.md             ← Blank (ADR format pre-loaded)
│   │   ├── systemPatterns.md          ← Blank template with section headers
│   │   └── productContext.md          ← Blank (filled after Phase 5)
│   └── archive-cold/
│       ├── sprint-logs/               ← Empty dir, .gitkeep
│       ├── completed-tickets/         ← Empty dir, .gitkeep
│       └── productContext_Master.md   ← Blank (historical BDD accumulator)
│
├── mcp.json                            ← NEW: Template with placeholders for DB path, AST root
│
├── prompts/                            ← Developer and QA agent prompts only
│   ├── SP-005-developer.md
│   └── SP-006-qa-engineer.md
│
└── scripts/
    ├── check-prompts-sync.ps1
    └── start-proxy.ps1
```

### What Will Exist on Calypso (Tier 2)

Calypso is the **orchestration server**. It runs headless Linux with RTX GPU, accessible via Tailscale from the Windows laptop.

```
/calypso/agentic-factory/
├── orchestrator_phase2.py              ← Batch API launch (Committee of Experts)
├── check_batch_status.py               ← Batch API polling + result extraction
├── orchestrator_phase3.py              ← Synthesizer Agent (Priority Matrix)
├── orchestrator_phase4.py              ← Devil's Advocate micro-loop
│
├── fastmcp_server.py                   ← MCP server exposing factory tools to local IDE
│   │                                      tools: launch_factory(), check_batch_status(), retrieve_backlog()
│
├── librarian_agent.py                  ← Retrospective: reads decisionLog, proposes promotions
├── proposed_promotions_schema.json     ← JSON schema for librarian output validation
│
├── global_brain/
│   ├── chroma_db/                      ← Vector database (4 pillars)
│   └── ingest_cold_archive.py          ← Indexes new archive-cold/ files into Chroma
│
├── prompts/
│   └── SP-010-librarian-agent.md
│
└── .env                                ← ANTHROPIC_API_KEY (never leaves Calypso)
```

### What Will Exist in the Cloud (Tier 3)

The Cloud tier is the **cognitive engine**. No persistent files live here. It is stateless from the workbench's perspective.

- **Anthropic Batch API**: Processes the Committee of Experts (Phase 2) JSONL payloads
- **Anthropic Messages API** (synchronous): Used by the Synthesizer (Phase 3) and Devil's Advocate (Phase 4) for complex reasoning calls
- **Model**: `claude-sonnet-4-5` (correcting the DOC6 hallucinated `claude-4.6-sonnet` identifier)
- **No data stored in Cloud**: All outputs flow back to Calypso immediately after completion

---

## 4. Migration Phases (The Roadmap)

---

### Phase A: Consolidate and Formalize the Memory Bank

**Phase Name and Goal:** Restructure the existing flat `memory-bank/` into the Hot/Cold architecture without breaking the current working system.

**Pedagogical Justification:**
This is the first phase because everything downstream depends on it. The Calypso orchestration scripts (Phases 2–4) will eventually deposit `final_backlog.json` into the local environment. The Librarian Agent will read `decisionLog.md`. The Developer Agent needs a stable `activeContext.md`. If the memory structure is wrong, **every subsequent phase is building on sand**. We fix the foundation before adding floors.

Additionally, this phase delivers immediate value even before Calypso exists: the current Developer Agent works better with a structured, bounded context than with 7 monolithic files loaded simultaneously. The context savings and reduction in "Lost in the Middle" errors are observable from day one.

**Concrete Steps:**

1. **Create the new directory structure inside the existing `memory-bank/`:**
   ```bash
   mkdir -p memory-bank/hot-context
   mkdir -p memory-bank/archive-cold/sprint-logs
   mkdir -p memory-bank/archive-cold/completed-tickets
   touch memory-bank/archive-cold/sprint-logs/.gitkeep
   touch memory-bank/archive-cold/completed-tickets/.gitkeep
   ```

2. **Migrate existing files to `hot-context/`:**
   ```bash
   # Move working files to hot-context
   mv memory-bank/activeContext.md memory-bank/hot-context/activeContext.md
   mv memory-bank/progress.md memory-bank/hot-context/progress.md
   mv memory-bank/decisionLog.md memory-bank/hot-context/decisionLog.md
   mv memory-bank/systemPatterns.md memory-bank/hot-context/systemPatterns.md
   mv memory-bank/productContext.md memory-bank/hot-context/productContext.md
   # Keep projectBrief.md and techContext.md in hot-context as well (project-level constants)
   mv memory-bank/projectBrief.md memory-bank/hot-context/projectBrief.md
   mv memory-bank/techContext.md memory-bank/hot-context/techContext.md
   ```

3. **Create `archive-cold/productContext_Master.md`** as the historical BDD accumulator (blank):
   ```bash
   touch memory-bank/archive-cold/productContext_Master.md
   ```
   Add the header:
   ```markdown
   # Product Context Master Archive
   *Full historical log of all completed BDD tickets. Populated automatically by memory:archive script. Human-readable, Git-versioned. Agents access via MCP semantic query only.*
   ```

---
