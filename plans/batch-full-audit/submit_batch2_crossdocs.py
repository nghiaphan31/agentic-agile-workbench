"""
submit_batch2_crossdocs.py
--------------------------
BATCH 2: Cross-Document Coherence Audit

Submits 4 parallel requests to the Anthropic Batch API to audit:
1. DOC-1 (PRD) vs DOC-2 (Architecture) intra-release consistency in v2.2
2. DOC-2 (Architecture) vs DOC-3 (Implementation) intra-release consistency in v2.2
3. Version drift across v1.0→v2.0→v2.1→v2.2 (are features from older releases still in newer?)
4. DOC-CURRENT.md pointers vs actual release files

Usage (from workspace root):
    python plans/batch-full-audit/submit_batch2_crossdocs.py

Prerequisites:
    - ANTHROPIC_API_KEY environment variable must be set
    - pip install anthropic

Output:
    - Prints the batch_id to stdout
    - Saves the batch_id to plans/batch-full-audit/batch_id_2_crossdocs.txt
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
BATCH_ID_FILE = BATCH_DIR / "batch_id_2_crossdocs.txt"

# ---------------------------------------------------------------------------
# Helper: load file with error checking
# ---------------------------------------------------------------------------
def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        return f"[FILE NOT FOUND: {path}]"
    return p.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Load all cross-document files
# ---------------------------------------------------------------------------
print("Loading cross-document files...")

# v2.2 release documents
doc1_v22 = load("docs/releases/v2.2/DOC-1-v2.2-PRD.md")
doc2_v22 = load("docs/releases/v2.2/DOC-2-v2.2-Architecture.md")
doc3_v22 = load("docs/releases/v2.2/DOC-3-v2.2-Implementation-Plan.md")
doc4_v22 = load("docs/releases/v2.2/DOC-4-v2.2-Operations-Guide.md")
doc5_v22 = load("docs/releases/v2.2/DOC-5-v2.2-Release-Notes.md")

# v2.1 release documents
doc1_v21 = load("docs/releases/v2.1/DOC-1-v2.1-PRD.md")
doc2_v21 = load("docs/releases/v2.1/DOC-2-v2.1-Architecture.md")

# v2.0 release documents
doc1_v20 = load("docs/releases/v2.0/DOC-1-v2.0-PRD.md")
doc2_v20 = load("docs/releases/v2.0/DOC-2-v2.0-Architecture.md")

# DOC-CURRENT pointers
doc1_current = load("docs/DOC-1-CURRENT.md")
doc2_current = load("docs/DOC-2-CURRENT.md")
doc3_current = load("docs/DOC-3-CURRENT.md")
doc4_current = load("docs/DOC-4-CURRENT.md")
doc5_current = load("docs/DOC-5-CURRENT.md")

print(f"  DOC-1 v2.2   : {len(doc1_v22):,} chars")
print(f"  DOC-2 v2.2   : {len(doc2_v22):,} chars")
print(f"  DOC-3 v2.2   : {len(doc3_v22):,} chars")
print(f"  DOC-4 v2.2   : {len(doc4_v22):,} chars")
print(f"  DOC-5 v2.2   : {len(doc5_v22):,} chars")
print(f"  DOC-1 v2.1   : {len(doc1_v21):,} chars")
print(f"  DOC-1 v2.0   : {len(doc1_v20):,} chars")
print(f"  DOC-CURRENT  : DOC-1..5 = {len(doc1_current):,} / {len(doc2_current):,} / {len(doc3_current):,} / {len(doc4_current):,} / {len(doc5_current):,} chars")

# ---------------------------------------------------------------------------
# Build the shared context block
# ---------------------------------------------------------------------------
SHARED_CONTEXT = f"""
=== DOC-1 v2.2 (PRD) ===

{doc1_v22}

=== DOC-2 v2.2 (Architecture) ===

{doc2_v22}

=== DOC-3 v2.2 (Implementation Plan) ===

{doc3_v22}

=== DOC-4 v2.2 (Operations Guide) ===

{doc4_v22}

=== DOC-5 v2.2 (Release Notes) ===

{doc5_v22}

=== DOC-1 v2.1 (PRD - previous release) ===

{doc1_v21}

=== DOC-1 v2.0 (PRD - older release) ===

{doc1_v20}
"""

CURRENT_CONTEXT = f"""
=== DOC-1-CURRENT.md ===

{doc1_current}

=== DOC-2-CURRENT.md ===

{doc2_current}

=== DOC-3-CURRENT.md ===

{doc3_current}

=== DOC-4-CURRENT.md ===

{doc4_current}

=== DOC-5-CURRENT.md ===

{doc5_current}
"""

# ---------------------------------------------------------------------------
# Request 1: DOC-1 vs DOC-2 intra-release consistency (v2.2)
# ---------------------------------------------------------------------------
SYSTEM_DOC12_V22 = """You are a Senior Technical Architect and Documentation Strategist with expertise in
traceability between requirements documents and architecture documents.

Your task: Audit intra-release consistency between DOC-1 (PRD) and DOC-2 (Architecture) for v2.2.

IMPORTANT CONTEXT:
- DOC-1-v2.2-PRD.md is the Product Requirements Document
- DOC-2-v2.2-Architecture.md is the Technical Architecture document
- Both are FROZEN for v2.2 and should be consistent with each other

Check for these specific things:
1. Are all features/epics in DOC-1 covered by an architectural component in DOC-2?
2. Are there any requirements in DOC-1 that contradict the architecture in DOC-2?
3. Are the technical choices (languages, frameworks, tools) in DOC-2 justified by requirements in DOC-1?
4. Does DOC-2 reference any components or phases that are NOT in DOC-1's scope?
5. Are the Phase definitions consistent (Phase 1, Phase 2, etc.)?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the cross-document consistency

## 2. Requirements-to-Architecture Traceability
For each major feature/epic in DOC-1:
| Feature | DOC-1 Section | DOC-2 Coverage | Consistent? |
|---|---|---|---|
| Feature A | Section X.Y | Section A.B | Yes/No |

## 3. Contradictions Found
| Location | DOC-1 Says | DOC-2 Says | Resolution |
|---|---|---|---|
| Section X.Y | ... | ... | ... |

## 4. Scope Creep Detection
Are there architectural components in DOC-2 that have no corresponding requirement in DOC-1?

## 5. Phase Definition Consistency
Are the phases/stages defined consistently in both documents?

## 6. Prioritized Remediation
- **P0 (Critical):** Requirement not covered by architecture (gap)
- **P1 (Important):** Contradiction between DOC-1 and DOC-2
- **P2 (Nice to have):** Missing traceability for minor features

## 7. Verdict
[CONSISTENT] / [MINOR_ISSUES] / [MAJOR_INCONSISTENCIES]
Justify in 2-3 sentences."""

USER_DOC12_V22 = f"""Please audit DOC-1 (PRD) vs DOC-2 (Architecture) intra-release consistency for v2.2.

{SHARED_CONTEXT}

Focus on:
1. Tracing each requirement/epic from DOC-1 to its architectural component in DOC-2
2. Identifying any contradictions between requirements and architecture
3. Detecting scope creep (DOC-2 references things not in DOC-1)
4. Verifying phase definitions match"""

# ---------------------------------------------------------------------------
# Request 2: DOC-2 vs DOC-3 intra-release consistency (v2.2)
# ---------------------------------------------------------------------------
SYSTEM_DOC23_V22 = """You are a Senior Engineering Program Manager and Technical Architect with expertise in
verifying that implementation plans accurately reflect architectural designs.

Your task: Audit intra-release consistency between DOC-2 (Architecture) and DOC-3 (Implementation Plan) for v2.2.

IMPORTANT CONTEXT:
- DOC-2-v2.2-Architecture.md is the Technical Architecture document
- DOC-3-v2.2-Implementation-Plan.md is the Implementation Plan
- Both are FROZEN for v2.2

Check for these specific things:
1. Does every architectural component in DOC-2 have a corresponding implementation step in DOC-3?
2. Are the phases/stages in DOC-3 the same as the phases in DOC-2?
3. Are the tools/technologies in DOC-3 consistent with DOC-2?
4. Are the Milestones in DOC-3 aligned with the architecture's delivery plan?
5. Does DOC-3 add any new technical decisions not in DOC-2?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing the architecture-to-implementation consistency

## 2. Component Coverage
For each major component/phase in DOC-2:
| Component | DOC-2 Section | DOC-3 Coverage | Consistent? |
|---|---|---|---|
| Component A | Section X.Y | Section A.B | Yes/No |

## 3. Tool/Technology Consistency
| Tool | DOC-2 | DOC-3 | Match? |
|---|---|---|---|
| Language | ... | ... | Yes/No |
| Framework | ... | ... | Yes/No |
| Infrastructure | ... | ... | Yes/No |

## 4. Phase Alignment
- Are the phases/stages the same in both documents?
- Are the phase order and dependencies consistent?

## 5. New Technical Decisions
Does DOC-3 introduce any technical decisions not present in DOC-2?

## 6. Prioritized Remediation
- **P0 (Critical):** Architecture component without implementation plan
- **P1 (Important):** Tool/technology inconsistency
- **P2 (Nice to have):** Minor phase ordering differences

## 7. Verdict
[CONSISTENT] / [MINOR_ISSUES] / [MAJOR_INCONSISTENCIES]
Justify in 2-3 sentences."""

USER_DOC23_V22 = f"""Please audit DOC-2 (Architecture) vs DOC-3 (Implementation Plan) intra-release consistency for v2.2.

{SHARED_CONTEXT}

Focus on:
1. Tracing each architectural component from DOC-2 to its implementation step in DOC-3
2. Checking tool/technology consistency
3. Verifying phase alignment
4. Detecting new technical decisions introduced in DOC-3"""

# ---------------------------------------------------------------------------
# Request 3: Version drift across v1.0→v2.0→v2.1→v2.2
# ---------------------------------------------------------------------------
SYSTEM_VERSION_DRIFT = """You are a Senior Technical Program Manager with expertise in release management,
version control, and tracking feature evolution across product releases.

Your task: Audit version drift across v1.0, v2.0, v2.1, and v2.2 for consistency.

IMPORTANT CONTEXT:
- Each release should have: DOC-1 (PRD), DOC-2 (Architecture), DOC-3 (Implementation Plan)
- Features should not disappear between releases without explanation
- New releases may add features but should not silently drop features from previous releases

Check for these specific things:
1. Are all features from v2.1 still present in v2.2 (or explicitly removed/deprecated)?
2. Are there any references to "v2.0" or "v2.1" specific features that appear inconsistent in v2.2?
3. Does the Release Notes (DOC-5) for v2.2 accurately reflect all changes from v2.1?
4. Is the hotfix/exception process described consistently across releases?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing version drift

## 2. Feature Continuity Check
For each major feature area:
| Feature Area | v2.1 Status | v2.2 Status | Continues? | Notes |
|---|---|---|---|---|
| Memory Bank | ... | ... | Yes/No | ... |
| Anthropic API | ... | ... | Yes/No | ... |
| Hot/Cold Memory | ... | ... | Yes/No | ... |
| Calypso Orchestration | ... | ... | Yes/No | ... |
| GitFlow | ... | ... | Yes/No | ... |

## 3. Orphaned References
Are there any references in v2.2 documents to features or processes that were specific to v2.0 or v2.1 but not present in v2.2?

## 4. Release Notes Accuracy (v2.2)
Does DOC-5-v2.2-Release-Notes.md accurately capture all changes from v2.1 to v2.2?

## 5. Breaking Changes
Are there any breaking changes between v2.1 and v2.2 that are NOT documented?

## 6. Prioritized Remediation
- **P0 (Critical):** Feature silently dropped between releases
- **P1 (Important):** Incomplete release notes
- **P2 (Nice to have):** Minor documentation inconsistencies

## 7. Verdict
[CONSISTENT] / [MINOR_DRIFT] / [MAJOR_DRIFT]
Justify in 2-3 sentences."""

USER_VERSION_DRIFT = f"""Please audit version drift across v1.0, v2.0, v2.1, and v2.2.

{SHARED_CONTEXT}

Focus on:
1. Checking feature continuity from v2.1 to v2.2
2. Identifying orphaned references
3. Verifying release notes accuracy
4. Detecting breaking changes not documented"""

# ---------------------------------------------------------------------------
# Request 4: DOC-CURRENT.md pointers vs actual release files
# ---------------------------------------------------------------------------
SYSTEM_CURRENT_POINTERS = """You are a Senior DevOps Architect specializing in configuration management,
symlink management, and pointer/reference integrity.

Your task: Audit whether DOC-CURRENT.md files correctly point to the actual current release files.

IMPORTANT CONTEXT:
- docs/DOC-1-CURRENT.md should point to the current PRD (v2.2)
- docs/DOC-2-CURRENT.md should point to the current Architecture (v2.2)
- docs/DOC-3-CURRENT.md should point to the current Implementation Plan (v2.2)
- docs/DOC-4-CURRENT.md should point to the current Operations Guide (v2.2)
- docs/DOC-5-CURRENT.md should point to the current Release Notes (v2.2)
- Each DOC-N-CURRENT.md contains metadata: "Current release: v2.2", "Git tag: v2.2.0"

Check for these specific things:
1. Does each DOC-N-CURRENT.md point to the correct file in docs/releases/v2.2/?
2. Is the "Current release" field correct (should be v2.2)?
3. Is the "Git tag" field correct (should be v2.2.0)?
4. Is the "Status" field correct (should be "Frozen")?
5. Do the files actually exist at the pointed-to locations?

Your review MUST be structured EXACTLY as follows:

## 1. Executive Summary
3-5 bullet points summarizing pointer integrity

## 2. Pointer Validation Table
| DOC-N-CURRENT | Points To | File Exists? | Release Field | Tag Field | Status Field |
|---|---|---|---|---|---|
| DOC-1-CURRENT.md | docs/releases/v2.2/... | Yes/No | v2.2 / Other | v2.2.0 / Other | Frozen / Other |
| DOC-2-CURRENT.md | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

## 3. Incorrect Pointers Found
| File | Says Points To | Actually Points To | Should Be |
|---|---|---|---|
| ... | ... | ... | ... |

## 4. Metadata Discrepancies
| File | Issue | Current Value | Expected Value |
|---|---|---|---|
| ... | ... | ... | ... |

## 5. Prioritized Remediation
- **P0 (Critical):** Pointer points to non-existent file
- **P1 (Important):** Metadata (release, tag, status) incorrect
- **P2 (Nice to have):** Minor pointer inconsistencies

## 6. Verdict
[CORRECT] / [MINOR_ISSUES] / [MAJOR_ISSUES]
Justify in 2-3 sentences."""

USER_CURRENT_POINTERS = f"""Please audit DOC-CURRENT.md pointers vs actual release files.

{SHARED_CONTEXT}

{CURRENT_CONTEXT}

Focus on:
1. Verifying each DOC-N-CURRENT.md points to the correct file in docs/releases/v2.2/
2. Checking metadata fields (Current release, Git tag, Status)
3. Ensuring all pointed-to files actually exist"""

# ---------------------------------------------------------------------------
# Build the batch requests
# ---------------------------------------------------------------------------
REVIEWS = [
    {
        "custom_id": "xd-doc12-v22",
        "system": SYSTEM_DOC12_V22,
        "user_message": USER_DOC12_V22,
    },
    {
        "custom_id": "xd-doc23-v22",
        "system": SYSTEM_DOC23_V22,
        "user_message": USER_DOC23_V22,
    },
    {
        "custom_id": "xd-version-drift",
        "system": SYSTEM_VERSION_DRIFT,
        "user_message": USER_VERSION_DRIFT,
    },
    {
        "custom_id": "xd-current-pointers",
        "system": SYSTEM_CURRENT_POINTERS,
        "user_message": USER_CURRENT_POINTERS,
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

print(f"\nSubmitting BATCH 2: Cross-Document Coherence with {len(requests)} requests to model {MODEL}...")
print("  Request 1: xd-doc12-v22 (DOC-1 vs DOC-2 in v2.2)")
print("  Request 2: xd-doc23-v22 (DOC-2 vs DOC-3 in v2.2)")
print("  Request 3: xd-version-drift (v1.0->v2.0->v2.1->v2.2)")
print("  Request 4: xd-current-pointers (DOC-CURRENT.md vs releases/)")

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
print(f"   python plans/batch-full-audit/retrieve_batch2.py")
