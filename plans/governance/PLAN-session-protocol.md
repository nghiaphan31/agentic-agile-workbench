# PLAN: Session Protocol — Timestamps, IDs, Lifecycle & Continuity

**Document ID:** PLAN-session-protocol  
**Version:** 1.0  
**Status:** Draft — For Human Review  
**Date:** 2026-04-01  
**Author:** Architect mode  
**Branch:** develop  

---

## Context

You asked:
1. How does a session work/start/end?
2. Timestamps and sequential numbering for artifacts + plans
3. What if laptop closes unexpectedly?
4. How ensure continuity and coherence between sessions?

---

## 1. Session: The Universal Unit of Work

### 1.1 What Is a Session?

A **session** is a continuous period of interaction between a human and an AI agent. It has:
- **Start**: Human initiates conversation or agent resumes work
- **During**: Work happens (edits, commits, decisions)
- **End**: Human closes, agent completes, or timeout

### 1.2 Session ID Format

```
sYYYY-MM-DD-{mode}-{NNNN}

Examples:
s2026-04-01-architect-0001
s2026-04-01-architect-0002
s2026-04-01-code-0001
```

| Part | Meaning | Format |
|------|---------|--------|
| `s` | Prefix (session) | Fixed |
| `YYYY-MM-DD` | Date | ISO 8601 |
| `{mode}` | Agent mode | architect, code, ask, etc. |
| `{NNNN}` | Sequential number | 4-digit, zero-padded, resets daily |

**Rules:**
- Sequential number resets to 0001 each day
- Same session ID never reused
- Session ID included in ALL artifacts created during that session

### 1.3 Artifact ID Format

Every artifact gets a unique, sequential ID:

```
{type}-{NNNN}

Examples:
IDEA-016
IDEA-017
ADR-015
PLAN-ideation-to-release-coherence
PLAN-integrated-ideation-to-release
```

| Type | Prefix | Example |
|------|--------|---------|
| Ideas | IDEA- | IDEA-016 |
| Decisions | ADR- | ADR-015 |
| Plans | PLAN- | PLAN-session-protocol |
| Conversations | CONV- | CONV-2026-04-01-architect |
| Sessions | s | s2026-04-01-architect-0001 |
| Commits | (Git SHA) | abc1234 |

---

## 2. Session Lifecycle

### 2.1 Session States

```
┌─────────────────────────────────────────────────────────────────┐
│                        SESSION LIFECYCLE                         │
│                                                                  │
│    ┌─────────┐     ┌──────────┐     ┌─────────┐     ┌────────┐ │
│    │ CREATED │────►│ ACTIVE   │────►│ PAUSED  │────►│ CLOSED │ │
│    └─────────┘     └──────────┘     └─────────┘     └────────┘ │
│         │               │               │              │      │
│         │               │               │              │      │
│         ▼               ▼               ▼              ▼      │
│    Human starts    Work happening   Timeout or    Normal end   │
│    new session     (edits, commits) manual pause   or crash     │
└─────────────────────────────────────────────────────────────────┘
```

| State | Meaning | Trigger |
|-------|---------|---------|
| **CREATED** | Session ID assigned, context loaded | Human opens VS Code / new conversation |
| **ACTIVE** | Work is happening | First user message or agent action |
| **PAUSED** | Temporarily stopped | Timeout (30 min no activity), manual pause |
| **CLOSED** | Session ended | Normal end, crash, or close |

### 2.2 Session Transition Table

| From | To | Trigger | Action |
|------|-----|---------|--------|
| — | CREATED | Human opens workspace | Generate session ID, load activeContext.md |
| CREATED | ACTIVE | First action | Set start_time, mark ACTIVE |
| ACTIVE | PAUSED | 30 min timeout | Write checkpoint, mark PAUSED |
| ACTIVE | CLOSED | Normal end | Final checkpoint, update artifacts |
| PAUSED | ACTIVE | Human resumes | Load checkpoint, continue |
| PAUSED | CLOSED | Human explicitly closes | Final checkpoint |
| ACTIVE | CLOSED | Crash/close | Detect via stale heartbeat |

---

## 3. Session Start Protocol

### 3.1 START SEQUENCE (Every Time)

```
┌─────────────────────────────────────────────────────────────────┐
│                     SESSION START SEQUENCE                       │
│                                                                  │
│  STEP 1: CHECK FOR EXISTING SESSION                             │
│  ─────────────────────────────────────                           │
│  1. Read activeContext.md                                       │
│  2. Check: Is there an uncompleted session?                     │
│     • last_session_id exists?                                   │
│     • last_heartbeat < 30 minutes ago?                           │
│     • git status clean?                                          │
│                                                                  │
│  IF uncompleted session:                                         │
│     → Load checkpoint                                            │
│     → Resume session (same session_id)                          │
│     → Report: "Resuming session {session_id}"                   │
│                                                                  │
│  IF no uncompleted session:                                      │
│     → Generate new session_id                                     │
│     → Create new checkpoint                                       │
│     → Report: "Starting new session {session_id}"                │
│                                                                  │
│  STEP 2: LOAD ARTIFACTS                                         │
│  ────────────────────────                                         │
│  1. READ activeContext.md                                       │
│  2. READ IDEAS-BACKLOG.md                                        │
│  3. READ decisionLog.md                                          │
│  4. Git status + log (derive context)                            │
│                                                                  │
│  STEP 3: GENERATE CONTEXT SUMMARY                               │
│  ──────────────────────────────────                              │
│  1. Diff from last commit                                        │
│  2. Active branches                                             │
│  3. Stale ideas (REFINING > 7 days)                              │
│  4. Pending tech reviews (TECH > 3 days)                          │
│  5. Recent decisions (last 7 days)                               │
│                                                                  │
│  STEP 4: REPORT TO HUMAN                                         │
│  ──────────────────────────                                       │
│  "Session: s2026-04-01-architect-0001"                         │
│  "Last session: s2026-04-01-architect-0000 (2 hours ago)"       │
│  "Uncommitted changes: 3 files"                                  │
│  "Stale ideas: IDEA-015 (8 days in REFINING)"                   │
│  "Recent decisions: ADR-014 proposed"                            │
│  "Ready to continue."                                            │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Checkpoint File

At session start, agent creates/updates checkpoint:

```markdown
<!-- memory-bank/hot-context/session-checkpoint.md -->
---
session_id: s2026-04-01-architect-0001
status: ACTIVE
created_at: 2026-04-01T09:00:00Z
started_at: 2026-04-01T09:00:05Z
last_heartbeat: 2026-04-01T09:15:00Z

artifacts:
  current_task: "Review integrated governance plan"
  work_done: []
  blockers: []
  next_steps: []

git_state:
  branch: develop
  last_commit: abc1234
  last_commit_time: 2026-04-01T08:30:00Z
  uncommitted_files: []

derived_context:
  stale_ideas: []
  pending_reviews: []
  recent_decisions: []
---
```

**Rule**: Checkpoint is written BEFORE any work. It's the recovery source.

### 3.3 Heartbeat

During active work, heartbeat updates every 5 minutes:

```bash
# Pseudocode
def heartbeat():
    checkpoint.last_heartbeat = now()
    checkpoint.artifacts.current_task = get_current_task()
    checkpoint.git_state = get_git_status()
    write_checkpoint(checkpoint)
```

**Recovery**: If heartbeat is > 30 minutes old, session is considered PAUSED. Human must explicitly resume.

---

## 4. During Session: Work Tracking

### 4.1 Every Action Gets Timestamped

| Action | Timestamp | Artifact |
|--------|-----------|----------|
| Idea captured | `{timestamp}` | IDEAS-BACKLOG.md (with timestamp) |
| Decision made | `{timestamp}` | decisionLog.md |
| File edited | `{timestamp}` | Git commit |
| Commit made | `{timestamp}` + Git SHA | Git log |
| Artifact created | `{timestamp}` | Filename includes `{timestamp}` |

### 4.2 Artifact Timestamps

All artifacts include metadata header:

```markdown
---
doc_id: PLAN-session-protocol
version: 1.0
status: Draft
created: 2026-04-01T09:00:00Z
modified: 2026-04-01T11:30:00Z
session_id: s2026-04-01-architect-0001
author: Architect mode
---
```

### 4.3 Sequential Plan Numbers

Plans get sequential IDs regardless of type:

```markdown
# PLAN: Session Protocol

**Document ID:** PLAN-session-protocol
**Plan Number:** PLAN-0005
**Version:** 1.0
**Created:** 2026-04-01T09:00:00Z
**Session:** s2026-04-01-architect-0001
```

**Plan Registry** (in `docs/plans/README.md`):

```markdown
# Plans Registry

| Plan # | Document ID | Title | Created | Session | Status |
|--------|-------------|-------|---------|---------|--------|
| PLAN-0001 | PLAN-ideation-to-release-full-process | Ideation-to-Release Complete Process | 2026-03-30 | s2026-03-30-architect-0001 | DRAFT |
| PLAN-0002 | PLAN-git-commit-strategy | Git Commit Strategy | 2026-04-01 | s2026-04-01-architect-0001 | DRAFT |
| PLAN-0003 | PLAN-what-is-not-in-git | What Is NOT in Git | 2026-04-01 | s2026-04-01-architect-0001 | DRAFT |
| PLAN-0004 | PLAN-integrated-ideation-to-release | Integrated Ideation-to-Release | 2026-04-01 | s2026-04-01-architect-0001 | DRAFT |
| PLAN-0005 | PLAN-session-protocol | Session Protocol | 2026-04-01 | s2026-04-01-architect-0001 | DRAFT |
```

---

## 5. Session End Protocol

### 5.1 NORMAL END SEQUENCE

```
┌─────────────────────────────────────────────────────────────────┐
│                     SESSION END SEQUENCE                         │
│                                                                  │
│  STEP 1: FINAL HEARTBEAT                                        │
│  ────────────────────────                                         │
│  checkpoint.last_heartbeat = now()                               │
│  checkpoint.status = CLOSING                                     │
│                                                                  │
│  STEP 2: CHECK FOR UNCOMMITTED WORK                              │
│  ──────────────────────────────────                              │
│  git_status = git status                                        │
│  IF git_status.has_uncommitted:                                 │
│     REPORT: "Uncommitted changes detected:"                      │
│     FOR EACH file:                                               │
│         PRINT: "  - {file}"                                     │
│     ASK: "Commit before closing? [y/n]"                         │
│     IF yes:                                                     │
│         run commit_advisor.py                                    │
│         git commit                                               │
│                                                                  │
│  STEP 3: UPDATE ARTIFACTS                                       │
│  ───────────────────────                                         │
│  1. Update activeContext.md:                                     │
│     - session_id (completed)                                     │
│     - work_done[]                                                │
│     - blockers[]                                                 │
│     - next_steps[]                                               │
│     - last_session_timestamp                                     │
│                                                                  │
│  2. Update IDEAS-BACKLOG if any status changes                   │
│                                                                  │
│  3. Update decisionLog.md if any new ADRs                        │
│                                                                  │
│  4. If significant work:                                         │
│     - Save conversation to docs/conversations/                   │
│     - Update docs/conversations/README.md                         │
│                                                                  │
│  STEP 4: FINALIZE CHECKPOINT                                    │
│  ────────────────────────────                                    │
│  checkpoint.status = CLOSED                                       │
│  checkpoint.closed_at = now()                                     │
│  checkpoint.closed_reason = NORMAL                                │
│  checkpoint.next_session_id = s{NEXT_DATE}-{mode}-0001           │
│                                                                  │
│  STEP 5: REPORT                                                  │
│  ─────────────                                                   │
│  "Session s2026-04-01-architect-0001 closed."                   │
│  "Work done: N files, M commits"                                │
│  "Ideas captured: N"                                             │
│  "Decisions made: N"                                             │
│  "Next session: s2026-04-02-architect-0001"                     │
│                                                                  │
│  STEP 6: PUSH TO REMOTE (if applicable)                         │
│  ───────────────────────────────────────────                     │
│  git push (if remote changes)                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 CRASH RECOVERY (Laptop Closes Unexpectedly)

```
┌─────────────────────────────────────────────────────────────────┐
│                      CRASH RECOVERY                              │
│                                                                  │
│  DETECTION:                                                     │
│  ──────────                                                     │
│  At next session start:                                          │
│  1. Read checkpoint                                              │
│  2. Check: checkpoint.last_heartbeat > 30 minutes?                │
│  3. Check: checkpoint.status == ACTIVE?                          │
│  4. IF both true → CRASH DETECTED                               │
│                                                                  │
│  RECOVERY SEQUENCE:                                              │
│  ───────────────────                                             │
│  REPORT: "⚠️ Previous session ended unexpectedly."              │
│  REPORT: "Session: {session_id}"                               │
│  REPORT: "Last heartbeat: {last_heartbeat} ({time_ago})"        │
│  REPORT: "Checking for uncommitted work..."                     │
│                                                                  │
│  git_status = git status                                        │
│  IF git_status.has_uncommitted:                                 │
│     REPORT: "Uncommitted changes found:"                         │
│     FOR EACH file:                                               │
│         PRINT: "  - {file}"                                     │
│     ASK: "How would you like to proceed?"                       │
│     OPTIONS:                                                    │
│       [A] Commit with message: "wip: {session_id} crash recovery" │
│       [B] Stash changes and start fresh                          │
│       [C] Review changes before deciding                         │
│                                                                  │
│  IF no uncommitted changes:                                       │
│     REPORT: "No uncommitted changes. Context recovered."        │
│                                                                  │
│  UPDATE checkpoint:                                              │
│  checkpoint.status = RECOVERED                                  │
│  checkpoint.recovered_at = now()                                  │
│  checkpoint.recovery_session = {new_session_id}                 │
│                                                                  │
│  CONTINUE with normal session start.                              │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Crash vs Normal End: Comparison

| Aspect | Normal End | Crash Recovery |
|--------|------------|---------------|
| Detection | Human closes | Stale heartbeat |
| Uncommitted work | Offered to commit | Offered to recover |
| Checkpoint status | CLOSED | RECOVERED (detected) |
| Context loss | None | Minimal (last heartbeat) |
| User experience | Smooth | Alerted, then smooth |

---

## 6. Cross-Session Continuity

### 6.1 The Continuity Chain

```
Session 1 (s2026-04-01-architect-0001)
    │
    │ ends at 17:00
    │ uncommitted: 1 file
    │
    ▼
Laptop closes

    │
    │ Next day: 09:00
    │ Laptop opens
    │
    ▼
Session 2 (s2026-04-02-architect-0001)
    │
    │ detects crash/pause
    │ checkpoint.last_heartbeat = yesterday 17:00
    │
    ▼
RECOVERY:
    │
    │ "Uncommitted changes found: 1 file"
    │ Human chooses: [A] Commit
    │
    ▼
    commit: "wip: s2026-04-01-architect-0001 crash recovery"
    session_id: s2026-04-02-architect-0001
    refs: s2026-04-01-architect-0001
    │
    ▼
Continue with normal session
```

### 6.2 Information Preserved Across Sessions

| Information | Where | How Preserved |
|-------------|-------|---------------|
| Session history | Git | Commits with session_id |
| Active ideas | IDEAS-BACKLOG.md | Persistent file |
| Decisions | decisionLog.md | Persistent file |
| Current context | activeContext.md | Persistent file |
| Checkpoint | session-checkpoint.md | Written before crash |
| Uncommitted work | Git staging | Survives crash |

### 6.3 The "No Memory Loss" Guarantee

> **Even if laptop closes unexpectedly, nothing is lost if:**
> 1. Checkpoint was written before crash (>30 sec of work)
> 2. Commits were made for significant changes
> 3. Human reviews uncommitted work on next session

**Worst case**: Last ~5 minutes of work may need to be re-done (heartbeat interval).

---

## 7. Git as Continuity Mechanism

### 7.1 Why Git?

Git is the **ultimate persistence layer** because:
- It survives laptop closes
- It's versioned (can recover any version)
- It's pushed to remote (survives disk failure)
- It has timestamps for everything
- It's searchable

### 7.2 Git Log as Session History

Every commit links to a session:

```bash
# Query all commits from a specific session
git log --all --grep="s2026-04-01-architect-0001" --oneline

# Query all commits from a specific day
git log --since="2026-04-01 00:00:00" --until="2026-04-01 23:59:59" --oneline

# Query all commits related to an IDEA
git log --all --grep="IDEA-016" --oneline
```

### 7.3 Git as Backup

If ALL local files are lost:
1. Clone from remote
2. Git log shows all session history
3. activeContext.md is in Git
4. IDEAS-BACKLOG.md is in Git
5. decisionLog.md is in Git

---

## 8. Complete File Naming Convention

### 8.1 Session Files

```
memory-bank/hot-context/
├── activeContext.md              # Current session context
├── session-checkpoint.md         # Recovery checkpoint
├── progress.md                   # Long-term progress
├── decisionLog.md                # Architecture decisions
└── systemPatterns.md            # System patterns

docs/
├── conversations/
│   ├── README.md                # Index
│   ├── CONV-s2026-04-01-architect-0001.md
│   └── CONV-s2026-04-02-code-0001.md
├── plans/
│   ├── README.md                # Plan registry
│   ├── PLAN-0001-ideation-to-release-full-process.md
│   ├── PLAN-0002-git-commit-strategy.md
│   └── PLAN-0003-session-protocol.md
├── batch-outputs/
│   └── 2026-03-27-doc6-review/
│       └── final_backlog.json
└── ideas/
    ├── IDEAS-BACKLOG.md
    └── IDEA-016.md
```

### 8.2 Timestamp Format

All timestamps in ISO 8601 UTC:

```
2026-04-01T09:00:00Z
2026-04-01T17:30:00Z
```

For display, convert to local time:
```
2026-04-01 11:00 (Paris, UTC+2)
```

---

## 9. Rules Summary

### 9.1 Session Rules (Add to .clinerules)

```markdown
## RULE S-1: SESSION ID

Every session has unique ID: sYYYY-MM-DD-{mode}-{NNNN}
At session start: load checkpoint, check for uncompleted session.
Include session_id in ALL artifacts created.

## RULE S-2: CHECKPOINT BEFORE WORK

Before ANY work, write session-checkpoint.md.
Include: session_id, status, current_task, git_state, timestamp.
Update heartbeat every 5 minutes during active work.

## RULE S-3: SESSION END SEQUENCE

Before attempt_completion or laptop close:
1. Check for uncommitted work
2. Commit or stash
3. Update activeContext.md
4. Update IDEAS-BACKLOG if changed
5. Save conversation if significant
6. Finalize checkpoint (status=CLOSED)

## RULE S-4: CRASH RECOVERY

At session start, if checkpoint.last_heartbeat > 30 minutes:
→ Detect as crash/pause
→ Report uncommitted work
→ Offer recovery options
→ Continue with new session_id, note recovery

## RULE S-5: ARTIFACT METADATA

ALL artifacts include header:
---
doc_id: {unique-id}
created: {ISO-timestamp}
modified: {ISO-timestamp}
session_id: {session-id}
---

## RULE S-6: PLAN SEQUENTIAL NUMBERING

Plans get PLAN-NNNN sequential number.
Update docs/plans/README.md registry with:
Plan #, Document ID, Title, Created, Session, Status
```

---

## 10. Workflow Diagram: Full Session

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION START                                 │
│                                                                  │
│  1. Read checkpoint                                               │
│  2. Check: uncompleted session? → YES → RESUME (same ID)         │
│                    → NO  → NEW SESSION (new ID)                  │
│  3. Report: session_id, last commit, stale ideas                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION ACTIVE                                │
│                                                                  │
│  Every 5 minutes:                                                │
│  → Update heartbeat in checkpoint                                 │
│                                                                  │
│  Work happens:                                                   │
│  → New idea → intake → IDEAS-BACKLOG (timestamp + session_id)    │
│  → Decision → decisionLog.md (timestamp + session_id)            │
│  → File edit → checkpoint updated                                 │
│  → Complete unit → commit (session_id in footer)                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
         ┌──────────────────┐     ┌──────────────────┐
         │   NORMAL END     │     │   CRASH/PAUSE    │
         │                  │     │                  │
         │ 1. Commit work   │     │ (Laptop closes)  │
         │ 2. Update files  │     │                  │
         │ 3. Finalize      │     │ At next start:   │
         │    checkpoint    │     │ → Detect stale   │
         │ 4. Push          │     │ → Recovery UI    │
         └──────────────────┘     │ → Continue       │
                                  └──────────────────┘
```

---

## 11. Implementation Phases

### Phase 1: Add Session Protocol to .clinerules (1 session)

- Add RULE S-1 through S-6
- Create session-checkpoint.md template

### Phase 2: Update Active Context Template (1 session)

- Add session_id field
- Add checkpoint reference
- Add heartbeat tracking

### Phase 3: Create Plan Registry (1 session)

- Create docs/plans/README.md
- Assign sequential numbers to existing plans

### Phase 4: Test Session Protocol (1 session)

- Start session, do work, close unexpectedly
- Resume, verify recovery

---

## 12. Summary

### Session = sYYYY-MM-DD-{mode}-{NNNN}

### Every artifact has:
- Unique ID (IDEA-NNN, ADR-NNN, PLAN-NNNN)
- ISO timestamp (created, modified)
- session_id

### Session lifecycle:
- CREATED → ACTIVE → PAUSED/CLOSED
- Checkpoint written before work
- Heartbeat every 5 minutes

### Crash recovery:
- Detect via stale heartbeat (>30 min)
- Report uncommitted work
- Human chooses recovery path

### Continuity:
- Git = ultimate backup
- Commits link sessions
- All files in Git = survives disk failure

---

**Next step:** Human reviews and approves. If approved → implement RULE S-1 through S-6 in .clinerules.
