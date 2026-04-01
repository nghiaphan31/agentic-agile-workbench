---
id: IDEA-019
title: Implement Conversation Logging Mechanism
status: [IDEA]
target_release: [v2.7]
source: Human (2026-04-01)
source_files: RULE 8.3, docs/conversations/
captured: 2026-04-01
captured_by: Developer mode
refined_by: 
refinement_session: 
---

## Description

Per RULE 8.3, conversations should be logged to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`. However, the conversation logging is NOT happening in practice - this very conversation is not being logged. We need an automated or semi-automated mechanism to trigger conversation logging.

## Motivation

RULE 8.3 Conversation Log Mandate states:
- When saving an AI conversation output, save to `docs/conversations/{YYYY-MM-DD}-{source}-{slug}.md`
- Add entry to `docs/conversations/README.md` with triage status "Not yet triaged"
- Never edit a conversation file after creation

But there is NO trigger mechanism in place:
- Agents don't automatically log conversations
- No pre-commit hook for conversation files
- No CI check to ensure conversations are logged
- The rule exists but isn't enforced

## Classification

Type: GOVERNANCE

## Required Actions

1. **Define trigger conditions:** When should a conversation be logged?
   - Every session? Only sessions with significant decisions?
   - Sessions that produce IDEAS or ADRs?
   - All sessions or selective?

2. **Implement logging mechanism:**
   - Automated logging at session end
   - Semi-automated (agent asks human for permission)
   - Manual with reminders

3. **Add CI check** to verify conversation logging

## Complexity Score

**Score: 4/10** — SYNCHRONOUS refinement recommended

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-01 | [IDEA] | Captured from human question |

## Session Mechanism Issues (Findings)

From examining `memory-bank/hot-context/session-checkpoint.md`:

| Issue | Finding |
|-------|---------|
| Session ID | Shows `s2026-04-01-architect-001` (yesterday's session) — no fresh session ID generated |
| Mode | `unknown` — `SESSION_MODE` env var NOT set by the tool |
| Heartbeat | Last heartbeat `2026-04-01T16:53:47` — from yesterday, not today |
| Conversation logging | Not auto-triggered at session end |
| Crash recovery | Session checkpoint mechanism exists but not started for today's session |

## Required Actions (Refined)

1. **Fix SESSION_MODE env var** — Tool must set this when starting a session
2. **Fix session ID generation** — Generate fresh ID `sYYYY-MM-DD-{mode}-{NNN}` per session start
3. **Start heartbeat automatically** — Or provide clear CLI instructions
4. **Auto-trigger conversation logging** — At session end (attempt_completion), log conversation
5. **CI check** — Verify session checkpoint updated within last 24h

---
