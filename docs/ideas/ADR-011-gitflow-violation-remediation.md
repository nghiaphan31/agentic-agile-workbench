---
id: ADR-011
title: GITFLOW Violation — ADR-006 Remediation (2026-03-30)
status: ACCEPTED
date: 2026-03-30
type: governance
tags: [git, governance, adr-006]
---

# ADR-011: GITFLOW Violation Remediation

## Status
**ACCEPTED** — 2026-03-30

## Context

On 2026-03-30, a critical violation of ADR-006 (GITFLOW branch lifecycle) was identified:

- **Violation:** 10 commits (76430e6 → 7f0809c) were made directly on `master` after v2.3.0 release
- **These commits contained:** IDEA-012A, 012B, 012C (Ideation-to-Release pipeline implementation)
- **Rule violated:** ADR-006 RULE 10.2 — "NEVER commit directly on main after a release tag"

### Timeline
- `39d0896` — v2.3.0 release merge (CORRECT)  
- `afb5f03` → `7f0809c` — 10 commits directly on master (VIOLATION)
- `develop` — stale, missing all IDEA-012 work

## Decision

**Option A: Cherry-pick** was chosen over:
- Option B (merge) — would bake violation lineage into develop
- Option C (reset) — too destructive, loses real work

### Remediation Steps Executed
1. All 10 violating commits were cherry-picked from master to develop
2. Each created a NEW commit on develop with same content, different hash
3. Master was left unchanged (violation remains visible in history)
4. develop now contains proper implementation of IDEA-012A/B/C

## Consequences

### Negative (Violation Impact)
- Historical record of ADR-006 breach on master branch
- Duplicate commits (same content, different hashes) across branches
- Violation visible in git history until resolved

### Positive (Remediation)
- Code properly resides on develop (correct branch)
- Violation documented as learning opportunity
- develop contains complete governance pipeline
- Future releases can proceed correctly via develop-vX.Y → master

## Prevention

Per RULE 10.3, ALL new development must use feature branches:
- `feature/{IDEA-NNN}-{slug}` from `develop` or `develop-vX.Y`
- NO direct commits on `develop` or `master`

Agents must check `git branch` before committing and verify target branch.

## See Also
- ADR-006: GITFLOW branch lifecycle
- IDEA-012: Ideation-to-Release Process
- docs/releases/v2.3/EXECUTION-TRACKER-v2.3.md