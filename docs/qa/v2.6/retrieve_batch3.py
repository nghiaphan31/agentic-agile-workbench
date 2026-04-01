"""
retrieve_batch3.py
------------------
Retrieves results from BATCH 3: Prompt vs Deployment Coherence

Usage (from workspace root):
    python docs/qa/v2.6/retrieve_batch3.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - Batch must have been submitted via submit_batch3_prompt.py
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BATCH_DIR = pathlib.Path("docs/qa/v2.6/BATCHES")
RESULTS_DIR = BATCH_DIR / "RESULTS"
BATCH_ID_FILE = BATCH_DIR / "batch_id_3_prompt.txt"
REPORT_FILE = RESULTS_DIR / "BATCH3-PROMPT-REPORT.md"

# Custom ID to title mapping
CUSTOM_IDS = {
    "prompt-productowner": "SP-003 (product-owner) vs .roomodes product-owner",
    "prompt-scrummaster": "SP-004 (scrum-master) vs .roomodes scrum-master",
    "prompt-developer": "SP-005 (developer) vs .roomodes developer",
    "prompt-qaengineer": "SP-006 (qa-engineer) vs .roomodes qa-engineer",
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not BATCH_ID_FILE.exists():
        print(f"[ERROR] batch_id file not found: {BATCH_ID_FILE}")
        print("Run submit_batch3_prompt.py first.")
        return
    
    batch_id = BATCH_ID_FILE.read_text(encoding="utf-8").strip()
    print(f"Retrieving batch: {batch_id}")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    client = anthropic.Anthropic(api_key=api_key)
    
    batch = client.messages.batches.retrieve(batch_id)
    print(f"Batch status: {batch.status}")
    
    if batch.status.value == "in_progress":
        print("[WAIT] Batch is still processing. Try again in 30 minutes.")
        return
    
    if batch.status.value != "ended":
        print(f"[ERROR] Unexpected batch status: {batch.status.value}")
        return
    
    print("Retrieving results...")
    results = client.messages.batches.list_results(batch_id)
    
    report = "# BATCH 3: Prompt vs Deployment Coherence Report\n\n"
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
        
        text_content = ""
        for content in result.result.content:
            if content.type == "text":
                text_content += content.text
        
        report += f"## {title}\n\n"
        report += text_content
        report += "\n\n---\n\n"
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"[OK] Report written to: {REPORT_FILE}")
    print(f"     Total size: {len(report):,} characters")

if __name__ == "__main__":
    main()
