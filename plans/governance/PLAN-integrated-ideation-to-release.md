# PLAN: Integrated Ideation-to-Release — Complete Governance

**Document ID:** PLAN-integrated-ideation-to-release  
**Version:** 1.0  
**Status:** Draft — For Human Review  
**Date:** 2026-04-01  
**Author:** Architect mode  
**Branch:** develop  

---

## Executive Summary

This document integrates four analyses into a **coherent, minimal governance system** that ensures:

1. **No idea loss** — every human input is captured, processed, never forgotten
2. **Multi-session continuity** — agents know context across days/weeks
3. **Agent proactivity** — agents remind human about stale ideas, pending reviews, sync opportunities
4. **Full traceability** — every change linked to IDEA/ADR, session, and commit

### The Four Documents This Integrates

| Source Document | What It Addresses |
|----------------|-------------------|
| `PLAN-ideation-to-release-coherence-analysis.md` | Found 4 overlaps, 6 gaps, 6 inconsistencies in tracking |
| `PLAN-tracking-artifacts-rationalized.md` | Simplified to 3 core artifacts + Git as authoritative history |
| `PLAN-what-is-not-in-git.md` | Identified precious artifacts (batch outputs, conversations) NOT in Git |
| `PLAN-git-commit-strategy.md` | Commit templates, triggers, local model intelligence |

---

## Part I: The Problem

### Current State: Artifact Overload

| Artifact | Problem |
|----------|---------|
| progress.md | Redundant with Git (checkbox = git log) |
| EXECUTION-TRACKER | Redundant with Git (session log = git log) |
| TECH-SUGGESTIONS-BACKLOG | Separate backlog = duplicated tracking |
| activeContext.md | Manually updated = drifts from Git state |
| DOC-3 | Manually maintained = diverges from reality |
| decisionLog.md | ✅ KEEP — ADR format is correct |
| IDEAS-BACKLOG.md | ✅ KEEP — need to track uncommitted ideas |

**Root cause**: We tracked "what's done" in 4 places, none authoritative.

### Current State: Precious Things Not Versioned

| Not in Git | Risk |
|------------|------|
| `batch_artifacts/` (expert reports, final_backlog.json) | HIGH — $50 of API calls, irreplaceable |
| Most conversations | CRITICAL — institutional memory loss |
| activeContext updates | Only updated when remembered |

### Current State: Commit Quality Issues

| Anti-Pattern | Problem |
|--------------|---------|
| Micro-commits | Noise in git log |
| Mega-commits | Unsearchable history |
| Orphan commits | No IDEA linkage |
| Vague messages | Can't reconstruct intent |

---

## Part II: The Solution — Unified Architecture

### Core Principle: Git as Authoritative History

> **Git is the source of truth for WHAT changed, WHEN, and WHO. Everything else derives from it or tracks what Git cannot (uncommitted ideas, human intent).**

### The 3-Artifact Scheme

| Artifact | Purpose | Single Source? |
|----------|---------|----------------|
| **IDEAS-BACKLOG.md** | WHAT WE WANT (unified backlog) | ✅ |
| **activeContext.md** | WHERE WE ARE (session context) | ✅ |
| **decisionLog.md** | WHY WE DECIDED (ADR format) | ✅ |

### The "Precious Things" Rule

Anything that **COST MONEY** or **COST TIME** must be versioned:

```
COST $     → batch_artifacts/ outputs → docs/batch-outputs/
COST TIME  → agent conversations → docs/conversations/
```

### Git Commit as the Universal Link

Every commit links:
- `Refs: IDEA-NNN` — what feature
- `Session: YYYY-MM-DD-mode-NNN` — what session
- `ADR-NNN` if applicable — what decision

---

## Part III: Detailed Design

### 1. IDEAS-BACKLOG.md — Single Source of Truth for WHAT

```markdown
# Ideas Backlog

**Last triage:** 2026-03-30
**Next triage:** At v2.6 release planning

---

## Status Legend

| Status | Meaning |
|--------|---------|
| `[IDEA]` | Captured, not yet evaluated |
| `[REFINING]` | Requirements being formalized |
| `[REFINED]` | Ready for triage |
| `[ACCEPTED]` | Approved for development |
| `[DEVELOPING]` | Branch created, implementation in progress |
| `[DONE]` | Implemented, merged, released |
| `[DEFERRED]` | Parked for later |
| `[REJECTED]` | Will not implement |

---

## Type Legend

| Type | Meaning |
|------|---------|
| `biz` | Business requirement (WHAT) |
| `tech` | Technical suggestion (HOW) |
| `governance` | Process/workflow improvement |
| `fix` | Bug fix |

---

## Backlog

| ID | Title | Type | Status | Captured | Triage | Release | Branch | Disposition |
|----|-------|------|--------|----------|--------|---------|--------|-------------|
| IDEA-001 | Hot/Cold memory | biz | [DONE] | 2026-03-28 | 2026-03-28 | v2.0 | — | Implemented |
| IDEA-015 | PDF export | biz | [REFINING] | 2026-04-01 | — | v2.6 | — | Awaiting refinement |
| TECH-001 | Redis caching | tech | [IDEA] | 2026-04-01 | — | — | — | New suggestion |

---

## Parked Ideas

| ID | Title | Status | Deferred Since | Reason |
|----|-------|--------|---------------|--------|
| IDEA-004 | Gherkin linter | [DEFERRED] | v2.0 | Too complex |
```

**Key features:**
- Single backlog for business + technical ideas (add `type` column)
- All status transitions logged with session_id
- Links to conversations in `docs/conversations/`

---

### 2. activeContext.md — Session Context (Derived + Fresh)

```markdown
---
# Active Context

**Last updated:** 2026-04-01T09:00:00Z
**Session ID:** 2026-04-01-architect-001
**Active mode:** architect
**LLM Backend:** minmax/minimax-m2.7

---

## Git State (Derived)
- Branch: `develop`
- Last commit: `abc1234` (2026-04-01)
- Tag (latest): `v2.5.0` (2026-03-31 on master)

---

## Session Summary

- **Current task:** Review integrated governance plan
- **Work done:**
  - Synthesized 4 analysis documents into unified plan
  - Designed 3-artifact + Git scheme
- **Blockers:** None
- **Next steps:**
  - [ ] Human review and approval
  - [ ] Implement changes

---

## Proactive Reminders (MANDATORY at Session Start)

### Stale Ideas
- IDEA-015 (PDF export): [REFINING] since 2026-04-01 (>0 days)

### Pending Technical Reviews
- TECH-001 (Redis caching): [IDEA] for 1 day

### Sync Opportunities
- TECH-001 may overlap with future batch caching idea

### Context Freshness
- Last commit: 2 hours ago — **FRESH**
```

**Key features:**
- **Derived from Git**: branch, last commit, tags
- **Session ID**: links to commit history
- **Proactive reminders**: MANDATORY section at session start

---

### 3. decisionLog.md — Why We Decided (ADR Format)

```markdown
# Decision Log — Architecture Decision Records (ADR)

---

## ADR-014: Simplify Tracking to 3 Artifacts + Git (PROPOSED)

**Date:** 2026-04-01  
**Status:** PROPOSED  
**Session:** 2026-04-01-architect-001

**Context:**
Over 6 months, tracking artifacts grew organically to 7+ files with overlaps, gaps, and inconsistencies.

**Decision:**
1. **IDEAS-BACKLOG.md** — unified backlog (biz + tech)
2. **activeContext.md** — session context (derived from Git)
3. **decisionLog.md** — ADR format (keep as-is)
4. **Git** — authoritative history (commits, tags, branches)

Drop:
- progress.md (derived from Git)
- EXECUTION-TRACKER (derived from Git)
- TECH-SUGGESTIONS-BACKLOG (merged into IDEAS-BACKLOG)

Version precious artifacts:
- `docs/batch-outputs/` — batch API outputs
- `docs/conversations/` — session conversations

**Consequences:**
- Single source of truth per concept
- Git = authoritative history
- ~67% fewer manual updates

---
```

---

### 4. docs/batch-outputs/ — Version Precious Artifacts

```
docs/batch-outputs/
├── 2026-03-27-doc6-review/
│   ├── expert_reports/
│   │   ├── architecture_expert.json
│   │   ├── security_expert.json
│   │   ├── ux_expert.json
│   │   └── qa_expert.json
│   ├── draft_backlog.json
│   └── final_backlog.json
└── 2026-03-30-ideation-review/
    └── ...
```

**Rule**: After each batch pipeline run, copy outputs to `docs/batch-outputs/{timestamp}/`

---

### 5. docs/conversations/ — Version Session Conversations

```
docs/conversations/
├── README.md                    ← Index of all conversations
├── 2026-03-27-gemini-doc6-architecture.md
├── 2026-03-28-gemini-workbench-explained.md
└── REF*INEMENT-template.md
```

**Rule**: At session end, if significant work done, save conversation + add to README.md index.

---

## Part IV: Git Commit Strategy

### Commit Message Template

```
<type>(<scope>): <subject>

<body>

• Changed: <files/features>
• Related: <linked IDEA/ADR>

Refs: IDEA-NNN | Session: YYYY-MM-DD-mode-NNN
```

**Example:**
```
feat(governance): implement 3-artifact scheme

• Created: IDEAS-BACKLOG.md (unified backlog)
• Created: activeContext.md template (Git-derived)
• Updated: decisionLog.md with ADR-014
• Dropped: progress.md, EXECUTION-TRACKER

Refs: ADR-014
Session: 2026-04-01-architect-001
```

### Type Vocabulary

| Type | When |
|------|------|
| `feat` | New feature (IDEAS-BACKLOG item) |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructure |
| `test` | Tests |
| `chore` | Tooling, config |
| `governance` | Process/workflow |
| `session` | Session metadata |

### Scope Vocabulary

| Scope | Meaning |
|-------|---------|
| `memory` | memory-bank/ |
| `prompts` | prompts/ |
| `docs` | docs/ |
| `src` | src/ |
| `calypso` | src/calypso/ |
| `batch` | scripts/batch/ |
| `governance` | Process files |

### Commit Granularity: The Sweet Spot

```
Too Atomic              Sweet Spot              Too Coarse
─────────────────────────────────────────────────────────────────
"fix typo"             "feat(intake): core"    "v2.6 release"
"remove space"          "feat(intake): scoring" "major changes"
     │                        │                       │
     ▼                        ▼                       ▼
  Noise                  Complete unit           Unsearchable
  Hard to bisect        Revert independently     Can't understand
```

**Rule**: Commit AFTER each complete, testable, logically isolated unit of work.

### Use Local Models for Commit Intelligence

Calypso (Linux + RTX 5060 Ti) runs `qwen3:8b` for:

| Script | Purpose |
|--------|---------|
| `commit_advisor.py` | Analyze staged diff → structured message |
| `commit_readiness.py` | Check granularity (too atomic? too coarse?) |
| `git_query.py` | Natural language git history search |

---

## Part V: Session Protocol

### Session Start (Every Session)

```
1. READ activeContext.md (last session state)
2. READ IDEAS-BACKLOG (current backlog state)
3. READ decisionLog.md (recent decisions)
4. Git status + log (what happened since last)
5. Derive current context from Git
6. UPDATE activeContext.md (fresh timestamp)
7. REPORT to human:
   - "Session: {session_id}"
   - "Last commit: {hash} ({time ago})"
   - "Stale ideas: N" (REFINING > 7 days)
   - "Pending reviews: N" (TECH IDEA > 3 days)
```

### During Session

```
- New idea → intake_agent.py → IDEAS-BACKLOG
- Decision → decisionLog.md
- Blocker → activeContext.md blockers[]
- Commit → git with session_id + IDEA linkage
```

### Session End (Before attempt_completion)

```
1. CHECK for uncommitted changes
2. COMMIT any complete units (with local model advice)
3. UPDATE activeContext.md
   - session_id
   - work_done[]
   - blockers[]
   - next_steps[]
4. VERIFY clean git state OR document what remains
5. SAVE conversation if significant
```

---

## Part VI: Proactivity Mechanisms

### Session Start: Mandatory Reminders

At EVERY session start, agent MUST check and report:

| Check | Threshold | Action |
|-------|-----------|--------|
| Stale ideas | [REFINING] > 7 days | "IDEA-015 has been refining for 8 days" |
| Pending tech reviews | [TECH IDEA] > 3 days | "TECH-001 needs architecture evaluation" |
| Sync opportunities | On new idea intake | "IDEA-016 may overlap with IDEA-012" |
| Context staleness | activeContext > 24h old | "Context is stale, refreshing..." |

### Intake: Proactive Linking

When a new idea is captured:

1. **Acknowledge** — "I've captured IDEA-016: PDF export"
2. **Scan for overlaps** — check IDEAS-BACKLOG
3. **Link related** — "This overlaps with TECH-001 (Redis caching)"
4. **Suggest coordination** — "Would you like to refine them together?"

### Branch Creation: Proactive Warning

When creating `feature/IDEA-NNN`:

1. **Check parallel work** — which branches touch same files?
2. **Inform human** — "feature/IDEA-015 also modifies src/batch/"
3. **Suggest order** — "IDEA-015 is 80% done, consider merging first"

---

## Part VII: Rules Summary

### New Rules for .clinerules

```markdown
## RULE C-1: THREE ARTIFACTS

Keep only:
1. IDEAS-BACKLOG.md — unified backlog (biz + tech)
2. activeContext.md — session context
3. decisionLog.md — ADR format

Drop: progress.md, EXECUTION-TRACKER, TECH-SUGGESTIONS-BACKLOG

## RULE C-2: GIT AS AUTHORITATIVE HISTORY

Git tracks: WHAT changed, WHEN, WHO, WHY (via commit messages)
Everything else derives from Git or tracks what Git cannot (uncommitted ideas).

## RULE C-3: SESSION ID PROPAGATION

Every session has unique ID: YYYY-MM-DD-{mode}-{NNN}
At session start: write to activeContext.md
At session end: update with work_done, blockers, next_steps
In commit: include Session: field

## RULE C-4: PROACTIVE REMINDERS (MANDATORY)

At session start, check and report:
- Stale ideas ([REFINING] > 7 days)
- Pending technical reviews ([TECH IDEA] > 3 days)
- Sync opportunities
- Context staleness

## RULE G-1: COMMIT MESSAGE TEMPLATE

Every commit follows:
<type>(<scope>): <subject>

<body>

Refs: IDEA-NNN | Session: YYYY-MM-DD-mode-NNN

## RULE G-2: COMMIT GRANULARITY

Commit AFTER each complete, testable, logically isolated unit.
Don't commit if build broken, mid-feature, or trivial.

## RULE G-3: USE LOCAL MODEL FOR COMMITS

Before committing, use Calypso:
python scripts/commit_advisor.py      # Generate message
python scripts/commit_readiness.py   # Check granularity

## RULE P-1: PRECIOUS THINGS RULE

Version anything that cost MONEY or TIME:
- batch_artifacts/ outputs → docs/batch-outputs/
- Significant conversations → docs/conversations/

## RULE P-2: CONVERSATION CAPTURE

At session end:
- If significant work: save to docs/conversations/
- Add entry to docs/conversations/README.md
- Link from related IDEA/ADR
```

---

## Part VIII: Implementation Phases

### Phase 1: Consolidate (1 session)

- [ ] Merge TECH-SUGGESTIONS into IDEAS-BACKLOG (add type column)
- [ ] Archive TECH-SUGGESTIONS-BACKLOG
- [ ] Retire EXECUTION-TRACKER (derive from Git)
- [ ] Retire progress.md (derive from Git)

### Phase 2: Version Precious Things (1 session)

- [ ] Create `docs/batch-outputs/` directory
- [ ] Copy existing batch artifacts to docs/batch-outputs/
- [ ] Create `docs/conversations/README.md` index
- [ ] Update .gitignore: allow docs/batch-outputs/

### Phase 3: Implement Commit Strategy (1 session)

- [ ] Add RULE G-1, G-2, G-3 to .clinerules
- [ ] Create `scripts/commit_advisor.py`
- [ ] Create `scripts/commit_readiness.py`
- [ ] Create `scripts/git_query.py`

### Phase 4: Enhance activeContext (1 session)

- [ ] Update activeContext template with proactivity section
- [ ] Document "Derived from Git" section
- [ ] Add session_id field

### Phase 5: Test & Iterate (ongoing)

- [ ] Use new process for 1 week
- [ ] Identify friction points
- [ ] Adjust rules as needed

---

## Part IX: Comparison

### Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| Tracking artifacts | 7+ files | 3 files |
| Manual updates | ~740 lines/session | ~250 lines/session |
| Batch outputs | Gitignored (lost) | Versioned |
| Conversations | Lost | Versioned |
| Commit messages | Vague | Structured + local model |
| Proactivity | None | Mandatory reminders |
| Git as history | Partial | Authoritative |

---

## Part X: Infrastructure Context

```
┌─────────────────────────────────────────────────────────────────┐
│              HUMAN (Windows PC) + VS Code + Roo                  │
│                    Main interface / orchestration                │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│              CALYPSO (Linux Headless)                           │
│              GPU: RTX 5060 Ti 16GB                               │
│                                                                  │
│              Local models (Ollama):                               │
│              • qwen3:8b — commit intelligence, git query        │
│              • llava — vision tasks                              │
│                                                                  │
│              For: fast, cheap, local inference                   │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│              OPENROUTER (Cloud)                                 │
│              GPT-4, Claude, MinMax                               │
│                                                                  │
│              For: complex reasoning, batch API                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part XI: Open Questions

1. **progress.md retention**: Keep as human-readable derived summary, or drop entirely?
2. **DOC-3 generation**: Fully auto-generate from Git, or human-editable with sync?
3. **Enforcement**: Git hook to block non-conforming commits, or only warn?
4. **Conversation granularity**: Save all sessions, or only significant ones?

---

## Part XII: Files Summary

### Files to CREATE

| File | Purpose |
|------|---------|
| `docs/batch-outputs/` | Version precious batch artifacts |
| `docs/conversations/README.md` | Conversation index |
| `scripts/commit_advisor.py` | Local model commit message generation |
| `scripts/commit_readiness.py` | Local model granularity check |
| `scripts/git_query.py` | Natural language git search |

### Files to MODIFY

| File | Change |
|------|--------|
| `.clinerules` | Add RULE C-1 through C-4, G-1 through G-3, P-1, P-2 |
| `IDEAS-BACKLOG.md` | Add type column, merge TECH-SUGGESTIONS |
| `activeContext.md` | Add proactivity section, session_id, Git-derived fields |
| `decisionLog.md` | Add ADR-014 |
| `.gitignore` | Allow docs/batch-outputs/ |

### Files to ARCHIVE (Keep for Reference)

| File | Action |
|------|--------|
| `progress.md` | Archive (derive from Git going forward) |
| `EXECUTION-TRACKER-v*.md` | Archive (Git log is source) |
| `TECH-SUGGESTIONS-BACKLOG.md` | Archive (merged into IDEAS-BACKLOG) |

---

**Next step:** Human reviews and approves. If approved → Phase 1 implementation.
