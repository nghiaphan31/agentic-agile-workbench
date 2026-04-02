# Orchestrator Intake: IDEA-020

**Date:** 2026-04-02  
**Source:** Human direct remark  
**Mode:** orchestrator  
**Session ID:** s2026-04-02-orchestrator-001  

---

## Human Input (verbatim)

> "i have a remark to be captured. it seems that we are lacking the true effective authoritative orchestrator to enforce the process. for exemple, i had to give a specific prompt so that roo switch to QA Engineer mode. I expect an Orchestrator to do this. I think that the orchestrator must be the default mode and that each time a task is completed the acting agent must give hands back to the orchestrator so that right next step is taken."

## Classification

**Type:** BUSINESS (WHAT) — Process/workflow improvement  
**Tier:** Major  
**Target:** v2.8  

## Intake Processing

1. **Detection:** Human expressed an improvement request outside current task scope (RULE 13)
2. **Routing:** Per RULE 13.2, routed to Orchestrator Agent for intake processing
3. **Classification:** BUSINESS requirement → IDEAS-BACKLOG.md
4. **Idea Created:** docs/ideas/IDEA-020-orchestrator-authoritative-default.md
5. **Backlog Updated:** Added to IDEAS-BACKLOG.md with [IDEA] status

## Key Points from Human

1. Orchestrator lacks authority to enforce process
2. Human had to manually prompt "switch to QA Engineer mode" — this should be automatic
3. Orchestrator should be the **default mode**
4. After any task completes, the acting agent must **return control to the Orchestrator**
5. Orchestrator determines next appropriate step

## Sync Detection

- Checked activeContext.md for parallel work
- No overlapping work detected on orchestrator-related files
- IDEA-002 (Calypso orchestration) is IMPLEMENTED — this is a different scope (enhanced orchestration vs. authoritative orchestration)

## Refinement Options

Human choices:
- [A] Refine now — structured requirement/feasibility session
- [B] Park for later — marked DEFERRED
- [C] Sync first — resolve overlap with existing ideas before refining

---

## Status

**Triage Status:** Not yet triaged  

**Next Action:** Awaiting human decision on refinement option [A], [B], or [C]
