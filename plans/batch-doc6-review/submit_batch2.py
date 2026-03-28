"""
submit_batch2.py
----------------
Second-pass Anthropic Message Batch for the Agentic Agile Workbench vision analysis.

This batch submits 3 parallel expert requests that:
1. Re-analyze BOTH Gemini conversations (DOC6 + _Agentic Workbench Architecture Explained)
2. Take into account the previous batch review results (DOC6-REVIEW-RESULTS.md)
3. Produce a coherent vision review + a detailed migration plan
4. Clearly differentiate core workbench vs. project template items

Usage (from workspace root):
    python plans/batch-doc6-review/submit_batch2.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to plans/batch-doc6-review/batch_id2.txt
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
BATCH_ID_FILE = pathlib.Path("plans/batch-doc6-review/batch_id2.txt")

# ---------------------------------------------------------------------------
# Load all source documents
# ---------------------------------------------------------------------------
def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}\n"
            "Run this script from the workspace root directory."
        )
    return p.read_text(encoding="utf-8")

print("Loading source documents...")
doc6 = load("workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md")
gemini_conv2 = load("workbench/_Agentic Workbench Architecture Explained .md")
previous_review = load("plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md")

print(f"  DOC6                  : {len(doc6):,} chars")
print(f"  Gemini conversation 2 : {len(gemini_conv2):,} chars")
print(f"  Previous review       : {len(previous_review):,} chars")

# ---------------------------------------------------------------------------
# Shared context block injected into every request
# ---------------------------------------------------------------------------
SHARED_CONTEXT = f"""
=== DOCUMENT A: DOC6-PRD-AGENTIC-AGILE-PROCESS.md ===
(First Gemini conversation — restructured by Gemini into a formal architecture document)

{doc6}

=== DOCUMENT B: _Agentic Workbench Architecture Explained .md ===
(Second Gemini conversation — deeper dive including Global Brain, Librarian Agent,
Cross-Project Memory, Calypso orchestration scripts, Hot/Cold memory, template taxonomy)

{gemini_conv2}

=== DOCUMENT C: DOC6-REVIEW-RESULTS.md ===
(Previous Claude Sonnet batch review of DOC6 — 3 expert perspectives:
coherence/clarity, architectural analysis, implementation feasibility)

{previous_review}

=== CURRENT WORKBENCH STATE (as of 2026-03-28) ===
The actual workbench repository currently contains:
- .clinerules (6 rules including mandatory Memory Bank read/write, Git versioning, chunking protocol)
- .roomodes (4 Agile personas: product-owner, scrum-master, developer, qa-engineer)
- Modelfile (uadf-agent, T=0.15, ctx=131072, base llama3.1:14b)
- proxy.py v2.8.0 (Gemini Chrome proxy server, SSE, FastAPI)
- memory-bank/ (7 files: activeContext, progress, projectBrief, productContext,
  systemPatterns, techContext, decisionLog)
- prompts/ (SP-001 to SP-007 system prompt registry)
- scripts/ (check-prompts-sync.ps1, start-proxy.ps1)
- template/ (project template folder with .clinerules, .roomodes, Modelfile,
  proxy.py, requirements.txt, prompts/, scripts/)
- src/ (hello.py, test_hello.py — placeholder application code)
- workbench/ (DOC1-DOC6 documentation, EXECUTION-TRACKER.md, RESUME-GUIDE.md)
- plans/ (batch-doc6-review/ with submit scripts and results)
- 3-mode LLM switcher: Ollama local (Calypso via Tailscale), Gemini proxy, Claude API
- Git repository on branch experiment/architecture-v2
- Pre-commit hook running check-prompts-sync.ps1
- Phase 10 (Anthropic Claude API) marked as completed in practice
"""

# ---------------------------------------------------------------------------
# Request 1: Vision Coherence & Synthesis Review
# ---------------------------------------------------------------------------
SYSTEM_COHERENCE = """You are a Senior Technical Architect and Documentation Strategist with 20 years of experience
designing AI-assisted development workflows, multi-agent systems, and developer tooling ecosystems.

Your task is to perform a rigorous VISION COHERENCE REVIEW across two Gemini conversations and one previous expert review.

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the overall coherence of the vision across both conversations.

## 2. Vision Evolution Analysis
Compare Document A (DOC6) with Document B (second conversation):
- What new concepts were introduced in the second conversation that were absent or implicit in DOC6?
- What concepts evolved, were refined, or contradicted between the two conversations?
- What is the final, authoritative vision that emerges from reading both together?

## 3. Consistency Audit
Identify all contradictions, naming conflicts, or semantic drift between the two conversations:
- Terminology inconsistencies (e.g., same concept named differently)
- Architectural contradictions (e.g., conflicting descriptions of the same phase)
- Scope creep or undefined boundaries between conversations

## 4. Integration with Previous Review
Cross-reference the previous expert review (Document C) with the second conversation (Document B):
- Which P0/P1 issues from the previous review are RESOLVED by the second conversation?
- Which P0/P1 issues remain UNRESOLVED even after the second conversation?
- What NEW issues does the second conversation introduce that were not in the previous review?

## 5. The Unified Vision Statement
Write a concise (300-500 word) unified vision statement that synthesizes both conversations into a single coherent description of the target Agentic Agile Workbench. This should resolve all contradictions and serve as the authoritative reference.

## 6. Prioritized Gaps
- **P0 (Critical):** Vision gaps that must be resolved before any implementation can begin.
- **P1 (Important):** Significant ambiguities that will cause implementation drift.
- **P2 (Nice to have):** Minor clarifications that would improve the vision.

## 7. Verdict
Choose exactly one: [Coherent unified vision] / [Needs reconciliation] / [Fundamentally contradictory]
Justify in 2-3 sentences."""

USER_COHERENCE = f"""Please perform a rigorous vision coherence review across the following documents.

{SHARED_CONTEXT}

Focus your analysis on:
1. How the second Gemini conversation (Document B) extends, refines, or contradicts the first (Document A)
2. Whether the previous expert review (Document C) has been addressed by the second conversation
3. What the final, unified, authoritative vision of the Agentic Agile Workbench should be
4. The clear boundary between what belongs to the CORE WORKBENCH vs. what belongs in APPLICATION PROJECT TEMPLATES"""

# ---------------------------------------------------------------------------
# Request 2: Core Workbench vs. Template Taxonomy
# ---------------------------------------------------------------------------
SYSTEM_TAXONOMY = """You are a Principal Platform Architect specializing in developer tooling, AI agent ecosystems,
and multi-project workspace design. You have deep expertise in separating concerns between
infrastructure/tooling layers and application project layers.

Your task is to produce a DEFINITIVE TAXONOMY that clearly separates every item discussed
across both Gemini conversations into two categories:
1. CORE WORKBENCH — items that belong to the workbench infrastructure itself
2. APPLICATION PROJECT TEMPLATE — items that are injected into every new application project

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the key architectural boundary decisions.

## 2. The Separation Principle
Define the exact rule/heuristic that determines whether an item belongs to the Core Workbench
or the Application Project Template. This must be a clear, testable criterion.

## 3. Core Workbench Items (Complete Inventory)
For EVERY item mentioned across both conversations, categorize it if it belongs to the Core Workbench.
Use this table format:

| Item | Category | Environment | Actor | Sync/Async | Type | Rationale |
|---|---|---|---|---|---|---|

Categories: Orchestration Script | AI Agent Prompt | Configuration | Documentation | Data Artifact | Infrastructure

## 4. Application Project Template Items (Complete Inventory)
For EVERY item mentioned across both conversations, categorize it if it belongs to the Project Template.
Use the same table format.

## 5. Items Requiring Clarification
List any items whose placement is ambiguous and explain why, with a recommended resolution.

## 6. The Current Workbench Gap Analysis
Compare the taxonomy above with the CURRENT WORKBENCH STATE described in the context.
For each item in the taxonomy:
- Mark [EXISTS] if it already exists in the current workbench
- Mark [PARTIAL] if a partial implementation exists
- Mark [MISSING] if it does not exist yet

## 7. Prioritized Improvements
- **P0 (Critical):** Items that MUST exist before the workbench can function as described.
- **P1 (Important):** Items that significantly improve the workbench's capability.
- **P2 (Nice to have):** Items that are aspirational or future-phase.

## 8. Verdict
Choose exactly one: [Taxonomy is clear and implementable] / [Boundary needs clarification] / [Fundamental redesign of separation required]
Justify in 2-3 sentences."""

USER_TAXONOMY = f"""Please produce a definitive taxonomy separating Core Workbench items from Application Project Template items,
based on all items discussed across both Gemini conversations.

{SHARED_CONTEXT}

Pay special attention to:
1. The explicit taxonomy table provided in Document B (Section: "Category 1: The Workbench Core" and "Category 2: The Project Template Folder")
2. The Summary Matrix in Document B
3. The current workbench state described above — what already exists vs. what is missing
4. The user's explicit requirement: "I'd like to keep at all time a full copy of the human readable memory alongside with the code, both of which are versioned with git"
5. The Hot/Cold memory architecture described at the end of Document B"""

# ---------------------------------------------------------------------------
# Request 3: Migration Plan (Current → Target Workbench)
# ---------------------------------------------------------------------------
SYSTEM_MIGRATION = """You are a Senior Engineering Lead and Technical Program Manager with expertise in
incremental system migrations, developer tooling evolution, and AI agent workflow design.

Your task is to produce a DETAILED, PEDAGOGICALLY JUSTIFIED MIGRATION PLAN that describes
exactly how to evolve the CURRENT workbench (described in the context) to the TARGET workbench
(described across both Gemini conversations).

The plan must be:
- Incremental (no big-bang rewrites)
- Pedagogically justified (explain WHY each step is taken in this order)
- Clearly differentiated between Core Workbench work and Application Template work
- Actionable (each step must be concrete and executable)

Your plan MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the migration strategy and key decisions.

## 2. Current State Assessment
Describe the current workbench state (from the context) in terms of:
- What is already implemented and working
- What is partially implemented
- What is completely missing relative to the target vision

## 3. Target State Description
Describe the target workbench in concrete terms:
- What will exist in the Core Workbench
- What will exist in the Application Project Template
- What will exist on Calypso (Tier 2)
- What will exist in the Cloud (Tier 3)

## 4. Migration Phases (The Roadmap)
Define concrete migration phases. For each phase:
- **Phase Name and Goal**
- **Pedagogical Justification:** Why this phase comes before the next one
- **Concrete Steps:** Numbered, actionable tasks
- **Deliverables:** What exists at the end of this phase
- **Validation Criteria:** How to verify the phase is complete
- **Estimated Effort:** Small / Medium / Large

## 5. Core Workbench Migration Steps
Detail specifically what needs to change in the core workbench (not the template):
- Files to create, modify, or delete
- Scripts to write
- Configurations to update
- Documentation to produce

## 6. Application Project Template Migration Steps
Detail specifically what needs to change in the template folder:
- Files to create, modify, or delete
- The Hot/Cold memory directory structure to implement
- The .clinerules updates needed
- The systemPatterns.md template to finalize

## 7. Calypso Integration Steps
Detail what needs to be built on the Tier 2 orchestrator (Calypso):
- Which scripts to deploy (orchestrator_phase2.py through orchestrator_phase4.py)
- The FastMCP server to build
- The Global Brain (Chroma/Mem0) to configure
- The Librarian Agent to deploy

## 8. Risk Register
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## 9. What NOT to do (Anti-patterns)
List the specific mistakes to avoid during this migration, based on the previous expert review findings.

## 10. Verdict
Choose exactly one: [Migration is straightforward] / [Migration requires careful sequencing] / [Migration requires architectural decisions before starting]
Justify in 2-3 sentences."""

USER_MIGRATION = f"""Please produce a detailed, pedagogically justified migration plan to evolve the current workbench
to the target vision described across both Gemini conversations.

{SHARED_CONTEXT}

Key constraints for the migration plan:
1. The user works on a Windows 11 laptop (Tier 1) with VS Code + Roo Code
2. Calypso is a headless Linux server with an RTX GPU accessible via Tailscale
3. The Anthropic Claude API is already configured and working
4. The Gemini proxy (proxy.py) is already working
5. The Ollama local model (uadf-agent on Calypso) is already working
6. The Memory Bank (.clinerules + 7 markdown files) is already working
7. The template/ folder already exists with basic files
8. The user explicitly wants: human-readable memory versioned in Git alongside code
9. The user explicitly wants: smart context management to avoid cost explosion
10. The migration must clearly separate what goes in the core workbench vs. the application template

Focus especially on:
- The gap between the current simple Memory Bank and the target Hot/Cold memory architecture
- The gap between the current template/ folder and the target Application Project Template
- The gap between the current workbench (no Calypso orchestration) and the target 3-tier architecture
- The pedagogical justification for the ORDER of migration steps"""

# ---------------------------------------------------------------------------
# Build the batch requests
# ---------------------------------------------------------------------------
REVIEWS = [
    {
        "custom_id": "vision-coherence-review",
        "system": SYSTEM_COHERENCE,
        "user_message": USER_COHERENCE,
    },
    {
        "custom_id": "taxonomy-core-vs-template",
        "system": SYSTEM_TAXONOMY,
        "user_message": USER_TAXONOMY,
    },
    {
        "custom_id": "migration-plan-current-to-target",
        "system": SYSTEM_MIGRATION,
        "user_message": USER_MIGRATION,
    },
]

requests = []
for review in REVIEWS:
    requests.append(
        anthropic.types.messages.batch_create_params.Request(
            custom_id=review["custom_id"],
            params=anthropic.types.messages.batch_create_params.MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=review["system"],
                messages=[
                    {"role": "user", "content": review["user_message"]}
                ],
            ),
        )
    )

# ---------------------------------------------------------------------------
# Submit the batch
# ---------------------------------------------------------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY environment variable is not set.\n"
        "Set it with: $env:ANTHROPIC_API_KEY = 'sk-ant-...'"
    )

client = anthropic.Anthropic(api_key=api_key)

print(f"\nSubmitting batch with {len(requests)} requests to model {MODEL}...")
print("  Request 1: vision-coherence-review")
print("  Request 2: taxonomy-core-vs-template")
print("  Request 3: migration-plan-current-to-target")

batch = client.messages.batches.create(requests=requests)

print(f"\n✅ Batch submitted successfully!")
print(f"   Batch ID  : {batch.id}")
print(f"   Status    : {batch.processing_status}")
print(f"   Created at: {batch.created_at}")
print(f"   Expires at: {batch.expires_at}")
print(f"\nSaving batch_id to {BATCH_ID_FILE}...")

BATCH_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
BATCH_ID_FILE.write_text(batch.id, encoding="utf-8")

print(f"✅ batch_id saved.")
print(f"\nRun the following command tomorrow morning to retrieve results:")
print(f"   python plans/batch-doc6-review/retrieve_batch2.py")
