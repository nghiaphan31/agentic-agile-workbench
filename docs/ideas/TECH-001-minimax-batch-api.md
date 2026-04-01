---
id: TECH-001
title: Investigate MinMax M2.7 Batch API Support
status: [IDEA]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: OpenRouter API docs, MinMax documentation
captured: 2026-04-01
captured_by: Developer mode
refined_by: 
refinement_session: 
---

## Description

Investigate and test the possibility of making batch requests to MinMax M2.7 via OpenRouter to lower costs versus using the Anthropic Batch API.

## Motivation

The Anthropic Batch API costs ~$1.20 for 11 requests (coherence audit). MinMax M2.7 via OpenRouter may support batch processing at a lower cost. If successful, we could:
1. Use MinMax batch for routine audits
2. Reserve Anthropic for high-priority or complex audits
3. Reduce overall operational costs

## Classification

Type: TECHNICAL

## Technical Investigation Required

1. Check OpenRouter API documentation for MinMax batch support
2. Test batch endpoint with MinMax M2.7
3. Compare latency, cost, and quality vs Anthropic batch
4. Determine if batch_artifacts schema needs modification

## Complexity Score

**Score: 6/10** — SYNCHRONOUS investigation recommended

## Affected Components

- `scripts/batch/` — May need OpenRouter/MinMax adapter
- `prompts/README.md` — Update if MinMax batch is viable

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human suggestion |

---
