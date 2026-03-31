# ADR-012: Canonical Docs Cumulative + GitFlow Enforcement

**Date:** 2026-03-31  
**Status:** Accepted  
**Type:** Governance Architecture  

---

## Context

The canonical docs (DOC-1 through DOC-5) in `docs/releases/vX.Y/` were historically **delta-based** — they referenced previous releases and contained only changes since the last release. This made individual release documents:
- Incomplete when read in isolation
- Dependent on previous releases for full context
- Unable to stand alone as comprehensive project documentation

Additionally, there was **no automated enforcement** of:
- GitFlow discipline for canonical doc modifications
- Cumulative nature (minimum line counts)
- Consistency across all 5 DOC pointers

## Decision

We adopt a **fully cumulative** documentation model with **automated GitFlow enforcement**:

### 1. Cumulative Documentation (R-CANON-0)

Each canonical doc in `docs/releases/vX.Y/` is **fully self-contained and cumulative** — it contains the complete state of that document for the entire project history up to vX.Y.

**Minimum line thresholds:**
| Doc | Minimum Lines |
|-----|--------------|
| DOC-1 (PRD) | 500 |
| DOC-2 (Architecture) | 500 |
| DOC-3 (Implementation Plan) | 300 |
| DOC-4 (Operations Guide) | 300 |
| DOC-5 (Release Notes) | 200 |

### 2. GitFlow Rules (R-CANON-1 through R-CANON-4)

- **R-CANON-1**: Canonical docs on `develop`: Only via feature branch (`feature/canon-doc-*`)
- **R-CANON-2**: Canonical docs on `develop-vX.Y`: Only via feature branch scoped to that release
- **R-CANON-3**: Direct commits on `develop` or `develop-vX.Y` to canonical docs are **FORBIDDEN**
- **R-CANON-4**: Exception: Governance-only commits (ADRs, RULE additions) MAY be committed directly

### 3. Consistency Rules (R-CANON-5 through R-CANON-7)

- **R-CANON-5**: All 5 canonical docs MUST be updated together for any release
- **R-CANON-6**: When merging to `develop-vX.Y`, all 5 DOC-*-vX.Y-*.md files must exist and be consistent
- **R-CANON-7**: The `DOC-*-CURRENT.md` pointer files MUST all point to the same release version

### 4. Automated Enforcement

Two enforcement mechanisms are deployed:

1. **Git pre-receive hook** at `.githooks/pre-receive`:
   - Checks cumulative line counts
   - Validates feature branch workflow
   
2. **GitHub Actions CI** at `.github/workflows/canonical-docs-check.yml`:
   - Checks DOC pointer consistency
   - Validates cumulative nature
   - Checks frozen docs not modified

Both are deployed to new projects via `deploy-workbench-to-project.ps1`.

## Consequences

### Positive
- Each release doc is self-contained and readable in isolation
- No need to trace through multiple delta files to understand project history
- Automated enforcement prevents GitFlow violations
- Consistent pointer state across all DOC files

### Negative
- Larger individual doc files (but manageable with chunking)
- More complex doc generation (must concatenate previous releases)
- Retroactive rewrite required for existing delta-based docs

### Neutral
- Existing frozen docs remain unchanged (they're already "frozen")
- New enforcement only applies going forward

## Implementation

### Phase 1: Retroactive Fix (COMPLETED)
- Rewrote all v2.3 canonical docs as cumulative
- Rewrote all v2.4 canonical docs as cumulative
- Updated all DOC-*-CURRENT.md pointers to v2.4

### Phase 2: Git Pre-Receive Hook
- Created `.githooks/pre-receive` with cumulative checks

### Phase 3: GitHub Actions CI
- Created `.github/workflows/canonical-docs-check.yml`

### Phase 4: Template Integration
- Added `.githooks/` and `.github/` to `deploy-workbench-to-project.ps1`
- Hooks and CI now deploy with the template

### Phase 5: Rules Update
- Added R-CANON rules to `.clinerules` (RULE 12)
- Added SYNC AWARENESS rules (RULE 11)

## References

- PLAN-canonical-docs-gitflow-enforcement.md
- RULE 12: CANONICAL DOCS — CUMULATIVE + GITHUB ACTIONS ENFORCEMENT
- RULE 11: SYNCHRONIZATION AWARENESS — MANDATORY FOR ALL AGENTS
