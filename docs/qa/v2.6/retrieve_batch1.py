"""
retrieve_batch1.py
-----------------
Retrieves results from BATCH 1: Code vs Documentation

Usage (from workspace root):
    python docs/qa/v2.6/retrieve_batch1.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - Batch must have been submitted via submit_batch1_code.py
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BATCH_DIR = pathlib.Path("docs/qa/v2.6/BATCHES")
RESULTS_DIR = BATCH_DIR / "RESULTS"
BATCH_ID_FILE = BATCH_DIR / "batch_id_1_code.txt"
REPORT_FILE = RESULTS_DIR / "BATCH1-CODE-REPORT.md"

# Custom ID to title mapping
CUSTOM_IDS = {
    "code-calypso": "Calypso Phase 2-4 Scripts vs DOC-2 Architecture",
    "code-sync": "SyncDetector + RefinementWorkflow vs DOC-3",
    "code-heartbeat": "Session Heartbeat vs MB-4 Rule",
    "code-memory": "Memory Bank vs DOC-1 PRD",
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # Load batch ID
    if not BATCH_ID_FILE.exists():
        print(f"[ERROR] batch_id file not found: {BATCH_ID_FILE}")
        print("Run submit_batch1_code.py first.")
        return
    
    batch_id = BATCH_ID_FILE.read_text(encoding="utf-8").strip()
    print(f"Retrieving batch: {batch_id}")
    
    # Initialize client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    client = anthropic.Anthropic(api_key=api_key)
    
    # Get batch status
    batch = client.messages.batches.retrieve(batch_id)
    print(f"Batch status: {batch.status}")
    
    if batch.status.value == "in_progress":
        print("[WAIT] Batch is still processing. Try again in 30 minutes.")
        return
    
    if batch.status.value != "ended":
        print(f"[ERROR] Unexpected batch status: {batch.status.value}")
        return
    
    # Retrieve results
    print("Retrieving results...")
    results = client.messages.batches.list_results(batch_id)
    
    # Build report
    report = "# BATCH 1: Code vs Documentation Coherence Report\n\n"
    report += f"**Batch ID:** {batch_id}\n"
    report += f"**Processed at:** {batch.processed_at}\n\n"
    report += "---\n\n"
    
    for result in sorted(results, key=lambda r: r.custom_id):
        custom_id = result.custom_id
        title = CUSTOM_IDS.get(custom_id, custom_id)
        
        if result.result.type == "error":
            report += f"## {title}\n\n"
            report += f"**ERROR:** {result.result.error}\n\n"
            continue
        
        # Extract text response
        text_content = ""
        for content in result.result.content:
            if content.type == "text":
                text_content += content.text
        
        report += f"## {title}\n\n"
        report += text_content
        report += "\n\n---\n\n"
    
    # Save report
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"[OK] Report written to: {REPORT_FILE}")
    print(f"     Total size: {len(report):,} characters")

if __name__ == "__main__":
    main()
