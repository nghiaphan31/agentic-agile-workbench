"""
submit_batch3_template.py
-------------------------
BATCH 3: Template Coherence + Implementation vs Documentation Audit

Submits 6 parallel requests to the Anthropic Batch API to audit:
1. Root .clinerules vs template/.clinerules (full sync check)
2. Root .roomodes vs template/.roomodes (persona sync check)
3. Root Modelfile vs template/Modelfile (system prompt sync check)
4. Root proxy.py vs template/proxy.py (proxy sync check)
5. src/calypso/ implementation vs DOC-2 Architecture Phase 2 description
6. memory-bank/ structure vs DOC-2 Architecture Section 4 description

Usage (from workspace root):
    python plans/batch-full-audit/submit_batch3_template.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to plans/batch-full-audit/batch_id_3_template.txt
"""

import os
import pathlib
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
TEMPERATURE = 0.3
BATCH_DIR = pathlib.Path("plans/batch-full-audit")
BATCH_ID_FILE = BATCH_DIR / "batch_id_3_template.txt"

# ---------------------------------------------------------------------------
# Helper: load file with error checking
# ---------------------------------------------------------------------------
def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        return f"[FILE NOT FOUND: {path}]"
    return p.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Load all template/implementation files
# ---------------------------------------------------------------------------
print("Loading template and implementation files...")

# Template vs Root pairs
clinerules_root = load(".clinerules")
clinerules_template = load("template/.clinerules")
roomodes_root = load(".roomodes")
roomodes_template = load("template/.roomodes")
modelfile_root = load("Modelfile")
modelfile_template = load("template/Modelfile")
proxy_root = load("proxy.py")
proxy_template = load("template/proxy.py")

# Architecture document
doc2_v22 = load("docs/releases/v2.2/DOC-2-v2.2-Architecture.md")

# Memory bank structure
memory_bank_files = {}
for f in pathlib.Path("memory-bank").glob("**/*.md"):
    rel = f.relative_to("memory-bank")
    memory_bank_files[str(rel)] = load(str(f))

# Calypso scripts
calypso_files = {}
calypso_dir = pathlib.Path("src/calypso")
if calypso_dir.exists():
    for f in sorted(calypso_dir.glob("*.py")):
        calypso_files[f.name] = load(str(f))

print(f"  .clinerules (root)    : {len(clinerules_root):,} chars")
print(f"  .clinerules (template): {len(clinerules_template):,} chars")
print(f"  .roomodes (root)      : {len(roomodes_root):,} chars")
print(f"  .roomodes (template)  : {len(roomodes_template):,} chars")
print(f"  Modelfile (root)      : {len(modelfile_root):,} chars")
print(f"  Modelfile (template)  : {len(modelfile_template):,} chars")
print(f"  proxy.py (root)       : {len(proxy_root):,} chars")
print(f"  proxy.py (template)   : {len(proxy_template):,} chars")
print(f"  DOC-2 v2.2            : {len(doc2_v22):,} chars")
print(f"  memory-bank/ files    : {len(memory_bank_files)} files")
print(f"  src/calypso/ files    : {len(calypso_files)} files")

# ---------------------------------------------------------------------------
# Build shared context
# ---------------------------------------------------------------------------
MEMORY_BANK_CONTEXT = "\n\n".join([
    f"=== memory-bank/{rel} ===\n\n{content}"
    for rel, content in sorted(memory_bank_files.items())
])

CALYPSO_CONTEXT = "\n\n".join([
    f"=== src/calypso/{name} ({len(content):,} chars) ===\n\n{content}"
    for name, content in sorted(calypso_files.items())
]) if calypso_files else "[No calypso files found]"

TEMPLATE_CONTEXT = f"""
=== Root .clinerules ===
First 50 chars: {clinerules_root[:50]!r}
{clinerules_root}

=== template/.clinerules ===
First 50 chars: {clinerules_template[:50]!r}
{clinerules_template}

=== Root .roomodes ===

{roomodes_root}

=== template/.roomodes ===

{roomodes_template}

=== Root Modelfile ===

{modelfile_root}

=== template/Modelfile ===

{modelfile_template}

=== Root proxy.py ===

{proxy_root}

=== template/proxy.py ===

{proxy_template}
"""

IMPLEMENTATION_CONTEXT = f"""
=== DOC-2 v2.2 Architecture (current release) ===

{doc2_v22}

=== memory-bank/ files ===

{MEMORY_BANK_CONTEXT}

=== src/calypso/ scripts ===

{CALYPSO_CONTEXT}
"""

# ---------------------------------------------------------------------------
# Request 1: .clinerules root vs template (full sync)
# ---------------------------------------------------------------------------
SYSTEM_TMPL_CLINERULES = """You are a Senior DevOps Architect specializing in infrastructure-as-code,
template management, and configuration drift detection.

Your task: Perform a DEEP sync audit between .clinerules (root) and template/.clinerules.

IMPORTANT CONTEXT:
- template/.clinerules is the TEMPLATE that gets copied into new application projects
- .clinerules at the root is the DEPLOYED INSTANCE for the workbench itself
- The template should be a CLEAN COPY of the root (modulo project-specific placeholders)

Check for these specific things:
1. Are the two files BYTE-IDENTICAL? If not, what are the differences?
2. Does .clinerules (root) have a BOM? Does template/.clinerules have a BOM? (Neither should)
3. Are em-dashes (—) corrupted in either file?
4. Are all 10 RULES present in BOTH files?
5. Are the Memory Bank templates (activeContext.md, progress.md) at the bottom identical?
6. Are there any literal \\\\n backslash-n in RULE 10 (they should be real newlines)?
7. Are there project-specific placeholders that differ intentionally?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing sync status

## 2. Byte-Level Diff
- Files are BYTE-IDENTICAL: Yes/No
- If not, list ALL differences with line numbers

## 3. Encoding Anomalies
| File | BOM | Em-dash Corruption | Literal \\\\n |
|---|---|---|---|
| .clinerules (root) | Yes/No | Yes/No | Yes/No |
| template/.clinerules | Yes/No | Yes/No | Yes/No |

## 4. Rule Completeness
| Rule | In Root | In Template | Identical |
|---|---|---|---|
| RULE 1 | Yes/No | Yes/No | Yes/No |
| ... | ... | ... | ... |
| RULE 10 | Yes/No | Yes/No | Yes/No |

## 5. Intentional vs Accidental Differences
For each difference found, classify as INTENTIONAL (project-specific) or ACCIDENTAL (drift)

## 6. Prioritized Remediation
- **P0 (Critical):** Accidental drift that could break new projects
- **P1 (Important):** Encoding issues that cause display problems
- **P2 (Nice to have):** Whitespace differences

## 7. Verdict
[SYNCHRONIZED] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_TMPL_CLINERULES = f"""Please audit .clinerules (root) vs template/.clinerules deep sync.

{TEMPLATE_CONTEXT}

Focus on:
1. Byte-level comparison
2. Encoding issues (BOM, em-dash)
3. Rule completeness in both files
4. Classifying differences as intentional vs accidental"""

# ---------------------------------------------------------------------------
# Request 2: .roomodes root vs template (persona sync)
# ---------------------------------------------------------------------------
SYSTEM_TMPL_ROOMODES = """You are a Senior Platform Architect and Roo Code expert specializing in
.roomodes configuration and multi-environment deployment.

Your task: Perform a DEEP sync audit between .roomodes (root) and template/.roomodes.

IMPORTANT CONTEXT:
- template/.roomodes is the TEMPLATE that gets copied into new application projects
- .roomodes at the root is the DEPLOYED INSTANCE for the workbench itself
- They should be IDENTICAL (no project-specific differences for personas)

Check for these specific things:
1. Are the two files BYTE-IDENTICAL? If not, what are the differences?
2. Are all 4 personas (product-owner, scrum-master, developer, qa-engineer) present in both?
3. Are the roleDefinition strings identical for each persona?
4. Are the groups/RBAC permissions identical for each persona?
5. Is the JSON syntax valid in both files?
6. Are there any project-specific values that should differ?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing sync status

## 2. Byte-Level Diff
- Files are BYTE-IDENTICAL: Yes/No
- If not, list ALL differences with line numbers

## 3. Persona Completeness
| Persona | In Root | In Template | roleDefinition Match |
|---|---|---|---|
| product-owner | Yes/No | Yes/No | Yes/No |
| scrum-master | Yes/No | Yes/No | Yes/No |
| developer | Yes/No | Yes/No | Yes/No |
| qa-engineer | Yes/No | Yes/No | Yes/No |

## 4. JSON Validity
| File | Valid JSON? | Errors |
|---|---|---|
| .roomodes (root) | Yes/No | ... |
| template/.roomodes | Yes/No | ... |

## 5. RBAC Consistency
- Are groups/permissions identical between root and template?

## 6. Prioritized Remediation
- **P0 (Critical):** Persona missing or roleDefinition mismatch
- **P1 (Important):** JSON syntax error or RBAC drift
- **P2 (Nice to have):** Whitespace differences

## 7. Verdict
[SYNCHRONIZED] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_TMPL_ROOMODES = f"""Please audit .roomodes (root) vs template/.roomodes deep sync.

{TEMPLATE_CONTEXT}

Focus on:
1. Byte-level comparison
2. Persona completeness and roleDefinition matching
3. JSON validity
4. RBAC consistency"""

# ---------------------------------------------------------------------------
# Request 3: Modelfile root vs template (system prompt sync)
# ---------------------------------------------------------------------------
SYSTEM_TMPL_MODELFILE = """You are a Senior Ollama/LLM Infrastructure Architect specializing in
Modelfile management and system prompt deployment.

Your task: Perform a DEEP sync audit between Modelfile (root) and template/Modelfile.

IMPORTANT CONTEXT:
- template/Modelfile is the TEMPLATE that gets copied into new application projects
- Modelfile at the root is the DEPLOYED INSTANCE for the workbench itself
- They should be IDENTICAL (system prompts, parameters, base model)

Check for these specific things:
1. Are the two files BYTE-IDENTICAL? If not, what are the differences?
2. Is the SYSTEM prompt content identical?
3. Are the PARAMETER values identical (temperature, num_ctx, etc.)?
4. Is the FROM (base model) identical?
5. Are there any project-specific values that should differ?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing sync status

## 2. Byte-Level Diff
- Files are BYTE-IDENTICAL: Yes/No
- If not, list ALL differences

## 3. SYSTEM Prompt Comparison
| Aspect | Root | Template | Match |
|---|---|---|---|
| SYSTEM block present | Yes/No | Yes/No | Yes/No |
| SYSTEM content identical | Yes/No | Yes/No | Yes/No |

## 4. PARAMETER Comparison
| Parameter | Root | Template | Match |
|---|---|---|---|
| temperature | ... | ... | Yes/No |
| num_ctx | ... | ... | Yes/No |
| other params... | ... | ... | Yes/No |

## 5. FROM Comparison
| Aspect | Root | Template | Match |
|---|---|---|---|
| base model | ... | ... | Yes/No |

## 6. Prioritized Remediation
- **P0 (Critical):** SYSTEM prompt or FROM mismatch
- **P1 (Important):** Parameter drift
- **P2 (Nice to have):** Whitespace differences

## 7. Verdict
[SYNCHRONIZED] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_TMPL_MODELFILE = f"""Please audit Modelfile (root) vs template/Modelfile deep sync.

{TEMPLATE_CONTEXT}

Focus on:
1. SYSTEM prompt content comparison
2. PARAMETER value comparison
3. FROM (base model) comparison
4. Classifying differences as intentional vs accidental"""

# ---------------------------------------------------------------------------
# Request 4: proxy.py root vs template
# ---------------------------------------------------------------------------
SYSTEM_TMPL_PROXY = """You are a Senior Python Backend Engineer specializing in API proxy servers,
FastAPI, and SSE (Server-Sent Events) implementation.

Your task: Perform a DEEP sync audit between proxy.py (root) and template/proxy.py.

IMPORTANT CONTEXT:
- template/proxy.py is the TEMPLATE that gets copied into new application projects
- proxy.py at the root is the DEPLOYED INSTANCE for the workbench itself
- They should be NEARLY IDENTICAL (proxy functionality should not vary by project)

Check for these specific things:
1. Are the two files BYTE-IDENTICAL? If not, what are the differences?
2. Is the API route structure identical (/chat, /models, etc.)?
3. Is the SSE implementation identical?
4. Is the CORS configuration identical?
5. Are there any project-specific values that SHOULD differ (ports, API keys)?
6. Is the version comment consistent?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing sync status

## 2. Byte-Level Diff
- Files are BYTE-IDENTICAL: Yes/No
- If not, list ALL differences with context

## 3. Functional Comparison
| Aspect | Root | Template | Match |
|---|---|---|---|
| API routes | ... | ... | Yes/No |
| SSE implementation | ... | ... | Yes/No |
| CORS config | ... | ... | Yes/No |
| Error handling | ... | ... | Yes/No |

## 4. Project-Specific Values
Are there values that SHOULD differ between root and template (e.g., ports)?

## 5. Prioritized Remediation
- **P0 (Critical):** Functional difference that breaks the proxy
- **P1 (Important):** Security or performance drift
- **P2 (Nice to have):** Version comment mismatch

## 6. Verdict
[SYNCHRONIZED] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_TMPL_PROXY = f"""Please audit proxy.py (root) vs template/proxy.py deep sync.

{TEMPLATE_CONTEXT}

Focus on:
1. Functional comparison (routes, SSE, CORS)
2. Identifying project-specific differences
3. Security implications of any drift"""

# ---------------------------------------------------------------------------
# Request 5: Calypso implementation vs DOC-2 Architecture Phase 2
# ---------------------------------------------------------------------------
SYSTEM_IMPL_CALYPSO = """You are a Senior Software Architect and Platform Engineer specializing in
AI/LLM orchestration pipelines, MCP (Model Context Protocol), and multi-agent systems.

Your task: Audit whether the src/calypso/ implementation matches the Phase 2 description in DOC-2 Architecture.

IMPORTANT CONTEXT:
- DOC-2-v2.2-Architecture.md describes the Calypso orchestration in Phase 2
- src/calypso/ contains the actual Python implementation scripts
- These should be consistent: what DOC-2 describes SHOULD be implemented

Check for these specific things:
1. Does the Calypso directory structure match what DOC-2 describes?
2. Are the phases (phase2, phase3, phase4) implemented as described?
3. Does the FastMCP server (fastmcp_server.py) exist and match the architecture?
4. Does the triage dashboard (triage_dashboard.py) exist and match the architecture?
5. Are the JSON schemas in src/calypso/schemas/ consistent with DOC-2?
6. Are there discrepancies between what DOC-2 describes and what is actually implemented?
7. Is there implementation in calypso that DOC-2 does NOT describe?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing implementation vs architecture consistency

## 2. Phase Coverage
| Phase (from DOC-2) | DOC-2 Section | Implementation File | Implemented? |
|---|---|---|---|
| Phase 2 Orchestration | Section X.Y | orchestrator_phase2.py | Yes/No |
| Phase 3 Expert Reports | Section X.Y | orchestrator_phase3.py | Yes/No |
| Phase 4 Backlog Items | Section X.Y | orchestrator_phase4.py | Yes/No |

## 3. Missing Components
What does DOC-2 describe that is NOT implemented in src/calypso/?

## 4. Orphaned Implementation
What is implemented in src/calypso/ that DOC-2 does NOT describe?

## 5. JSON Schema Consistency
Are the schemas in src/calypso/schemas/ consistent with DOC-2 data contracts?

## 6. Prioritized Remediation
- **P0 (Critical):** Phase described in DOC-2 but not implemented
- **P1 (Important):** Significant implementation drift from architecture
- **P2 (Nice to have):** Minor schema inconsistencies

## 7. Verdict
[CONSISTENT] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_IMPL_CALYPSO = f"""Please audit src/calypso/ implementation vs DOC-2 Architecture Phase 2.

{IMPLEMENTATION_CONTEXT}

Focus on:
1. Checking each phase (phase2, phase3, phase4) against DOC-2 description
2. Identifying missing components (in DOC-2 but not implemented)
3. Identifying orphaned implementation (in code but not in DOC-2)
4. Verifying JSON schema consistency"""

# ---------------------------------------------------------------------------
# Request 6: memory-bank/ structure vs DOC-2 Architecture Section 4
# ---------------------------------------------------------------------------
SYSTEM_IMPL_MEMORY = """You are a Senior Technical Architect and Knowledge Management Specialist
specializing in AI memory systems, Hot/Cold memory architecture, and documentation structures.

Your task: Audit whether the memory-bank/ directory structure matches the DOC-2 Architecture Section 4.

IMPORTANT CONTEXT:
- DOC-2-v2.2-Architecture.md Section 4 describes the Memory Bank architecture
- memory-bank/ at the root contains the actual working memory files
- memory-bank/hot-context/ contains active working memory
- memory-bank/archive-cold/ contains archived/stale memory
- These should be consistent: what DOC-2 describes SHOULD exist

Check for these specific things:
1. Does the memory-bank/ directory structure match what DOC-2 describes?
2. Are all files listed in DOC-2 present in the actual memory-bank/?
3. Are the hot-context/ files (activeContext.md, progress.md, etc.) consistent with DOC-2?
4. Does the archive-cold/ directory exist with the expected structure?
5. Are there files in memory-bank/ that DOC-2 does NOT describe?
6. Are there files described in DOC-2 that do NOT exist in memory-bank/?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing memory structure vs architecture

## 2. Directory Structure Comparison
| DOC-2 Describes | File/Dir Exists? | Path |
|---|---|---|
| hot-context/activeContext.md | Yes/No | memory-bank/hot-context/... |
| hot-context/progress.md | Yes/No | memory-bank/hot-context/... |
| hot-context/productContext.md | Yes/No | memory-bank/hot-context/... |
| hot-context/systemPatterns.md | Yes/No | memory-bank/hot-context/... |
| hot-context/techContext.md | Yes/No | memory-bank/hot-context/... |
| hot-context/decisionLog.md | Yes/No | memory-bank/hot-context/... |
| archive-cold/... | Yes/No | memory-bank/archive-cold/... |

## 3. Missing from DOC-2
What exists in memory-bank/ that is NOT described in DOC-2?

## 4. Missing from Implementation
What does DOC-2 describe that does NOT exist in memory-bank/?

## 5. Hot/Cold Boundary
Is the RULE 9 HOT/COLD boundary correctly described in DOC-2 and implemented in .clinerules?

## 6. Prioritized Remediation
- **P0 (Critical):** File described in DOC-2 but missing from memory-bank/
- **P1 (Important):** Significant structure drift
- **P2 (Nice to have):** Minor file inconsistencies

## 7. Verdict
[CONSISTENT] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_IMPL_MEMORY = f"""Please audit memory-bank/ structure vs DOC-2 Architecture Section 4.

{IMPLEMENTATION_CONTEXT}

Focus on:
1. Checking each file/directory in memory-bank/ against DOC-2 description
2. Verifying hot-context/ file presence and consistency
3. Checking archive-cold/ structure
4. Validating HOT/COLD boundary implementation (.clinerules RULE 9 vs DOC-2)"""

# ---------------------------------------------------------------------------
# Build the batch requests
# ---------------------------------------------------------------------------
REVIEWS = [
    {
        "custom_id": "tmpl-clinerules",
        "system": SYSTEM_TMPL_CLINERULES,
        "user_message": USER_TMPL_CLINERULES,
    },
    {
        "custom_id": "tmpl-roomodes",
        "system": SYSTEM_TMPL_ROOMODES,
        "user_message": USER_TMPL_ROOMODES,
    },
    {
        "custom_id": "tmpl-modelfile",
        "system": SYSTEM_TMPL_MODELFILE,
        "user_message": USER_TMPL_MODELFILE,
    },
    {
        "custom_id": "tmpl-proxy",
        "system": SYSTEM_TMPL_PROXY,
        "user_message": USER_TMPL_PROXY,
    },
    {
        "custom_id": "impl-calypso",
        "system": SYSTEM_IMPL_CALYPSO,
        "user_message": USER_IMPL_CALYPSO,
    },
    {
        "custom_id": "impl-memory",
        "system": SYSTEM_IMPL_MEMORY,
        "user_message": USER_IMPL_MEMORY,
    },
]

requests = []
for review in REVIEWS:
    requests.append(
        anthropic.types.messages.batch_create_params.Request(
            custom_id=review["custom_id"],
            params=anthropic.types.messages.batch_create_params.MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=review["system"],
                messages=[
                    {"role": "user", "content": review["user_message"]}
                ],
            ),
        )
    )

# ---------------------------------------------------------------------------
# Submit the batch
# ---------------------------------------------------------------------------
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY environment variable is not set.\n"
        "Set it with: $env:ANTHROPIC_API_KEY = 'sk-ant-...'"
    )

client = anthropic.Anthropic(api_key=api_key)

print(f"\nSubmitting BATCH 3: Template + Implementation Audit with {len(requests)} requests to model {MODEL}...")
print("  Request 1: tmpl-clinerules (.clinerules root vs template)")
print("  Request 2: tmpl-roomodes (.roomodes root vs template)")
print("  Request 3: tmpl-modelfile (Modelfile root vs template)")
print("  Request 4: tmpl-proxy (proxy.py root vs template)")
print("  Request 5: impl-calypso (src/calypso/ vs DOC-2 Phase 2)")
print("  Request 6: impl-memory (memory-bank/ vs DOC-2 Section 4)")

batch = client.messages.batches.create(requests=requests)

print(f"\n[OK] Batch submitted successfully!")
print(f"   Batch ID  : {batch.id}")
print(f"   Status    : {batch.processing_status}")
print(f"   Created at: {batch.created_at}")
print(f"   Expires at: {batch.expires_at}")
print(f"\nSaving batch_id to {BATCH_ID_FILE}...")

BATCH_DIR.mkdir(parents=True, exist_ok=True)
BATCH_ID_FILE.write_text(batch.id, encoding="utf-8")

print(f"[OK] batch_id saved.")
print(f"\nRun the following command to retrieve results (after 1-4 hours):")
print(f"   python plans/batch-full-audit/retrieve_batch3.py")
