# Rigorous Robustness Review — Part 2 (Sections 6–10)
## Continuation of plans/REVIEW-Gemini-Proxy-Path-Robustness.md

---

## 6. SP-007 Gem Instructions Review

The [`SP-007-gem-gemini-roo-agent.md`](template/prompts/SP-007-gem-gemini-roo-agent.md) Gem instructions are reviewed against the actual proxy behavior and the full Roo Code tool set.

### SP-007 Issue 1 — Missing critical XML tags in Gem instructions

The proxy validates for these tags (from `proxy.py` `ROO_XML_TAGS`):
```
<write_to_file>, <read_file>, <execute_command>, <attempt_completion>,
<ask_followup_question>, <replace_in_file>, <list_files>, <search_files>,
<browser_action>, <new_task>
```

SP-007 only documents 6 of these 10 tags in its "FORMAT DE REPONSE OBLIGATOIRE" section.

**Missing from SP-007 Gem instructions:**
- `<replace_in_file>` — NOT documented
- `<list_files>` — NOT documented
- `<browser_action>` — NOT documented
- `<new_task>` — NOT documented

**Impact of missing `<replace_in_file>`:** This is the most critical gap. Without it, Gemini will use `<write_to_file>` for every file modification, which:
1. Requires the full file content in every response (larger clipboard, more tokens)
2. Risks overwriting files with incomplete content if Gemini truncates its response
3. Is slower and more error-prone than surgical edits

**Impact of missing `<list_files>`:** Gemini cannot discover file structure. It must guess paths, leading to hallucinated file paths.

**Severity:** HIGH — `<replace_in_file>` is the preferred tool for surgical edits in any non-trivial development task.

### SP-007 Issue 2 — Hardcoded UADF project context

The Gem instructions contain:
```
CONTEXTE DU PROJET :
Tu travailles sur un projet utilisant le framework UADF (Unified Agentic Development Framework).
```

This hardcodes the UADF context. When the Gem is used for a different project (e.g., a React app, a Python API), the context is wrong. The Gem instructions should be project-agnostic, relying on the Memory Bank for project context.

**Severity:** LOW — the Gem is project-specific by design, but this should be documented as a deployment consideration.

### SP-007 Issue 3 — No instruction to use new conversation per session

The Gem instructions do not tell Gemini anything about conversation management. Combined with GAP-006 (the proxy sends full history in clipboard), this creates the history duplication problem.

**Severity:** MEDIUM — contributes to GAP-006.

---

## 7. Overall Robustness Verdict

### Verdict by Use Case Category

| Category | Verdict | Human Cycles | Notes |
| :--- | :---: | :---: | :--- |
| Simple single-turn tasks (PROMPT 0.1, 0.4, 1.1, 1.4) | ✅ ROBUST | 1 | Works as designed |
| Short iterative dialogues (PROMPT 0.3, 1.3 — 3–5 turns) | ✅ ROBUST | 3–5 | Manageable human load |
| Sprint Planning (PROMPT 4.2 — 5 turns) | ✅ ACCEPTABLE | 5 | ~4 min active attention |
| Sprint Review / Retrospective (PROMPT 4.5, 4.6) | ✅ ACCEPTABLE | 4–6 | ~5 min active attention |
| User Story Development (PROMPT 4.3 — 15–25 turns) | ⚠️ DEGRADED | 15–25 | ~15–20 min active attention |
| QA Testing (PROMPT 4.4 — 10–15 turns) | ⚠️ DEGRADED | 10–15 | Large clipboard from test output |
| Session startup (Protocol 9.1) | ⚠️ OVERHEAD | +3 mandatory | Before any real work begins |
| Boomerang Tasks (REQ-1.4) | ❌ BROKEN | N/A | Architecturally incompatible |
| Parallel tasks | ❌ BROKEN | N/A | Clipboard conflict |
| Unattended execution | ❌ IMPOSSIBLE | N/A | Fundamental constraint |
| Error recovery | ✅ WORKS | +2 per error | Self-correcting loop |
| Timeout recovery | ⚠️ UNDEFINED | N/A | HTTP 408 behavior not tested |
| Accidental clipboard overwrite | ⚠️ RISK | N/A | Silent corruption possible |

### Is the Gemini Proxy Path "as robust as the Claude API path"?

**No — and it cannot be, by design.** The fundamental difference is:

| Property | Claude API | Gemini Proxy |
| :--- | :--- | :--- |
| **Autonomy** | Fully autonomous | Requires human at every LLM turn |
| **Reliability** | Deterministic | Depends on human attention and accuracy |
| **Speed** | API latency (~2–5s/turn) | Human latency (~30–60s/turn) |
| **Parallelism** | Supported | Impossible (clipboard conflict) |
| **Boomerang Tasks** | Supported | Broken |
| **Unattended operation** | Yes | No |
| **Clipboard safety** | N/A | Risk of accidental overwrite |
| **History management** | Automatic | Manual (new conversation required) |

**However**, for the use cases where the proxy IS designed to work (simple to medium tasks with human in the loop), it is **sufficiently robust** with the following conditions met:

1. The human uses a **new Gemini conversation** for each proxy session (fixes GAP-006)
2. The human does not use the clipboard for other purposes during a proxy session (mitigates GAP-005)
3. Tasks are kept to **fewer than 10 LLM turns** to avoid clipboard size issues (mitigates GAP-001/002)
4. Boomerang Tasks are **not used** in proxy mode (documented limitation for GAP-003)

---

## 8. Prioritized Recommendations

### P0 — Blocking (must fix before regular use)

| ID | Fix | File to Change | Effort |
| :--- | :--- | :--- | :--- |
| **FIX-001** | Add explicit "NOUVELLE conversation" instruction to proxy console output | `template/proxy.py` | Low |
| **FIX-002** | Add `replace_in_file` and `list_files` to SP-007 Gem instructions | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Low |
| **FIX-003** | Document Boomerang Tasks as explicitly unsupported in proxy mode | `workbench/DOC1-PRD.md`, `workbench/DOC2-ARCH.md`, `workbench/DOC5-GUIDE.md` | Low |

### P1 — High Priority (fix before regular use)

| ID | Fix | File to Change | Effort |
| :--- | :--- | :--- | :--- |
| **FIX-004** | Add `try/except` around `pyperclip.paste()` in `_wait_clipboard()` | `template/proxy.py` | Low |
| **FIX-005** | Add request counter to console output | `template/proxy.py` | Low |
| **FIX-006** | Add minimum content length check before accepting clipboard change | `template/proxy.py` | Low |
| **FIX-007** | Test and document Roo Code behavior on HTTP 408 | `workbench/DOC5-GUIDE.md` section 9.6 | Medium |
| **FIX-008** | Add `MAX_HISTORY_CHARS` truncation in `_format_prompt()` | `template/proxy.py` | Medium |

### P2 — Medium Priority (quality improvements)

| ID | Fix | File to Change | Effort |
| :--- | :--- | :--- | :--- |
| **FIX-009** | Add "task chunking" guidance in DOC5 for proxy mode | `workbench/DOC5-GUIDE.md` | Low |
| **FIX-010** | Make SP-007 project-agnostic (remove UADF hardcoding) | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Low |
| **FIX-011** | Add proxy mode limitations section to DOC5 section 9.4 | `workbench/DOC5-GUIDE.md` | Low |
| **FIX-012** | Add `browser_action` and `new_task` to SP-007 with usage notes | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Low |

---

## 9. Recommended Minimal Code Changes

### Change 1 — `proxy.py` — Improved console message (FIX-001, FIX-005)

Replace the current console print:
```python
print(f"[{ts}] PROMPT COPIE ! ACTION : 1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C")
```

With:
```python
req_num = getattr(chat_completions, '_req_count', 0) + 1
chat_completions._req_count = req_num
print(f"[{ts}] ═══ REQUETE #{req_num} ═══")
print(f"[{ts}] PROMPT COPIE ({len(formatted)} chars) — ACTIONS REQUISES :")
print(f"         1. Chrome → gemini.google.com → Gem 'Roo Code Agent'")
print(f"         2. ⚠️  NOUVELLE conversation (ou effacer l'historique)")
print(f"         3. Ctrl+V pour coller le prompt")
print(f"         4. Attendre la fin de la reponse Gemini")
print(f"         5. Ctrl+A puis Ctrl+C pour copier TOUTE la reponse")
print(f"         ⚠️  Ne pas utiliser le presse-papiers pour autre chose !")
print(f"         Timeout dans {TIMEOUT_SECONDS}s...")
```

### Change 2 — `proxy.py` — Clipboard error handling + minimum length check (FIX-004, FIX-006)

Replace `_wait_clipboard()`:
```python
async def _wait_clipboard(initial_hash: str, ts: str) -> str:
    start = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)
        try:
            current = pyperclip.paste()
        except Exception as e:
            print(f"[{ts}] AVERTISSEMENT: Erreur acces presse-papiers: {e}")
            continue
        if _hash(current) != initial_hash:
            elapsed = time.time() - start
            if len(current) < 20:
                print(f"[{ts}] AVERTISSEMENT: Contenu trop court ({len(current)} chars) — verifier le presse-papiers")
                print(f"[{ts}] Contenu recu: {repr(current[:100])}")
                # Reset hash to keep waiting for a real response
                # Uncomment next line to make this blocking (safer):
                # continue
            print(f"[{ts}] REPONSE DETECTEE ! {len(current)} chars en {elapsed:.1f}s")
            if not _validate_response(current):
                print(f"[{ts}] AVERTISSEMENT : Aucune balise XML Roo Code detectee.")
            return current
        if time.time() - start > TIMEOUT_SECONDS:
            raise HTTPException(status_code=408, detail="Timeout: Relancez votre requete dans Roo Code.")
```

### Change 3 — SP-007 — Add missing XML tags

Add to the "FORMAT DE REPONSE OBLIGATOIRE" section of the Gem instructions:

```
Pour modifier partiellement un fichier existant (PREFERER a write_to_file) :
<replace_in_file>
<path>chemin/vers/fichier</path>
<diff>
[bloc de recherche et remplacement au format unifie]
</diff>
</replace_in_file>

Pour lister les fichiers d'un dossier :
<list_files>
<path>dossier/a/lister</path>
<recursive>false</recursive>
</list_files>
```

Also add to "REGLES IMPORTANTES":
```
7. Toujours utiliser replace_in_file plutot que write_to_file pour les modifications partielles
8. Toujours utiliser list_files pour decouvrir la structure du projet avant de coder
```

### Change 4 — DOC5 section 9.4 — Add proxy limitations (FIX-011)

Add to the "Protocole de Changement de Backend LLM" section:

```
LIMITATIONS CONNUES DU MODE PROXY GEMINI (a documenter dans activeContext.md) :
- Boomerang Tasks (new_task) : NON SUPPORTE — utiliser Claude API pour les taches
  necessitant des sous-agents
- Taches longues (> 10 tours LLM) : DECONSEILLE — decouper en sous-taches ou
  utiliser Claude API
- Utilisation parallele du presse-papiers : IMPOSSIBLE pendant une session proxy
- Execution sans surveillance : IMPOSSIBLE — presence humaine continue requise
- Conversation Gemini : TOUJOURS utiliser une NOUVELLE conversation a chaque session
  (ne pas continuer une conversation existante — le proxy envoie deja l'historique complet)
```

---

## 10. Final Summary

### Robustness Score by Dimension

| Dimension | Score | Justification |
| :--- | :---: | :--- |
| **Technical correctness** (proxy code) | 8/10 | Works correctly for designed use cases; 4 minor code issues |
| **Use case coverage** (simple tasks) | 9/10 | Excellent for 1–5 turn tasks |
| **Use case coverage** (complex tasks) | 5/10 | Degraded for 10+ turn tasks; broken for Boomerang |
| **Human UX** | 6/10 | Manageable but requires continuous attention |
| **Error resilience** | 6/10 | Self-correcting but vulnerable to accidental overwrites |
| **Documentation completeness** | 5/10 | GAP-006 (conversation mode) undocumented; SP-007 incomplete |
| **Parity with Claude API** | 3/10 | Fundamentally different model; not a drop-in replacement |

### Overall Verdict

```
╔══════════════════════════════════════════════════════════════════════════╗
║           GEMINI PROXY PATH — ROBUSTNESS REVIEW FINAL VERDICT           ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  VERDICT: ⚠️  CONDITIONALLY ROBUST                                       ║
║           (NOT equivalent to Claude API — different usage model)         ║
║                                                                          ║
║  WORKS WELL FOR (use freely):                                            ║
║    Phase 0 Amont Ouvert tasks (1–3 turns each)                           ║
║    Phase 1 Cadrage tasks (3–5 turns each)                                ║
║    Sprint Planning, Review, Retrospective (4–6 turns each)               ║
║    Short iterative dialogues with human feedback                         ║
║                                                                          ║
║  USE WITH CAUTION (chunk into smaller tasks):                            ║
║    User Story Development (break into sub-tasks of < 10 turns)           ║
║    QA Testing (run tests separately, paste only summary)                 ║
║    Any task requiring multiple large file reads                          ║
║                                                                          ║
║  DO NOT USE (switch to Claude API or Ollama):                            ║
║    Boomerang Tasks / sub-agent delegation                                ║
║    Unattended / background execution                                     ║
║    Tasks requiring parallel clipboard operations                         ║
║    Long autonomous agentic loops (20+ turns)                             ║
║                                                                          ║
║  BLOCKING FIXES REQUIRED BEFORE PRODUCTION USE:                         ║
║    FIX-001: Add "NOUVELLE conversation" to proxy console                 ║
║    FIX-002: Add replace_in_file + list_files to SP-007 Gem               ║
║    FIX-003: Document Boomerang Tasks as unsupported in proxy mode        ║
║                                                                          ║
║  CORRECT MENTAL MODEL FOR USERS:                                         ║
║    Claude API  = "Delegate and walk away"                                ║
║    Gemini Proxy = "Supervised co-pilot — you are the relay"              ║
║    Ollama Local = "Delegate and walk away (offline)"                     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

The proxy path is a **cost-free supervised alternative** to the Claude API, not a transparent replacement. Its robustness is sufficient for its intended use cases when the three blocking fixes are applied and users understand the "supervised co-pilot" mental model.
