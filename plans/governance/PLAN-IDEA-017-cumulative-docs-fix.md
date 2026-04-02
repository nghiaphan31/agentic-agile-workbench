# PLAN: IDEA-017 Cumulative Docs Remediation — v2.7 FULL REBUILD

**IDEA:** IDEA-017 — Fix Canonical Docs Cumulative Self-Contained Requirement
**Status:** [IMPLEMENTATION IN PROGRESS]
**Target Release:** v2.7
**Approach:** Full canonical documentation rebuild using ALL 236 project files
**Project Statistics:** 236 files, 43,558 lines of content
**Date:** 2026-04-02

---

## EXECUTIVE SUMMARY

Build v2.7 canonical docs (DOC-1 through DOC-5) that properly document the complete v2.6 codebase in cumulative format, using EVERY available source file.

**Target Structure:** Each v2.7 doc contains sections for v1.0 through v2.7, meeting minimum line counts:
- DOC-1 (PRD): 500+ lines
- DOC-2 (Architecture): 500+ lines
- DOC-3 (Implementation Plan): 300+ lines
- DOC-4 (Operations Guide): 300+ lines
- DOC-5 (Release Notes): 200+ lines

---

## COMPLETE SOURCE-TO-TARGET MAPPING

### SECTION 1: v1.0 Requirements (Base Documentation)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v1.0/DOC-1-v1.0-PRD.md | 387 | Foundational requirements, 8 domains, RBAC matrix |
| docs/releases/v1.0/DOC-2-v1.0-Architecture.md | 603 | Technical architecture, system design |
| docs/releases/v1.0/DOC-3-v1.0-Implementation-Plan.md | 1715 | Phase 0-12 implementation |
| docs/releases/v1.0/DOC-4-v1.0-Operations-Guide.md | 1985 | Operations procedures |
| docs/releases/v1.0/DOC-5-v1.0-Release-Notes.md | 77 | v1.0 release notes |
| docs/releases/v1.0/EXECUTION-TRACKER-v1.0.md | ~100 | Implementation status |
| memory-bank/hot-context/systemPatterns.md | ~50 | System patterns template |
| .clinerules | ~100 | Global rules |
| .roomodes | ~200 | Persona definitions |

**Target Sections:** v2.7 DOC-1 Section 2, DOC-2 Section 2, DOC-3 Section 2, DOC-4 Section 2, DOC-5 Section 2

---

### SECTION 2: v2.0 Requirements (Major Enhancement)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v2.0/DOC-1-v2.0-PRD.md | 191 | Hot/Cold memory, Calypso orchestration |
| docs/releases/v2.0/DOC-2-v2.0-Architecture.md | 310 | Updated architecture |
| docs/releases/v2.0/DOC-3-v2.0-Implementation-Plan.md | 666 | Phase 1-4 implementation |
| docs/releases/v2.0/DOC-4-v2.0-Operations-Guide.md | 688 | Updated operations |
| docs/releases/v2.0/DOC-5-v2.0-Release-Notes.md | 189 | v2.0 release notes |
| docs/releases/v2.0/EXECUTION-TRACKER-v2.0.md | ~80 | Implementation status |
| memory-bank/hot-context/decisionLog.md | ~200 | ADRs from v2.0 |
| docs/ideas/IDEA-001-hot-cold-memory.md | ~100 | Hot/Cold memory spec |
| docs/ideas/IDEA-002-calypso-orchestration.md | ~150 | Calypso spec |
| docs/ideas/IDEA-003-release-governance.md | ~80 | Release governance |
| docs/ideas/IDEA-006-template-enrichment.md | ~60 | Template enrichment |
| docs/ideas/IDEA-007-global-brain-librarian.md | ~120 | Librarian Agent spec |
| src/calypso/intake_agent.py | 12745 | Intake agent implementation |
| src/calypso/orchestrator_phase2.py | 9932 | Orchestrator Phase 2 |
| src/calypso/orchestrator_phase3.py | 10708 | Orchestrator Phase 3 |
| src/calypso/orchestrator_phase4.py | 10463 | Orchestrator Phase 4 |
| prompts/SP-008-synthesizer-agent.md | ~200 | Synthesizer prompt |
| prompts/SP-009-devils-advocate-agent.md | ~200 | Devil's advocate prompt |
| prompts/SP-010-librarian-agent.md | ~200 | Librarian prompt |

**Key Features in v2.0:**
- IDEA-001: Hot/Cold memory architecture
- IDEA-002: Calypso orchestration scripts
- IDEA-003: Release governance model
- IDEA-006: Template enrichment
- IDEA-007: Global Brain / Librarian Agent

**Target Sections:** v2.7 DOC-1 Section 3, DOC-2 Section 3, DOC-3 Section 3, DOC-4 Section 3, DOC-5 Section 3

---

### SECTION 3: v2.1 Requirements (MinMax Default)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v2.1/DOC-1-v2.1-PRD.md | 44 | Delta PRDs |
| docs/releases/v2.1/DOC-2-v2.1-Architecture.md | 38 | Delta architecture |
| docs/releases/v2.1/DOC-3-v2.1-Implementation-Plan.md | 43 | Delta implementation |
| docs/releases/v2.1/DOC-4-v2.1-Operations-Guide.md | 39 | Delta operations |
| docs/releases/v2.1/DOC-5-v2.1-Release-Notes.md | 91 | v2.1 release notes |
| docs/releases/v2.1/EXECUTION-TRACKER-v2.1.md | ~50 | Implementation status |
| docs/ideas/IDEA-008-openrouter-minimax-default.md | ~100 | OpenRouter MinMax spec |
| prompts/README.md | ~100 | Prompt registry documentation |

**Key Features in v2.1:**
- IDEA-008: OpenRouter MinMax M2.7 as default LLM

**Target Sections:** v2.7 DOC-1 Section 4, DOC-2 Section 4, DOC-3 Section 4, DOC-4 Section 4, DOC-5 Section 4

---

### SECTION 4: v2.2 Requirements (MinMax Merge)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v2.2/DOC-1-v2.2-PRD.md | 27 | Delta PRDs |
| docs/releases/v2.2/DOC-2-v2.2-Architecture.md | 18 | Delta architecture |
| docs/releases/v2.2/DOC-3-v2.2-Implementation-Plan.md | 26 | Delta implementation |
| docs/releases/v2.2/DOC-4-v2.2-Operations-Guide.md | 18 | Delta operations |
| docs/releases/v2.2/DOC-5-v2.2-Release-Notes.md | 55 | v2.2 release notes |
| docs/releases/v2.2/EXECUTION-TRACKER-v2.2.md | ~50 | Implementation status |
| memory-bank/hot-context/productContext.md | ~100 | Product context |

**Key Features in v2.2:**
- MinMax merged into default LLM backend
- Minor tooling improvements

**Target Sections:** v2.7 DOC-1 Section 5, DOC-2 Section 5, DOC-3 Section 5, DOC-4 Section 5, DOC-5 Section 5

---

### SECTION 5: v2.3 Requirements (Batch API Toolkit)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v2.3/DOC-1-v2.3-PRD.md | 309 | Comprehensive PRD |
| docs/releases/v2.3/DOC-2-v2.3-Architecture.md | 743 | Detailed architecture |
| docs/releases/v2.3/DOC-3-v2.3-Implementation-Plan.md | 323 | Implementation details |
| docs/releases/v2.3/DOC-4-v2.3-Operations-Guide.md | 135 | Operations guide |
| docs/releases/v2.3/DOC-5-v2.3-Release-Notes.md | 241 | v2.3 release notes |
| docs/releases/v2.3/EXECUTION-TRACKER-v2.3.md | ~100 | Implementation status |
| docs/ideas/IDEA-009-batch-api-toolkit.md | ~150 | Batch API toolkit spec |
| docs/ideas/IDEA-011-fix-sp002-coherence.md | ~100 | SP-002 coherence fix |
| scripts/batch/__init__.py | ~50 | Batch toolkit |
| scripts/batch/cli.py | ~200 | Batch CLI |
| scripts/batch/config.py | ~100 | Batch config |
| scripts/batch/generate.py | ~150 | Batch generator |
| scripts/batch/poll.py | ~100 | Batch poller |
| scripts/batch/retrieve.py | ~100 | Batch retriever |
| scripts/batch/submit.py | ~150 | Batch submitter |
| prompts/SP-002-clinerules-global.md | ~300 | Updated clinerules |
| docs/qa/v2.3/COHERENCE-AUDIT-v2.3.md | ~200 | Coherence audit |

**Key Features in v2.3:**
- IDEA-009: Generic Anthropic Batch API Toolkit
- IDEA-011: Fix SP-002/.clinerules Coherence

**Target Sections:** v2.7 DOC-1 Section 6, DOC-2 Section 6, DOC-3 Section 6, DOC-4 Section 6, DOC-5 Section 6

---

### SECTION 6: v2.4 Requirements (Ideation-to-Release Pipeline)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v2.4/DOC-1-v2.4-PRD.md | 326 | Comprehensive PRD |
| docs/releases/v2.4/DOC-2-v2.4-Architecture.md | 911 | Detailed architecture |
| docs/releases/v2.4/DOC-3-v2.4-Implementation-Plan.md | 456 | Implementation details |
| docs/releases/v2.4/DOC-4-v2.4-Operations-Guide.md | 267 | Operations guide |
| docs/releases/v2.4/DOC-5-v2.4-Release-Notes.md | 337 | v2.4 release notes |
| docs/releases/v2.4/EXECUTION-TRACKER-v2.4.md | ~150 | Implementation status |
| docs/ideas/IDEA-012A-phases-implementation-idea-to-release.md | ~200 | PHASE-A Foundation |
| docs/ideas/IDEA-012B-phases-implementation-idea-to-release.md | ~250 | PHASE-B Core Logic |
| docs/ideas/IDEA-012C-phases-implementation-idea-to-release.md | ~300 | PHASE-C Full Features |
| src/calypso/sync_detector.py | 18633 | Sync detector implementation |
| src/calypso/refinement_workflow.py | 14171 | Refinement workflow |
| src/calypso/branch_tracker.py | 14154 | Branch tracker |
| src/calypso/execution_tracker.py | 15846 | Execution tracker |
| src/calypso/ideas_dashboard.py | 7342 | Ideas dashboard |
| plans/governance/PLAN-ideation-to-release-full-process.md | ~400 | Full process plan |
| plans/governance/PLAN-integrated-ideation-to-release.md | ~300 | Integration plan |
| docs/ideas/TECH-SUGGESTIONS-BACKLOG.md | ~150 | Tech suggestions |

**Key Features in v2.4:**
- IDEA-012A/B/C: Ideation-to-Release Pipeline (PHASE-A, B, C)
- SyncDetector, RefinementWorkflow, BranchTracker, ExecutionTracker, IdeasDashboard

**Target Sections:** v2.7 DOC-1 Section 7, DOC-2 Section 7, DOC-3 Section 7, DOC-4 Section 7, DOC-5 Section 7

---

### SECTION 7: v2.5 Requirements (Ideation-to-Release Completion)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v2.5/DOC-1-v2.5-PRD.md | 171 | Comprehensive PRD |
| docs/releases/v2.5/DOC-2-v2.5-Architecture.md | 285 | Architecture |
| docs/releases/v2.5/DOC-3-v2.5-Implementation-Plan.md | 99 | Implementation |
| docs/releases/v2.5/DOC-4-v2.5-Operations-Guide.md | 116 | Operations |
| docs/releases/v2.5/DOC-5-v2.5-Release-Notes.md | 84 | v2.5 release notes |
| docs/releases/v2.5/EXECUTION-TRACKER-v2.5.md | ~100 | Implementation status |
| src/calypso/triage_dashboard.py | 8481 | Triage dashboard |
| src/calypso/fastmcp_server.py | 13171 | MCP server |
| plans/governance/ADR-010-dev-tooling-process-bypass.md | ~100 | ADR-010 |
| plans/governance/ADR-011-gitflow-violation-remediation.md | ~150 | ADR-011 |
| plans/governance/ADR-006-develop-main-branching.md | ~200 | ADR-006 GitFlow |

**Key Features in v2.5:**
- Full pipeline completion
- TriageDashboard
- FastMCP server
- ADR-010, ADR-011 GitFlow enforcement

**Target Sections:** v2.7 DOC-1 Section 8, DOC-2 Section 8, DOC-3 Section 8, DOC-4 Section 8, DOC-5 Section 8

---

### SECTION 8: v2.6 Requirements (Current Release)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/releases/v2.6/DOC-1-v2.6-PRD.md | 84 | v2.6 PRD (delta) |
| docs/releases/v2.6/DOC-2-v2.6-Architecture.md | 109 | v2.6 Architecture |
| docs/releases/v2.6/DOC-3-v2.6-Implementation-Plan.md | 121 | v2.6 Implementation |
| docs/releases/v2.6/DOC-4-v2.6-Operations-Guide.md | 88 | v2.6 Operations |
| docs/releases/v2.6/DOC-5-v2.6-Release-Notes.md | 116 | v2.6 release notes |
| memory-bank/hot-context/progress.md | ~100 | Progress tracking |
| memory-bank/hot-context/session-checkpoint.md | ~50 | Session checkpoint |
| docs/ideas/ADR-012-canonical-docs-cumulative-gitflow-enforcement.md | ~150 | ADR-012 |
| docs/qa/v2.6/COHERENCE-AUDIT-v2.6.md | ~300 | Coherence audit |
| docs/qa/v2.6/AUDIT-PLAN-v2.6.md | ~100 | Audit plan |
| docs/conversations/2026-04-01-code-p1-triage-v2.6.md | ~200 | Triage conversation |
| plans/governance/PLAN-canonical-docs-gitflow-enforcement.md | ~200 | Enforcement plan |

**Key Features in v2.6:**
- ADR-012: Canonical docs cumulative GitFlow enforcement
- Session checkpoint enhancement
- Memory bank improvements

**Target Sections:** v2.7 DOC-1 Section 9, DOC-2 Section 9, DOC-3 Section 9, DOC-4 Section 9, DOC-5 Section 9

---

### SECTION 9: v2.7 Requirements (NEW - This Release)

#### Source Files Used:
| Source File | Lines | Content Extracted |
|-------------|-------|-------------------|
| docs/ideas/IDEAS-BACKLOG.md | ~400 | All IDEA items |
| docs/ideas/IDEA-013-batch-toolkit-usability.md | ~100 | Batch toolkit improvements |
| docs/ideas/IDEA-014-canonical-docs-status-governance.md | ~100 | Status governance |
| docs/ideas/IDEA-015-mandatory-release-coherence-audit.md | ~100 | Coherence audit |
| docs/ideas/IDEA-016-enrich-docs-with-diagrams.md | ~100 | Mermaid diagrams |
| docs/ideas/IDEA-017-docs-must-be-cumulative-self-contained.md | ~100 | Cumulative docs fix |
| docs/ideas/IDEA-018-rules-authoritative-coherent.md | ~150 | Rules coherence |
| docs/ideas/IDEA-019-conversation-logging-mechanism.md | ~100 | Conversation logging |
| plans/governance/PLAN-IDEA-017-cumulative-docs-fix.md | ~500 | This plan |

**Target Sections:** v2.7 DOC-1 Section 10, DOC-2 Section 10, DOC-3 Section 10, DOC-4 Section 10, DOC-5 Section 10

---

## SUPPORTING SOURCE FILES (All Version Content)

### Conversations & Discussions (~2,000 lines)
| Source File | Lines | Content |
|-------------|-------|---------|
| docs/conversations/2026-03-27-gemini-doc6-architecture.md | ~400 | Architecture discussion |
| docs/conversations/2026-03-28-gemini-workbench-explained.md | ~500 | Workbench explanation |
| docs/conversations/2026-04-01-code-p1-triage-v2.6.md | ~300 | Triage session |
| docs/conversations/README.md | ~50 | Conversation index |

### Plans & Governance (~3,000 lines)
| Source File | Lines | Content |
|-------------|-------|---------|
| plans/governance/PLAN-release-governance.md | ~300 | Release governance |
| plans/governance/PLAN-roo-code-session-model.md | ~200 | Session model |
| plans/governance/PLAN-session-protocol.md | ~200 | Session protocol |
| plans/governance/PLAN-integrated-ideation-to-release-v2.md | ~300 | Integration v2 |
| plans/batch-doc6-review/* | ~500 | Batch review docs |
| plans/batch-full-audit/* | ~1000 | Full audit docs |

### Templates (~2,000 lines)
| Source File | Lines | Content |
|-------------|-------|---------|
| template/.clinerules | ~100 | Template rules |
| template/.roomodes | ~200 | Template personas |
| template/Modelfile | ~100 | Template model |
| template/proxy.py | ~374 | Template proxy |
| template/docs/*.md | ~500 | Template docs |
| template/prompts/*.md | ~1000 | Template prompts |

### Scripts & Tools (~2,000 lines)
| Source File | Lines | Content |
|-------------|-------|---------|
| scripts/check-prompts-sync.ps1 | ~200 | Prompt sync checker |
| scripts/checkpoint_heartbeat.py | ~100 | Heartbeat script |
| scripts/memory-archive.ps1 | ~100 | Memory archiver |
| scripts/rebuild_sp002.py | ~100 | SP-002 rebuild |
| scripts/start-proxy.ps1 | ~50 | Proxy starter |
| scripts/audit_cumulative_docs.py | ~300 | Audit script |

### CI/CD
| Source File | Lines | Content |
|-------------|-------|---------|
| .github/workflows/canonical-docs-check.yml | ~100 | CI enforcement |

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Create v2.7 Directory Structure
- [x] Create docs/releases/v2.7/ directory

### Phase 2: Build DOC-1-v2.7-PRD.md
- [ ] Section 1: Context and Strategic Vision (from README, conversations)
- [ ] Section 2: v1.0 Requirements (from v1.0 DOC-1)
- [ ] Section 3: v2.0 Requirements (from v2.0 DOC-1, IDEA-001/002/003/006/007)
- [ ] Section 4: v2.1 Requirements (from v2.1 DOC-1, IDEA-008)
- [ ] Section 5: v2.2 Requirements (from v2.2 DOC-1)
- [ ] Section 6: v2.3 Requirements (from v2.3 DOC-1, IDEA-009/011)
- [ ] Section 7: v2.4 Requirements (from v2.4 DOC-1, IDEA-012A/B/C)
- [ ] Section 8: v2.5 Requirements (from v2.5 DOC-1)
- [ ] Section 9: v2.6 Requirements (from v2.6 DOC-1, ADR-012)
- [ ] Section 10: v2.7 Requirements (from IDEAS-BACKLOG)

### Phase 3: Build DOC-2-v2.7-Architecture.md
- [ ] Section 1: Architecture Overview
- [ ] Section 2: v1.0 Architecture (from v1.0 DOC-2)
- [ ] Section 3: v2.0 Architecture (from v2.0 DOC-2, src/calypso)
- [ ] Section 4: v2.1 Architecture (from v2.1-v2.2 DOC-2)
- [ ] Section 5: v2.3 Architecture (from v2.3 DOC-2)
- [ ] Section 6: v2.4 Architecture (from v2.4 DOC-2, sync_detector.py)
- [ ] Section 7: v2.5 Architecture (from v2.5 DOC-2, ADR-010/011)
- [ ] Section 8: v2.6 Architecture (from v2.6 DOC-2)
- [ ] Section 9: v2.7 Architecture (new)

### Phase 4: Build DOC-3-v2.7-Implementation-Plan.md
- [ ] Section 1: Implementation Overview
- [ ] Section 2: v1.0 Implementation (from v1.0 DOC-3)
- [ ] Section 3: v2.0 Implementation (from v2.0 DOC-3)
- [ ] Section 4: v2.1-v2.2 Implementation (from EXECUTION-TRACKERs)
- [ ] Section 5: v2.3 Implementation (from v2.3 DOC-3, scripts/batch)
- [ ] Section 6: v2.4 Implementation (from v2.4 DOC-3, IDEA-012)
- [ ] Section 7: v2.5 Implementation (from v2.5 DOC-3)
- [ ] Section 8: v2.6 Implementation (from v2.6 DOC-3)
- [ ] Section 9: v2.7 Implementation (new)

### Phase 5: Build DOC-4-v2.7-Operations-Guide.md
- [ ] Section 1: Operations Overview
- [ ] Section 2: v1.0 Operations (from v1.0 DOC-4)
- [ ] Section 3: v2.0 Operations (from v2.0 DOC-4)
- [ ] Section 4: v2.1-v2.3 Operations (from v2.3 DOC-4)
- [ ] Section 5: v2.4-v2.5 Operations (from v2.4-v2.5 DOC-4)
- [ ] Section 6: v2.6 Operations (from v2.6 DOC-4, scripts)
- [ ] Section 7: v2.7 Operations (new)

### Phase 6: Build DOC-5-v2.7-Release-Notes.md
- [ ] Section 1: Release Notes Overview
- [ ] Section 2: v1.0 Release Notes (from v1.0 DOC-5)
- [ ] Section 3: v2.0 Release Notes (from v2.0 DOC-5)
- [ ] Section 4: v2.1 Release Notes (from v2.1 DOC-5)
- [ ] Section 5: v2.2 Release Notes (from v2.2 DOC-5)
- [ ] Section 6: v2.3 Release Notes (from v2.3 DOC-5)
- [ ] Section 7: v2.4 Release Notes (from v2.4 DOC-5)
- [ ] Section 8: v2.5 Release Notes (from v2.5 DOC-5)
- [ ] Section 9: v2.6 Release Notes (from v2.6 DOC-5)
- [ ] Section 10: v2.7 Release Notes (new)

### Phase 7: Validation
- [ ] Run audit script to verify cumulative compliance
- [ ] Verify all minimum line counts met
- [ ] Verify all sections present

---

## VERIFICATION CRITERIA

```
DOC-1-v2.7-PRD.md:
  - Line count: >= 500 lines
  - Sections: v1.0, v2.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7

DOC-2-v2.7-Architecture.md:
  - Line count: >= 500 lines
  - Sections: v1.0, v2.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7

DOC-3-v2.7-Implementation-Plan.md:
  - Line count: >= 300 lines
  - Sections: v1.0, v2.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7

DOC-4-v2.7-Operations-Guide.md:
  - Line count: >= 300 lines
  - Sections: v1.0, v2.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7

DOC-5-v2.7-Release-Notes.md:
  - Line count: >= 200 lines
  - Sections: v1.0, v2.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7
```

---

## NOTES

- All 236 files in the project contribute to the canonical docs
- v1.0 and v2.4 docs are the largest and most comprehensive
- v2.1-v2.2 and v2.5-v2.6 docs are smaller deltas
- EXECUTION-TRACKERs provide implementation history
- IDEAS-BACKLOG provides feature catalog
- Conversations provide design rationale
- Source code provides implementation details

---

## Complete Source Inventory (ALL Files to Be Used)

### Root Project Files (~750 lines)
| File | Purpose |
|------|---------|
| CHANGELOG.md | Release history |
| README.md | Project overview |
| Modelfile | Ollama model configuration |
| .roomodes | Agile persona definitions |
| .clinerules | Global rules |
| .gitattributes | Git configuration |
| .gitignore | Ignore patterns |
| proxy.py | Gemini Chrome proxy |
| deploy-workbench-to-project.ps1 | Deployment script |
| requirements.txt | Python dependencies |

### Source Code (~15,000 lines)
| File | Purpose |
|------|---------|
| src/calypso/__init__.py | Package init |
| src/calypso/apply_triage.py | Triage workflow |
| src/calypso/branch_tracker.py | GitFlow branch tracking |
| src/calypso/check_batch_status.py | Batch API status |
| src/calypso/execution_tracker.py | Progress tracking |
| src/calypso/fastmcp_server.py | MCP server |
| src/calypso/ideas_dashboard.py | Backlog UI |
| src/calypso/intake_agent.py | Idea intake |
| src/calypso/librarian_agent.py | Archive management |
| src/calypso/orchestrator_phase2.py | Phase 2 orchestration |
| src/calypso/orchestrator_phase3.py | Phase 3 orchestration |
| src/calypso/orchestrator_phase4.py | Phase 4 orchestration |
| src/calypso/refinement_workflow.py | Idea refinement |
| src/calypso/sync_detector.py | Overlap detection |
| src/calypso/triage_dashboard.py | Triage UI |
| src/calypso/tests/*.py | Test suite |

### System Prompts (~2,000 lines)
| File | Purpose |
|------|---------|
| prompts/SP-001-ollama-modelfile-system.md | Ollama setup |
| prompts/SP-002-clinerules-global.md | Global rules (synced with .clinerules) |
| prompts/SP-003-persona-product-owner.md | PO persona |
| prompts/SP-004-persona-scrum-master.md | SM persona |
| prompts/SP-005-persona-developer.md | Dev persona |
| prompts/SP-006-persona-qa-engineer.md | QA persona |
| prompts/SP-007-gem-gemini-roo-agent.md | Gemini agent |
| prompts/SP-008-synthesizer-agent.md | Synthesizer |
| prompts/SP-009-devils-advocate-agent.md | Devil's advocate |
| prompts/SP-010-librarian-agent.md | Librarian |

### Memory Bank (~2,000 lines)
| File | Purpose |
|------|---------|
| memory-bank/hot-context/activeContext.md | Current session context |
| memory-bank/hot-context/decisionLog.md | Architecture decisions |
| memory-bank/hot-context/productContext.md | Product requirements context |
| memory-bank/hot-context/progress.md | Project progress |
| memory-bank/hot-context/session-checkpoint.md | Session recovery |
| memory-bank/hot-context/systemPatterns.md | System patterns |

### Ideas & Backlog (~2,000 lines)
| File | Purpose |
|------|---------|
| docs/ideas/IDEAS-BACKLOG.md | All IDEA items |
| docs/ideas/TECH-SUGGESTIONS-BACKLOG.md | Technical suggestions |
| docs/ideas/IDEA-001 through IDEA-019 | Individual IDEA files |
| docs/ideas/ADR-010, ADR-011, ADR-012 | Architecture decisions |
| docs/ideas/P1-TRIAGE-2026-04-01-001.md | Triage records |

### Conversations (~2,000 lines)
| File | Purpose |
|------|---------|
| docs/conversations/2026-03-27-gemini-doc6-architecture.md | Architecture discussion |
| docs/conversations/2026-03-28-gemini-workbench-explained.md | Workbench explanation |
| docs/conversations/2026-04-01-code-p1-triage-v2.6.md | Triage session |
| docs/conversations/README.md | Conversation index |

### Plans (~3,000 lines)
| File | Purpose |
|------|---------|
| plans/governance/ADR-006-develop-main-branching.md | GitFlow ADR |
| plans/governance/PLAN-canonical-docs-gitflow-enforcement.md | Docs enforcement plan |
| plans/governance/PLAN-ideation-to-release-full-process.md | Full process |
| plans/governance/PLAN-integrated-ideation-to-release.md | Integration plan |
| plans/governance/PLAN-release-governance.md | Release governance |
| plans/governance/PLAN-roo-code-session-model.md | Session model |
| plans/governance/PLAN-session-protocol.md | Session protocol |
| plans/batch-doc6-review/* | Batch review batch_doc6-review |
| plans/batch-full-audit/* | Full audit batch_doc6-review |

### Template (~2,000 lines)
| File | Purpose |
|------|---------|
| template/.clinerules | Template rules |
| template/.roomodes | Template personas |
| template/Modelfile | Template config |
| template/proxy.py | Template proxy |
| template/requirements.txt | Template deps |
| template/docs/*.md | Template docs |
| template/prompts/*.md | Template prompts |

### QA (~minimal)
| File | Purpose |
|------|---------|
| docs/qa/.gitkeep | QA placeholder |

---

## Implementation Roadmap

---

## Executive Summary

**Goal:** Build v2.7 canonical docs (DOC-1 through DOC-5) that properly document the complete v2.6 codebase in cumulative format.

**Key Decision:** Rebuild from scratch using best available sources (NOT modify v2.6 frozen docs).

---

## Available Source Analysis

### Source Quality Assessment

| Source | DOC-1 | DOC-2 | DOC-3 | DOC-4 | DOC-5 | Notes |
|--------|-------|-------|-------|-------|-------|-------|
| v1.0 | 313 ⚠️ | 603 ✅ | 1715 ✅ | 1985 ✅ | 77 ⚠️ | Best base - comprehensive |
| v2.0 | 191 ⚠️ | 310 ⚠️ | 666 ⚠️ | 688 ⚠️ | 189 ⚠️ | Partial |
| v2.1 | 44 ❌ | 38 ❌ | 43 ❌ | 39 ❌ | 91 ⚠️ | Minimal delta |
| v2.2 | 27 ❌ | 18 ❌ | 26 ❌ | 18 ❌ | 55 ❌ | Minimal delta |
| v2.3 | 309 ⚠️ | 743 ✅ | 323 ⚠️ | 135 ❌ | 241 ⚠️ | Good Architecture |
| v2.4 | 326 ⚠️ | 911 ✅ | 456 ✅ | 267 ⚠️ | 337 ✅ | Best intermediate |
| v2.5 | 171 ❌ | 285 ❌ | 99 ❌ | 116 ❌ | 84 ❌ | Partial |
| v2.6 | 84 ❌ | 109 ❌ | 121 ❌ | 88 ❌ | 116 ❌ | Minimal (frozen) |

**Total usable content across versions:** ~6,500 lines of documentation

### Additional Sources for v2.7 Rebuild

| Source | Content | Lines |
|--------|---------|-------|
| src/calypso/*.py | All Python source code | ~150KB |
| memory-bank/systemPatterns.md | System patterns | ~500 |
| memory-bank/productContext.md | Product context | ~300 |
| prompts/*.md | System prompts | ~2000 |
| IDEAS-BACKLOG.md | All IDEAS with status | ~400 |
| EXECUTION-TRACKER-v2.*.md | Implementation history | ~1500 |

---

## v2.7 Rebuild Strategy

### DOC-1 (PRD) — 500+ lines target

**Structure:**
- Section 1: Context and Strategic Vision (from v2.6)
- Section 2: v1.0 Requirements (from v1.0 DOC-1)
- Section 3: v2.0-v2.2 Requirements (synthesize from IDEAS-BACKLOG)
- Section 4: v2.3 Requirements (from v2.3 DOC-1)
- Section 5: v2.4 Requirements (from v2.4 DOC-1)
- Section 6: v2.5 Requirements (from IDEAS-BACKLOG)
- Section 7: v2.6 Requirements (from IDEAS-BACKLOG + code analysis)
- Section 8: v2.7 Requirements (new)

**Sources:** v1.0 DOC-1, v2.3 DOC-1, v2.4 DOC-1, IDEAS-BACKLOG

### DOC-2 (Architecture) — 500+ lines target

**Structure:**
- Section 1: Architecture Overview
- Section 2: v1.0 Architecture (from v1.0 DOC-2)
- Section 3: v2.0-v2.2 Architecture (synthesize)
- Section 4: v2.3 Architecture (from v2.3 DOC-2)
- Section 5: v2.4 Architecture (from v2.4 DOC-2)
- Section 6: v2.5-v2.6 Architecture (synthesize from code)
- Section 7: v2.7 Architecture (new)

**Sources:** v1.0 DOC-2, v2.3 DOC-2, v2.4 DOC-2, src/calypso/*.py

### DOC-3 (Implementation Plan) — 300+ lines target

**Structure:**
- Section 1: Implementation Overview
- Section 2: v1.0 Implementation (from v1.0 DOC-3)
- Section 3: v2.0-v2.2 Implementation (synthesize)
- Section 4: v2.3 Implementation (from v2.3 DOC-3)
- Section 5: v2.4 Implementation (from v2.4 DOC-3)
- Section 6: v2.5-v2.6 Implementation (from EXECUTION-TRACKERs)
- Section 7: v2.7 Implementation (new)

**Sources:** v1.0 DOC-3, v2.3 DOC-3, v2.4 DOC-3, EXECUTION-TRACKERs

### DOC-4 (Operations Guide) — 300+ lines target

**Structure:**
- Section 1: Operations Overview
- Section 2: v1.0 Operations (from v1.0 DOC-4)
- Section 3: v2.0-v2.2 Operations (synthesize)
- Section 4: v2.3-v2.4 Operations (from v2.3/v2.4 DOC-4)
- Section 5: v2.5-v2.6 Operations (synthesize)
- Section 6: v2.7 Operations (new)

**Sources:** v1.0 DOC-4, v2.3 DOC-4, v2.4 DOC-4

### DOC-5 (Release Notes) — 200+ lines target

**Structure:**
- Section 1: Release Notes Overview
- Section 2: v1.0 Release Notes (from v1.0 DOC-5)
- Section 3: v2.0-v2.2 Release Notes (synthesize)
- Section 4: v2.3 Release Notes (from v2.3 DOC-5)
- Section 5: v2.4 Release Notes (from v2.4 DOC-5)
- Section 6: v2.5-v2.6 Release Notes (synthesize)
- Section 7: v2.7 Release Notes (new)

**Sources:** All DOC-5 versions, EXECUTION-TRACKERs

---

## Implementation Steps

### Phase 1: Create v2.7 directory structure
- [ ] Create docs/releases/v2.7/ directory
- [ ] Create DOC-1-v2.7-PRD.md with front matter and TOC
- [ ] Create DOC-2-v2.7-Architecture.md with front matter and TOC
- [ ] Create DOC-3-v2.7-Implementation-Plan.md with front matter and TOC
- [ ] Create DOC-4-v2.7-Operations-Guide.md with front matter and TOC
- [ ] Create DOC-5-v2.7-Release-Notes.md with front matter and TOC

### Phase 2: Populate v1.0 sections
- [ ] Copy v1.0 DOC-1 content to DOC-1-v2.7 section 2
- [ ] Copy v1.0 DOC-2 content to DOC-2-v2.7 section 2
- [ ] Copy v1.0 DOC-3 content to DOC-3-v2.7 section 2
- [ ] Copy v1.0 DOC-4 content to DOC-4-v2.7 section 2
- [ ] Copy v1.0 DOC-5 content to DOC-5-v2.7 section 2

### Phase 3: Populate v2.3-v2.4 sections (largest intermediate docs)
- [ ] Copy v2.3 DOC-1 to DOC-1-v2.7 section 4
- [ ] Copy v2.3 DOC-2 to DOC-2-v2.7 section 4
- [ ] Copy v2.3 DOC-3 to DOC-3-v2.7 section 4
- [ ] Copy v2.3 DOC-4 to DOC-4-v2.7 section 4
- [ ] Copy v2.3 DOC-5 to DOC-5-v2.7 section 4
- [ ] Copy v2.4 DOC-1 to DOC-1-v2.7 section 5
- [ ] Copy v2.4 DOC-2 to DOC-2-v2.7 section 5
- [ ] Copy v2.4 DOC-3 to DOC-3-v2.7 section 5
- [ ] Copy v2.4 DOC-4 to DOC-4-v2.7 section 5
- [ ] Copy v2.4 DOC-5 to DOC-5-v2.7 section 5

### Phase 4: Synthesize v2.0-v2.2 and v2.5-v2.6 sections
- [ ] Analyze IDEAS-BACKLOG for v2.0-v2.2 scope
- [ ] Analyze IDEAS-BACKLOG for v2.5-v2.6 scope
- [ ] Create placeholder sections with synthesized content
- [ ] Verify line counts meet minimums

### Phase 5: Add v2.7 new requirements section
- [ ] Document new v2.7 features
- [ ] Update front matter

### Phase 6: Validation
- [ ] Run audit script
- [ ] Verify line counts
- [ ] Verify all sections present
- [ ] Human review

---

## Verification Criteria

```
v2.7 DOC-1: >= 500 lines, 8 sections (v1.0 through v2.7)
v2.7 DOC-2: >= 500 lines, 8 sections (v1.0 through v2.7)
v2.7 DOC-3: >= 300 lines, 8 sections (v1.0 through v2.7)
v2.7 DOC-4: >= 300 lines, 8 sections (v1.0 through v2.7)
v2.7 DOC-5: >= 200 lines, 8 sections (v1.0 through v2.7)
```

---

## Notes

- v2.6 docs remain FROZEN and unmodified
- This plan creates NEW v2.7 docs that properly accumulate content
- Historical sections may be reconstructed from best available sources
- Some delta-based intermediate docs may be skipped if content is minimal

---

## 1. Problem Statement

Canonical docs (DOC-1 through DOC-5) violate RULE 12 cumulative requirement:

| Issue | Evidence |
|-------|----------|
| v2.6 DOC-1 (120 lines) | Claims sections for v2.1-v2.5 in TOC, but actual content only has v1.0 and v2.6 |
| v2.6 DOC-2 (148 lines) | Far below 500-line minimum |
| v2.6 DOC-3 (166 lines) | Far below 300-line minimum |
| v2.6 DOC-4 (128 lines) | Far below 300-line minimum |
| v2.6 DOC-5 (165 lines) | Far below 200-line minimum |
| Missing source content | Intermediate docs (v2.1-v2.5) are also delta-based and tiny (18-64 lines) |

**Constraint:** v2.6 docs are FROZEN per front matter — cannot be modified.

---

## 2. Root Cause Analysis

1. **RULE 12 created without enforcement**: The cumulative requirement existed but was never enforced
2. **CI check existed but wasn't blocking**: `.github/workflows/canonical-docs-check.yml` has proper checks but workflow failures didn't block merges
3. **Frozen docs violate their own standard**: v2.6 claims `cumulative: true` but doesn't actually meet the requirement
4. **Source content reconstruction gap**: Historical content for v2.1-v2.5 never existed in proper form

---

## 3. Remediation Options Analysis

### Option A: Full Retroactive Rebuild (Reconstruct Missing Content)
- **Pros:** Complete fix, proper cumulative docs
- **Cons:** Massive effort (reconstruct ~35 documents worth of content from EXECUTION-TRACKERs, conversation logs, IDEAS-BACKLOG), may not be possible accurately

### Option B: Pragmatic Partial Fix (Forward-Looking)
- **Pros:** Realistic, focuses on preventing future violations
- **Cons:** Historical gap remains in v2.6 docs

### Option C: Hybrid — Mark Frozen Docs as Non-Cumulative
- **Pros:** Honest about the problem
- **Cons:** Admits failure of governance

---

## 4. Recommended Approach: Option B (Forward-Looking Fix)

**Rationale:** Retroactive reconstruction of 7 versions × 5 docs is not feasible with high confidence. The pragmatic path is to:
1. Acknowledge the gap in v2.6 (frozen, non-cumulative)
2. Fix the CI enforcement to block future violations
3. Ensure v2.7 docs are properly cumulative
4. Document the limitation

### 4.1 Immediate Actions (This Session)

#### A. Fix CI Enforcement
The GitHub Actions workflow already exists but needs to be ENFORCED:

```yaml
# Current: exits with error on failures (correct)
# Issue: workflow may not be required status check

Jobs needed:
- canonical-docs-check (required status check for PRs)
- Must pass before merge to develop-v2.7
```

#### B. Create v2.7 docs with proper cumulative structure

For each DOC-1 through DOC-5 at v2.7:
1. Copy v2.6 doc structure as base
2. For v2.1-v2.5 sections: Create placeholder content from available sources:
   - EXECUTION-TRACKERs (v2.1-v2.5)
   - IDEAS-BACKLOG (what was implemented)
   - Conversation logs (design discussions)
   - Git history (what changed)
3. Add v2.7 new requirements section

#### C. Document the Gap

Add to v2.6 docs front matter:
```
note: "This version's canonical docs do not meet cumulative requirement (IDEA-017). 
       Historical sections reconstructed from secondary sources. 
       See v2.7 for properly cumulative docs."
```

### 4.2 Content Reconstruction Strategy

For missing v2.1-v2.5 sections, extract from:

| Source | Information Available |
|--------|----------------------|
| EXECUTION-TRACKER-v2.1.md | What was implemented in v2.1 |
| EXECUTION-TRACKER-v2.2.md | What was implemented in v2.2 |
| EXECUTION-TRACKER-v2.3.md | What was implemented in v2.3 |
| EXECUTION-TRACKER-v2.4.md | What was implemented in v2.4 |
| EXECUTION-TRACKER-v2.5.md | What was implemented in v2.5 |
| IDEAS-BACKLOG.md | All IDEAS with target versions |
| conversation logs | Design rationale |

---

## 5. Implementation Plan

### Phase 1: CI Enforcement (Day 1)
- [ ] Ensure `canonical-docs-check.yml` is a required status check
- [ ] Add pre-commit hook to run local check before commit
- [ ] Test that CI fails on current docs (confirming the bug)

### Phase 2: v2.7 Doc Structure (Day 1-2)
- [ ] Create DOC-1-v2.7-PRD.md skeleton with sections for v1.0-v2.7
- [ ] Create DOC-2-v2.7-Architecture.md skeleton
- [ ] Create DOC-3-v2.7-Implementation-Plan.md skeleton
- [ ] Create DOC-4-v2.7-Operations-Guide.md skeleton
- [ ] Create DOC-5-v2.7-Release-Notes.md skeleton

### Phase 3: Content Population (Day 2-3)
- [ ] Populate v2.1-v2.5 sections from EXECUTION-TRACKERs
- [ ] Add v2.6 content (extract from current v2.6 docs)
- [ ] Add v2.7 new requirements section

### Phase 4: Validation (Day 3)
- [ ] Run `python scripts/audit_cumulative_docs.py` on v2.7 docs
- [ ] Verify all docs meet minimum line counts
- [ ] Verify all version sections present

---

## 6. Verification Checklist

```
v2.7 DOC-1: >= 500 lines, sections for v1.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7
v2.7 DOC-2: >= 500 lines, sections for v1.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7
v2.7 DOC-3: >= 300 lines, sections for v1.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7
v2.7 DOC-4: >= 300 lines, sections for v1.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7
v2.7 DOC-5: >= 200 lines, sections for v1.0, v2.1, v2.2, v2.3, v2.4, v2.5, v2.6, v2.7
```

---

## 7. Open Questions

1. **Historical accuracy**: How important is it that reconstructed content be word-for-word identical to original intent?
2. **Scope of reconstruction**: Should we try to reconstruct v2.1-v2.5 content from secondary sources, or use placeholder/brief summaries?
3. **v2.6 frozen status**: Should we add a note to v2.6 docs acknowledging they don't meet cumulative requirement?

---

## 8. Decision Required

Please approve or modify this plan:

**[A]** Proceed with Option B (Forward-Looking Fix) as outlined above  
**[B]** Attempt Option A (Full Retroactive Rebuild) - higher effort but complete fix  
**[C]** Modify the approach - provide specific guidance  
**[D]** Defer to future sprint - document gap and move on
