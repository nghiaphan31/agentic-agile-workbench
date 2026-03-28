# DOC6 Expert Review Results

**Document reviewed:** [`workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md`](../../workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md)
**Batch ID:** `msgbatch_01QkGMqo8AXmRcSvqccVzX3G`
**Retrieved at:** 2026-03-28 09:01 UTC
**Model:** `claude-sonnet-4-6`
**Total tokens:** 23,502 input / 12,288 output

---

## Table of Contents

1. [Review 1: Coherence & Clarity](#review-1-coherence--clarity)
2. [Review 2: Architectural Analysis](#review-2-architectural-analysis)
3. [Review 3: Implementation Feasibility](#review-3-implementation-feasibility)

---

## 📝 Review 1: Coherence & Clarity
**Expert persona:** Senior Technical Writer & Documentation Architect

*Tokens: 7,764 input / 4,096 output*

## 1. Executive Summary

- The document presents an ambitious and conceptually rich architecture for an AI-assisted software development pipeline, covering greenfield development, brownfield refactoring, tooling context, and infrastructure — demonstrating genuine depth of thinking.
- **The document's fundamental structural flaw is that it is a chat response, not a specification.** It retains first-person conversational framing ("your machine," "as per your request"), an unresolved closing question, and editorial headers ("Here is the complete…") that disqualify it as a standalone reference artifact.
- Internal consistency is undermined by undefined references (GAP-001/GAP-002, SP-004, SP-005, SP-006, "Calypso," `systemPatterns.md`, `productContext.md`) that are assumed rather than defined, creating a significant onboarding barrier for any new reader.
- Critical operational gaps exist: there is no error-handling strategy beyond the Devil's Advocate loop, no versioning or rollback protocol for the Memory Bank files, no SLA or latency expectations, and no security model for the 3-tier architecture.
- The document's quality of individual phase specifications is high and actionable, but it cannot yet function as an authoritative, team-shareable reference without targeted revision.

---

## 2. Document Structure Analysis

**Positive observations:**
- The four-part macro-structure (Greenfield Pipeline → Brownfield Workflow → Industry Validation → MCP/Infrastructure) follows a logical coarse-grained progression.
- Embedding system prompts and artifact templates within their respective phases is an effective design choice that reduces cross-reference burden.
- The use of consistent sub-sections per phase (Actor, Environment, Input, Action, Output, Gate) creates a reliable schema that aids navigation.

**Structural problems:**

| Issue | Location | Severity |
|---|---|---|
| Document opens with "Here is the complete, detailed restructuring of **your**..." — conversational framing, not a specification header | Preamble | Critical |
| Document closes with an open question to the reader | Final line | Critical |
| No table of contents | Global | High |
| No document metadata block (version, authors, date, status) | Global | High |
| Part 3 (Industry Validation) and Part 4 (MCP/Infrastructure) are architecturally foundational but placed *after* the operational phases they underpin | Global | High |
| Phase 5 and Phase 6 are described in the Brownfield section only by reference to their Greenfield counterparts, with no explicit delta | Part 2 | Medium |
| The "Inverted Phase 1" naming convention breaks the numeric ordering schema established in Part 1 | Part 2 | Medium |
| Placeholder image references (three instances of what appear to be missing images/diagrams based on context breaks) appear without captions or alt text | Phases 1, 6, and Part 2 header | Medium |
| `systemPatterns.md` and `productContext.md` are used throughout but never formally defined or templated, unlike the four Phase 1 files | Phases 2–6 | High |

**Missing sections:**
- A **Glossary** (the document relies on undefined terms throughout)
- A **System Overview / Architecture Diagram** as an introductory anchor
- A **Prerequisites and Environment Setup** section
- A **Failure and Recovery** section
- A **Document Scope and Intended Audience** statement

---

## 3. Internal Consistency Check

**Undefined terms and forward references:**

| Term/Reference | First Used | Defined? | Issue |
|---|---|---|---|
| `SP-004`, `SP-005`, `SP-006` | Phase 5, 6 | Never | Agent identifiers appear with no registry or explanation |
| `GAP-001`, `GAP-002` | Part 4 intro | Never | Referenced as known problems but never described |
| `systemPatterns.md` | Phase 3 input | Never templated | Used as input in Phase 3 but not created as an output of any prior phase |
| `productContext.md` | Phase 5 output | Never templated | Introduced as an output artifact but no schema is provided |
| `progress.md` | Phase 6 gate | Never templated | Referenced but not specified |
| `decisionLog.md` | Phase 5, 6 | Never templated | Referenced but not specified |
| "Calypso" | Part 4 | Never introduced | Appears suddenly as a named server; assumed to be the user's hardware but never stated |
| "Roo Code Memory Bank" / "Cline Memory Bank" | Part 3, Part 4 | Partially explained | Described in Part 3 after it is operationally required in Phase 1 |
| "Book of Laws" | Phase 4 | Informal alias | Used as a synonym for `systemPatterns.md` without a declared equivalence |

**Contradictions and inconsistencies:**

1. **Phase 1 outputs vs. Phase 3 inputs:** Phase 1 outputs `draft_prd.md` and `domain_lexicon.md`. Phase 3 lists `systemPatterns.md` as an input artifact — but `systemPatterns.md` has no defined creation point in the pipeline prior to Phase 3. It is implied to pre-exist, but this is never stated.

2. **PRD naming collision:** Phase 1 describes producing both a "`projectBrief.md` (The Constitution)" and a "`draft_prd.md`" as separate outputs. The Passing Criterion then refers to a "final PRD" being validated. It is unclear whether the `projectBrief.md`, the `draft_prd.md`, or some merged artifact is the authoritative PRD shipped to Phase 2. Phase 2's input lists only `draft_prd.md`.

3. **Batch API vs. Cloud model naming:** Part 4 specifies "Claude 4.6 Sonnet via Batch API" as the Tier 3 model. Phase 2 and 3 describe Cloud/Batch API usage without specifying the model. These should be consistent.

4. **Temperature specification conflict:** Phase 2 specifies Temperature 0.1–0.2 with Top-P 0.1. Phase 3 specifies Temperature 0.0–0.1. No rationale is given for the difference, and using both Top-P and Temperature simultaneously as restrictors without explanation is technically ambiguous.

5. **Devil's Advocate loop — agent count:** Phase 4 describes the Devil's Advocate as a *separate agent* debating the Synthesizer. Part 3's tooling references (LangGraph, CrewAI) imply this is a graph loop. The implementation model for this loop is never specified — is it a single model prompted differently, two separate API calls, or a LangGraph node cycle? This is operationally critical and unresolved.

6. **`activeContext.md` lifecycle:** Phase 6 states the system "empties `activeContext.md`" after a ticket completes. The Brownfield Phase 5/6 section reuses the same execution model but never addresses whether `activeContext.md` is shared, isolated per ticket, or reset between Greenfield/Brownfield runs.

---

## 4. Clarity and Precision

**Vague or abstract statements that require precision:**

| Statement | Location | Problem |
|---|---|---|
| "abandon the notion of 'free text' and treat LLMs as deterministic functions" | Phase 2 intro | Metaphorically evocative but technically imprecise. LLMs are not deterministic even at Temperature 0. The intended meaning (enforce structured output contracts) should be stated directly. |
| "purged of hallucination" (in `tdd_target` description) | Phase 4 output contract | Not a verifiable condition. What specific validation ensures this? |
| "Prompts synchronization ensures local agents have read the latest `systemPatterns.md`" | Phase 5 gate | The mechanism for this synchronization is never described. |
| "Graceful Degradation: The Synthesizer is allowed a limited number of attempts (e.g., 2)" | Phase 4 | "e.g., 2" signals this is illustrative, not specified. A reference document requires a fixed value or a configuration parameter reference. |
| "The Asynchronous Factory stops" | Phase 4 gate | Ambiguous — does it stop permanently, hand off, or await human intervention? The transition to Phase 5 is implied but not made explicit. |
| "This architecture reconstructs the state of the art in agentic software engineering (circa early 2026)" | Part 3 header | A marketing/conversational claim with no place in a technical specification. |
| "an RTX 5060 Ti 16GB cannot run 5 frontier models locally" | Part 4 | Hardware-specific assumption that will become stale and may not apply to all readers/deployments. |
| "so as not to lose them" (re: `tech_parking_lot.md`) | Phase 1 memory bank | Acceptable in conversation; imprecise in a spec. Should state the functional purpose: *preserving human proposals for post-PRD technical design phases.* |

**Sections a new reader would find confusing:**

- **The entire Phase 4 Devil's Advocate loop** lacks a sequence diagram or pseudo-code. The attack/defense/escalation cycle is described narratively but the state machine is not defined. A reader implementing this would have multiple valid interpretations.
- **The Brownfield "Adapted Phase 3 and 4"** section is a brief paragraph summarizing what Greenfield Phases 3 and 4 do differently. It uses terms like "characterization tests" and "refactoring slicing" without definition, and provides no artifact contracts or system prompts — creating a significant asymmetry with the Greenfield specification depth.
- **Part 4's "Hybrid Cognitive Architecture"** introduces Hot/Cold Memory perimeter separation without connecting it explicitly to any specific phase. A reader cannot determine at which phase the Cold perimeter is populated or how the RAG retrieval integrates with agent prompts.

---

## 5. Completeness Assessment

**Gaps between stated goals and documented content:**

**Operational Gaps:**

1. **No error handling beyond the Devil's Advocate:** What happens if the Batch API call fails mid-flight in Phase 2? If a Phase 3 schema validation fails? If `ideation_state.md` is corrupted? There is no recovery protocol anywhere in the document.

2. **`systemPatterns.md`, `productContext.md`, `progress.md`, `decisionLog.md` have no templates.** Four of the Phase 1 Memory Bank files receive full templates; the equally critical Workbench files receive none. This is the single largest completeness gap.

3. **No agent-to-agent communication protocol for Phase 2.** The document states agents "do not communicate with each other at this stage" but does not describe how their outputs are collected, named, and stored for Phase 3 consumption.

4. **No CI/CD or deployment integration.** Phase 6 produces validated source code. What happens next? The pipeline has no documented connection to version control commits, deployment pipelines, or sprint review processes.

5. **No token budget / cost model.** The document explicitly references cost as a driver ("explore all technical dimensions at a lower cost," "drastically reduces API costs"). No estimates, guardrails, or token budget limits are provided for any phase.

**Security and Access Control Gaps:**

6. **The 3-Tier Architecture's security model is limited to "API keys secured on Calypso."** For a document that gives Security a P0 priority in its own Priority Matrix, the infrastructure section contains no authentication model, no inter-tier communication security, no secret rotation policy.

7. **The `tech_parking_lot.md` contains human proposals including implementation choices.** No access control or handling policy is defined for when this file is later consumed in technical phases — creating a risk that "parked" proposals re-enter as constraints.

**Brownfield-Specific Gaps:**

8. **No equivalent Memory Bank specification for Brownfield.** The Greenfield pipeline has four defined Memory Bank files. The Brownfield workflow introduces `draft_prd_brut.md` and `current_techContext.md` but does not integrate them into a defined file system structure.

9. **No handling of partial brownfield migrations** — the document treats brownfield as a full reverse-engineering exercise but does not address incrementally migrating one module of a larger legacy system.

---

## 6. Prioritized Improvements

### P0 (Critical) — Must fix before this document can be used as a reference

- **P0-1: Remove all conversational framing.** Strip the opening paragraph ("Here is the complete, detailed restructuring of *your*..."), the closing question, and all instances of "your machine," "as per your request." Replace with a formal document header including title, version, status, authors, and date.

- **P0-2: Define all undefined file artifacts.** Provide canonical templates for `systemPatterns.md`, `productContext.md`, `progress.md`, and `decisionLog.md` equivalent in detail to the Phase 1 templates. These files are load-bearing throughout the pipeline.

- **P0-3: Resolve the PRD naming collision.** Clarify the relationship between `projectBrief.md` and `draft_prd.md`. Define exactly one authoritative artifact that is passed as input to Phase 2 and name it consistently throughout.

- **P0-4: Define SP-004, SP-005, SP-006 and GAP-001, GAP-002.** Either provide an Agent Registry section or remove these identifiers and replace them with descriptive names. GAP-001/002 must be described or removed entirely.

- **P0-5: Specify the creation point of `systemPatterns.md`.** The document uses it as a Phase 3 input with no prior creation step. Either add it as a pre-existing prerequisite (with a setup instruction) or define which phase produces it.

- **P0-6: Add a Glossary.** Define "Calypso," "Memory Bank," "Green Ticket," "Orange Ticket," "Asynchronous Factory," "Hot/Cold Perimeter," "Book of Laws," and "TDD Target" in a single reference section. "Book of Laws" must be explicitly equated to `systemPatterns.md` or given its own identity.

### P1 (Important) — Should fix to improve usability

- **P1-1: Add a document Table of Contents** with anchor links to all phases and sub-sections.

- **P1-2: Add an Architecture Overview diagram** (or define a canonical Mermaid source block) showing all phases, data flows between them, artifact hand-offs, and the 3-tier infrastructure — ideally at the start of the document.

- **P1-3: Specify the Devil's Advocate loop implementation.** Provide a state machine or sequence diagram. Define whether this is a single-model self-critique loop or a two-model API pattern. Define the exact retry count as a configuration constant, not an example.

- **P1-4: Add a Failure and Recovery section.** For each phase, specify the behavior on API failure, schema validation failure, and file system corruption. At minimum, define whether the system halts, retries, or escalates to human.

- **P1-5: Provide Brownfield artifact contracts.** The Brownfield section must receive equivalent artifact templates and system prompt specifications to Phase 1–6 of the Greenfield pipeline. Current asymmetry makes Brownfield unimplementable from this document alone.

- **P1-6: Replace hardware-specific claims with configuration parameters.** Move the RTX 5060 Ti reference into an appendix or example configuration. The 3-tier architecture section should specify a hardware *profile* (e.g., "local GPU with ≥8GB VRAM for routing model tier") rather than a product name.

- **P1-7: Unify model/temperature specifications.** Create a single "Model Configuration" table listing each phase, the applicable model, temperature, Top-P, and output format. Resolve the Phase 2/3 temperature discrepancy with explicit rationale.

### P2 (Nice to have) — Minor polish

- **P2-1:** Replace "purged of hallucination" with a precise validation criterion (e.g., "passes schema validation and Gherkin linter with zero lint errors").

- **P2-2:** Remove the claim "reconstructs the state of the art... circa early 2026." Replace with a "Related Work and Influences" section if industry alignment is desired, framed factually.

- **P2-3:** Add a "Prerequisites" section listing required tooling (VS Code, Roo Code/Cline, Batch API access, Calypso server configuration) and environment setup steps, so the document is self-contained for a new team member.

- **P2-4:** Add estimated token costs or relative cost indicators per phase to support the document's stated cost-optimization goals.

- **P2-5:** Replace all three missing image/diagram placeholders with either actual diagrams, Mermaid code blocks, or explicit `[DIAGRAM PENDING: description]` callouts so readers know what visual is intended.

- **P2-6:** Add a `CHANGELOG` section or version history table to the document header to support future revision tracking.

---

## 7. Verdict

**Needs revision**

The document contains genuinely sophisticated

---

## 🏗️ Review 2: Architectural Analysis
**Expert persona:** Principal Software Architect

*Tokens: 7,826 input / 4,096 output*

# Architectural Review: Agentic Agile Workbench

---

## 1. Executive Summary

- The architecture demonstrates **sophisticated conceptual thinking** about agentic pipelines, correctly separating asynchronous "factory" work from synchronous "workbench" execution, and showing genuine awareness of LLM failure modes (amnesia, hallucination, context overflow).
- **Critical state management gaps** exist throughout: the file-based "Memory Bank" is a single point of failure with no locking, versioning, or conflict resolution, making concurrent or resumed sessions inherently unsafe.
- The **JSON contracts between phases are underspecified**: missing schema versioning, no envelope for errors/partial results, ambiguous array item types, and no idempotency keys — making the pipeline brittle at every phase boundary.
- The **security posture is aspirational rather than implemented**: API key management is mentioned but not architected, the local filesystem holds sensitive artifacts without protection, and the MCP server attack surface is entirely unaddressed.
- The **Devil's Advocate loop (Phase 4) has an unbounded failure mode** and the overall pipeline lacks observable retry semantics, distributed tracing, rollback capability, and formal SLAs for any phase transition gate.

---

## 2. Architectural Soundness

### Phase 1 — Ideation Workshop
**Issues:**
- The "Memory Bank" uses raw Markdown files on a local filesystem as the sole persistence mechanism. This is a **single point of failure**: file corruption, concurrent write collisions (if multiple sessions exist), or an agent crash mid-write leaves the system in an indeterminate state with no recovery path.
- The `draft_prd.md` is described as "updated silently in the background" while a conversation is happening. This implies the LLM is performing **concurrent reads and writes within a single context window**, which is not how LLM inference works. There is no transactional write mechanism — a partial update mid-session is a corruption event.
- The "Scope Lock Gate" (human formal approval) has **no artifact fingerprinting**. Nothing prevents the PRD from being modified after approval, invalidating all downstream work without detection.
- The `tech_parking_lot.md` extraction is a **business logic encoded in a system prompt**, not enforced by schema. An LLM will occasionally mis-classify "How" vs. "What", with no automated correction path.

### Phase 2 — Committee of Experts (Batch)
**Issues:**
- Agents "do not communicate with each other at this stage" is architecturally correct for independence, but creates a known problem: the Architecture Agent and Security Agent will produce **structurally contradictory outputs** (e.g., recommending different auth mechanisms) with no intra-phase resolution. All contradiction handling is deferred to Phase 3, increasing Synthesizer cognitive load unpredictably.
- `temperature: 0.1`, `top_p: 0.1` simultaneously is **redundant and potentially harmful**. These two parameters interact multiplicatively; setting both near-zero can cause degenerate token distributions in some model backends, causing repetition loops. Choose one constraint.
- "Context Window: Maximum. The complete PRD and lexicon must be injected entirely" — this is a **naive context management strategy**. For large PRDs, this will exceed practical limits and the document offers no fallback. The MCP RAG solution in Part 4 is proposed as a fix but not integrated back into Phase 2's design.
- The Batch API completion check ("100% of agents finished") has **no timeout or dead-letter handling**. A single hung batch job blocks the entire pipeline.

### Phase 3 — Synthesizer
**Issues:**
- The Synthesizer is described as a "logical compiler" operating at `temperature: 0.0`, but it is also expected to exercise **judgment** (Priority Matrix arbitration, conflict resolution, deduplication). These are incompatible goals. A deterministic temperature is appropriate for formatting; the arbitration logic requires probabilistic reasoning and will produce inconsistent results at `0.0` across different model versions.
- `systemPatterns.md` appears as an input here for the first time, but its genesis is never defined in the Greenfield pipeline. It is a **ghost artifact**: referenced but never created by any prior phase.
- The Gherkin Linter gate is correct in principle but the document provides **no specification of which linter, what rule set, or how linter failures are surfaced** back to the Synthesizer for correction.

### Phase 4 — Devil's Advocate
**Issues:**
- The "limited number of attempts (e.g., 2)" is a critical design decision expressed as a parenthetical example. The **retry budget is undefined** at the contract level, meaning the loop termination condition is ambiguous in implementation.
- The "Synthesizer modifies the test to integrate the constraint and resubmits it" implies **stateful agent memory across loop iterations**, but the architecture provides no mechanism for the Synthesizer to maintain its reasoning state between attack/defense rounds without re-injecting the full prior context, which grows with each iteration — a context window bomb.
- **Orange Ticket escalation reason** quality is entirely LLM-dependent with no structured template, making Phase 5 human triage inconsistent.

### Phase 5 — Triage (Human Gate)
**Issues:**
- "Prompts synchronization ensures local agents have read the latest `systemPatterns.md`" is stated as a passing criterion but is **architecturally undefined**. How is this verified? File modification timestamps? Hash comparison? This is a critical correctness guarantee with no implementation.
- Option C ("Force the ticket to GREEN with manual boundaries") introduces a **human override path that bypasses all automated validation**. This is necessary for pragmatism but must be logged as a formal audit event. The document treats it casually.

### Phase 6 — TDD Execution
**Issues:**
- `activeContext.md` is a single file representing the currently active ticket. This means **only one ticket can be in flight at any time**, creating a hard serialization constraint with no architectural justification. Parallelism is implicitly abandoned here.
- The "tunnel vision" protection (restricted file list) is implemented by including the list in a Markdown file that the AI reads. This is a **prompt-level constraint, not a sandbox constraint**. The Developer Agent can still attempt to read or write files outside scope; only enforcement at the filesystem or tool-call level would prevent this.
- The `activeContext.md` template embeds a Gherkin block inside a Markdown code fence, which terminates the outer Markdown fence prematurely — a **document formatting bug** that will cause parsing failures in any automated processor.

---

## 3. Scalability and Resilience

### Bottlenecks

| Bottleneck | Location | Impact |
|---|---|---|
| Sequential file I/O on local filesystem | Phase 1, 5, 6 | All state changes are blocking; no parallelism |
| Single-threaded `activeContext.md` | Phase 6 | Hard serialization of all development work |
| Batch API completion polling | Phase 2 | No partial progress; 100% completion or full stall |
| Context window "inject everything" | Phase 2 | Hard failure on large PRDs with no graceful degradation |
| Calypso as single orchestrator | Tier 2 | SPOF for the entire pipeline routing |

### Failure Propagation
The pipeline is designed as a **strict linear sequence of gates**. This means any phase failure propagates as a full stop. There is no:
- **Partial success handling** (e.g., 3 of 4 expert agents succeed in Phase 2)
- **Checkpoint/resume semantics** (if Phase 3 fails mid-synthesis, the whole phase restarts)
- **Circuit breakers** on the Cloud API tier
- **Backpressure** from the Workbench to the Factory if the local execution queue is overloaded

### Load Behavior
The 3-Tier architecture is conceptually sound, but under load:
- Calypso has **no defined queue management** — concurrent `launch_factory()` calls have undefined behavior
- The Cloud Batch API has rate limits and quota constraints that are entirely unaddressed
- The local filesystem state store does not scale beyond a single developer; no mention of team collaboration scenarios

---

## 4. Data Flow and State Management

### Artifact Lineage Map

```
raw_idea
  └─► draft_prd.md ──────────────────────────────────────┐
  └─► domain_lexicon.md                                   │
  └─► tech_parking_lot.md                                 │
                                                          │
  [Phase 2 JSON Reports] ◄────────────────────────────────┤
        │                                                  │
        ▼                                                  │
  draft_backlog.json ◄── systemPatterns.md (UNDEFINED ORIGIN)
        │
        ▼
  final_backlog.json
        │
        ▼
  productContext.md + systemPatterns.md (updated)
        │
        ▼
  activeContext.md (single ticket)
        │
        ▼
  source code + tests
```

### JSON Contract Deficiencies

**Phase 2 Output Schema — Missing Fields:**
```json
// CURRENT (incomplete)
{
  "domain": "Security",
  "identified_risks": [...],
  "technical_constraints": [...],
  "proposed_entities": [...],
  "edge_cases": [...]
}

// REQUIRED ADDITIONS
{
  "schema_version": "1.0.0",          // No versioning — breaking changes are silent
  "agent_id": "security-agent-01",    // No agent identity for audit
  "execution_timestamp": "ISO8601",   // No temporal provenance
  "prd_hash": "sha256:...",           // No input binding — cannot detect stale reports
  "confidence_scores": {},            // No uncertainty quantification
  "error": null,                      // No error envelope — partial failures are invisible
  "identified_risks": [
    {
      "id": "RISK-001",               // Array items are untyped strings, not objects
      "description": "...",
      "severity": "HIGH",
      "prd_reference": "Rule-3.2"     // No traceability to source PRD element
    }
  ]
}
```

**Phase 3/4 Backlog Schema — Missing Fields:**
```json
// MISSING
{
  "task_id": "TASK-001",
  "schema_version": "1.0.0",
  "idempotency_key": "hash(bdd_scenario)",  // No idempotency — reprocessing creates duplicates
  "parent_prd_section": "Journey-2",
  "estimated_complexity": null,             // No sizing signal for sprint planning
  "test_file_path": null,                   // No explicit file target for Developer Agent
  "dependencies": [],                       // No task dependency graph
  "status_history": []                      // No state machine audit log
}
```

### State Machine Ambiguities
- There is **no defined state machine** for ticket lifecycle. Tickets go from existence → GREEN/ORANGE, but transitions back (e.g., GREEN→ORANGE after Phase 5 review) are mentioned without formal state definitions.
- `productContext.md` is described as being "populated with the clean backlog" in Phase 5, but it already exists as part of the Workbench. The merge/overwrite semantics are undefined — **destructive overwrite of in-flight work is possible**.

---

## 5. Security Architecture

### Critical Vulnerabilities

**1. API Key Exposure**
The document states Calypso "secures API keys" as a benefit, but provides no specification of how. Questions that must be answered:
- Are keys stored in environment variables, a secrets manager (Vault, AWS SSM), or config files?
- How are keys rotated without restarting the pipeline?
- How is Calypso itself authenticated to by the local workstation?
- The FastMCP server on Calypso exposes `launch_factory(prd_path)` — is this endpoint authenticated? A malicious call to this endpoint with an arbitrary `prd_path` is a **path traversal + prompt injection vector**.

**2. Prompt Injection Attack Surface**
Every phase that reads external artifacts (code, PRD content, user input) into a prompt is vulnerable to prompt injection. The document has **zero mitigations**:
- Phase 1: Raw human input is directly injected into agent context
- Brownfield Phase 1: Raw source code is injected into the Analyst Agent prompt — a **critical injection vector** (malicious comments in legacy code can hijack the agent)
- Phase 4 backlog items flow from cloud agents through Calypso to local agents with no sanitization layer

**3. Sensitive Data in Plaintext Markdown**
- `draft_prd.md`, `domain_lexicon.md`, and all backlog files may contain **PII, business trade secrets, and compliance requirements** (the Security Agent is explicitly tasked with identifying PII). These sit as plaintext on the local filesystem with no encryption at rest, no access controls beyond OS permissions, and no data classification tagging.
- The RAG/vector database (Cold Memory) will **index and embed sensitive business logic**, creating a persistent exfiltration risk if the vector store is compromised.

**4. MCP Server Attack Surface**
The document recommends 7+ MCP servers with capabilities including filesystem access, database queries, Git operations, and test execution. This is a **significant attack surface expansion** with no:
- Authentication/authorization model for MCP tool calls
- Input validation on MCP tool parameters
- Audit logging of MCP operations
- Sandboxing of the test executor MCP (arbitrary code execution risk)

**5. Brownfield Code Analysis**
The Analyst Agent reads "entire source code" which may contain **hardcoded secrets, credentials, or private keys** that would be embedded into the agent's context and potentially into `draft_prd_brut.md`.

**6. Supply Chain Risk**
The document lists specific MCP server packages (`mcp-server-memory`, `crystaldba/postgres-mcp`, etc.) with no mention of:
- Package integrity verification
- Dependency pinning
- Security audit of third-party MCP server code

---

## 6. Missing Architectural Concerns

### Observability (Complete Absence)
There is no specification of:
- **Distributed tracing** across phases (no trace ID propagates through the pipeline)
- **Metrics collection** (token usage, phase latency, gate pass/fail rates)
- **Centralized logging** (each phase presumably logs locally, if at all)
- **Alerting** (no definition of what constitutes an alertable failure vs. expected degradation)
- **Cost tracking** (Batch API costs are mentioned as a benefit but never tracked)

Without observability, debugging a failure in Phase 3 that originates from corrupted Phase 2 output is a manual forensic exercise.

### Idempotency and Replay
No phase is designed to be idempotent:
- Re-running Phase 2 with the same PRD will generate new reports with different `task_id` values (if UUIDs are time-based), creating duplicate backlog entries
- Phase 3 synthesis has no mechanism to detect it already processed a given set of Phase 2 reports
- There is no "dry run" mode for any phase

### Schema Versioning and Pipeline Versioning
- JSON schemas have no version field. When the Architecture Agent schema changes (adding a new key), downstream Synthesizer prompts will silently mishandle the new field.
- There is no versioning of the pipeline itself. A bug fix to the Phase 3 Synthesizer prompt cannot be deployed to in-flight pipelines without undefined consequences.

### Rollback and Compensating Transactions
- If Phase 5 human triage determines that Phase 3 synthesis was fundamentally wrong, there is no defined rollback path. The document implies manually editing files.
- `systemPatterns.md` is mutated across multiple phases. There is no immutable history of this file (Git is mentioned in MCP servers but not integrated into the pipeline's state management).
- No **saga pattern** or compensating transaction mechanism exists for multi-phase failures.

### Error Budget and Graceful Degradation
- What happens when the Batch API returns a 429 (rate limit)? Timeout? 500?
- What is the defined SLA for each phase?
- What is the escalation path when all 4 expert agents fail validation in Phase 2?

### Multi-Developer / Team Collaboration
The entire architecture assumes a **single developer, single machine, single in-flight project**. There is no:
- Multi-tenancy consideration
- Concurrent project isolation
- Shared `systemPatterns.md` governance across team members
- Merge conflict resolution for simultaneously modified Markdown artifacts

### LLM Model Versioning and Drift
- The architecture is described as using "Claude 4.6 Sonnet" but makes no provision for:
  - Model deprecation events breaking prompt contracts
  - Non-determinism drift between model versions (a Phase 3 Synthesizer prompt that worked on Sonnet 3.5 may produce different JSON structure on 4.6)
  - Fallback models if the primary model is unavailable

### Testing the Pipeline Itself
There is no specification of how the pipeline is tested:

---

## ⚙️ Review 3: Implementation Feasibility
**Expert persona:** Senior Platform Engineer & DevOps Architect

*Tokens: 7,912 input / 4,096 output*

# Implementation Feasibility Review: Agentic Agile Workbench

---

## 1. Executive Summary

- The architectural vision is conceptually sound and aligns with legitimate patterns (Memory Bank, BDD/TDD convergence, multi-agent orchestration), but the document operates at a **design-fiction level** — it describes *what* without specifying *how*, leaving most critical implementation details unresolved.
- The **3-tier hardware assumption is flawed**: the RTX 5060 Ti 16GB is an unreleased consumer GPU (as of mid-2025) being asked to serve as a production orchestration tier, running routing LLMs, vectorization, and a FastMCP server simultaneously — an overloaded role for the described hardware.
- The **Batch API usage** (Phase 2 and 3) introduces 15–60 minute latency gaps that are architecturally unacknowledged — the document treats batch responses as near-synchronous, which they are not, and provides no retry, failure, or partial-completion handling.
- The **MCP server layer is underspecified**: several recommended servers are experimental, unmaintained, or fictitious (e.g., `excalidraw-architect-mcp`, `mcp-server-jest`), and no `mcp.json` configuration, authentication model, or inter-server communication protocol is provided.
- The **Devil's Advocate loop** (Phase 4) is the most architecturally innovative component but is also the least specified — the "limited attempts" mechanism, conflict resolution logic, and escalation pathway lack any concrete implementation.

---

## 2. Tooling and Technology Choices

### VS Code + Roo Code / Cline
**Assessment: Appropriate, but version-locked.** Roo Code is a maintained fork of Cline with MCP support. Both are production-usable for agentic coding. The document correctly identifies these as the local execution layer. However, no extension version pinning is specified, and both tools have breaking changes between minor versions. **Risk: Medium.**

### Anthropic Batch API (Claude 4.6 Sonnet)
**Assessment: Problematic model reference.** "Claude 4.6 Sonnet" does not exist as of this review. The current production model is `claude-sonnet-4-5` (claude-sonnet-4-5-20251001 range). This is either a hallucinated model identifier or a forward-looking placeholder. Using a non-existent model ID will cause immediate API rejection. **Risk: P0 blocker.**

### LangGraph & CrewAI (mentioned as orchestration engines)
**Assessment: Appropriate mention, but neither is actually implemented.** The document references them as validation for the architecture pattern but proposes a *custom FastMCP server* (Calypso) as the actual orchestration mechanism. This creates a gap: no orchestration framework is actually specified for the Devil's Advocate loop, the batch polling logic, or the agent-to-agent JSON passing. **Risk: High — the entire multi-agent coordination layer is unimplemented.**

### Gherkin / BDD Tooling
**Assessment: Referenced but unanchored.** The document mandates a "Gherkin Linter" as a gate in Phase 3 but names no specific tool. Options include `cucumber`, `behave`, `pytest-bdd`, or `jest-cucumber` — each with different syntax validation behavior. Without specifying the linter, the "Gherkin Linter gate" is not implementable. **Risk: Medium.**

### FastMCP (Calypso custom server)
**Assessment: Feasible but significantly underspecified.** FastMCP is a legitimate Python framework for building MCP servers. However, the proposed tools (`launch_factory`, `check_batch_status`, `retrieve_backlog`) require: async job queue management, persistent state storage between calls, Anthropic Batch API polling logic, and secure credential management. None of this is designed in the document. **Risk: High.**

### Llama-4 8B (routing model on Calypso)
**Assessment: Model name is speculative.** "Llama-4 8B" is not a released model as of mid-2025. Meta has released Llama 3.1/3.2/3.3 series. If this is a forward-looking placeholder, that must be stated. The actual routing/validation use case could be served by `Llama-3.2-3B-Instruct` or `Phi-3.5-mini-instruct` on 16GB VRAM. **Risk: Medium (naming), Low (concept).**

### Mem0 MCP Server / Chroma MCP
**Assessment: Mixed production-readiness.** Mem0 has an MCP server in active development. Chroma has community MCP adapters. Neither is enterprise-production-hardened. For a system where "the Lead PM Agent has the obligation to read these files before speaking," a reliability failure in the memory layer cascades into every phase. **Risk: Medium-High.**

---

## 3. MCP Ecosystem Assessment

### Production-Ready Servers

| Server | Status | Notes |
|---|---|---|
| `github-mcp-server` | ✅ Production-ready | Officially maintained by GitHub/Anthropic |
| `mcp-server-git` | ✅ Stable | Part of the official MCP reference implementations |
| `postgres` MCP | ✅ Stable | Multiple maintained implementations exist |
| `sqlite` MCP | ✅ Stable | Reference implementation available |
| Sourcegraph Cody MCP | ⚠️ Beta | Enterprise-tier; requires Sourcegraph instance |

### Experimental / Unverified Servers

| Server | Status | Issue |
|---|---|---|
| `mcp-server-memory` | ⚠️ Experimental | Anthropic reference impl; no persistence guarantees |
| `excalidraw-architect-mcp` | ❌ Unverified | No public repository found; likely fictitious or renamed |
| `mcp-server-jest` | ❌ Unverified | No established implementation found in MCP registries |
| `mcp-server-pytest` | ⚠️ Community | Fragmented implementations; no canonical version |
| `crystaldba/postgres-mcp` | ⚠️ Niche | Real but very early-stage |
| `mermaid-mcp-server` | ⚠️ Community | Exists but diagram rendering in agentic loops is brittle |

### Missing from MCP Configuration

1. **Authentication model**: No OAuth, API key rotation, or mTLS specification between Calypso and the local workstation.
2. **MCP server orchestration**: When multiple MCP servers are active simultaneously, tool namespace collision and routing priority are unaddressed.
3. **No `mcp.json` is actually provided** — the document ends by *offering* to create it but never does. This is the single most critical missing artifact for implementation.
4. **Error handling contracts**: What happens when the Chroma MCP server is unavailable mid-session? The Memory Bank reading requirement in Phase 1 becomes a hard dependency with no fallback.
5. **Tree-sitter AST parser MCP**: No established MCP server exists for Tree-sitter. Direct Tree-sitter integration in Python/Node is straightforward, but wrapping it as an MCP tool requires custom implementation not described here.
6. **Rate limiting and backpressure**: No MCP-level throttling to prevent the Calypso tier from flooding the Anthropic API.

---

## 4. 3-Tier Architecture Feasibility

### Hardware Assumption: RTX 5060 Ti 16GB

**This GPU does not exist as a shipping product as of mid-2025.** NVIDIA has announced the RTX 5060 Ti, but availability and final specs (including confirmed 16GB VRAM variant) are not yet established in the consumer market. The architecture is being designed around vaporware specifications.

Assuming an equivalent GPU with 16GB VRAM (e.g., RTX 4080 Super 16GB or RTX 3090 24GB), the workload assigned to Calypso is:

| Task | VRAM Requirement | Feasibility on 16GB |
|---|---|---|
| Llama-4 8B inference (routing) | ~8–10GB (Q4) | ✅ Tight but feasible |
| Embedding/vectorization (Chroma) | ~2–4GB | ✅ Feasible |
| FastMCP server process | Minimal (CPU-bound) | ✅ Feasible |
| Simultaneous routing + vectorization | ~12–14GB combined | ⚠️ Marginal |
| Any batch prompt pre-processing | +2–4GB spike | ❌ Will OOM |

**Conclusion:** The simultaneous operation of a routing LLM, embedding model, and vectorization pipeline on 16GB VRAM is **marginal to infeasible** without aggressive quantization (Q3/Q4) and sequential (not concurrent) model loading. The document assumes concurrent operation.

### Network Latency and Reliability Risks

1. **Local ↔ Calypso link**: Assumed to be LAN/local network. If Calypso is a home server or NAS-class machine, network reliability (especially for long-running batch polling) is not enterprise-grade. A 12-hour batch job polling over a home network is a real failure scenario.

2. **Calypso ↔ Anthropic Batch API**: No retry logic, exponential backoff, or dead-letter queue is specified. Anthropic's Batch API has its own rate limits and occasional processing delays.

3. **State consistency**: The document has the Workbench writing to Markdown files (`activeContext.md`, `systemPatterns.md`) while Calypso simultaneously reads them for batch preparation. No file locking, versioning, or conflict resolution is specified. This is a **race condition risk**.

4. **Failure atomicity**: If Calypso crashes mid-batch (Phase 2), there is no checkpoint/resume mechanism. The entire 4-agent batch would need to be resubmitted.

---

## 5. Batch API Usage

### Temperature and Top-P Settings

| Phase | Temp | Top-P | Assessment |
|---|---|---|---|
| Phase 2 (Expert Agents) | 0.1–0.2 | 0.1 | ⚠️ Problematic combination |
| Phase 3 (Synthesizer) | 0.0–0.1 | Implied low | ✅ Appropriate for compilation task |

**Critical Issue — Top-P=0.1 with Temperature=0.1–0.2**: These settings are intended to produce highly deterministic outputs, but the combination is more aggressive than necessary and risks **degenerate repetition** in longer JSON outputs. Anthropic's guidance typically recommends adjusting either temperature *or* top-p, not both to extremes simultaneously. For structured JSON output tasks, `temperature=0.0` with `top_p=1.0` (default) or `temperature=0.1` with `top_p=0.95` is more robust. The dual-constraint approach can cause the model to get "stuck" in local probability maxima, producing syntactically valid but semantically repetitive JSON arrays.

### Cost Implications

Anthropic Batch API pricing is approximately 50% of standard API pricing with up to 24-hour turnaround. For the described pipeline:

- Phase 2: 4 agents × full PRD context (~10K–50K tokens input each) = **40K–200K input tokens per batch**
- Phase 3: 1 synthesizer × 4 expert reports + PRD = **~80K–300K input tokens**
- Phase 4: Devil's Advocate loop × N iterations = **variable, potentially 2–5× Phase 3**

At claude-sonnet pricing (~$3/MTok input, $15/MTok output at batch discount ~50%), a single pipeline run could cost **$5–$40 depending on PRD complexity**. This is not prohibitive but is also not "drastically reduced" compared to synchronous API calls — the cost saving is real (~50%) but the document implies near-zero cost which is misleading.

### Latency Implications

**This is the most underacknowledged risk in the document.** Anthropic Batch API has a guaranteed SLA of *up to 24 hours*. In practice, batches often complete in 15 minutes to 4 hours. The document describes this pipeline as if it flows sequentially (Phase 2 → gate → Phase 3 → gate → Phase 4), meaning:

- **Minimum realistic pipeline time (Phases 2–4): 45 minutes to 12+ hours**
- The document never communicates this to the human stakeholder
- Phase 5 (Human Triage) cannot begin until Phase 4 completes — meaning the human who "disconnected after Phase 1" may wait hours before receiving Orange Tickets

The document's framing of "The human system can disconnect" after Phase 1 implies a fast turnaround that the Batch API cannot guarantee.

---

## 6. Brownfield Workflow Feasibility

### Analyst Agent (Code → PRD)

The concept is well-established (tools like Aider, Copilot, and various code-analysis pipelines do similar things), but the implementation as described has serious practical limitations:

**Token limit collision**: The instruction "reads your entire source code" is immediately problematic. A real legacy codebase of 100K–2M lines of code cannot be injected into a single context window. The document acknowledges this problem (GAP-001/GAP-002) but the proposed solution (Tree-sitter AST MCP) is itself unimplemented. For a 500K-line Java monolith, even AST summaries may exceed 200K tokens.

**The `[BUSINESS AMBIGUITY]` tag mechanism**: Elegant in concept, but the downstream handling of these tags in the Phase 1 synchronous workshop is not specified. How does the Lead PM Agent prioritize which ambiguities to address? How are they de-duplicated if 40 ambiguities are found? This workflow could quickly overwhelm the human.

**Dead code identification**: Instructing an LLM to "ignore dead code" is unreliable. Static analysis tools (e.g., `vulture` for Python, `ts-prune` for TypeScript, `PMD` for Java) do this deterministically and should be prerequisites. The document assumes LLM judgment for a task that has established tool solutions.

**Characterization Tests (Adapted Phase 3)**: This is the strongest part of the Brownfield section and aligns with Michael Feathers' "Working Effectively with Legacy Code." The approach of "freeze current behavior with tests before refactoring" is correct methodology. However, the document doesn't address the most common blocking condition: code that cannot be tested without significant seam-introduction (e.g., static method calls, singleton abuse, direct database access in business logic). The Devil's Advocate would correctly flag these, but the human resolution path (Option B: Architectural Update) could cascade into a refactoring scope that dwarfs the original plan.

**Coupling with Phase 6 execution**: The "Surgical Execution" section describes a micro-cycle but doesn't address rollback strategy if a characterization test passes pre-refactor and fails post-refactor due to an unexpected coupling. In a CI-less legacy environment, this is a common and dangerous scenario.

---

## 7. Prioritized Improvements

### P0 (Critical — Implementation Blockers)

**P0-1: Non-existent model identifier**
`claude-4.6-sonnet` must be replaced with a real, currently available Anthropic model identifier (e.g., `claude-sonnet-4-5` or equivalent). All Batch API calls will fail with an invalid model error until corrected.

**P0-2: Missing `mcp.json` and server startup configuration**
The document ends by offering to create this file but never does. Without `mcp.json`, the MCP layer (which underpins the entire architecture from Phase 5 onward) cannot be initialized. This is the single most critical missing artifact.

**P0-3: No orchestration framework specified for multi-agent loops**
The Devil's Advocate loop (Phase 4), batch job polling, and agent-to-agent JSON passing require an actual implementation — a Python script, LangGraph graph definition, CrewAI crew, or equivalent. The document describes agent behavior but provides zero executable orchestration code or even pseudocode. Nothing runs without this.

**P0-4: No file-locking or state consistency mechanism**
Concurrent read/write of shared Markdown files (`systemPatterns.md`, `activeContext.md`) between the local workstation and Calypso is an unaddressed race condition. In a multi-process system, this will cause data corruption or stale reads without a locking mechanism (file locks, SQLite WAL, or a message queue).

**P0-5: Fictitious or unverifiable MCP servers**
`excalidraw-architect-mcp` and `mcp-server-jest` cannot be installed because no canonical package exists. Any setup procedure referencing these will fail immediately.

### P1 (Important — Significant Gaps)

**P1-1: Batch API lat

---
