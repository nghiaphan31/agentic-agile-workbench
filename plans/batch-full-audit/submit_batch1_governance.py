"""
submit_batch1_governance.py
----------------------------
BATCH 1: Governance Coherence Audit

Submits 4 parallel requests to the Anthropic Batch API to audit:
1. SP-002 vs .clinerules (rule definitions consistency)
2. SP-003..006 vs .roomodes (persona definitions consistency)
3. prompts/README.md vs actual SP-001..010 files (registry integrity)
4. .clinerules vs template/.clinerules (template vs root sync)

Usage (from workspace root):
    python plans/batch-full-audit/submit_batch1_governance.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to plans/batch-full-audit/batch_id_1_governance.txt
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
BATCH_ID_FILE = BATCH_DIR / "batch_id_1_governance.txt"

# ---------------------------------------------------------------------------
# Helper: load file with error checking
# ---------------------------------------------------------------------------
def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}\n"
            "Run this script from the workspace root directory."
        )
    return p.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Load all governance files
# ---------------------------------------------------------------------------
print("Loading governance files...")

clinerules_root = load(".clinerules")
clinerules_template = load("template/.clinerules")
roomodes_root = load(".roomodes")
prompts_readme = load("prompts/README.md")

# Load SP-001 through SP-010
sp_files = {}
for i in range(1, 11):
    matches = list(pathlib.Path("prompts").glob(f"SP-{i:03d}-*.md"))
    if matches:
        sp_files[f"SP-{i:03d}"] = load(str(matches[0]))
    else:
        sp_files[f"SP-{i:03d}"] = f"[FILE NOT FOUND: SP-{i:03d}]"

print(f"  .clinerules (root)     : {len(clinerules_root):,} chars")
print(f"  .clinerules (template) : {len(clinerules_template):,} chars")
print(f"  .roomodes (root)      : {len(roomodes_root):,} chars")
print(f"  prompts/README.md      : {len(prompts_readme):,} chars")
for sp_id, content in sp_files.items():
    print(f"  {sp_id}                 : {len(content):,} chars")

# ---------------------------------------------------------------------------
# Build the shared context block (injected into every request)
# ---------------------------------------------------------------------------
SHARED_CONTEXT = f"""
=== FILE: .clinerules (ROOT) ===
First 50 chars (hex check for BOM): {clinerules_root[:50]!r}
First line: {clinerules_root.split(chr(10))[0]!r}
Total lines: {clinerules_root.count(chr(10))}

{clinerules_root}

=== FILE: .roomodes (ROOT) ===

{roomodes_root}

=== FILE: template/.clinerules ===

{clinerules_template}

=== FILE: prompts/README.md ===

{prompts_readme}
"""

# Add each SP file to context
for sp_id, content in sp_files.items():
    SHARED_CONTEXT += f"""
=== FILE: {sp_id} ===

{content}
"""

# ---------------------------------------------------------------------------
# Request 1: SP-002 vs .clinerules coherence
# ---------------------------------------------------------------------------
SYSTEM_SP_CLINERULES = """You are a Senior Technical Writer and Documentation Architect with 15 years of experience
auditing technical documentation coherence, identifying silent corruption, and verifying that
canonical sources match their deployed counterparts.

Your task: Audit whether the deployed .clinerules (root) matches what SP-002 prescribes.

IMPORTANT CONTEXT:
- SP-002 (prompts/SP-002-clinerules-global.md) is the CANONICAL SOURCE for .clinerules
- The .clinerules file at the root is the DEPLOYED TARGET
- SP-002 contains BOTH the metadata/header AND the actual .clinerules content in a "Prompt Content" section

Check for these KNOWN ISSUES:
1. BOM (Byte Order Mark) at the start of .clinerules
2. Em-dash corruption: aGrment instead of —
3. Literal \\n backslash-n appearing as text instead of real newlines in RULE 10
4. Double-embedded content: SP-002 contains .clinerules TWICE (before and after the "---" separator)

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the coherence state

## 2. BOM and Encoding Check
- Does .clinerules have a BOM at the start?
- Are em-dashes (—) corrupted to aGrment or similar?
- Are there any other encoding anomalies?

## 3. Rule-by-Rule Comparison
For each RULE (RULE 1 through RULE 10):
- Does the deployed .clinerules match the SP-002 prescription?
- Are there any discrepancies in wording, formatting, or content?

## 4. Structural Anomalies
- Is SP-002 double-embedded? (contains .clinerules content twice)
- Are the Memory Bank templates at the bottom of SP-002 identical in both embeddings?

## 5. Known Issues Status
| Issue | Status | Evidence |
|---|---|---|
| BOM in .clinerules | FOUND / NOT FOUND | evidence |
| Em-dash corruption | FOUND / NOT FOUND | evidence |
| Literal \\\\n in RULE 10 | FOUND / NOT FOUND | evidence |
| Double embedding in SP-002 | FOUND / NOT FOUND | evidence |

## 6. Prioritized Remediation
- **P0 (Critical):** Encoding corruption that breaks parsing or display
- **P1 (Important):** Content mismatch between SP-002 and .clinerules
- **P2 (Nice to have):** Structural anomalies in SP-002

## 7. Verdict
[CONSISTENT] / [MINOR_ISSUES] / [MAJOR_INCONSISTENCIES]
Justify in 2-3 sentences."""

USER_SP_CLINERULES = f"""Please audit SP-002 vs .clinerules coherence.

{SHARED_CONTEXT}

Focus on:
1. Comparing the .clinerules content in SP-002's "Prompt Content" section with the deployed .clinerules
2. Checking for BOM, em-dash corruption, and literal \\\\n in RULE 10
3. Verifying all 10 RULES match between SP-002 and .clinerules
4. Identifying the double-embedding issue in SP-002 if present"""

# ---------------------------------------------------------------------------
# Request 2: SP-003..006 vs .roomodes coherence
# ---------------------------------------------------------------------------
SYSTEM_SP_ROOMODES = """You are a Senior Platform Architect and Roo Code expert with deep knowledge of
.roomodes configuration, persona system prompts, and role-based access control (RBAC) in AI agents.

Your task: Audit whether SP-003, SP-004, SP-005, and SP-006 (persona definitions) match the
deployed .roomodes file at the root.

IMPORTANT CONTEXT:
- SP-003..006 are the CANONICAL SOURCES for the 4 Agile personas
- .roomodes is the DEPLOYED TARGET (JSON file with persona configurations)
- SP-003 = product-owner, SP-004 = scrum-master, SP-005 = developer, SP-006 = qa-engineer

Check for these specific things:
1. Does each SP-NN roleDefinition match the corresponding entry in .roomodes.customModes[n].roleDefinition?
2. Are the groups/RBAC permissions consistent between each SP and .roomodes?
3. Does the prompts/README.md inventory correctly list all 4 persona SPs and their deployment targets?
4. Are there any JSON syntax errors in .roomodes?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the coherence state

## 2. Persona-by-Persona Comparison
For each persona (product-owner, scrum-master, developer, qa-engineer):
- Extract the roleDefinition from SP-NN
- Extract the roleDefinition from .roomodes.customModes[n]
- Compare them character-by-character
- Report ANY discrepancy (even whitespace)

## 3. RBAC/Groups Consistency
- Do the groups permissions in .roomodes match what each SP prescribes?
- Are there any additional or missing permissions?

## 4. prompts/README.md Inventory Check
- Does the README correctly list SP-003..006 with their .roomodes deployment targets?
- Are the target_field values accurate?

## 5. JSON Validity
- Is .roomodes valid JSON?
- Are there any trailing commas, missing quotes, or other JSON syntax errors?

## 6. Prioritized Remediation
- **P0 (Critical):** Role definition mismatch that would cause wrong agent behavior
- **P1 (Important):** RBAC discrepancy or README inventory error
- **P2 (Nice to have):** Whitespace-only differences

## 7. Verdict
[CONSISTENT] / [MINOR_ISSUES] / [MAJOR_INCONSISTENCIES]
Justify in 2-3 sentences."""

USER_SP_ROOMODES = f"""Please audit SP-003..006 vs .roomodes coherence.

{SHARED_CONTEXT}

Focus on:
1. Extracting the roleDefinition from each SP and comparing to .roomodes
2. Verifying the 4 customModes array order matches the SP order (SP-003=product-owner, etc.)
3. Checking prompts/README.md accuracy for SP-003..006
4. Validating .roomodes JSON syntax"""

# ---------------------------------------------------------------------------
# Request 3: prompts/README.md vs actual SP files (registry integrity)
# ---------------------------------------------------------------------------
SYSTEM_README_SP = """You are a Senior Documentation Architect specializing in maintaining single-source-of-truth
 registries and configuration management systems.

Your task: Audit whether prompts/README.md correctly reflects the actual state of the prompts/ directory.

IMPORTANT CONTEXT:
- prompts/README.md is the INVENTORY/REGISTRY of all system prompts
- SP-001 through SP-010 are the actual canonical prompt files
- The registry should match reality exactly

Check for these specific things:
1. Does the Prompt Inventory table list all 10 SP files (SP-001 through SP-010)?
2. Does each SP file actually exist in prompts/?
3. Are the deployment targets accurate?
4. Are the depends_on relationships accurate?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the registry integrity

## 2. File Existence Check
| SP ID | Listed in README | File Exists | Path |
|---|---|---|---|
| SP-001 | Yes/No | Yes/No | prompts/... |
| ... | ... | ... | ... |

## 3. Deployment Target Accuracy
For each SP that exists:
| SP ID | README Target | Match? |
|---|---|---|
| SP-001 | Modelfile | Yes/No |
| SP-002 | .clinerules | Yes/No |
| SP-003..006 | .roomodes | Yes/No |
| SP-007 | Gemini Gem | Yes/No |
| SP-008 | orchestrator_phase3.py | Yes/No |
| SP-009 | orchestrator_phase4.py | Yes/No |
| SP-010 | librarian_agent.py | Yes/No |

## 4. Orphaned Files
Are there any .md files in prompts/ that are NOT listed in the README inventory?

## 5. Missing from README
Are there any SP files that exist but are NOT listed in the README inventory?

## 6. Prioritized Remediation
- **P0 (Critical):** Missing files, wrong deployment targets
- **P1 (Important):** Orphaned files, missing from README
- **P2 (Nice to have):** Incomplete depends_on relationships

## 7. Verdict
[CONSISTENT] / [MINOR_ISSUES] / [MAJOR_INCONSISTENCIES]
Justify in 2-3 sentences."""

USER_README_SP = f"""Please audit prompts/README.md vs actual SP files (registry integrity).

{SHARED_CONTEXT}

Focus on:
1. Comparing the Prompt Inventory table against actual files in prompts/
2. Verifying deployment target accuracy for each SP
3. Checking for orphaned or missing SP files"""

# ---------------------------------------------------------------------------
# Request 4: .clinerules vs template/.clinerules (template-root sync)
# ---------------------------------------------------------------------------
SYSTEM_TEMPLATE_ROOT = """You are a Senior DevOps Architect specializing in infrastructure-as-code,
template management, and configuration drift detection.

Your task: Audit whether .clinerules (root) and template/.clinerules are properly synchronized.

IMPORTANT CONTEXT:
- template/.clinerules is the TEMPLATE that gets copied into new application projects
- .clinerules at the root is the DEPLOYED INSTANCE for the workbench itself
- The template should be identical to the root (they are the same protocol)

Check for these specific things:
1. Are the two .clinerules files identical in content?
2. If not identical, what are the differences and are they justified?
3. Does template/.clinerules have the BOM issue?
4. Are all 10 RULES present in both files?
5. Are the Memory Bank templates at the bottom identical?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the sync state

## 2. Byte-Level Comparison
- Are the files identical? (Yes/No)
- If not, report the line-by-line differences

## 3. Content Comparison by Section
For each RULE (1-10) and the Memory Bank templates:
| Section | Root | Template | Match? | Notes |
|---|---|---|---|---|
| RULE 1 | present/absent | present/absent | Yes/No | ... |
| ... | ... | ... | ... | ... |

## 4. Encoding Anomalies
| File | BOM | Other Encoding Issues |
|---|---|---|
| .clinerules (root) | Yes/No | ... |
| template/.clinerules | Yes/No | ... |

## 5. Justified Differences
Are any differences intentional (project-specific) vs accidental (drift)?

## 6. Prioritized Remediation
- **P0 (Critical):** Accidental drift that breaks functionality
- **P1 (Important):** Encoding differences that cause display issues
- **P2 (Nice to have):** Whitespace or comment-only differences

## 7. Verdict
[SYNCHRONIZED] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_TEMPLATE_ROOT = f"""Please audit .clinerules (root) vs template/.clinerules sync.

{SHARED_CONTEXT}

Focus on:
1. Comparing the two files line-by-line
2. Identifying any differences and classifying them as intentional vs accidental
3. Checking encoding issues (BOM, em-dash corruption) in both files
4. Verifying all 10 RULES exist in both"""

# ---------------------------------------------------------------------------
# Build the batch requests
# ---------------------------------------------------------------------------
REVIEWS = [
    {
        "custom_id": "gov-sp-clinerules",
        "system": SYSTEM_SP_CLINERULES,
        "user_message": USER_SP_CLINERULES,
    },
    {
        "custom_id": "gov-sp-roomodes",
        "system": SYSTEM_SP_ROOMODES,
        "user_message": USER_SP_ROOMODES,
    },
    {
        "custom_id": "gov-readme-sp",
        "system": SYSTEM_README_SP,
        "user_message": USER_README_SP,
    },
    {
        "custom_id": "gov-template-root",
        "system": SYSTEM_TEMPLATE_ROOT,
        "user_message": USER_TEMPLATE_ROOT,
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

print(f"\nSubmitting BATCH 1: Governance Coherence with {len(requests)} requests to model {MODEL}...")
print("  Request 1: gov-sp-clinerules (SP-002 vs .clinerules)")
print("  Request 2: gov-sp-roomodes (SP-003..006 vs .roomodes)")
print("  Request 3: gov-readme-sp (prompts/README.md vs SP-001..010)")
print("  Request 4: gov-template-root (.clinerules vs template/.clinerules)")

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
print(f"   python plans/batch-full-audit/retrieve_batch1.py")
