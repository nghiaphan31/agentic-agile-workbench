# PLAN: Roo Code Session Model — Revised Understanding

**Document ID:** PLAN-roo-code-session-model  
**Version:** 1.0  
**Status:** Draft — For Human Review  
**Date:** 2026-04-01  
**Author:** Architect mode  
**Branch:** develop  

---

## Executive Summary

Based on research into the actual Roo Code implementation, this document revises the session protocol to match how Roo Code actually works:

1. **Session = VS Code window lifetime** (implicit, human-controlled)
2. **Task = a unit of work** (user message → agent → `<attempt_completion>`)
3. **No explicit session management** — it's implicit via VS Code open/close
4. **Crash recovery gap** — memory files NOT updated if laptop closes unexpectedly

---

## 1. How Roo Code Sessions Actually Work

### 1.1 The Session/Task Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    VS CODE WINDOW (Open)                        │
│                                                                  │
│  SESSION = The entire period while VS Code is open              │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   TASK 1   │  │   TASK 2   │  │   TASK 3   │             │
│  │             │  │             │  │             │             │
│  │ Human: "do X"│  │ Human: "fix Y"│  │ Human: "add Z"│             │
│  │ Agent: ...   │  │ Agent: ...   │  │ Agent: ...   │             │
│  │ <attempt_    │  │ <attempt_    │  │ <attempt_    │             │
│  │  completion> │  │  completion> │  │  completion> │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  MEMORY FILES: Updated after each <attempt_completion>         │
│  CHAT HISTORY: Accumulates throughout session                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
              VS Code Closes → Session Ends
```

### 1.2 Session Start (Automatic)

When VS Code opens (or new Roo Code conversation starts):

```
1. Roo Code injects .clinerules above user prompt
2. Agent executes RULE 1: CHECK→CREATE→READ sequence
3. Agent READS: activeContext.md, progress.md (from memory-bank/)
4. Agent ACTS on user's first message
```

**Source**: `.clinerules` RULE 1:
> "Before any action, you MUST execute: CHECK → CREATE → READ → ACT"

### 1.3 Task Execution

Each user message starts a task:

```
Human types: "Review PLAN-ideation-to-release and suggest improvements"
     │
     ▼
Agent receives: .clinerules (injected) + user message
     │
     ▼
Agent works: reads files, makes changes, etc.
     │
     ▼
Agent signals completion: <attempt_completion>
     │
     ▼
Roo Code shows: "Task completed" UI
```

### 1.4 Session End (Implicit)

Session ends when:
- Human closes VS Code
- Human closes the workspace
- Timeout (if configured)
- Explicit new conversation (clears chat history)

**There is NO explicit "end session" command.**

### 1.5 Memory Update (RULE 2)

After each `<attempt_completion>`:

```
Agent MUST update:
1. activeContext.md (new state, next action)
2. progress.md (check off completed items)
3. decisionLog.md (if ADR made during task)
4. Git commit (before attempt_completion)
```

---

## 2. The Crash Recovery Gap

### 2.1 The Problem

```
SCENARIO: Agent working on TASK 2, laptop closes unexpectedly

BEFORE CRASH:
- activeContext.md: shows TASK 1 state
- progress.md: TASK 1 checked off
- TASK 2 work: NOT YET in memory files
- Git: TASK 2 changes maybe in staging, maybe not

AFTER CRASH (next session):
- Agent reads activeContext.md → sees TASK 1 state
- TASK 2 work: LOST (not in memory files)
- Git staging: MAY have TASK 2 files (if human staged)
- No way to know what was actually completed
```

### 2.2 Why This Happens

RULE 2 says update memory files **before `attempt_completion`**.

But:
1. If laptop closes **before** `attempt_completion`, rule is not executed
2. No checkpoint is written during task execution
3. Chat history may be lost (depends on Roo Code settings)
4. Only git staging (if human committed) survives

### 2.3 The Session Files Problem

From research (REVIEW3):
> "Context loss at truncation boundary remains a fundamental constraint"
> "The current task (last user message) is always preserved"
> "But early context (Memory Bank reads) is lost"

This means:
- Even within a session, long tasks can lose context
- Between sessions, only memory files + git survive

---

## 3. Revised Design: Checkpoint-Based Recovery

### 3.1 New Session Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION (VS Code Open)                        │
│                                                                  │
│  TASK 1 ──► <attempt_completion> ──► Memory updated           │
│       │                                                          │
│       │ CHECKPOINT WRITTEN                                      │
│       │ (to session-checkpoint.md)                               │
│       │                                                          │
│  TASK 2 ──► <attempt_completion> ──► Memory updated           │
│       │                                                          │
│       │ CHECKPOINT WRITTEN                                      │
│                                                                  │
│  TASK 3 ──► [LAPTOP CLOSES]                                    │
│       │                                                          │
│       │ NO CHECKPOINT (crash point)                             │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              NEXT SESSION (VS Code Reopens)                     │
│                                                                  │
│  1. Read session-checkpoint.md                                  │
│  2. Compare: last checkpoint vs git state                      │
│  3. Detect: "TASK 3 was in progress, no checkpoint"           │
│  4. Report: "Recovering from crash. TASK 3 was interrupted."  │
│  5. Offer: Review git staging, resume TASK 3                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Checkpoint File

```markdown
<!-- memory-bank/hot-context/session-checkpoint.md -->
---
session_id: s2026-04-01-architect-0001
vscode_window_id: [uuid]  # If available
status: ACTIVE | PAUSED | CLOSED

task_history:
  - task_id: 1
    started_at: 2026-04-01T09:00:00Z
    completed_at: 2026-04-01T09:30:00Z
    outcome: COMPLETED
    memory_updated: true
    
  - task_id: 2
    started_at: 2026-04-01T09:30:05Z
    completed_at: 2026-04-01T10:00:00Z
    outcome: COMPLETED
    memory_updated: true
    
  - task_id: 3
    started_at: 2026-04-01T10:00:10Z
    checkpoint_at: 2026-04-01T10:05:00Z
    status: INTERRUPTED  # No attempt_completion
    git_staged: [list of files]
    last_heartbeat: 2026-04-01T10:05:00Z

last_memory_update: 2026-04-01T10:00:00Z  # From TASK 2

git_state:
  branch: develop
  last_commit: abc1234
  staged_files: [list from checkpoint]
---
```

### 3.3 Crash Detection

```python
def detect_crash():
    checkpoint = read_checkpoint()
    
    # Get current git state
    git_status = subprocess.run(["git", "status", "--porcelain"], ...)
    staged_files = parse_git_status(git_status)
    
    # Check for interrupted task
    last_task = checkpoint.task_history[-1]
    
    if last_task.status == "INTERRUPTED":
        # Crash detected
        report = f"""
⚠️ INTERRUPTED TASK DETECTED

Last task: TASK {len(checkpoint.task_history)}
Started: {last_task.started_at}
Last checkpoint: {last_task.last_heartbeat}
Git staged files: {len(last_task.git_staged)} files
Current git staged: {len(staged_files)} files

Recovery options:
[A] Continue from checkpoint (load TASK 3 context)
[B] Start fresh (clear checkpoint, keep git staged files)
[C] Review staged files before deciding
"""
        return report
    
    return None
```

---

## 4. Revised Session Protocol

### 4.1 Session Start (Enhanced)

```
┌─────────────────────────────────────────────────────────────────┐
│                     SESSION START                                 │
│                                                                  │
│  1. EXECUTE RULE 1 (as before)                                 │
│     CHECK: activeContext.md exists?                              │
│     CREATE: if not                                               │
│     READ: activeContext.md, progress.md                          │
│                                                                  │
│  2. CHECK FOR INTERRUPTED SESSION                               │
│     Read session-checkpoint.md                                   │
│     IF last task.status == INTERRUPTED:                         │
│        → Report crash detection                                  │
│        → Offer recovery options                                  │
│        → Human chooses recovery path                            │
│                                                                  │
│  3. LOAD CONTEXT                                                 │
│     From activeContext.md (if no crash)                         │
│     OR from checkpoint (if recovering)                           │
│                                                                  │
│  4. REPORT TO HUMAN                                              │
│     "Session: s2026-04-01-architect-0001"                       │
│     "Task: 3 of 3 (2 completed, 1 interrupted)"                │
│     "Ready to continue TASK 3"                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 During Task (Checkpoint Writing)

```
┌─────────────────────────────────────────────────────────────────┐
│                      DURING TASK                                  │
│                                                                  │
│  Every 5 minutes OR significant milestone:                       │
│  ─────────────────────────────────────────────────────────────  │
│  WRITE CHECKPOINT:                                               │
│  - current task status                                           │
│  - git staged files                                             │
│  - last heartbeat                                               │
│                                                                  │
│  TO session-checkpoint.md                                        │
│                                                                  │
│  (This is NEW — was not in original design)                     │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 After Task Completion (Enhanced)

```
┌─────────────────────────────────────────────────────────────────┐
│                   AFTER <attempt_completion>                      │
│                                                                  │
│  1. UPDATE MEMORY FILES (RULE 2, unchanged)                     │
│     activeContext.md                                             │
│     progress.md                                                  │
│     decisionLog.md (if ADR)                                      │
│                                                                  │
│  2. GIT COMMIT (before attempt_completion)                       │
│                                                                  │
│  3. UPDATE CHECKPOINT (NEW)                                      │
│     - Mark task as COMPLETED                                    │
│     - Include outcome summary                                    │
│     - Clear interrupted flag                                     │
│                                                                  │
│  4. WRITE SESSION SUMMARY (NEW)                                  │
│     - Task completed                                            │
│     - Files changed                                             │
│     - Decisions made                                            │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 Session End (Implicit + Explicit)

```
VS CODE CLOSES (implicit end)
    │
    ▼
NO AUTOMATIC ACTION (Roo Code limitation)
    │
    ▼
NEXT SESSION START:
    │
    ▼
DETECT: No checkpoint for recent task
    │
    ▼
RECOVERY UI presented to human
```

**Note**: There's no way to run code when VS Code closes. The checkpoint at step 4.2 is the only recovery mechanism.

---

## 5. What "Conversation" Should Be Called

### 5.1 Revised Terminology

| Old Word | Correct Word | Definition |
|----------|-------------|------------|
| **Conversation** | **Session** | VS Code window lifetime |
| **Conversation log** | **Chat history** | What was said in Roo Code chat |
| **Conversation file** | **Task output** | Files generated by agent during task |
| **Session artifact** | **Task record** | Checkpoint + memory update for one task |

### 5.2 What Gets Saved

| What | Where | When |
|------|-------|-------|
| Memory updates | `memory-bank/` | After each `<attempt_completion>` |
| Git commits | Git | After each task (before attempt_completion) |
| Checkpoint | `session-checkpoint.md` | Every 5 min during task |
| Chat history | Roo Code internal | Continuous |
| Task outputs | Git (staged files) | On crash, recovered from git staging |

### 5.3 What Doesn't Get Saved

| What | Lost on crash? | Mitigation |
|------|---------------|------------|
| Uncommitted file changes | YES | Checkpoint recovery (git staging) |
| Chat context (mid-task) | YES | Checkpoint has task summary |
| Agent reasoning | YES | Not recoverable |
| User's last message | NO | Always at end of chat |

---

## 6. Integration with Roo Code Modes

### 6.1 Mode = Persona, Not Session

| Mode | Persona | Used for |
|------|---------|----------|
| `architect` | Architect | Planning, design, ADRs |
| `code` | Developer | Implementation, refactoring |
| `ask` | — | Questions, explanations |
| `debug` | QA Engineer | Troubleshooting |

**Key insight**: A session can switch modes multiple times. The session_id persists, but the mode can change.

### 6.2 Session ID Format (Revised)

```
s{date}-{mode}-{n}

Example: s2026-04-01-architect-0001

Note: mode in session_id = the mode at session START
      (may change during session)
```

---

## 7. Summary: What Changes

### 7.1 New Files

| File | Purpose |
|------|---------|
| `session-checkpoint.md` | Recovery checkpoint, written every 5 min |

### 7.2 New Protocol Steps

| When | Action |
|------|--------|
| Every 5 min during task | Write checkpoint to `session-checkpoint.md` |
| Session start | Check for interrupted tasks, offer recovery |
| After `<attempt_completion>` | Mark task complete in checkpoint |

### 7.3 Revised Terminology

| Old | New |
|-----|-----|
| Conversation | Session (VS Code window lifetime) |
| Conversation file | Task record |
| Session artifact | Memory + checkpoint |

---

## 8. Open Questions

1. **Checkpoint frequency**: 5 minutes OK, or shorter?
2. **What to include in checkpoint**: Just file list? Also agent reasoning?
3. **Chat history**: Should we try to save Roo Code chat history? (May not be accessible)
4. **Mode changes within session**: Should session_id track mode changes?

---

**Next step:** Human reviews and approves this revised understanding. If correct → update `.clinerules` with checkpoint protocol.
