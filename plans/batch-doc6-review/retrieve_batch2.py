"""
retrieve_batch2.py
------------------
Retrieves the results of the second-pass Agentic Workbench vision analysis batch.

Usage (from workspace root):
    python plans/batch-doc6-review/retrieve_batch2.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic
    - submit_batch2.py must have been run first (batch_id2.txt must exist)

Output:
    - If batch is complete: writes DOC6-REVIEW-RESULTS2.md with all 3 expert analyses
    - If batch is still processing: prints status and instructs to retry later
"""

import os
import pathlib
import datetime
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BATCH_ID_FILE = pathlib.Path("plans/batch-doc6-review/batch_id2.txt")
RESULTS_FILE = pathlib.Path("plans/batch-doc6-review/DOC6-REVIEW-RESULTS2.md")

REVIEW_LABELS = {
    "vision-coherence-review": {
        "title": "Analysis 1: Vision Coherence & Synthesis Review",
        "persona": "Senior Technical Architect & Documentation Strategist",
        "emoji": "🔭",
    },
    "taxonomy-core-vs-template": {
        "title": "Analysis 2: Core Workbench vs. Application Template Taxonomy",
        "persona": "Principal Platform Architect",
        "emoji": "🗂️",
    },
    "migration-plan-current-to-target": {
        "title": "Analysis 3: Migration Plan — Current Workbench → Target Vision",
        "persona": "Senior Engineering Lead & Technical Program Manager",
        "emoji": "🗺️",
    },
}

# ---------------------------------------------------------------------------
# Load the batch ID
# ---------------------------------------------------------------------------
if not BATCH_ID_FILE.exists():
    raise FileNotFoundError(
        f"batch_id2.txt not found at {BATCH_ID_FILE}.\n"
        "Run submit_batch2.py first to create a batch."
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
        text_content = ""
        for block in message.content:
            if hasattr(block, "text"):
                text_content += block.text
        results[custom_id] = {
            "text": text_content,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        }
        print(f"  ✅ {custom_id}: {message.usage.input_tokens:,} in / {message.usage.output_tokens:,} out tokens")
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
    "# Agentic Workbench Vision Analysis — Second-Pass Results",
    "",
    "**Source documents:**",
    "- [`workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md`](../../workbench/DOC6-PRD-AGENTIC-AGILE-PROCESS.md) — First Gemini conversation",
    "- [`workbench/_Agentic Workbench Architecture Explained .md`](../../workbench/_Agentic%20Workbench%20Architecture%20Explained%20.md) — Second Gemini conversation",
    "- [`plans/batch-doc6-review/DOC6-REVIEW-RESULTS.md`](DOC6-REVIEW-RESULTS.md) — Previous expert review",
    "",
    f"**Batch ID:** `{batch_id}`",
    f"**Retrieved at:** {now}",
    f"**Model:** `claude-sonnet-4-6`",
    f"**Total tokens:** {total_input:,} input / {total_output:,} output",
    "",
    "---",
    "",
    "## Table of Contents",
    "",
    "1. [Vision Coherence & Synthesis Review](#analysis-1-vision-coherence--synthesis-review)",
    "2. [Core Workbench vs. Application Template Taxonomy](#analysis-2-core-workbench-vs-application-template-taxonomy)",
    "3. [Migration Plan — Current → Target](#analysis-3-migration-plan--current-workbench--target-vision)",
    "",
    "---",
    "",
]

# Add each analysis in fixed order
for custom_id in ["vision-coherence-review", "taxonomy-core-vs-template", "migration-plan-current-to-target"]:
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
