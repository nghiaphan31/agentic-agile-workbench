"""
submit_batch.py
---------------
Submits a 3-request Anthropic Message Batch to review DOC6-PRD-AGENTIC-AGILE-PROCESS.md.

Usage (from workspace root):
    python plans/batch-doc6-review/submit_batch.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to plans/batch-doc6-review/batch_id.txt
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
DOC6_PATH = pathlib.Path("workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md")
BATCH_ID_FILE = pathlib.Path("plans/batch-doc6-review/batch_id.txt")

# ---------------------------------------------------------------------------
# Load the document
# ---------------------------------------------------------------------------
if not DOC6_PATH.exists():
    raise FileNotFoundError(
        f"DOC6 not found at {DOC6_PATH}. "
        "Run this script from the workspace root directory."
    )

doc6_content = DOC6_PATH.read_text(encoding="utf-8")
print(f"Loaded DOC6: {len(doc6_content)} characters, {doc6_content.count(chr(10))} lines.")

# ---------------------------------------------------------------------------
# Expert review definitions
# ---------------------------------------------------------------------------
REVIEWS = [
    {
        "custom_id": "review-coherence",
        "system": (
            "You are a Senior Technical Writer and Documentation Architect with 15 years of experience "
            "reviewing technical specifications, PRDs, and architecture documents. "
            "Your task is to perform a rigorous coherence and clarity review of the provided document.\n\n"
            "Your review MUST be structured EXACTLY as follows (use these exact Markdown headings):\n\n"
            "## 1. Executive Summary\n"
            "3 to 5 bullet points summarizing your overall assessment.\n\n"
            "## 2. Document Structure Analysis\n"
            "Evaluate the logical flow, section ordering, and navigability. "
            "Identify any structural inconsistencies or missing sections.\n\n"
            "## 3. Internal Consistency Check\n"
            "Identify contradictions, ambiguities, or undefined terms between sections. "
            "Flag any concepts introduced without prior definition.\n\n"
            "## 4. Clarity and Precision\n"
            "Identify vague, ambiguous, or overly abstract statements. "
            "Flag any section that a new reader would find confusing.\n\n"
            "## 5. Completeness Assessment\n"
            "What is missing? What gaps exist between the stated goals and the documented content?\n\n"
            "## 6. Prioritized Improvements\n"
            "- **P0 (Critical):** Must fix before this document can be used as a reference.\n"
            "- **P1 (Important):** Should fix to improve usability.\n"
            "- **P2 (Nice to have):** Minor polish.\n\n"
            "## 7. Verdict\n"
            "Choose exactly one: [Ready as reference] / [Needs revision] / [Major rework required]\n"
            "Justify your verdict in 2-3 sentences."
        ),
        "user_message": (
            "Please perform a rigorous coherence and clarity review of the following document.\n\n"
            "---BEGIN DOCUMENT---\n"
            f"{doc6_content}\n"
            "---END DOCUMENT---"
        ),
    },
    {
        "custom_id": "review-architecture",
        "system": (
            "You are a Principal Software Architect with deep expertise in distributed systems, "
            "AI/LLM orchestration pipelines, multi-agent systems, and enterprise software design. "
            "Your task is to perform a rigorous architectural review of the provided document.\n\n"
            "Your review MUST be structured EXACTLY as follows (use these exact Markdown headings):\n\n"
            "## 1. Executive Summary\n"
            "3 to 5 bullet points summarizing your overall architectural assessment.\n\n"
            "## 2. Architectural Soundness\n"
            "Evaluate each phase/component for architectural correctness. "
            "Identify single points of failure, tight coupling, or anti-patterns.\n\n"
            "## 3. Scalability and Resilience\n"
            "How does this architecture behave under load or partial failure? "
            "What are the bottlenecks?\n\n"
            "## 4. Data Flow and State Management\n"
            "Evaluate the artifact handoff between phases. "
            "Are the JSON contracts sufficient? Are there missing fields or type ambiguities?\n\n"
            "## 5. Security Architecture\n"
            "Evaluate the security posture of the described system. "
            "Are API keys, secrets, and sensitive data handled correctly?\n\n"
            "## 6. Missing Architectural Concerns\n"
            "What critical architectural decisions are not addressed? "
            "Examples: error recovery, idempotency, observability, versioning, rollback.\n\n"
            "## 7. Prioritized Improvements\n"
            "- **P0 (Critical):** Architectural flaws that would cause system failure.\n"
            "- **P1 (Important):** Significant gaps that reduce reliability or maintainability.\n"
            "- **P2 (Nice to have):** Enhancements for production-grade robustness.\n\n"
            "## 8. Verdict\n"
            "Choose exactly one: [Architecturally sound] / [Needs architectural revision] / [Fundamental redesign required]\n"
            "Justify your verdict in 2-3 sentences."
        ),
        "user_message": (
            "Please perform a rigorous architectural review of the following document.\n\n"
            "---BEGIN DOCUMENT---\n"
            f"{doc6_content}\n"
            "---END DOCUMENT---"
        ),
    },
    {
        "custom_id": "review-implementation",
        "system": (
            "You are a Senior Platform Engineer and DevOps Architect with expertise in LLM tooling, "
            "MCP (Model Context Protocol) ecosystems, local/cloud hybrid deployments, and AI developer workflows. "
            "Your task is to perform a rigorous implementation feasibility review of the provided document.\n\n"
            "Your review MUST be structured EXACTLY as follows (use these exact Markdown headings):\n\n"
            "## 1. Executive Summary\n"
            "3 to 5 bullet points summarizing your overall feasibility assessment.\n\n"
            "## 2. Tooling and Technology Choices\n"
            "Evaluate each tool, framework, or technology mentioned. "
            "Are the choices current, appropriate, and well-justified? "
            "Flag any deprecated, experimental, or poorly-supported tools.\n\n"
            "## 3. MCP Ecosystem Assessment\n"
            "Evaluate the MCP server recommendations in Part 4. "
            "Are these servers production-ready? Are there better alternatives? "
            "What is missing from the MCP configuration?\n\n"
            "## 4. 3-Tier Architecture Feasibility\n"
            "Evaluate the Local Workstation / Calypso / Cloud split. "
            "Is the hardware assumption (RTX 5060 Ti 16GB) realistic for the described workload? "
            "What are the network latency and reliability risks?\n\n"
            "## 5. Batch API Usage\n"
            "Evaluate the proposed use of the Anthropic Batch API in Phases 2 and 3. "
            "Are the temperature/top-p settings appropriate? "
            "What are the cost and latency implications?\n\n"
            "## 6. Brownfield Workflow Feasibility\n"
            "Is the Reverse Engineering workflow (Part 2) practically implementable? "
            "What are the main risks when applying this to real legacy codebases?\n\n"
            "## 7. Prioritized Improvements\n"
            "- **P0 (Critical):** Implementation blockers that would prevent the system from working.\n"
            "- **P1 (Important):** Significant gaps in the implementation plan.\n"
            "- **P2 (Nice to have):** Optimizations and enhancements.\n\n"
            "## 8. Verdict\n"
            "Choose exactly one: [Implementable as described] / [Needs implementation revision] / [Not feasible without major changes]\n"
            "Justify your verdict in 2-3 sentences."
        ),
        "user_message": (
            "Please perform a rigorous implementation feasibility review of the following document.\n\n"
            "---BEGIN DOCUMENT---\n"
            f"{doc6_content}\n"
            "---END DOCUMENT---"
        ),
    },
]

# ---------------------------------------------------------------------------
# Build the batch requests
# ---------------------------------------------------------------------------
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
print(f"   python plans/batch-doc6-review/retrieve_batch.py")
