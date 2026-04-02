# IDEA-020: Authoritative Orchestrator as Default Mode

**ID:** IDEA-020  
**Title:** Authoritative Orchestrator as Default Mode  
**Source:** Human (direct remark)  
**Captured:** 2026-04-02  
**Status:** [IDEA]  
**Type:** governance  
**Tier:** Major  
**Target Release:** v2.8  

---

## Problem Statement

The current orchestration model is incomplete. Observations:

1. **Human had to manually prompt mode switches** — e.g., "switch to QA Engineer mode" should not require human intervention
2. **No automatic handoff protocol** — when one agent completes a task, there is no enforced mechanism to return control to the orchestrator
3. **Orchestrator is not the default entry point** — the human must know to invoke the orchestrator

## Proposed Solution

### 1. Orchestrator as Default Mode
- The Orchestrator Agent should be the **default mode** for the workbench
- When any task is received, the Orchestrator is invoked first
- The Orchestrator then delegates to specialized personas (QA Engineer, Developer, etc.) as needed

### 2. Mandatory Handoff Protocol
- After completing any task, an agent MUST return control to the Orchestrator
- This ensures the Orchestrator can:
  - Assess the completed work
  - Determine the next appropriate step
  - Route to the correct agent or persona
  - Enforce process compliance

### 3. Mode Switching Should Be Orchestrator-Driven
- Instead of humans prompting "switch to QA Engineer mode", the Orchestrator should:
  - Detect when QA validation is needed
  - Automatically switch to QA Engineer mode
  - Receive results back and continue orchestration

## Motivation

The human user expects a self-managing workflow where:
1. They state a goal
2. The Orchestrator drives the entire process
3. Specialized agents are invoked as needed
4. The Orchestrator maintains state and determines next steps

Currently, the human must manually manage mode transitions, which defeats the purpose of having an Orchestrator.

## Affected Documents

- `.roomodes` — default mode configuration
- `.clinerules` — handoff protocol rules
- `prompts/SP-008` or new orchestrator prompt — Orchestrator behavior specification
- `memory-bank/hot-context/session-checkpoint.md` — session state management

## Technical Considerations

1. **Roo Code Mode Switching** — Investigate if mode switching can be triggered programmatically by the AI agent itself, not just by human prompts
2. **Session State** — The Orchestrator must maintain enough context to determine next steps after any agent completes
3. **Handoff Detection** — Need a clear signal/pattern that indicates task completion and return of control

## Questions for Refinement

1. Can Roo Code be configured to always start in Orchestrator mode?
2. Is there an existing mechanism for an agent to trigger a mode switch autonomously?
3. What minimal state must be preserved during handoff?

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-04-02 | [IDEA] | Captured from human remark |

---
