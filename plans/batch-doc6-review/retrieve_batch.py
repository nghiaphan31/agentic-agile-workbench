"""
retrieve_batch.py
-----------------
Retrieves the results of the DOC6 review batch from the Anthropic Batch API.

Usage (from workspace root):
    python plans/batch-doc6-review/retrieve_batch.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic
    - submit_batch.py must have been run first (batch_id.txt must exist)

Output:
    - If batch is complete: writes DOC6-REVIEW-RESULTS.md with all 3 expert reviews
    - If batch is still processing: prints status and instructs to retry later
"""

import os
import pathlib
import datetime
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BATCH_ID_FILE = pathlib.Path("plans/batch-doc6-review/batch_id.txt")
RESULTS_FILE = pathlib.Path("plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md")

REVIEW_LABELS = {
    "review-coherence": {
        "title": "Review 1: Coherence & Clarity",
        "persona": "Senior Technical Writer & Documentation Architect",
        "emoji": "📝",
    },
    "review-architecture": {
        "title": "Review 2: Architectural Analysis",
        "persona": "Principal Software Architect",
        "emoji": "🏗️",
    },
    "review-implementation": {
        "title": "Review 3: Implementation Feasibility",
        "persona": "Senior Platform Engineer & DevOps Architect",
        "emoji": "⚙️",
    },
}

# ---------------------------------------------------------------------------
# Load the batch ID
# ---------------------------------------------------------------------------
if not BATCH_ID_FILE.exists():
    raise FileNotFoundError(
        f"batch_id.txt not found at {BATCH_ID_FILE}.\n"
        "Run submit_batch.py first to create a batch."
    )

batch_id = BATCH_ID_FILE.read_text(encoding="utf-8").strip()
print(f"Loaded batch ID: {batch_id}")

# ---------------------------------------------------------------------------
# Connect to Anthropic
# ---------------------------------------------------------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY environment variable is not set.\n"
        "Set it with: $env:ANTHROPIC_API_KEY = 'sk-ant-...'"
    )

client = anthropic.Anthropic(api_key=api_key)

# ---------------------------------------------------------------------------
# Check batch status
# ---------------------------------------------------------------------------
print(f"Checking batch status...")
batch = client.messages.batches.retrieve(batch_id)

print(f"\nBatch status: {batch.processing_status}")
print(f"  Request counts: {batch.request_counts}")
print(f"  Created at   : {batch.created_at}")
print(f"  Expires at   : {batch.expires_at}")

if batch.processing_status != "ended":
    print(f"\n⏳ Batch is still '{batch.processing_status}'. Try again later.")
    print(f"   Succeeded : {batch.request_counts.succeeded}")
    print(f"   Processing: {batch.request_counts.processing}")
    print(f"   Errored   : {batch.request_counts.errored}")
    print(f"   Canceled  : {batch.request_counts.canceled}")
    print(f"   Expired   : {batch.request_counts.expired}")
    exit(0)

# ---------------------------------------------------------------------------
# Retrieve and parse results
# ---------------------------------------------------------------------------
print(f"\n✅ Batch complete! Retrieving results...")

results = {}
errors = {}

for result in client.messages.batches.results(batch_id):
    custom_id = result.custom_id
    if result.result.type == "succeeded":
        message = result.result.message
        # Extract text content from the response
        text_content = ""
        for block in message.content:
            if hasattr(block, "text"):
                text_content += block.text
        results[custom_id] = {
            "text": text_content,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        }
        print(f"  ✅ {custom_id}: {message.usage.input_tokens} in / {message.usage.output_tokens} out tokens")
    elif result.result.type == "errored":
        error = result.result.error
        errors[custom_id] = f"Error type: {error.type}"
        print(f"  ❌ {custom_id}: {error.type}")
    else:
        errors[custom_id] = f"Unexpected result type: {result.result.type}"
        print(f"  ⚠️  {custom_id}: unexpected result type {result.result.type}")

# ---------------------------------------------------------------------------
# Build the results Markdown file
# ---------------------------------------------------------------------------
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
total_input = sum(r["input_tokens"] for r in results.values())
total_output = sum(r["output_tokens"] for r in results.values())

lines = [
    "# DOC6 Expert Review Results",
    "",
    f"**Document reviewed:** [`workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md`](../../workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md)",
    f"**Batch ID:** `{batch_id}`",
    f"**Retrieved at:** {now}",
    f"**Model:** `claude-sonnet-4-6`",
    f"**Total tokens:** {total_input:,} input / {total_output:,} output",
    "",
    "---",
    "",
    "## Table of Contents",
    "",
    "1. [Review 1: Coherence & Clarity](#review-1-coherence--clarity)",
    "2. [Review 2: Architectural Analysis](#review-2-architectural-analysis)",
    "3. [Review 3: Implementation Feasibility](#review-3-implementation-feasibility)",
    "",
    "---",
    "",
]

# Add each review in a fixed order
for custom_id in ["review-coherence", "review-architecture", "review-implementation"]:
    label = REVIEW_LABELS[custom_id]
    lines.append(f"## {label['emoji']} {label['title']}")
    lines.append(f"**Expert persona:** {label['persona']}")
    lines.append("")

    if custom_id in results:
        tokens = results[custom_id]
        lines.append(
            f"*Tokens: {tokens['input_tokens']:,} input / {tokens['output_tokens']:,} output*"
        )
        lines.append("")
        lines.append(results[custom_id]["text"])
    elif custom_id in errors:
        lines.append(f"⚠️ **Error:** {errors[custom_id]}")
    else:
        lines.append("⚠️ **No result returned for this request.**")

    lines.append("")
    lines.append("---")
    lines.append("")

# Write the file
RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
RESULTS_FILE.write_text("\n".join(lines), encoding="utf-8")

print(f"\n✅ Results written to: {RESULTS_FILE}")
print(f"   Total: {len(results)} succeeded, {len(errors)} errored")
print(f"   Total tokens: {total_input:,} input / {total_output:,} output")

if errors:
    print(f"\n⚠️  Some requests errored. Check {RESULTS_FILE} for details.")
