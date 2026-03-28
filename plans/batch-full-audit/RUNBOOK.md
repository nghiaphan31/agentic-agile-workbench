# RUNBOOK: Full Coherence Audit — Execution Guide

**Date:** 2026-03-28
**Batches:** 3 parallel batches (14 total requests)
**API:** Anthropic Batch API (50% cost reduction)
**Total Estimated Cost:** ~$0.21

---

## Overview

This runbook describes how to execute the full coherence audit in 3 steps:
1. **Submit** all 3 batches simultaneously (they run in parallel)
2. **Wait** 1-4 hours for batch processing
3. **Retrieve** results from all 3 batches

---

## Prerequisites

1. **Set ANTHROPIC_API_KEY:**
   ```powershell
   $env:ANTHROPIC_API_KEY = "sk-ant-..."
   ```

2. **Install anthropic package:**
   ```powershell
   pip install anthropic
   ```

3. **Verify you're in the workspace root:**
   ```powershell
   cd c:/Users/nghia/AGENTIC_DEVELOPMENT_PROJECTS/agentic-agile-workbench
   ```

---

## Step 1: Submit All 3 Batches

Run these 3 commands in sequence (they submit to the API but don't wait for results):

```powershell
# Submit BATCH 1: Governance Coherence (4 requests)
python plans/batch-full-audit/submit_batch1_governance.py

# Submit BATCH 2: Cross-Document Coherence (4 requests)
python plans/batch-full-audit/submit_batch2_crossdocs.py

# Submit BATCH 3: Template + Implementation Audit (6 requests)
python plans/batch-full-audit/submit_batch3_template.py
```

**Expected output for each:**
```
Submitting BATCH X: ... with N requests to model claude-sonnet-4-6...
[OK] Batch submitted successfully!
   Batch ID  : msgbatch_...
   Status    : in_progress
   Created at: 2026-03-28T...
   Expires at: 2026-04-...

Saving batch_id to plans/batch-full-audit/batch_id_X_...
[OK] batch_id saved.
```

**After this step, you should have:**
- `plans/batch-full-audit/batch_id_1_governance.txt`
- `plans/batch-full-audit/batch_id_2_crossdocs.txt`
- `plans/batch-full-audit/batch_id_3_template.txt`

---

## Step 2: Wait for Batch Processing

**Typical wait time:** 1-4 hours
**Maximum wait time:** 24 hours

Batches are processed asynchronously by Anthropic. You can:
- Check status manually with the retrieve scripts
- Wait and retrieve the next day

---

## Step 3: Retrieve Results

After 1-4 hours, run these 3 commands:

```powershell
# Retrieve BATCH 1 results
python plans/batch-full-audit/retrieve_batch1.py

# Retrieve BATCH 2 results
python plans/batch-full-audit/retrieve_batch2.py

# Retrieve BATCH 3 results
python plans/batch-full-audit/retrieve_batch3.py
```

**If batch is still processing:**
```
[WAIT] Batch status is 'in_progress'.
       Try again in 30 minutes.
```

**If batch is complete:**
```
[OK] Results written to: plans/batch-full-audit/RESULTS/BATCH1-GOVERNANCE-REPORT.md
     Total report size: X,XXX characters
```

---

## Output Files

After retrieval, you'll have:

```
plans/batch-full-audit/
├── RESULTS/
│   ├── BATCH1-GOVERNANCE-REPORT.md    # SP vs .clinerules, .roomodes, README
│   ├── BATCH2-CROSSDOCS-REPORT.md     # DOC-1..5 intra-release, version drift
│   └── BATCH3-TEMPLATE-REPORT.md      # Template sync, implementation vs docs
├── batch_id_1_governance.txt          # (from submit)
├── batch_id_2_crossdocs.txt           # (from submit)
└── batch_id_3_template.txt            # (from submit)
```

---

## Report Structure

Each report contains:

| Section | Description |
|---|---|
| Executive Summary | 3-5 bullet points |
| Findings | Detailed findings with file:line references |
| Inconsistencies Found | Severity + location + description |
| Prioritized Remediation | P0/P1/P2 classification |
| Verdict | CONSISTENT / MINOR_ISSUES / MAJOR_INCONSISTENCIES |

---

## Known Issues to Look For

Based on previous audits, these issues are expected:

| Batch | Issue | Severity |
|---|---|---|
| BATCH 1 | BOM in .clinerules root | P0 |
| BATCH 1 | Em-dash corruption (â€") in .clinerules | P0 |
| BATCH 1 | Literal \\n in RULE 10 GitFlow section | P1 |
| BATCH 1 | SP-002 double-embedded in prompts/SP-002 | P1 |
| BATCH 3 | Template vs root .clinerules drift | P1 |
| BATCH 3 | Template vs root .roomodes drift | P1 |

---

## Cost Summary

| Batch | Requests | Est. Tokens | Batch API Cost |
|---|---|---|---|
| BATCH 1 | 4 | ~15,000 in + ~16,000 out | ~$0.05 |
| BATCH 2 | 4 | ~25,000 in + ~16,000 out | ~$0.07 |
| BATCH 3 | 6 | ~30,000 in + ~24,000 out | ~$0.09 |
| **TOTAL** | **14** | **~70,000 in + ~56,000 out** | **~$0.21** |

At Batch API pricing (50% of standard Sonnet-4-6 pricing).

---

## Next Steps After Audit

1. **Read** all 3 reports in `plans/batch-full-audit/RESULTS/`
2. **Consolidate** findings into `docs/qa/v2.3/COHERENCE-AUDIT-v2.3.md`
3. **Triage** P0 findings using IDEA capture process (RULE 8.2)
4. **Fix** P0 issues in a dedicated feature branch
5. **Commit** fixes with Conventional Commits
6. **Update** `docs/releases/v2.3/` if needed

---

## Troubleshooting

**"batch_id file not found":**
- Run the submit script first
- Check that you're in the workspace root

**"ANTHROPIC_API_KEY environment variable is not set":**
- Set the environment variable before running:
  ```powershell
  $env:ANTHROPIC_API_KEY = "sk-ant-..."
  ```

**Batch status shows "in_progress" after 4+ hours:**
- Batches can take up to 24 hours
- Check Anthropic status page if available
- Batches expire after 29 days if not retrieved

**"File not found" when loading documents:**
- Verify you're in the workspace root
- Check that `docs/releases/v2.2/` files exist
- Run from: `c:/Users/nghia/AGENTIC_DEVELOPMENT_PROJECTS/agentic-agile-workbench`
