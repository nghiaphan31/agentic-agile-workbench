---
doc_id: DOC-2
release: v2.1
status: Frozen
title: Architecture
version: 1.0
date_created: 2026-03-28
date_frozen: 2026-03-28
authors: [Code mode, Human]
previous_release: docs/releases/v2.0/DOC-2-v2.0-Architecture.md
---

# DOC-2 -- Architecture (v2.1)

> **Status: FROZEN** -- This document is read-only. Do not modify.

---

## Delta from v2.0

v2.1 introduces **no architectural changes**. The architecture described in [DOC-2 v2.0](docs/releases/v2.0/DOC-2-v2.0-Architecture.md) applies in full.

---

## Additions in v2.1

### RULE 10 -- GitFlow Enforcement

See [DOC-2 v2.0 § ADR-005](docs/releases/v2.0/DOC-2-v2.0-Architecture.md#adr-005-gitflow-enforcement) for the full ADR.

Branch lifecycle summary:

| Branch | Purpose | Lifecycle |
|--------|---------|----------|
| `master` | Production state — frozen after each release tag | Never commit directly after tag |
| `release/vX.Y` | Release branch — all planned work for vX.Y | Closed after merge to master |
| `release/vX.Y+1` | Next release branch | Active — all new work lands here |
| `hotfix/vX.Y.Z` | Emergency fixes from production tag | Merged to master + active release |
| `feature/{slug}` | Single feature | Branch from `release/vX.Y+1` |

---

### LLM Backend Resilience (IDEA-008)

The 3-tier architecture from [DOC-2 v2.0](docs/releases/v2.0/DOC-2-v2.0-Architecture.md) is unchanged. The Tier-1 LLM routing now includes:

```
Default:  minimax/minimax-m2.7  (via OpenRouter)
Fallback: claude-sonnet-4-6     (after 3 consecutive errors)
```

All other architecture specifications remain as documented in v2.0.

---

*End of DOC-2 v2.1*
