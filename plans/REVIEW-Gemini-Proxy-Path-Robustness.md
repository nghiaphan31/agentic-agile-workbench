# Rigorous Robustness Review — Gemini Chrome Proxy Path
## Agentic Agile Workbench — Mode Proxy vs Mode Cloud (Claude API)

**Date :** 2026-03-23  
**Reviewer :** Architect Mode (claude-sonnet-4-6)  
**Scope :** Full simulation of all use cases through the Gemini Chrome proxy path  
**Reference documents :** DOC1-PRD v2.0, DOC2-ARCH v2.0, DOC5-GUIDE v2.0, SP-007 v1.0.0, `template/proxy.py` v2.0  
**Verdict summary :** ⚠️ **CONDITIONALLY ROBUST** — 7 critical gaps identified, 4 blocking for production parity with Claude API

---

## 1. Review Methodology

The review simulates every use case from DOC5-GUIDE through the proxy path, tracing each step through the full data flow:

```
Roo Code → POST /v1/chat/completions → proxy.py → pyperclip.copy()
→ [HUMAN: Chrome → Gem → Ctrl+V → wait → Ctrl+A+C] → pyperclip.paste()
→ proxy.py → SSE/JSON → Roo Code → action execution
```

For each use case, the simulation asks:
1. Does the proxy correctly format and transmit the prompt?
2. Does the human step introduce failure modes?
3. Does Gemini (via the Gem) produce a valid XML response?
4. Does the proxy correctly detect and re-inject the response?
5. Does Roo Code correctly execute the returned XML action?
6. Is the outcome equivalent to the Claude API path?

---

## 2. Use Case Simulation Matrix

### UC-001 — Simple single-turn task (e.g., PROMPT 0.1 — Collecte des entrées brutes)

**Roo Code sends:**
```json
{
  "model": "gemini-manual",
  "messages": [
    {"role": "system", "content": "[Roo Code system prompt — ~3000 tokens]"},
    {"role": "user", "content": "Crée le fichier docs/brief/BRIEF-001..."}
  ],
  "stream": true
}
```

**Proxy processing (USE_GEM_MODE=true):**
- System message filtered ✅
- Formatted clipboard content: `[USER]\nCrée le fichier docs/brief/BRIEF-001...`
- Hash computed: `md5("[USER]\nCrée le fichier...")` ✅
- Console: `[HH:MM:SS] PROMPT COPIE ! ACTION : 1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C` ✅

**Human step:**
- Switch to Chrome, open Gem "Roo Code Agent", Ctrl+V, wait for Gemini response, Ctrl+A+C ✅

**Expected Gemini response:**
```xml
<write_to_file>
<path>docs/brief/BRIEF-001-vision-narrative.md</path>
<content>...</content>
</write_to_file>
```

**Proxy detection:** Hash changes → response captured ✅  
**Validation:** `<write_to_file>` tag found → no warning ✅  
**SSE injection:** Single chunk → Roo Code receives and executes ✅

**Verdict:** ✅ WORKS — equivalent to Claude API path for simple tasks.

---

### UC-002 — Multi-turn iterative dialogue (e.g., PROMPT 0.3 — Clarification des ambiguïtés)

**Scenario:** Agent asks a question, human answers, agent asks next question, etc. (N turns)

**Turn 1 — Roo Code sends:**
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "Lis BRIEF-002 et pose-moi une question..."},
    {"role": "assistant", "content": "<ask_followup_question>...Q1...</ask_followup_question>"},
    {"role": "user", "content": "Réponse à Q1 : ..."},
    {"role": "assistant", "content": "<ask_followup_question>...Q2...</ask_followup_question>"},
    {"role": "user", "content": "Réponse à Q2 : ..."}
  ]
}
```

**Proxy clipboard content (USE_GEM_MODE=true):**
```
[USER]
Lis BRIEF-002 et pose-moi une question...

---

[ASSISTANT]
<ask_followup_question>...Q1...</ask_followup_question>

---

[USER]
Réponse à Q1 : ...

---

[ASSISTANT]
<ask_followup_question>...Q2...</ask_followup_question>

---

[USER]
Réponse à Q2 : ...
```

**⚠️ GAP-001 — CLIPBOARD SIZE EXPLOSION ON LONG CONVERSATIONS**

As the conversation grows (N turns), the clipboard content grows linearly. A typical DOC5 workflow with 10+ turns (Sprint Planning → Development → Tests → Review → Retrospective) can accumulate:
- Each Roo Code XML action: ~500–2000 chars
- Each user message: ~200–500 chars
- 10 turns × 1500 chars average = ~15,000 chars

This is manageable. However, for complex tasks like PROMPT 4.3 (Developer implementing a User Story with multiple sub-tasks), the history can reach:
- 20+ turns × 2000 chars = ~40,000 chars
- Plus file contents read via `<read_file>` injected back as assistant messages

**Risk:** At ~50,000+ chars, the clipboard paste into Gemini Web may:
1. Trigger Gemini's input length limits (Gemini 1.5 Pro: 1M tokens, but the Web UI may have practical limits)
2. Cause the human to paste a very large block that takes time to process
3. Cause Gemini to lose focus on the actual task due to context dilution

**Severity:** MEDIUM — not blocking for typical use cases, but degrades for long sessions.

**Claude API comparison:** Claude API handles this transparently — no human sees the message history size.

---

### UC-003 — File read result injection (read_file → content returned to agent)

**Scenario:** Agent sends `<read_file>`, Roo Code executes it, then sends the file content back as the next user message.

**Turn N+1 — Roo Code sends:**
```json
{
  "messages": [
    ...(previous history)...,
    {"role": "assistant", "content": "<read_file><path>memory-bank/activeContext.md</path></read_file>"},
    {"role": "user", "content": "[File content of memory-bank/activeContext.md]\n\n# Active Context\n...(500 lines)..."}
  ]
}
```

**⚠️ GAP-002 — LARGE FILE CONTENT IN CLIPBOARD**

When Roo Code injects file contents back into the conversation (standard agentic loop), the clipboard content can become very large very quickly:
- `memory-bank/activeContext.md`: ~100–500 lines
- `memory-bank/systemPatterns.md`: ~200–800 lines
- Source code files: potentially thousands of lines

A single `<read_file>` on a large source file (e.g., `src/main.py` with 500 lines) adds ~15,000 chars to the clipboard.

**Concrete failure scenario:**
1. Developer persona reads `memory-bank/systemPatterns.md` (300 lines = ~8,000 chars)
2. Then reads `memory-bank/techContext.md` (200 lines = ~5,000 chars)
3. Then reads `src/app.py` (400 lines = ~12,000 chars)
4. Total clipboard: ~25,000 chars of file content + history

The human must paste this entire block into Gemini Web. This is:
- Tedious (large paste)
- Error-prone (partial paste if clipboard is corrupted)
- Potentially hitting Gemini Web UI input limits

**Severity:** HIGH — this is a real operational bottleneck for any non-trivial development task.

**Claude API comparison:** Claude API handles file contents natively — no human involvement, no size concern.

---

### UC-004 — Boomerang Tasks (sub-task delegation)

**Scenario:** Main agent (32B in Ollama mode, or Gemini in proxy mode) creates a sub-task via `<new_task>`.

**⚠️ GAP-003 — BOOMERANG TASKS NOT SUPPORTED IN PROXY MODE**

The `<new_task>` XML tag is listed in `ROO_XML_TAGS` for validation in `proxy.py`, but Boomerang Tasks require Roo Code to spawn a **new agent instance** with a **different model**. In proxy mode:

- The proxy is configured as a single endpoint (`localhost:8000`)
- All requests from all Roo Code instances (main + sub-task) go to the same proxy
- The human must handle **two simultaneous clipboard polling loops** — which is impossible

**Concrete failure scenario:**
1. Main agent sends `<new_task>` to delegate to a sub-agent
2. Roo Code spawns a new agent instance, also configured to use `localhost:8000`
3. Sub-agent sends its first request to the proxy
4. **The proxy has no way to distinguish main-agent requests from sub-agent requests**
5. The human is now expected to handle two interleaved clipboard sessions
6. **Result: deadlock or corrupted responses**

**Severity:** CRITICAL — Boomerang Tasks are completely broken in proxy mode. REQ-1.4 is not achievable via the proxy path.

**Claude API comparison:** Claude API handles Boomerang Tasks natively — Roo Code manages the sub-task lifecycle transparently.

**Note:** This is an acknowledged architectural limitation (the proxy is designed for single-agent use), but it is not documented as a known limitation in DOC1, DOC2, or DOC5.

---

### UC-005 — Timeout scenario (human is slow or distracted)

**Scenario:** Human receives the clipboard notification but takes > 300 seconds to respond.

**Proxy behavior:**
```python
if time.time() - start > TIMEOUT_SECONDS:
    raise HTTPException(status_code=408, detail="Timeout: Relancez votre requete dans Roo Code.")
```

**Roo Code receives HTTP 408.**

**⚠️ GAP-004 — HTTP 408 HANDLING BY ROO CODE IS UNDEFINED**

The proxy returns HTTP 408 on timeout. However:
1. Roo Code's behavior when receiving HTTP 408 from an OpenAI-compatible endpoint is **not documented** and **not tested** in the design
2. Roo Code may interpret 408 as a fatal error and abort the entire task
3. Roo Code may retry the request — which would trigger a **new clipboard copy** (overwriting the previous one)
4. The human has no way to know if Roo Code retried or aborted

**Concrete failure scenario:**
1. Human is distracted for 6 minutes (> 300s timeout)
2. Proxy returns HTTP 408
3. Roo Code retries → proxy copies a new prompt to clipboard
4. Human returns, sees the clipboard notification, pastes into Gemini
5. But the clipboard now contains the **retry request** (possibly identical or slightly different)
6. Human pastes, Gemini responds, human copies response
7. **But Roo Code may have already aborted the task** — the response is injected into a dead connection

**Severity:** HIGH — the timeout recovery path is undefined and potentially leads to silent task failure.

**Claude API comparison:** Claude API has no timeout — the connection stays open until the model responds (or network error). No human intervention needed.

---

### UC-006 — Human copies wrong content (accidental clipboard overwrite)

**Scenario:** Human accidentally copies something else (e.g., a URL, a file path) before copying the Gemini response.

**Proxy behavior:**
```python
current = pyperclip.paste()
if _hash(current) != initial_hash:
    # ANY change triggers detection
    return current
```

**⚠️ GAP-005 — NO VALIDATION THAT THE CLIPBOARD CONTENT IS A GEMINI RESPONSE**

The proxy detects **any** clipboard change as a valid Gemini response. If the human accidentally:
- Copies a URL: `https://gemini.google.com/...`
- Copies a file path: `C:\Users\nghia\...`
- Copies a partial response (Ctrl+C before Gemini finishes)
- Copies from another application

The proxy will:
1. Detect the hash change ✅
2. Check for XML tags → **no tags found** → print WARNING (non-blocking) ✅
3. **Inject the garbage content into Roo Code as the LLM response** ❌

Roo Code will then try to parse `https://gemini.google.com/...` as an LLM response, which will either:
- Cause a parsing error
- Cause the agent to produce nonsensical output
- Silently corrupt the conversation history

**Severity:** HIGH — this is a real operational risk in a human-in-the-loop system. The warning is non-blocking by design (REQ-2.3.4), but the consequence is silent corruption.

**Claude API comparison:** Claude API responses are always valid — no human can accidentally inject garbage.

---

### UC-007 — Sprint Planning (PROMPT 4.2) — complex multi-file read

**Scenario:** Product Owner persona runs Sprint Planning. The agent needs to:
1. Read `memory-bank/productContext.md`
2. Read `memory-bank/progress.md`
3. Create `docs/sprints/sprint-001/SPR-001-001-sprint-backlog.md`
4. Update `memory-bank/activeContext.md`
5. Execute `git commit`

**Simulation trace:**

**Request 1:** Read productContext.md
- Clipboard: `[USER]\nLis memory-bank/productContext.md et memory-bank/progress.md...`
- Human: paste into Gem, wait, copy response
- Gemini returns: `<read_file><path>memory-bank/productContext.md</path></read_file>`
- Proxy injects → Roo Code reads file → sends content back

**Request 2:** File content injected back
- Clipboard now contains: `[USER]\n...\n\n---\n\n[ASSISTANT]\n<read_file>...</read_file>\n\n---\n\n[USER]\n[File content of memory-bank/productContext.md]\n...(300 lines)...`
- Human: paste into Gem, wait, copy response
- Gemini returns: `<read_file><path>memory-bank/progress.md</path></read_file>`

**Request 3:** Second file content injected
- Clipboard now contains: previous history + progress.md content (~200 lines)
- Human: paste into Gem, wait, copy response
- Gemini returns: `<write_to_file><path>docs/sprints/sprint-001/SPR-001-001-sprint-backlog.md</path><content>...</content></write_to_file>`

**Request 4:** Write confirmation + update activeContext.md
- Clipboard: full history + write confirmation
- Human: paste, wait, copy
- Gemini returns: `<write_to_file><path>memory-bank/activeContext.md</path>...</write_to_file>`

**Request 5:** Git commit
- Clipboard: full history
- Human: paste, wait, copy
- Gemini returns: `<execute_command><command>git add . && git commit -m "feat(sprint-001): sprint planning"</command></execute_command>`

**Total human interventions for Sprint Planning: 5 copy-paste cycles**
**Total clipboard size at step 5: ~15,000–25,000 chars**
**Total elapsed time: 5 × (30s Gemini response + 15s human action) = ~4 minutes**

**Verdict:** ✅ WORKS but requires significant human attention. Each step requires the human to:
1. Notice the console notification
2. Switch to Chrome
3. Navigate to the correct Gem
4. Paste (Ctrl+V)
5. Wait for Gemini to finish
6. Select all (Ctrl+A)
7. Copy (Ctrl+C)
8. Switch back to VS Code

**⚠️ GAP-006 — NO GUIDANCE ON WHICH GEM CONVERSATION TO USE**

The proxy console says: `1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C`

But it does NOT specify:
- Whether to use the **same Gemini conversation** (to maintain history) or start a new one
- What happens if the human accidentally starts a new conversation (losing history)
- Whether the Gem maintains conversation history between proxy requests

**Critical issue:** The proxy transmits the **full conversation history** in the clipboard (via `_format_prompt()`). This means:
- If the human uses the **same Gemini conversation**, Gemini sees the history **twice** (once from its own memory, once from the clipboard)
- If the human uses a **new Gemini conversation** each time, the history is correctly provided via clipboard

**This is a fundamental ambiguity in the design.** The correct behavior is to use a **new conversation each time** (or clear the existing one), but this is not documented anywhere in DOC2, DOC4, or DOC5.

**Severity:** HIGH — using the wrong conversation mode causes history duplication, leading to confused Gemini responses.

---

### UC-008 — Developer implementing a User Story (PROMPT 4.3) — long agentic loop

**Scenario:** Developer persona implements US-001. Typical agentic loop:
1. Read 3 Memory Bank files
2. Read sprint backlog
3. Create 3–5 source files
4. Run tests
5. Fix bugs (2–3 iterations)
6. Update Memory Bank
7. Git commit

**Estimated human interventions: 15–25 copy-paste cycles**
**Estimated elapsed time: 15–25 × 45s = 11–19 minutes of active human attention**

**⚠️ GAP-007 — COGNITIVE LOAD AND ATTENTION FATIGUE**

The proxy design assumes the human is **always present and attentive**. For a complex Developer task:
- 20+ copy-paste cycles over 15+ minutes
- Each cycle requires switching between VS Code and Chrome
- The human must NOT do anything else (no other copy-paste operations)
- The human must recognize when Gemini has finished generating (vs. still typing)

**This is fundamentally different from the Claude API path**, where the human can:
- Start a task and walk away
- Come back to find the task completed
- Work on something else in parallel

**Severity:** MEDIUM-HIGH — not a technical failure, but a significant UX degradation that makes the proxy path impractical for long tasks.

**Claude API comparison:** Claude API is fully autonomous — zero human interventions for a 20-step task.

---

### UC-009 — QA Engineer running tests (PROMPT 4.4)

**Scenario:** QA Engineer runs `pytest` and reports results.

**Simulation:**
1. Agent sends `<execute_command><command>pytest</command></execute_command>`
2. Roo Code executes pytest → output returned as user message
3. Proxy copies history + pytest output to clipboard
4. Human pastes into Gem
5. Gemini analyzes output and writes test report

**Specific issue:** pytest output can be very long (hundreds of lines for a large test suite).

**Clipboard content at step 4:**
```
[USER]
Lis docs/sprints/sprint-001/SPR-001-001-sprint-backlog.md...

---

[ASSISTANT]
<execute_command><command>pytest</command></execute_command>

---

[USER]
[Command output]
============================= test session starts ==============================
...
(500 lines of pytest output)
...
============================== 500 passed in 12.34s ============================
```

**Total clipboard size: ~20,000+ chars for a medium test suite**

**Verdict:** ✅ WORKS technically, but the clipboard size is large. Gemini Web UI should handle it, but the human experience is poor.

---

### UC-010 — Session startup (VÉRIFIER→CRÉER→LIRE→AGIR sequence)

**Scenario:** Human starts a new Roo Code session. The `.clinerules` REGLE 1 forces the agent to read `activeContext.md` and `progress.md` before acting.

**Simulation:**
1. Human sends any prompt to Roo Code
2. Agent (following REGLE 1) first sends `<read_file><path>memory-bank/activeContext.md</path></read_file>`
3. Proxy copies to clipboard: `[USER]\n[original prompt]\n\n---\n\n[ASSISTANT]\n<read_file>...</read_file>`

**Wait — this is wrong.** The agent's `<read_file>` is an **action**, not a message. Roo Code executes it locally and injects the result back. The proxy only sees the **next LLM request** after Roo Code has already executed the read.

**Correct flow:**
1. Human sends prompt → Roo Code sends to proxy
2. Proxy copies to clipboard: `[USER]\n[original prompt]`
3. Human pastes → Gemini responds: `<read_file><path>memory-bank/activeContext.md</path></read_file>`
4. Proxy injects → Roo Code executes read → sends file content back to proxy
5. Proxy copies to clipboard: `[USER]\n[prompt]\n\n---\n\n[ASSISTANT]\n<read_file>...</read_file>\n\n---\n\n[USER]\n[file content]`
6. Human pastes → Gemini responds: `<read_file><path>memory-bank/progress.md</path></read_file>`
7. Proxy injects → Roo Code reads → sends back
8. Human pastes → Gemini responds with actual action

**Total human interventions just for session startup: 3 copy-paste cycles before any real work begins**

**Verdict:** ✅ WORKS but adds 3 mandatory copy-paste cycles to every session start. For a 5-minute task, this overhead is significant.

---

### UC-011 — Error recovery (agent produces wrong output, human needs to correct)

**Scenario:** Gemini produces a response with a syntax error in the XML (e.g., unclosed tag).

**Example bad response:**
```xml
<write_to_file>
<path>src/app.py</path>
<content>
def hello():
    print("Hello")
</content>
<!-- missing </write_to_file> -->
```

**Proxy behavior:**
- `_validate_response()` checks for `<write_to_file>` → found → no warning ✅
- Proxy injects the malformed XML into Roo Code
- Roo Code tries to parse → **XML parsing error**
- Roo Code sends error back to proxy as next user message
- Proxy copies error to clipboard
- Human pastes → Gemini sees the error and corrects

**Verdict:** ✅ WORKS — the error recovery loop functions, but requires 2 additional human copy-paste cycles.

---

### UC-012 — Concurrent clipboard usage (human uses clipboard for other tasks)

**Scenario:** While waiting for Gemini to respond, the human copies something else (e.g., a URL from a browser tab).

**Proxy behavior:**
```python
current = pyperclip.paste()
if _hash(current) != initial_hash:
    # Triggered by the URL copy, not Gemini response
    return current  # Returns the URL as the "LLM response"
```

**This is GAP-005 again, but from a different angle.** The proxy has no way to distinguish:
- A legitimate Gemini response (XML with tool calls)
- An accidental clipboard overwrite (URL, text, file path)

**The only protection is the non-blocking XML validation warning.** But the response is still injected into Roo Code.

**Severity:** HIGH — this is a real operational risk that will occur in practice.

---

## 3. Comparative Robustness Matrix

| Dimension | Claude API Path | Gemini Proxy Path | Gap |
| :--- | :---: | :---: | :--- |
| **Single-turn simple task** | ✅ Automatic | ✅ 1 human cycle | Acceptable |
| **Multi-turn iterative dialogue** | ✅ Automatic | ⚠️ N human cycles | Manageable |
| **Large file reads** | ✅ Transparent | ⚠️ Large clipboard | Degraded UX |
| **Boomerang Tasks** | ✅ Native | ❌ Broken | **BLOCKING** |
| **Timeout recovery** | ✅ No timeout | ⚠️ HTTP 408 undefined | Risk |
| **Accidental clipboard overwrite** | ✅ Impossible | ⚠️ Silent corruption | **HIGH RISK** |
| **Conversation history management** | ✅ Automatic | ⚠️ Ambiguous (new vs. same conv.) | **HIGH RISK** |
| **Cognitive load** | ✅ Zero | ⚠️ High (20+ cycles/task) | Significant |
| **Session startup overhead** | ✅ Zero | ⚠️ 3 mandatory cycles | Overhead |
| **Error recovery** | ✅ Automatic | ✅ Works (2 extra cycles) | Acceptable |
| **Long agentic loops (20+ steps)** | ✅ Fully autonomous | ⚠️ 20+ human interventions | Impractical |
| **Parallel tasks** | ✅ Possible | ❌ Impossible (clipboard conflict) | **BLOCKING** |
| **Unattended execution** | ✅ Yes | ❌ No | Fundamental difference |

---

## 4. Critical Gaps — Detailed Analysis

### GAP-001 — Clipboard Size Explosion (MEDIUM)
**Root cause:** The proxy transmits the full conversation history at every turn. No truncation or summarization.  
**Impact:** Clipboard becomes unwieldy for long sessions (>10 turns with file reads).  
**Fix:** Implement a `MAX_HISTORY_CHARS` limit with truncation of oldest messages (keep last N turns).

### GAP-002 — Large File Content in Clipboard (HIGH)
**Root cause:** Roo Code injects full file contents as user messages. No size limit.  
**Impact:** A single large file read can add 10,000–50,000 chars to the clipboard.  
**Fix:** Implement file content truncation in `_clean_content()` with a `[TRUNCATED - {N} chars omitted]` marker.

### GAP-003 — Boomerang Tasks Broken (CRITICAL)
**Root cause:** The proxy is a single-endpoint server. Multiple concurrent Roo Code instances share the same clipboard channel.  
**Impact:** Boomerang Tasks (REQ-1.4) are completely non-functional in proxy mode.  
**Fix:** Document this as an explicit limitation. Add a warning in the proxy console when `<new_task>` is detected in a response.

### GAP-004 — HTTP 408 Timeout Recovery Undefined (HIGH)
**Root cause:** The proxy returns HTTP 408 on timeout, but Roo Code's behavior on 408 is not tested or documented.  
**Impact:** Timeout may cause silent task failure or confusing retry behavior.  
**Fix:** Test Roo Code's behavior on HTTP 408. Document the recovery procedure in DOC5 section 9.6.

### GAP-005 — Accidental Clipboard Overwrite (HIGH)
**Root cause:** The proxy detects ANY clipboard change as a valid response. No content validation beyond XML tag presence.  
**Impact:** Accidental clipboard operations silently corrupt the LLM response.  
**Fix:** Add a minimum content length check (e.g., `len(current) > 20`) and optionally a "confirm injection" step for responses without XML tags.

### GAP-006 — Gemini Conversation Mode Ambiguity (HIGH)
**Root cause:** The design does not specify whether the human should use a new Gemini conversation or continue an existing one.  
**Impact:** Using the same conversation causes history duplication (proxy sends history + Gemini remembers history). Using a new conversation is correct but not documented.  
**Fix:** Add explicit instruction in the proxy console: `"IMPORTANT: Toujours utiliser une NOUVELLE conversation Gemini (ou effacer l'historique)"`. Document in DOC4 and DOC5.

### GAP-007 — Cognitive Load and Attention Fatigue (MEDIUM-HIGH)
**Root cause:** The proxy requires continuous human attention for every LLM request. No batching, no queuing.  
**Impact:** Long tasks (20+ steps) require 15–25 minutes of active human attention with no ability to multitask.  
**Fix:** This is a fundamental architectural constraint of the clipboard-based approach. Mitigate by documenting "task chunking" strategies in DOC5 — break long tasks into smaller prompts that require fewer LLM turns.

---

## 5. Proxy Code Review — Specific Issues

### Issue P-001 — `_format_prompt()` produces duplicate history in Gemini

```python
def _format_prompt(messages: List[MessageContent]) -> str:
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if not content.strip():
            continue
        if msg.role == "system":
            if USE_GEM_MODE:
                continue
        elif msg.role == "user":
            parts.append("[USER]\n" + content)
        elif msg.role == "assistant":
            parts.append("[ASSISTANT]\n" + content)
    return "\n\n---\n\n".join(parts)
```

**Problem:** This correctly formats the full history. But if the human uses the **same Gemini conversation** (not a new one), Gemini already has the previous turns in its memory. The clipboard then provides the history **again**, causing Gemini to see:
- Its own memory: `[Turn 1][Turn 2][Turn 3]`
- The clipboard: `[Turn 1][Turn 2][Turn 3][Turn 4 — new request]`

Gemini will process the history twice, potentially producing confused responses.

**Fix:** The proxy console must explicitly instruct the human to use a **new conversation** each time, OR the proxy should only send the **last user message** (not the full history) and rely on the Gem's conversation memory. This is a design choice that needs to be made explicit.

### Issue P-002 — No request ID in console output

```python
print(f"[{ts}] PROMPT COPIE ! ACTION : 1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C")
```

**Problem:** If the human is slow and a second request arrives (e.g., Roo Code retries), the console shows two identical messages. The human cannot tell which clipboard content corresponds to which request.

**Fix:** Add a request counter: `[{ts}] REQUEST #{n} | PROMPT COPIE ! ...`

### Issue P-003 — `_wait_clipboard()` does not handle pyperclip exceptions

```python
async def _wait_clipboard(initial_hash: str, ts: str) -> str:
    start = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)
        current = pyperclip.paste()  # Can raise exception if clipboard is locked
        if _hash(current) != initial_hash:
            ...
```

**Problem:** `pyperclip.paste()` can raise exceptions on Windows if:
- The clipboard is locked by another application
- The clipboard contains non-text content (e.g., an image)
- Windows clipboard access is temporarily unavailable

**Fix:** Wrap in try/except:
```python
try:
    current = pyperclip.paste()
except Exception as e:
    print(f"[{ts}] AVERTISSEMENT: Erreur clipboard: {e}")
    continue
```

### Issue P-004 — SSE streaming sends full content in one chunk

```python
async def _stream_response(content: str, model: str) -> AsyncGenerator[str, None]:
    chunk = {..., "choices": [{"delta": {"role": "assistant", "content": content}, ...}]}