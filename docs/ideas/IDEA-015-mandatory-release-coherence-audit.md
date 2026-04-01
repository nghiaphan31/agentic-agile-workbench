---
id: IDEA-015
title: Mandatory Coherence Audit Before Release
status: [IDEA]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: docs/qa/, .github/workflows/
captured: 2026-04-01
captured_by: Developer mode
refined_by: 
refinement_session: 
---

## Description

Run a systematic, deep and rigorous coherence audit **before every release** (not after). The v2.6 release had 14 P0, 17 P1, and 14 P2 findings — this should have been caught before tagging the release.

## Motivation

The coherence audit is currently a reactive process (done after issues are found). Given the workbench's complexity (multiple docs, prompts, scripts, rules), we need:
1. A mandatory coherence audit gate in the release workflow
2. Zero P0 findings required before a release can be tagged
3. P1 findings must be triaged and either fixed or formally deferred via ENH

## Classification

Type: GOVERNANCE

## Complexity Score

**Score: 4/10** — SYNCHRONOUS refinement recommended

## Affected Documents

- `.github/workflows/` — Add release gate workflow
- DOC-4 (Operations Guide) — Document release procedure
- RULE 13-14 (Ideation-to-Release) — May need enhancement

## Next Steps

1. Design the release gate (what checks must pass?)
2. Add GitHub Actions workflow for automated coherence checks
3. Update release procedure in DOC-4

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human remark |

---
