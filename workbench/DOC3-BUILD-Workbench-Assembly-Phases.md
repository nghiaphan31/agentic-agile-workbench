# Document 3: Complete Sequential Implementation Plan
## Agentic Agile Workbench â€” Phases 0 to 12

**Project Name:** Agentic Agile Workbench
**Version:** 3.0 â€” Single merged document (phases 0-12 continuous)
**Date:** 2026-03-23
**Target Platform:** Windows 10/11 (laptop `pc`) + Visual Studio Code + Linux Server `calypso` (Tailscale)
**References:** DOC1-PRD-Workbench-Requirements.md v2.0, DOC2-ARCH-Workbench-Technical-Design.md v2.0

---

## System Prerequisites

Before starting, verify that both machines are ready:

### Windows Laptop `pc`
- Windows 10/11 (64-bit)
- Google Chrome installed with an active Google account
- Git installed (`git --version` must respond in PowerShell)
- Python 3.10+ installed (`python --version` must respond in PowerShell)
- Tailscale installed and connected (`tailscale status` shows `calypso` as an active peer)
- Internet connection for initial downloads

### Linux Server `calypso`
- Linux (Ubuntu 22.04+ or Debian 12+ recommended), headless
- NVIDIA RTX 5060 Ti graphics card with 16 GB of VRAM
- At least 32 GB of RAM (recommended for the 32B model)
- At least 30 GB of free disk space (models + project)
- Tailscale installed and connected (`tailscale status` shows `pc` as an active peer)
- NVIDIA drivers installed (`nvidia-smi` must respond)
- Internet connection for initial downloads (Ollama models)

---

## Phase Overview

```
PHASE 0  : Clean Base â€” VS Code + Roo Code Cleanup and Reinstallation
    |
    v
PHASE 1  : System Infrastructure (Ollama + LLM Models)
    |
    v
PHASE 2  : Creation of the le workbench Git Repository
    |
    v
PHASE 3  : Modelfile and Custom Ollama Model
    |
    v
PHASE 4  : Agile Personas (.roomodes) with Git Rules
    |
    v
PHASE 5  : Memory Bank (.clinerules with 6 Rules + 7 .md files)
    |
    v
PHASE 6  : Gemini Chrome Proxy (proxy.py v2.0 with SSE)
    |
    v
PHASE 7  : Gemini Chrome Configuration (Dedicated Gem)
    |
    v
PHASE 8  : Roo Code Configuration (3-Mode LLM Switcher)
    |
    v
PHASE 9  : End-to-End Validation Tests
    |
    v
PHASE 10 : Direct Cloud Mode â€” Anthropic Claude Sonnet API
    |
    v
PHASE 11 : Central System Prompts Registry (prompts/)
    |
    v
PHASE 12 : Automatic Prompt Consistency Verification
```

### Phase / PRD Requirements Mapping Table

| Phase | Description | PRD Requirements |
| :--- | :--- | :--- |
| Phase 0 | Clean VS Code + Roo Code base | REQ-000 |
| Phase 1 | Ollama + models installation | REQ-1.0, REQ-1.1, REQ-1.2 |
| Phase 2 | Git repository + complete .gitignore | REQ-000, REQ-4.1, REQ-4.5 |
| Phase 3 | Custom Modelfile + commit | REQ-1.2, REQ-1.3 |
| Phase 4 | Agile personas .roomodes + Git rules | REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4 |
| Phase 5 | .clinerules (6 rules) + 7 Memory Bank files | REQ-4.1 to REQ-4.5 |
| Phase 6 | proxy.py v2.0 (SSE + JSON) + scripts/ | REQ-2.1.1 to REQ-2.4.4 |
| Phase 7 | Gemini Chrome Gem + Memory Bank doc | REQ-5.1, REQ-5.2, REQ-5.3 |
| Phase 8 | Roo Code 3-mode LLM switcher | REQ-2.0, REQ-6.0 |
| Phase 9 | End-to-end tests (including self-contained Git test) | REQ-000 |
| Phase 10 | Anthropic Claude Sonnet API (claude-sonnet-4-6) | REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4 |
| Phase 11 | Central prompts registry (prompts/) | REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5 |
| Phase 12 | Automatic prompt consistency verification (script + pre-commit hook) | REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4 |

---

## PHASE 0: Clean Base â€” VS Code + Roo Code Cleanup and Reinstallation

**Objective:** Start from a clean VS Code and Roo Code environment, free from previous configuration pollution.
**Requirements addressed:** REQ-000

> **Why this phase is critical:** A "polluted" VS Code environment can cause unpredictable Roo Code behavior: residual API settings, conflicting extensions, corrupted cache, or old versions of Roo Code (Cline) coexisting with the new one. This phase guarantees a clean slate.

### Step 0.1 â€” Back Up Current VS Code Settings (Optional)

```powershell
$vscodeSettings = "$env:APPDATA\Code\User"
$backup = "$env:USERPROFILE\Desktop\vscode-backup-$(Get-Date -Format 'yyyyMMdd')"
Copy-Item -Path $vscodeSettings -Destination $backup -Recurse
Write-Host "Backup created: $backup"
```

### Step 0.2 â€” Uninstall All Versions of Roo Code / Cline

1. In VS Code, open the Extensions panel (`Ctrl+Shift+X`)
2. Search for **"Roo"** in the search bar
3. For each extension found (Roo Code, Roo Cline, Cline, etc.): click the gear â†’ **"Uninstall"**
4. Search for **"Cline"** and repeat the operation
5. Reload VS Code (`Ctrl+Shift+P` > "Developer: Reload Window")

### Step 0.3 â€” Clean Roo Code Cache and Data

Close VS Code completely, then in PowerShell:

```powershell
$extensionsPath = "$env:USERPROFILE\.vscode\extensions"
$globalStoragePath = "$env:APPDATA\Code\User\globalStorage"

Write-Host "=== Roo/Cline Extensions Found ==="
Get-ChildItem $extensionsPath | Where-Object { $_.Name -match "roo|cline|saoud" } | Select-Object Name

Write-Host "=== Roo/Cline Global Data Found ==="
Get-ChildItem $globalStoragePath | Where-Object { $_.Name -match "roo|cline|saoud" } | Select-Object Name
```

Delete the identified folders:

```powershell
Get-ChildItem $extensionsPath | Where-Object { $_.Name -match "roo|cline|saoud" } | Remove-Item -Recurse -Force
Get-ChildItem $globalStoragePath | Where-Object { $_.Name -match "roo|cline|saoud" } | Remove-Item -Recurse -Force
Write-Host "Cleanup complete."
```

### Step 0.4 â€” Clean Residual VS Code Settings

```powershell
$settingsFile = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $settingsFile) {
    Write-Host "=== Roo/Cline Entries in settings.json ==="
    Get-Content $settingsFile | Select-String -Pattern "roo|cline|ollama|anthropic" -CaseSensitive:$false
}
```

If residual entries are found, open `settings.json` in a text editor and delete the relevant sections.

### Step 0.5 â€” Reinstall VS Code (If Necessary)

If VS Code itself is unstable:
1. **Windows Settings > Apps** â†’ search for "Visual Studio Code" â†’ **Uninstall**
2. Delete residual folders:
   ```powershell
   Remove-Item "$env:APPDATA\Code" -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item "$env:USERPROFILE\.vscode" -Recurse -Force -ErrorAction SilentlyContinue
   ```
3. Download the latest stable version from **https://code.visualstudio.com**
4. Install with default options

### Step 0.6 â€” Install the Latest Version of Roo Code

1. Open VS Code
2. Open the Extensions panel (`Ctrl+Shift+X`)
3. Search for **"Roo Code"**
4. Verify the publisher is **"Roo Coder"** (the official publisher)
5. Click **"Install"**

**Validation criterion:** The Roo Code icon appears in the VS Code left sidebar.

### Step 0.7 â€” Verify the Clean State of Roo Code

1. Click the Roo Code icon in the sidebar
2. The panel opens without errors
3. In Roo Code settings (gear): no API key should be pre-filled
4. The mode list contains only the default modes (Code, Architect, Ask, Debug, Orchestrator)

> **If custom modes or API keys already appear:** Repeat steps 0.3 and 0.4.

### Step 0.8 â€” Verify Git and Python

```powershell
git --version
python --version
pip --version
```

Each command must return a version number. If one fails:
- **Git:** https://git-scm.com/download/win
- **Python:** https://python.org/downloads (check "Add to PATH" during installation)

---

## PHASE 1: System Infrastructure â€” Installing Ollama on `calypso`

**Objective:** Install the inference engine on the Linux server `calypso` and download the LLM models. All commands in this phase run **on `calypso`** via SSH from the laptop `pc`.
**Requirements addressed:** REQ-1.0, REQ-1.1, REQ-1.2

> **Prerequisites:** Tailscale must be active on both machines. Verify from `pc`:
> ```powershell
> tailscale status
> # calypso must appear as an active peer with a Tailscale IP address
> ```

### Step 1.1 â€” Connect to `calypso` via SSH

From the laptop `pc` (PowerShell):

```powershell
ssh calypso
```

> **Note:** Tailscale automatically resolves the name `calypso` to a private IP address. If SSH is not configured, use the Tailscale IP address: `ssh user@100.x.x.x`.

### Step 1.2 â€” Install Ollama on `calypso` (Linux)

On `calypso` (SSH terminal):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Validation criterion:**
```bash
ollama --version
```
Expected result: `ollama version 0.x.x`

### Step 1.3 â€” Configure Ollama to Listen on the Tailscale Network

By default, Ollama only listens on `localhost`. To make it accessible from `pc` via Tailscale, configure the `OLLAMA_HOST` environment variable:

```bash
# Edit the Ollama systemd service
sudo systemctl edit ollama
```

Add to the file:
```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Then reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

> **Security:** Ollama listens on `0.0.0.0:11434` but Tailscale filters connections to the private network only. The API is not exposed on the Internet.

### Step 1.4 â€” Download the Main Model (Qwen3 32B optimized for Roo Code)

On `calypso`:

```bash
ollama pull mychen76/qwen3_cline_roocode:32b
```

> **Note:** This download may take 15 to 45 minutes. The model weighs approximately 20 GB.

**Validation criterion:**
```bash
ollama list
```
You must see `mychen76/qwen3_cline_roocode:32b` in the list.

### Step 1.5 â€” Download the Secondary Model (Qwen3 7B for Boomerang Tasks)

On `calypso`:

```bash
ollama pull qwen3:7b
```

**Validation criterion:** `ollama list` shows `qwen3:7b`.

### Step 1.6 â€” Verify that the Ollama API is Accessible from `pc`

From the laptop `pc` (PowerShell):

```powershell
Invoke-WebRequest -Uri "http://calypso:11434/api/tags" -Method GET | Select-Object -ExpandProperty Content
```

You must see a JSON response listing your models. If connection error:
1. Verify that Tailscale is active on both machines (`tailscale status`)
2. Verify that `OLLAMA_HOST=0.0.0.0:11434` is configured on `calypso` (`sudo systemctl show ollama | grep Environment`)
3. Restart Ollama on `calypso`: `sudo systemctl restart ollama`

---

## PHASE 2: Creation of the le workbench Git Repository

**Objective:** Create the Git repository that will version EVERYTHING: code, scripts, prompts, configurations, Memory Bank.
**Requirements addressed:** REQ-000, REQ-4.1, REQ-4.5

> **Fundamental principle:** In the workbench, Git does not only version application code. It versions the entire intelligence of the project: system prompts (`.clinerules`, `.roomodes`), scripts (`template/proxy.py`), configuration (`Modelfile`), and persistent memory (`memory-bank/`). Each significant modification to any of these elements must be the subject of a Git commit with a descriptive message.

### Step 2.1 â€” Create the Project Folder

```powershell
# Canonical folder structure:
# $env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\
# â”œâ”€â”€ agentic-agile-workbench\   â† THE WORKBENCH (master template, this repository)
# â””â”€â”€ PROJECTS\                  â† All application projects
#     â””â”€â”€ my-project\

$Projet = "$env:USERPROFILE\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\mon-projet"
New-Item -Path $Projet -ItemType Directory -Force
cd $Projet
code .
```

### Step 2.2 â€” Initialize Git

In the VS Code terminal (`` Ctrl+` ``):
```powershell
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

### Step 2.3 â€” Create the Complete `.gitignore` File

```powershell
New-Item -Name ".gitignore" -ItemType File
```

Open `.gitignore` and paste:
```gitignore
# Python environment (never versioned)
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/

# Environment variables (contains API keys â€” NEVER versioned)
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Windows temporary files
Thumbs.db
Desktop.ini
*.tmp

# Local VS Code files (personal settings, not project)
.vscode/settings.json
.vscode/launch.json
.vscode/tasks.json

# IMPORTANT: The following files MUST be versioned (do not add them here)
# .roomodes        -> Versioned (Agile personas)
# .clinerules      -> Versioned (Memory Bank + Git rules)
# Modelfile        -> Versioned (Ollama model config)
# proxy.py         -> Versioned (Gemini proxy server)
# memory-bank/     -> Versioned (persistent memory)
# requirements.txt -> Versioned (Python dependencies)
# prompts/         -> Versioned (central prompts registry)
# scripts/         -> Versioned (PowerShell scripts)
```

Save (`Ctrl+S`).

### Step 2.4 â€” Create the Project Folder Structure

```powershell
mkdir memory-bank
mkdir docs
mkdir docs\qa
mkdir scripts
mkdir prompts
```

### Step 2.5 â€” First Commit: Project Skeleton

```powershell
git add .gitignore
git commit -m "chore: initialize le workbench repository - project skeleton and .gitignore"
```

**Validation criterion:** `git log --oneline` shows the initial commit.

---

## PHASE 3: Modelfile and Custom Ollama Model

**Objective:** Create a custom Ollama model with determinism parameters and extended context window.
**Requirements addressed:** REQ-1.2, REQ-1.3

### Step 3.1 â€” Create the `Modelfile`

```powershell
New-Item -Name "Modelfile" -ItemType File
```

Open `Modelfile` in VS Code and paste exactly:
```dockerfile
FROM mychen76/qwen3_cline_roocode:32b

# Determinism parameters (anti-hallucination) â€” REQ-1.3
PARAMETER temperature 0.15
PARAMETER min_p 0.03
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.1

# Maximum context window (128K tokens) â€” REQ-1.2
PARAMETER num_ctx 131072

# GPU performance parameters
PARAMETER num_gpu 99
PARAMETER num_thread 8

SYSTEM """
Tu es un agent de developpement logiciel expert integre dans Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank (memory-bank/) avant d'agir.
Tu dois toujours mettre a jour la Memory Bank apres chaque tache.
Apres chaque tache significative, tu dois effectuer un commit Git avec un message descriptif.
"""
```

Save (`Ctrl+S`).

### Step 3.2 â€” Compile the Custom Model

On `calypso` (via SSH from `pc`):

```bash
ollama create uadf-agent -f Modelfile
```

**Validation criterion:**
```powershell
ollama show uadf-agent --modelfile
```
Must show `PARAMETER num_ctx 131072` and `PARAMETER temperature 0.15`.

### Step 3.3 â€” Test the Model

```powershell
ollama run uadf-agent "Dis bonjour en une phrase."
```

Type `/bye` to quit.

### Step 3.4 â€” Version the Modelfile

```powershell
git add Modelfile
git commit -m "feat: add Ollama Modelfile (uadf-agent, T=0.15, ctx=131072)"
```

---

## PHASE 4: Agile Personas â€” `.roomodes` File with Git Rules

**Objective:** Create the 4 Agile personas with their RBAC permissions and mandatory Git versioning.
**Requirements addressed:** REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4

> **Why embed Git in roleDefinitions?** The Developer and Scrum Master have terminal access. By embedding the Git commit obligation in their `roleDefinition`, we guarantee that this behavior is self-contained: even if `.clinerules` is not read, the persona itself knows it must version. This is defense in depth.

> **Scrum Master â€” pure facilitator (REQ-3.4):** The Scrum Master can read all files (including `docs/qa/`), write to `memory-bank/` and `docs/`, and execute only Git commands. It cannot execute test commands or modify source code. To know the test status, it reads the QA reports in `docs/qa/` produced by the QA Engineer.

### Step 4.1 â€” Create the `.roomodes` File

```powershell
New-Item -Name ".roomodes" -ItemType File
```

### Step 4.2 â€” Insert the Persona Configuration

Open `.roomodes` in VS Code and paste the following JSON content:

```json
{
  "customModes": [
    {
      "slug": "product-owner",
      "name": "Product Owner",
      "roleDefinition": "Tu es le Product Owner de l'Ã©quipe Scrum. Ton rÃ´le est de dÃ©finir et prioriser le backlog produit. Tu rÃ©diges les User Stories au format 'En tant que [persona], je veux [action] afin de [bÃ©nÃ©fice]'. Tu maintiens le fichier memory-bank/productContext.md Ã  jour. Tu ne touches JAMAIS au code source ni aux scripts. Si on te demande d'Ã©crire du code, tu refuses poliment et suggÃ¨res de basculer vers le mode Developer.",
      "groups": [
        "read",
        ["edit", { "fileRegex": "memory-bank/productContext\\.md|docs/.*\\.md|user-stories.*\\.md", "description": "Documentation produit uniquement" }]
      ],
      "source": "project"
    },
    {
      "slug": "scrum-master",
      "name": "Scrum Master",
      "roleDefinition": "Tu es le Scrum Master de l'Ã©quipe Scrum. Tu facilites les cÃ©rÃ©monies Agile (Sprint Planning, Daily, Review, RÃ©trospective). Tu identifies et supprimes les impediments. Tu maintiens memory-bank/progress.md et memory-bank/activeContext.md Ã  jour. Tu ne touches pas au code source applicatif. Tu peux lire tous les fichiers du projet, y compris les rapports QA dans docs/qa/. Pour connaÃ®tre l'Ã©tat des tests, tu lis les rapports produits par le QA Engineer dans docs/qa/ â€” tu n'exÃ©cutes pas de commandes de test toi-mÃªme. RÃˆGLE GIT OBLIGATOIRE : AprÃ¨s chaque mise Ã  jour de la Memory Bank, tu DOIS exÃ©cuter un commit Git avec le message format 'docs(memory): [description de la mise Ã  jour]'.",
      "groups": [
        "read",
        ["edit", { "fileRegex": "memory-bank/.*\\.md|docs/.*\\.md", "description": "Memory Bank et documentation" }],
        ["command", { "allowedCommands": ["git add", "git commit", "git status", "git log"], "description": "Commandes Git pour versionner la Memory Bank" }]
      ],
      "source": "project"
    },
    {
      "slug": "developer",
      "name": "Developer",
      "roleDefinition": "Tu es le Developer senior de l'Ã©quipe Scrum. Tu implÃ©mentes les User Stories du backlog. Tu Ã©cris du code propre, testÃ© et documentÃ©. PROTOCOLE OBLIGATOIRE EN 3 Ã‰TAPES : (1) AVANT de coder : lire memory-bank/activeContext.md, memory-bank/systemPatterns.md et memory-bank/techContext.md. (2) APRÃˆS avoir codÃ© : mettre Ã  jour memory-bank/activeContext.md et memory-bank/progress.md. (3) AVANT de clÃ´turer la tÃ¢che : exÃ©cuter 'git add .' puis 'git commit -m [message descriptif au format conventionnel]'. Le versionnement Git est NON NÃ‰GOCIABLE : tout fichier crÃ©Ã© ou modifiÃ© doit Ãªtre commitÃ© avant attempt_completion.",
      "groups": [
        "read",
        "edit",
        "browser",
        "command",
        "mcp"
      ],
      "source": "project"
    },
    {
      "slug": "qa-engineer",
      "name": "QA Engineer",
      "roleDefinition": "Tu es le QA Engineer de l'Ã©quipe Scrum. Tu conÃ§ois et exÃ©cutes les plans de test. Tu analyses les logs et rapports de test. Tu rÃ©diges les rapports de bugs avec reproduction steps clairs dans docs/qa/. Tu ne modifies JAMAIS le code source applicatif. Tu peux exÃ©cuter des commandes de test (npm test, pytest, etc.) et lire tous les fichiers.",
      "groups": [
        "read",
        ["edit", { "fileRegex": "docs/qa/.*\\.md|memory-bank/progress\\.md", "description": "Rapports QA et suivi progression" }],
        ["command", { "allowedCommands": ["npm test", "npm run test", "pytest", "python -m pytest", "dotnet test", "go test", "git status", "git log"], "description": "Commandes de test et consultation Git" }]
      ],
      "source": "project"
    }
  ]
}
```

Save (`Ctrl+S`).

### Step 4.3 â€” Verify Mode Loading in Roo Code

1. Click the Roo Code icon in the sidebar
2. Click the mode selector at the top of the panel
3. You must see: "Product Owner", "Scrum Master", "Developer", "QA Engineer"

> **If the modes do not appear:** Reload VS Code (`Ctrl+Shift+P` > "Developer: Reload Window").

### Step 4.4 â€” Version `.roomodes`

```powershell
git add .roomodes
git commit -m "feat(agile): add Agile RBAC personas with integrated Git rules (.roomodes)"
```

**RBAC Validation Criterion:**
- Product Owner mode â†’ ask "Write Python code" â†’ must refuse
- Scrum Master mode â†’ ask "Run pytest" â†’ must refuse
- QA Engineer mode â†’ ask "Modify src/main.py" â†’ must refuse

---

## PHASE 5: Memory Bank â€” `.clinerules` with 6 Rules + 7 Markdown Files

**Objective:** Create the persistent memory system (7 Markdown files) and global directives (`.clinerules`) that force the agent to follow the CHECKâ†’CREATEâ†’READâ†’ACT sequence at each session.
**Requirements addressed:** REQ-4.1, REQ-4.2, REQ-4.3, REQ-4.4, REQ-4.5, REQ-7.3
**Architecture decisions:** DA-002, DA-003

---

### Step 5.1 â€” Create the `.clinerules` File

Create the `.clinerules` file at the project root:

```powershell
New-Item -Path "." -Name ".clinerules" -ItemType File
```

Open `.clinerules` and paste **exactly** this content (canonical source: [`SP-002-clinerules-global.md`](../prompts/SP-002-clinerules-global.md)):

```markdown
# PROTOCOL le workbench â€” MANDATORY DIRECTIVES (ALL SESSIONS, ALL MODES)

## RULE 1 : MANDATORY READ AT THE START OF EACH SESSION
Before any action, you MUST execute the following sequence in this exact order:

1. CHECK : Does memory-bank/activeContext.md exist?
   - If NO â†’ proceed to the CREATE step
   - If YES â†’ proceed to the READ step
2. CREATE (if absent) : Immediately create memory-bank/activeContext.md AND memory-bank/progress.md
   using the templates defined at the bottom of this file.
3. READ : Read memory-bank/activeContext.md then memory-bank/progress.md
4. ACT : Process the user's request

This CHECKâ†’CREATEâ†’READâ†’ACT sequence is NON-NEGOTIABLE and applies to ALL sessions.

## RULE 2 : MANDATORY WRITE AT THE CLOSE OF EACH TASK
Before closing any task (before attempt_completion), you MUST update:
1. memory-bank/activeContext.md  (new state, next action)
2. memory-bank/progress.md       (check off completed features)

If an architecture decision was made during the session:
3. memory-bank/decisionLog.md    (ADR with date, context, decision, consequences)

## RULE 3 : CONTEXTUAL READ BASED ON THE TASK
- Before modifying the architecture: read memory-bank/systemPatterns.md
- Before executing build/test commands: read memory-bank/techContext.md
- At the start of a sprint or new feature: read memory-bank/productContext.md

## RULE 4 : NO EXCEPTIONS TO RULES 1-3
These rules apply to ALL modes and ALL sessions, without exception.

## RULE 5 : MANDATORY AND SELF-CONTAINED GIT VERSIONING
This rule applies to all modes with access to the terminal (developer, scrum-master).

### 5.1 â€” What MUST be versioned
EVERYTHING must be versioned under Git, without exception:
- Application source code (src/, app/, etc.)
- System scripts (proxy.py, scripts/start-proxy.ps1, etc.)
- Configuration files (Modelfile, .roomodes, .clinerules, requirements.txt)
- The Memory Bank (memory-bank/*.md)
- System prompts (prompts/SP-*.md and prompts/README.md)
- Plans and architecture documents (workbench/*.md)
- QA reports (docs/qa/*.md)

### 5.2 â€” When to commit
You MUST execute a Git commit in the following situations:
- After creating or modifying a code file
- After updating the Memory Bank
- After modifying .roomodes, .clinerules, Modelfile or any file in prompts/
- After modifying proxy.py or any other script
- Before closing a task (before attempt_completion)

### 5.3 â€” Commit message format (Conventional Commits)
You MUST use the Conventional Commits format:
- feat(scope): description     -> New feature
- fix(scope): description      -> Bug fix
- docs(memory): description    -> Memory Bank update
- docs(plans): description     -> Documentation update
- chore(config): description   -> Configuration change
- chore(prompts): description  -> System prompt modification
- refactor(scope): description -> Refactoring without functional change
- test(scope): description     -> Adding or modifying tests

### 5.4 â€” Git commands to use
  git add .
  git commit -m "type(scope): concise description"

### 5.5 â€” What must NOT be versioned
- The venv/ folder (local Python environment)
- .env files (API keys â€” NEVER in Git)
- __pycache__/ files and *.pyc
- Logs (*.log)

## RULE 6 : PROMPT REGISTRY CONSISTENCY
This rule applies to developer and scrum-master modes.

### 6.1 â€” Before any commit touching an artifact linked to a prompt
If you modify one of the following files: proxy.py, .roomodes, .clinerules, Modelfile
you MUST check whether the change impacts a system prompt in prompts/.

### 6.2 â€” Verification procedure
1. Read prompts/README.md to identify the affected prompt
2. Open the corresponding SP-XXX file in prompts/
3. If the prompt content must change: modify SP-XXX, increment its version
4. If SP-007 (Gem Gemini) is impacted: add a warning in the commit:
   "MANUAL DEPLOYMENT REQUIRED: update the Gem Gemini with SP-007"
5. Include the modified prompts/ files in the same commit as the target files

### 6.3 â€” Example commit with prompt update
  git add proxy.py prompts/SP-007-gem-gemini-roo-agent.md
  git commit -m "chore(prompts): mise a jour SP-007 suite modification proxy.py - DEPLOIEMENT MANUEL REQUIS"

## MEMORY BANK FILE TEMPLATES

### Template activeContext.md
---
# Active Context
**Last updated:** [DATE]
**Active mode:** [MODE]
**Active LLM backend:** [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]

## Current task
[Description of the current task]

## Last result
[Result of the last action]

## Next step(s)
- [ ] [Next immediate action]

## Blockers / Open questions
[None | Description of the blocker]

## Last Git commit
[Short hash and message of the last commit]
---

### Template progress.md
---
# Project Progress
**Last updated:** [DATE]

## le workbench Infrastructure
- [ ] Phase 0 : Clean VS Code + Roo Code base
- [ ] Phase 1 : Ollama + models
- [ ] Phase 2 : Git repository initialized
- [ ] Phase 3 : Custom Modelfile
- [ ] Phase 4 : .roomodes (Agile personas)
- [ ] Phase 5 : Memory Bank + .clinerules
- [ ] Phase 6 : proxy.py (Gemini Chrome)
- [ ] Phase 7 : Gem Gemini configured
- [ ] Phase 8 : Roo Code 3-mode switcher
- [ ] Phase 9 : End-to-end tests validated
- [ ] Phase 10 : Anthropic Claude API configured
- [ ] Phase 11 : prompts/ registry initialized
- [ ] Phase 12 : check-prompts-sync.ps1 + pre-commit hook

## Product Features

### Epic 1 : [To be defined]
- [ ] [Feature to be defined]

## Legend
- [ ] To do  |  [-] In progress  |  [x] Done
---
```

Save (Ctrl+S).

> **Why CHECKâ†’CREATEâ†’READâ†’ACT?** Without the prior check, the agent would attempt to read a non-existent file and fail silently. The sequence guarantees that the Memory Bank is always initialized before being read.

---

### Step 5.2 â€” Create the Memory Bank Structure

```powershell
# Create the memory-bank folder and the 7 files
New-Item -Path "." -Name "memory-bank" -ItemType Directory
New-Item -Path "memory-bank" -Name "projectBrief.md" -ItemType File
New-Item -Path "memory-bank" -Name "productContext.md" -ItemType File
New-Item -Path "memory-bank" -Name "systemPatterns.md" -ItemType File
New-Item -Path "memory-bank" -Name "techContext.md" -ItemType File
New-Item -Path "memory-bank" -Name "activeContext.md" -ItemType File
New-Item -Path "memory-bank" -Name "progress.md" -ItemType File
New-Item -Path "memory-bank" -Name "decisionLog.md" -ItemType File
```

---

### Step 5.3 â€” Fill `memory-bank/projectBrief.md`

Open `memory-bank/projectBrief.md` and paste:

```markdown
# Project Brief

## Project Vision
[Describe the overall vision of your project in 2-3 sentences]

## Main Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

## Non-Goals (What this project does NOT do)
- [Non-goal 1]
- [Non-goal 2]

## Constraints
- [Technical or business constraint]

## Stakeholders
- Product Owner: [Name]
- Target users: [Description]
```

> **Note:** This file is filled in once at the start of the project. It only changes if the project vision changes fundamentally.

---

### Step 5.4 â€” Fill `memory-bank/productContext.md`

Open `memory-bank/productContext.md` and paste:

```markdown
# Product Context

## User Stories for the Current Sprint

### Sprint [N] â€” [Dates]

#### US-001: [Title]
**As a** [persona]
**I want** [action]
**So that** [benefit]
**Acceptance criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Backlog (Next Sprints)
- [ ] [Upcoming feature 1]
- [ ] [Upcoming feature 2]
```

---

### Step 5.5 â€” Fill `memory-bank/systemPatterns.md`

Open `memory-bank/systemPatterns.md` and paste:

```markdown
# System Patterns

## Folder Architecture
[Paste the tree structure of your project here]

## Naming Conventions
- Files: [convention, e.g.: kebab-case]
- Variables: [convention, e.g.: camelCase]
- Classes: [convention, e.g.: PascalCase]
- Constants: [convention, e.g.: UPPER_SNAKE_CASE]

## Adopted Technical Patterns
- [Pattern 1: e.g.: Repository Pattern for data access]
- [Pattern 2: e.g.: Service Layer for business logic]

## Anti-Patterns to Avoid
- [Anti-pattern 1]
```

---

### Step 5.6 â€” Fill `memory-bank/techContext.md`

Open `memory-bank/techContext.md` and paste:

```markdown
# Tech Context

## Technology Stack
- Main language: [e.g.: Python 3.11]
- Framework: [e.g.: FastAPI 0.110]
- Database: [e.g.: SQLite / PostgreSQL]
- Tests: [e.g.: pytest]

## Essential Commands
```bash
pip install -r requirements.txt
python main.py
pytest tests/
```

## Required Environment Variables
- `[VAR_NAME]`: [Description and default value]

## Critical Dependencies and Versions
| Package | Version | Reason |
| :--- | :--- | :--- |
| [package] | [version] | [reason] |

## LLM Backend Configuration (le workbench Switcher)

### Mode 1: Local Ollama (Sovereign and Free â€” via Tailscale)
- API Provider: Ollama
- Base URL: http://calypso:11434
- Model: uadf-agent
- Prerequisites: Tailscale active on `pc` and `calypso`, Ollama running on `calypso`

### Mode 2: Gemini Chrome Proxy (Free Cloud + Copy-Paste)
- API Provider: OpenAI Compatible
- Base URL: http://localhost:8000/v1
- API Key: sk-fake-key-uadf
- Model: gemini-manual
- Prerequisites: proxy.py started + Chrome open on Gem "Roo Code Agent"

### Mode 3: Direct Cloud Claude Sonnet (Paid and Fully Automatic)
- API Provider: Anthropic
- Model: claude-sonnet-4-6
- API Key: [stored in VS Code SecretStorage â€” never write here]
- Prerequisites: Internet connection + available Anthropic credit
```

---

### Step 5.7 â€” Fill `memory-bank/activeContext.md`

Open `memory-bank/activeContext.md` and paste:

```markdown
# Active Context

**Last updated:** 2026-03-23
**Active mode:** developer
**Active LLM backend:** Ollama uadf-agent

## Current task
Initialization of the le workbench project â€” Development environment configuration.

## Last result
Initial project structure created. Memory Bank initialized. Git repository initialized.

## Next step(s)
- [ ] Complete information in projectBrief.md
- [ ] Define the first User Stories in productContext.md
- [ ] Configure the Gemini Chrome proxy (proxy.py)
- [ ] Configure the Gemini Chrome Gem

## Blockers / Open questions
No blockers identified at this time.

## Last Git commit
[To be filled after the first Memory Bank commit]
```

---

### Step 5.8 â€” Fill `memory-bank/progress.md`

Open `memory-bank/progress.md` and paste:

```markdown
# Project Progress

**Last updated:** 2026-03-23

## le workbench Infrastructure

### Setup Phase
- [x] Phase 0: Clean VS Code + Roo Code base (clean reinstallation)
- [x] Phase 1: Ollama + Qwen3-32B and 7B models installed
- [x] Phase 2: Git repository initialized with complete .gitignore
- [x] Phase 3: Custom Modelfile (uadf-agent, T=0.15, ctx=131072)
- [x] Phase 4: .roomodes (4 Agile personas with Git rules)
- [x] Phase 5: Memory Bank (7 files) + .clinerules (6 rules)
- [ ] Phase 6: proxy.py (Gemini Chrome server, SSE)
- [ ] Phase 7: Gemini Chrome Gem configured
- [ ] Phase 8: Roo Code 3-mode LLM switcher
- [ ] Phase 9: End-to-end tests validated
- [ ] Phase 10: Anthropic Claude Sonnet API configured
- [ ] Phase 11: prompts/ registry initialized
- [ ] Phase 12: check-prompts-sync.ps1 + pre-commit hook

## Product Features

### Epic 1: [To be defined]
- [ ] [Feature to be defined]

## Legend
- [ ] To do  |  [-] In progress  |  [x] Done
```

---

### Step 5.9 â€” Fill `memory-bank/decisionLog.md`

Open `memory-bank/decisionLog.md` and paste:

```markdown
# Decision Log â€” Architecture Decision Records (ADR)

---

## ADR-001: Choice of local inference engine
**Date:** 2026-03-23
**Status:** Accepted

**Context:**
Need for a local LLM inference engine, free and compatible with the OpenAI API for Roo Code.

**Decision:**
Use of Ollama with the model mychen76/qwen3_cline_roocode:32b compiled as uadf-agent.

**Consequences:**
- Advantage: Total sovereignty, free, OpenAI-compatible
- Advantage: Model specifically optimized for Roo Code Tool Calling
- Disadvantage: Requires 20+ GB of storage and 16+ GB of RAM

---

## ADR-002: Gemini Chrome Proxy Architecture
**Date:** 2026-03-23
**Status:** Accepted

**Context:**
Need to use Gemini Chrome for free from Roo Code without modifying its behavior.

**Decision:**
Local FastAPI server emulating the OpenAI API, with clipboard relay for human intervention.
SSE streaming in a single chunk for full compatibility with Roo Code (DA-014).

**Consequences:**
- Advantage: Roo Code unmodified, native compatibility
- Advantage: Gemini Chrome completely free
- Disadvantage: Requires human intervention (copy-paste) for each request

---

## ADR-003: Full Git versioning of all le workbench artifacts
**Date:** 2026-03-23
**Status:** Accepted

**Context:**
Need to track the evolution of all system artifacts: code, prompts, scripts, Memory Bank.

**Decision:**
Git versions EVERYTHING (code, .clinerules, .roomodes, Modelfile, proxy.py, memory-bank/).
The commit rule is embedded in .clinerules (RULE 5) AND in the roleDefinitions
of the Developer and Scrum Master for self-contained defense in depth.

**Consequences:**
- Advantage: Complete traceability of system evolution
- Advantage: Ability to rollback any artifact
- Advantage: Self-contained behavior: the AI itself maintains versioning
- Disadvantage: Requires consistent commit discipline
```

---

### Step 5.10 â€” Create the `docs/qa/` Folder

```powershell
New-Item -Path "." -Name "docs" -ItemType Directory
New-Item -Path "docs" -Name "qa" -ItemType Directory
New-Item -Path "docs/qa" -Name ".gitkeep" -ItemType File
```

> **Why `docs/qa/` now?** The Scrum Master reads QA reports in `docs/qa/`. This folder must exist before the first Scrum Master session to avoid a read error.

---

### Step 5.11 â€” Version the Memory Bank and `.clinerules`

```powershell
git add .clinerules memory-bank/ docs/
git commit -m "feat(workbench): Memory Bank (7 files) + .clinerules (6 rules CHECKâ†’CREATEâ†’READâ†’ACT)"
```

**Phase 5 Validation Criterion:**
1. Open Roo Code and start a new session in Developer mode
2. The agent must automatically read `memory-bank/activeContext.md` and `memory-bank/progress.md` before responding
3. If you ask "What is the project status?", the agent must respond based on the content of `progress.md`

> **If the agent does not use the Memory Bank:** Verify that `.clinerules` is at the project root (not in a subfolder). Reload VS Code (`Ctrl+Shift+P` > "Developer: Reload Window").

---

## PHASE 6: Gemini Chrome Proxy â€” `template/proxy.py` v2.1.0 with SSE

**Objective:** Create the Python FastAPI proxy server that relays Roo Code requests to Gemini Chrome via the Windows clipboard, with transparent SSE support.
**Requirements addressed:** REQ-2.1.1 to REQ-2.4.4
**Architecture decisions:** DA-006, DA-007, DA-008, DA-009, DA-014

---

### Step 6.1 â€” Create the Python Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **If PowerShell execution policy error:**
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then rerun `.\venv\Scripts\Activate.ps1`. You must see `(venv)` at the beginning of the prompt.

---

### Step 6.2 â€” Install Python Dependencies

```powershell
pip install fastapi uvicorn pyperclip pydantic
pip freeze > requirements.txt
```

> **Minimum required versions:** `fastapi>=0.110.0`, `uvicorn>=0.27.0`, `pyperclip>=1.8.2`, `pydantic>=2.0.0`

---

### Step 6.3 â€” Create `template/proxy.py` v2.1.0

Create `template/proxy.py` at the project root. Canonical source: [`SP-007-gem-gemini-roo-agent.md`](../prompts/SP-007-gem-gemini-roo-agent.md) for the system prompt of the associated Gem.

> **Version note:** The `template/proxy.py` file in this repository is at version **v2.1.0** (10 robustness fixes applied since the initial v2.0). The code below is the original v2.0 reference version. For the complete version with all fixes, consult [`template/proxy.py`](../template/proxy.py) directly.
>
> **Changelog v2.0 â†’ v2.1.0:**
> - `v2.0.1` â€” FIX-001: Multi-line console with NEW conversation warning (GAP-006)
> - `v2.0.2` â€” FIX-004: `try/except` around `pyperclip.paste()` to avoid crash if clipboard is locked (P-003)
> - `v2.0.3` â€” FIX-005: Request counter in console to distinguish concurrent requests (P-002)
> - `v2.0.4` â€” FIX-006: Minimum length check of pasted content (GAP-005)
> - `v2.0.5` â€” FIX-008: Automatic history truncation via `MAX_HISTORY_CHARS` (GAP-001)
> - `v2.0.6` â€” FIX-014: BLOCKING minimum length check (100 char threshold) to avoid parasitic content injection (REG-001)
> - `v2.0.7` â€” FIX-015: Runtime guard `<new_task>` in `_wait_clipboard()` to avoid deadlock (GAP R1-003)
> - `v2.0.8` â€” FIX-016: Truncation fallback in `_format_prompt()` when a single message exceeds `MAX_HISTORY_CHARS` (REG-002)
> - `v2.0.9` â€” FIX-017: `asyncio.Lock()` for clipboard serialization (GAP R1-004)
> - `v2.1.0` â€” FIX-018: Remove "or clear existing history" â€” ALWAYS NEW conversation (GAP R1-001)

```python
"""
le workbench Proxy v2.0 â€” Bridge Roo Code <-> Gemini Chrome
Supports stream=true (SSE) and stream=false (complete JSON).
Requirements: REQ-2.1.1 to REQ-2.4.4
"""
import asyncio, hashlib, json, os, time, uuid
from datetime import datetime
from typing import AsyncGenerator, List, Optional, Union

import pyperclip, uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

USE_GEM_MODE = os.getenv("USE_GEM_MODE", "true").lower() == "true"
POLLING_INTERVAL = float(os.getenv("POLLING_INTERVAL", "1.0"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "300"))
PORT = int(os.getenv("PROXY_PORT", "8000"))

ROO_XML_TAGS = [
    "<write_to_file>", "<read_file>", "<execute_command>",
    "<attempt_completion>", "<ask_followup_question>", "<replace_in_file>",
    "<list_files>", "<search_files>", "<browser_action>", "<new_task>"
]

class MessageContent(BaseModel):
    role: str
    content: Union[str, list]

class ChatRequest(BaseModel):
    model: str
    messages: List[MessageContent]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

app = FastAPI(title="le workbench Proxy", version="2.0.0")

def _hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def _clean_content(content) -> str:
    """Clean content: remove base64 images. REQ-2.1.5"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif item.get("type") == "image_url":
                    parts.append("[IMAGE OMITTED - Not supported by clipboard proxy]")
                else:
                    parts.append(str(item))
        return "\n".join(parts)
    return str(content)

def _format_prompt(messages: List[MessageContent]) -> str:
    """Format messages as readable text. REQ-2.1.3, REQ-2.1.4, REQ-2.2.2"""
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if not content.strip():
            continue
        if msg.role == "system":
            if USE_GEM_MODE:
                continue  # Filter system prompt in Gem mode (DA-008)
            parts.append("[SYSTEM PROMPT]\n" + content)
        elif msg.role == "user":
            parts.append("[USER]\n" + content)
        elif msg.role == "assistant":
            parts.append("[ASSISTANT]\n" + content)
    return "\n\n---\n\n".join(parts)

def _validate_response(text: str) -> bool:
    """Check for presence of Roo Code XML tags. REQ-2.3.4"""
    return any(tag in text for tag in ROO_XML_TAGS)

def _build_json_response(content: str, model: str) -> dict:
    """Build an OpenAI JSON response. REQ-2.4.2"""
    return {
        "id": "chatcmpl-proxy-" + uuid.uuid4().hex[:8],
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }

async def _stream_response(content: str, model: str) -> AsyncGenerator[str, None]:
    """Generate an SSE response in a single chunk. REQ-2.4.1, DA-014"""
    rid = "chatcmpl-proxy-" + uuid.uuid4().hex[:8]
    ts = int(time.time())
    chunk = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
             "choices": [{"index": 0, "delta": {"role": "assistant", "content": content}, "finish_reason": None}]}
    yield f"data: {json.dumps(chunk)}\n\n"
    done = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}
    yield f"data: {json.dumps(done)}\n\n"
    yield "data: [DONE]\n\n"

async def _wait_clipboard(initial_hash: str, ts: str) -> str:
    """Wait for Gemini response in the clipboard. REQ-2.3.1, REQ-2.3.2, REQ-2.3.3"""
    start = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)
        current = pyperclip.paste()
        if _hash(current) != initial_hash:
            elapsed = time.time() - start
            print(f"[{ts}] RESPONSE DETECTED! {len(current)} chars in {elapsed:.1f}s")
            if not _validate_response(current):
                print(f"[{ts}] WARNING: No Roo Code XML tags detected.")
            return current
        if time.time() - start > TIMEOUT_SECONDS:
            raise HTTPException(status_code=408, detail="Timeout: Relaunch your request in Roo Code.")

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Main entry point. REQ-2.1.1, REQ-2.1.2"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*60}\n[{ts}] REQUEST | model: {request.model} | stream: {request.stream}")
    formatted = _format_prompt(request.messages)
    pyperclip.copy(formatted)
    initial_hash = _hash(formatted)
    print(f"[{ts}] {'GEM MODE' if USE_GEM_MODE else 'FULL MODE'} | {len(formatted)} chars")
    print(f"[{ts}] PROMPT COPIED! ACTION: 1.Chrome 2.Gem 3.Ctrl+V 4.Wait 5.Ctrl+A+C")
    print(f"         Timeout in {TIMEOUT_SECONDS}s...")
    response_text = await _wait_clipboard(initial_hash, ts)
    if request.stream:
        return StreamingResponse(_stream_response(response_text, request.model), media_type="text/event-stream")
    return JSONResponse(content=_build_json_response(response_text, request.model), status_code=200)

@app.get("/v1/models")
async def list_models():
    return JSONResponse({"object": "list", "data": [{"id": "gemini-manual", "object": "model", "created": int(time.time()), "owned_by": "uadf-proxy"}]})

@app.get("/health")
async def health_check():
    return {"status": "ok", "proxy": "le workbench", "version": "2.0.0", "gem_mode": USE_GEM_MODE}

if __name__ == "__main__":
    print(f"{'='*60}\n  le workbench PROXY v2.0 | http://localhost:{PORT}/v1\n  Mode: {'GEM' if USE_GEM_MODE else 'FULL'} | Timeout: {TIMEOUT_SECONDS}s\n{'='*60}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
```

> **Key points of the code:**
> - `USE_GEM_MODE=true` (default): filters the `system` message â€” the system prompt is in the Gem (DA-008)
> - `_stream_response()`: returns the response in a single SSE chunk followed by `[DONE]` â€” transparent for Roo Code (DA-014)
> - `_wait_clipboard()`: non-blocking asynchronous polling every second (DA-006)
> - `_validate_response()`: non-blocking warning if no XML tags (REQ-2.3.4)

---

### Step 6.4 â€” Create the Startup Script `scripts/start-proxy.ps1`

```powershell
New-Item -Path "." -Name "scripts" -ItemType Directory
```

Create `scripts/start-proxy.ps1`:

```powershell
# le workbench Proxy â€” Startup script
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
& ".\venv\Scripts\Activate.ps1"
Write-Host "Starting le workbench Proxy v2.0..." -ForegroundColor Green
Write-Host "URL: http://localhost:8000/v1" -ForegroundColor Cyan
python proxy.py
```

---

### Step 6.5 â€” Test the Proxy

**Terminal 1 â€” Start the proxy:**
```powershell
.\venv\Scripts\Activate.ps1
python proxy.py
```

Expected output:
```
============================================================
  le workbench PROXY v2.0 | http://localhost:8000/v1
  Mode: GEM | Timeout: 300s
============================================================
```

**Terminal 2 â€” Test `/health`:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```
Expected response: `{"status": "ok", "proxy": "le workbench", "version": "2.0.0", "gem_mode": true}`

**Terminal 2 â€” Test `/v1/models`:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/v1/models" -Method Get
```
Expected response: list containing `"id": "gemini-manual"`.

---

### Step 6.6 â€” Version `template/proxy.py` and Scripts

```powershell
git add proxy.py requirements.txt scripts/
git commit -m "feat(proxy): proxy.py v2.0 FastAPI SSE â€” bridge Roo Code <-> Gemini Chrome"
```

**Phase 6 Validation Criterion:**
- `python proxy.py` starts without error
- `http://localhost:8000/health` responds `{"status": "ok"}`
- `http://localhost:8000/v1/models` responds with `gemini-manual`

---

## PHASE 7: Gemini Chrome Configuration â€” Gem "Roo Code Agent"

**Objective:** Create a dedicated Gemini Gem with the integrated Roo Code system prompt, to avoid retransmitting the system prompt with each request via the clipboard.
**Requirements addressed:** REQ-5.1, REQ-5.2, REQ-5.3
**Architecture decisions:** DA-010

---

### Step 7.1 â€” Create the Gemini Gem "Roo Code Agent"

1. Open **Google Chrome** (not another browser)
2. Go to **https://gemini.google.com**
3. Sign in with your Google account
4. In the left sidebar menu, click **"Gems"**
5. Click **"New Gem"**
6. Give the name: **`Roo Code Agent`**
7. In the **"Instructions"** field, paste **exactly** this text (canonical source: [`SP-007-gem-gemini-roo-agent.md`](../prompts/SP-007-gem-gemini-roo-agent.md)):

```
Tu es un agent de developpement logiciel expert qui travaille en collaboration avec Roo Code (extension VS Code).

TON ROLE :
Tu recois des demandes de Roo Code via un systeme de relai clipboard (proxy). Tu dois analyser ces demandes et fournir des reponses structurees que Roo Code pourra interpreter et executer.

FORMAT DE REPONSE OBLIGATOIRE :
Tu DOIS toujours structurer tes reponses avec les balises XML suivantes selon le type d'action :

Pour lire un fichier :
<read_file>
<path>chemin/vers/fichier</path>
</read_file>

Pour ecrire dans un fichier :
<write_to_file>
<path>chemin/vers/fichier</path>
<content>
contenu complet du fichier
</content>
</write_to_file>

Pour executer une commande terminal :
<execute_command>
<command>commande a executer</command>
</execute_command>

Pour rechercher dans les fichiers :
<search_files>
<path>dossier/de/recherche</path>
<regex>pattern de recherche</regex>
</search_files>

Pour terminer une tache :
<attempt_completion>
<result>
Description du resultat accompli
</result>
</attempt_completion>

REGLES IMPORTANTES :
1. Toujours utiliser les balises XML ci-dessus pour les actions â€” jamais de texte libre pour les actions
2. Toujours lire la Memory Bank (memory-bank/) avant d'agir sur le code
3. Toujours mettre a jour memory-bank/activeContext.md apres chaque action significative
4. Toujours effectuer un commit Git apres chaque modification de fichier
5. Etre concis et precis dans les descriptions â€” eviter les explications superflues
6. Si une tache est ambigue, demander une clarification avant d'agir

CONTEXTE DU PROJET :
Tu travailles sur un projet utilisant le framework le workbench (Agentic Agile Workbench).
Le projet utilise une equipe Agile virtuelle avec 4 personas : Product Owner, Scrum Master, Developer, QA Engineer.
La memoire persistante est stockee dans le dossier memory-bank/ (7 fichiers Markdown).
```

8. Click **"Save"**

> **IMPORTANT â€” Mandatory manual deployment:** This prompt is the only one in the le workbench registry that cannot be deployed automatically via Git. Any future modification to this Gem must be accompanied by a Git commit with the mention: `"MANUAL DEPLOYMENT REQUIRED: update the Gem Gemini with SP-007"` (see RULE 6.2 of `.clinerules`).

---

### Step 7.2 â€” Verify the Gem Works Correctly

1. Open the "Roo Code Agent" Gem in Gemini
2. Send this test message:
   ```
   Lis le fichier memory-bank/activeContext.md
   ```
3. The Gem must respond **only** with:
   ```xml
   <read_file>
   <path>memory-bank/activeContext.md</path>
   </read_file>
   ```

> **If the Gem responds in free text without XML tags:** The instructions were not correctly saved. Redo step 7.1 making sure to paste the text in the "Instructions" field (not in the chat area).

---

### Step 7.3 â€” Configure Chrome for the Proxy Workflow

To use the proxy efficiently:

1. **Pin the Gemini tab** in Chrome (right-click on the tab > "Pin")
2. **Keep the "Roo Code Agent" Gem open** permanently during development sessions
3. **Workflow for each proxy request:**
   - The proxy displays in the terminal: `PROMPT COPIED! ACTION: 1.Chrome 2.Gem 3.Ctrl+V 4.Wait 5.Ctrl+A+C`
   - Switch to Chrome (`Alt+Tab`)
   - Click in the Gem input area
   - Paste (`Ctrl+V`) â€” the Roo Code prompt appears
   - Wait for Gemini's response
   - Select all (`Ctrl+A`) and copy (`Ctrl+C`)
   - The proxy automatically detects the clipboard change and returns the response to Roo Code

---

## PHASE 8: Roo Code â€” 3-Mode LLM Switcher

**Objective:** Configure Roo Code to switch between the 3 LLM backends (local Ollama, Gemini Chrome Proxy, Anthropic Claude API) via the "API Provider" parameter.
**Requirements addressed:** REQ-2.0, REQ-000
**Architecture decisions:** DA-007, DA-011

---

### Step 8.1 â€” Configure Mode 1: Local Ollama

1. In VS Code, click the **Roo Code** icon in the sidebar
2. Click the **âš™ï¸ Settings** icon (gear) at the top of the Roo Code panel
3. In the **"API Provider"** section, select **"Ollama"**
4. In **"Base URL"**, enter: `http://calypso:11434`
5. In **"Model"**, enter: `uadf-agent`
6. Save

**Mode 1 Validation Test:**
```powershell
ollama list
# Must show uadf-agent in the list
```
Then in Roo Code (Developer mode), send: `Dis bonjour en une phrase.`
The agent must respond via Ollama (verifiable in Ollama logs).

---

### Step 8.2 â€” Configure Mode 2: Gemini Chrome Proxy

1. In Roo Code Settings > **"API Provider"**, select **"OpenAI Compatible"**
2. In **"Base URL"**, enter: `http://localhost:8000/v1`
3. In **"API Key"**, enter: `sk-fake-key-uadf` (fictitious value required by Roo Code)
4. In **"Model"**, enter: `gemini-manual`
5. Save

**Mode 2 Validation Test:**
1. Start the proxy: `python proxy.py`
2. Open Chrome on the "Roo Code Agent" Gem
3. In Roo Code (Developer mode), send: `Dis bonjour en une phrase.`
4. The proxy must display: `PROMPT COPIED! ACTION: 1.Chrome 2.Gem 3.Ctrl+V 4.Wait 5.Ctrl+A+C`
5. Follow the proxy instructions (copy-paste in Chrome)
6. Roo Code must receive Gemini's response

---

### Step 8.3 â€” Configure Mode 3: Anthropic Claude API

> **Note:** This configuration is detailed in Phase 10. You can skip it for now and return after validating Modes 1 and 2.

1. In Roo Code Settings > **"API Provider"**, select **"Anthropic"**
2. In **"API Key"**, enter your Anthropic key (`sk-ant-api03-...`)
3. In **"Model"**, enter: `claude-sonnet-4-6`
4. Save

---

### Step 8.4 â€” Document the Switcher in `memory-bank/techContext.md`

Open `memory-bank/techContext.md` and complete the "LLM Backend Configuration" section with the actual values of your configuration (confirmed URLs, models).

```powershell
git add memory-bank/techContext.md
git commit -m "docs(memory): techContext.md updated with 3-mode LLM switcher configuration"
```

---

## PHASE 9: End-to-End Tests â€” Complete System Validation

**Objective:** Validate that the 3 LLM modes work correctly with the Memory Bank, Agile personas, and Git versioning.
**Requirements addressed:** REQ-000, REQ-4.2, REQ-4.3

---

### Step 9.1 â€” End-to-End Test Mode 1 (Ollama)

**Prerequisites:** Ollama running, `uadf-agent` available, Roo Code configured in Mode 1.

**Test scenario:**
1. Select **"Developer"** mode in Roo Code
2. Send: `Create a file src/hello.py with a hello() function that returns "Hello le workbench"`
3. **Expected behavior:**
   - The agent reads `memory-bank/activeContext.md` and `memory-bank/progress.md` (RULE 1 â€” CHECKâ†’CREATEâ†’READâ†’ACT sequence)
   - The agent creates `src/hello.py`
   - The agent updates `memory-bank/activeContext.md` (RULE 2)
   - The agent executes `git add . && git commit -m "feat(src): add hello.py"` (RULE 5)

**Verification:**
```powershell
Test-Path "src/hello.py"          # Must return True
git log --oneline -3              # Must show a recent commit with "feat(src)"
Get-Content "memory-bank/activeContext.md"  # Must mention the creation of hello.py
```

---

### Step 9.2 â€” End-to-End Test Mode 2 (Gemini Proxy)

**Prerequisites:** `python proxy.py` running, Chrome open on Gem "Roo Code Agent", Roo Code configured in Mode 2.

**Test scenario:**
1. Select **"QA Engineer"** mode in Roo Code
2. Send: `Create a test report in docs/qa/test-hello-2026-03-23.md`
3. **Expected behavior:**
   - The proxy displays copy-paste instructions in the terminal
   - You perform the copy-paste in Chrome/Gemini
   - Gemini responds with XML tags
   - The proxy returns the response to Roo Code (via SSE or JSON depending on `stream`)
   - The agent creates the report in `docs/qa/`
   - The agent CANNOT modify `src/hello.py` (RBAC QA Engineer)

**Verification:**
```powershell
Test-Path "docs/qa/test-hello-2026-03-23.md"  # Must return True
git log --oneline -3                           # Must show a recent commit
```

---

### Step 9.3 â€” Complete RBAC Test

| Mode | Request | Expected Behavior |
| :--- | :--- | :--- |
| Product Owner | "Write Python code" | Refused â€” out of scope |
| Product Owner | "Create a User Story" | Accepted â€” writes in `memory-bank/productContext.md` |
| Scrum Master | "Run pytest" | Refused â€” no test execution |
| Scrum Master | "What is the test status?" | Accepted â€” reads `docs/qa/` and responds |
| Developer | "Modify src/hello.py" | Accepted â€” modifies the file and commits |
| QA Engineer | "Modify src/hello.py" | Refused â€” out of scope |
| QA Engineer | "Run pytest" | Accepted â€” executes tests |

---

### Step 9.4 â€” Version the Test Results

```powershell
git add src/ docs/ memory-bank/
git commit -m "test(e2e): complete validation 3 LLM modes + RBAC + Memory Bank"
```

**Phase 9 Validation Criterion:**
- The 3 LLM modes respond correctly
- The Memory Bank is read and updated at each session
- RBAC blocks out-of-scope actions for each persona
- Each action is versioned in Git with a Conventional Commits message

---

## PHASE 10: Anthropic Claude API â€” Direct Cloud Mode

**Objective:** Configure the direct connection to the Anthropic API with the `claude-sonnet-4-6` model, without an intermediate proxy.
**Requirements addressed:** REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4
**Architecture decisions:** DA-011

---

### Step 10.1 â€” Obtain an Anthropic API Key

1. Go to **https://console.anthropic.com**
2. Create an account or sign in
3. In **"API Keys"**, click **"Create Key"**
4. Give a name: `roo-code-agent`
5. Copy the key (`sk-ant-api03-...`) â€” **it will only be displayed once**

> **ABSOLUTE SECURITY:** Never store this key in a project file. Never commit it to Git. VS Code SecretStorage is the only authorized location (DA-011, REQ-6.4).

---

### Step 10.2 â€” Configure Roo Code with the Anthropic Key

1. In VS Code, open Roo Code Settings
2. In **"API Provider"**, select **"Anthropic"**
3. In **"API Key"**, paste your key `sk-ant-api03-...`
4. In **"Model"**, enter: `claude-sonnet-4-6`
5. Save

> **Maintenance note (REQ-6.2):** The model `claude-sonnet-4-6` is the reference version as of 2026-03-23. Anthropic regularly publishes new versions. To check the latest available version: https://docs.anthropic.com/en/docs/about-claude/models. Update this field, REQ-6.2 in DOC1, and DA-011 in DOC2 with each major update.

---

### Step 10.3 â€” Test the Anthropic Connection

In Roo Code (Developer mode), send:
```
Say hello and indicate which model you are.
```

**Expected behavior:**
- The response arrives without human intervention (unlike Mode 2)
- The response uses Roo Code XML tags
- The Memory Bank is read and updated automatically
- A Git commit is performed automatically

---

### Step 10.4 â€” Verify API Key Security

```powershell
# Verify that the key is NOT in the project files
Select-String -Path "*.py", "*.md", "*.json", "*.txt", "*.env" -Pattern "sk-ant-api" -Recurse
# Must return NO results
```

> **If the key appears in the results:** Remove it immediately from the file, invalidate the key on console.anthropic.com, and create a new one. Verify that `.gitignore` contains `*.env`.

---

### Step 10.5 â€” Version the Memory Bank Update

```powershell
git add memory-bank/
git commit -m "docs(memory): activeContext.md updated â€” Mode 3 Claude API validated"
```

**Phase 10 Validation Criterion:**
- Roo Code responds via the Anthropic API without proxy
- The API key is in no project file (`Select-String` returns empty)
- The Memory Bank is updated after the test session

---

## PHASE 11: Prompts Registry â€” Initialization of `prompts/`

**Objective:** Initialize the centralized system prompts registry in `prompts/` with the 7 canonical SP files and the `README.md` index.
**Requirements addressed:** REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5
**Architecture decisions:** DA-012

---

### Step 11.1 â€” Verify the Registry Structure

The `prompts/` folder should already exist if you cloned this repository. Verify:

```powershell
Get-ChildItem -Path "prompts/" -Name
```

Expected output:
```
README.md
SP-001-ollama-modelfile-system.md
SP-002-clinerules-global.md
SP-003-persona-product-owner.md
SP-004-persona-scrum-master.md
SP-005-persona-developer.md
SP-006-persona-qa-engineer.md
SP-007-gem-gemini-roo-agent.md
```

> **If the `prompts/` folder is absent:** Create it and the SP files manually following steps 11.2 to 11.4.

---

### Step 11.2 â€” Understand the Structure of a Canonical SP File

Each `SP-XXX-*.md` file in `prompts/` follows this structure:

```markdown
---
id: SP-XXX
name: [Descriptive name]
version: 1.0.0
last_updated: [DATE]
status: active

target_type: [ollama_modelfile | roo_clinerules | roo_roomodes | gemini_gem_instructions]
target_file: [Target file or EXTERNAL]
target_field: "[Exact field to modify in the target file]"
target_location: >
  [Detailed deployment instructions]

hors_git: [true | false]  # true only for SP-007

depends_on:
  - [SP-XXX]: "[Reason for the dependency]"

changelog:
  - version: 1.0.0
    date: [DATE]
    change: [Description of the change]
---

# SP-XXX â€” [Name]

## Prompt Content

> Copy this text exactly into [target].

[PROMPT CONTENT]

## Deployment Notes

[Step-by-step instructions]

## Impact on Other Prompts

[Dependencies and impacts]
```

> **Why this structure?** The YAML header allows the `check-prompts-sync.ps1` script (Phase 12) to automatically identify the deployment target and extract the content to compare.

---

### Step 11.3 â€” Verify the Consistency of Deployed Prompts

Manually verify that each deployed artifact matches its canonical SP:

| Canonical SP | Deployed Artifact | Verification |
| :--- | :--- | :--- |
| `SP-001` | `Modelfile` block `SYSTEM """..."""` | Compare content |
| `SP-002` | `.clinerules` (entire file) | Compare content |
| `SP-003` | `.roomodes` > `customModes[0].roleDefinition` | Compare JSON string |
| `SP-004` | `.roomodes` > `customModes[1].roleDefinition` | Compare JSON string |
| `SP-005` | `.roomodes` > `customModes[2].roleDefinition` | Compare JSON string |
| `SP-006` | `.roomodes` > `customModes[3].roleDefinition` | Compare JSON string |
| `SP-007` | Gemini Gem "Roo Code Agent" > Instructions | Manual verification |

---

### Step 11.4 â€” Version the Prompts Registry

```powershell
git add prompts/
git commit -m "feat(prompts): initialize canonical SP registry (SP-001 to SP-007)"
```

**Phase 11 Validation Criterion:**
- `prompts/` contains 8 files (README.md + 7 SPs)
- Each SP has a valid YAML header with `id`, `version`, `target_file`, `target_field`
- SP-007 is marked `hors_git: true`
- The content of each SP matches the deployed artifact

---

## PHASE 12: Automatic Verification â€” `check-prompts-sync.ps1` + Git Hook

**Objective:** Create the PowerShell prompt consistency verification script and the Git pre-commit hook that calls it automatically before each commit.
**Requirements addressed:** REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4
**Architecture decisions:** DA-013

---

### Step 12.1 â€” Create `template/scripts/check-prompts-sync.ps1`

Create `template/scripts/check-prompts-sync.ps1` and paste **exactly** this code:

```powershell
<#
.SYNOPSIS
    le workbench â€” Verification of consistency between canonical system prompts and deployed artifacts.
    REQ-8.1, REQ-8.3, REQ-8.4 | DA-013

.DESCRIPTION
    Compares the content of each canonical SP (prompts/SP-XXX-*.md) with the
    corresponding deployed artifact. Uses normalized comparison (CRLF->LF, trim).
    SP-007 (Gem Gemini) is excluded from automatic verification with a warning.
    Returns exit code 0 if everything is synchronized, 1 if desynchronization detected.
#>

param(
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PromptsDir = Join-Path $ProjectRoot "prompts"
$PassCount = 0
$FailCount = 0
$WarnCount = 0

function Normalize-Text {
    param([string]$Text)
    # Normalization: CRLF -> LF, trim leading/trailing spaces and line breaks
    return $Text.Replace("`r`n", "`n").Replace("`r", "`n").Trim()
}

function Extract-PromptContent {
    param([string]$SpFile)
    # Extract content between ```markdown or ``` tags (first code block)
    $content = Get-Content $SpFile -Raw -Encoding UTF8
    if ($content -match "(?s)```(?:markdown|python|)?\r?\n(.*?)\r?\n```") {
        return Normalize-Text $Matches[1]
    }
    return $null
}

function Show-Diff {
    param([string]$Expected, [string]$Actual, [string]$Label)
    $expLines = $Expected -split "`n"
    $actLines = $Actual -split "`n"
    $maxLines = [Math]::Max($expLines.Count, $actLines.Count)
    $diffLines = @()
    for ($i = 0; $i -lt [Math]::Min($maxLines, 20); $i++) {
        $e = if ($i -lt $expLines.Count) { $expLines[$i] } else { "" }
        $a = if ($i -lt $actLines.Count) { $actLines[$i] } else { "" }
        if ($e -ne $a) {
            $diffLines += "  Line $($i+1):"
            $diffLines += "    SP (expected) : $e"
            $diffLines += "    Deployed      : $a"
        }
    }
    if ($diffLines.Count -gt 0) {
        Write-Host "  First differences:" -ForegroundColor Yellow
        $diffLines | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }
}

Write-Host ""
Write-Host "=" * 60
Write-Host "  le workbench â€” Prompt Consistency Verification" -ForegroundColor Cyan
Write-Host "=" * 60

# --- SP-001: Modelfile ---
Write-Host ""
Write-Host "[SP-001] Modelfile SYSTEM block..." -NoNewline
$ModelfilePath = Join-Path $ProjectRoot "Modelfile"
$Sp001Path = Join-Path $PromptsDir "SP-001-ollama-modelfile-system.md"
if (-not (Test-Path $ModelfilePath)) {
    Write-Host " SKIP (Modelfile absent)" -ForegroundColor Yellow
    $WarnCount++
} else {
    $spContent = Extract-PromptContent $Sp001Path
    $modelfileRaw = Get-Content $ModelfilePath -Raw -Encoding UTF8
    if ($modelfileRaw -match '(?s)SYSTEM\s+"""(.*?)"""') {
        $deployedContent = Normalize-Text $Matches[1]
        if ($spContent -eq $deployedContent) {
            Write-Host " PASS" -ForegroundColor Green
            $PassCount++
        } else {
            Write-Host " FAIL" -ForegroundColor Red
            Show-Diff $spContent $deployedContent "SP-001"
            $FailCount++
        }
    } else {
        Write-Host " FAIL (SYSTEM block not found in Modelfile)" -ForegroundColor Red
        $FailCount++
    }
}

# --- SP-002: .clinerules ---
Write-Host "[SP-002] .clinerules (entire file)..." -NoNewline
$ClinerPath = Join-Path $ProjectRoot ".clinerules"
$Sp002Path = Join-Path $PromptsDir "SP-002-clinerules-global.md"
if (-not (Test-Path $ClinerPath)) {
    Write-Host " SKIP (.clinerules absent)" -ForegroundColor Yellow
    $WarnCount++
} else {
    $spContent = Extract-PromptContent $Sp002Path
    $deployedContent = Normalize-Text (Get-Content $ClinerPath -Raw -Encoding UTF8)
    if ($spContent -eq $deployedContent) {
        Write-Host " PASS" -ForegroundColor Green
        $PassCount++
    } else {
        Write-Host " FAIL" -ForegroundColor Red
        Show-Diff $spContent $deployedContent "SP-002"
        $FailCount++
    }
}

# --- SP-003 to SP-006: .roomodes ---
$RoomodesPath = Join-Path $ProjectRoot ".roomodes"
$SpPersonas = @(
    @{ Id = "SP-003"; File = "SP-003-persona-product-owner.md"; Slug = "product-owner"; Index = 0 },
    @{ Id = "SP-004"; File = "SP-004-persona-scrum-master.md"; Slug = "scrum-master"; Index = 1 },
    @{ Id = "SP-005"; File = "SP-005-persona-developer.md"; Slug = "developer"; Index = 2 },
    @{ Id = "SP-006"; File = "SP-006-persona-qa-engineer.md"; Slug = "qa-engineer"; Index = 3 }
)

if (-not (Test-Path $RoomodesPath)) {
    Write-Host "[SP-003..006] .roomodes absent â€” SKIP" -ForegroundColor Yellow
    $WarnCount += 4
} else {
    $roomodesJson = Get-Content $RoomodesPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($persona in $SpPersonas) {
        Write-Host "[$($persona.Id)] .roomodes > $($persona.Slug) roleDefinition..." -NoNewline
        $spFile = Join-Path $PromptsDir $persona.File
        $spContent = Extract-PromptContent $spFile
        $mode = $roomodesJson.customModes | Where-Object { $_.slug -eq $persona.Slug }
        if ($null -eq $mode) {
            Write-Host " FAIL (slug '$($persona.Slug)' not found in .roomodes)" -ForegroundColor Red
            $FailCount++
        } else {
            $deployedContent = Normalize-Text $mode.roleDefinition
            if ($spContent -eq $deployedContent) {
                Write-Host " PASS" -ForegroundColor Green
                $PassCount++
            } else {
                Write-Host " FAIL" -ForegroundColor Red
                Show-Diff $spContent $deployedContent $persona.Id
                $FailCount++
            }
        }
    }
}

# --- SP-007: Gem Gemini (outside Git â€” manual verification) ---
Write-Host ""
Write-Host "[SP-007] Gem Gemini 'Roo Code Agent'..." -NoNewline
Write-Host " WARNING (manual deployment required)" -ForegroundColor Yellow
Write-Host "  -> Verify manually at https://gemini.google.com > Gems > 'Roo Code Agent'"
Write-Host "  -> Compare with: prompts/SP-007-gem-gemini-roo-agent.md"
$WarnCount++

# --- Summary ---
Write-Host ""
Write-Host "=" * 60
Write-Host "  SUMMARY: $PassCount PASS | $FailCount FAIL | $WarnCount WARN" -ForegroundColor $(if ($FailCount -gt 0) { "Red" } elseif ($WarnCount -gt 0) { "Yellow" } else { "Green" })
Write-Host "=" * 60
Write-Host ""

if ($FailCount -gt 0) {
    Write-Host "FAILURE: $FailCount prompt(s) out of sync. Commit blocked." -ForegroundColor Red
    Write-Host "Required action: update the deployed artifacts to match the canonical SPs." -ForegroundColor Red
    exit 1
} else {
    Write-Host "SUCCESS: All verifiable prompts are synchronized." -ForegroundColor Green
    exit 0
}
```

---

### Step 12.2 â€” Create the Git `pre-commit` Hook

```powershell
# Create the pre-commit hook file
$hookContent = @'
#!/bin/sh
# le workbench â€” pre-commit hook: prompt consistency verification (REQ-8.2, DA-013)
echo "le workbench pre-commit: verifying prompt consistency..."
powershell.exe -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"
if [ $? -ne 0 ]; then
    echo "COMMIT BLOCKED: Desynchronization detected in prompts."
    echo "Fix the desynchronizations before committing."
    exit 1
fi
exit 0
'@

$hookPath = Join-Path $ProjectRoot ".git/hooks/pre-commit"
Set-Content -Path $hookPath -Value $hookContent -Encoding UTF8 -NoNewline
```

> **Windows note:** The Git hook is a shell script (`#!/bin/sh`). Git for Windows executes hooks via its integrated shell (Git Bash). The `powershell.exe` command is available in Git Bash on Windows.

---

### Step 12.3 â€” Test the Verification Script

```powershell
# Manually test the script
.\venv\Scripts\Activate.ps1  # If necessary for the environment
powershell.exe -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"
```

**Expected output (everything synchronized):**
```
============================================================
  le workbench â€” Prompt Consistency Verification
============================================================

[SP-001] Modelfile SYSTEM block... PASS
[SP-002] .clinerules (entire file)... PASS
[SP-003] .roomodes > product-owner roleDefinition... PASS
[SP-004] .roomodes > scrum-master roleDefinition... PASS
[SP-005] .roomodes > developer roleDefinition... PASS
[SP-006] .roomodes > qa-engineer roleDefinition... PASS

[SP-007] Gem Gemini 'Roo Code Agent'... WARNING (manual deployment required)
  -> Verify manually at https://gemini.google.com > Gems > 'Roo Code Agent'
  -> Compare with: prompts/SP-007-gem-gemini-roo-agent.md

============================================================
  SUMMARY: 6 PASS | 0 FAIL | 1 WARN
============================================================

SUCCESS: All verifiable prompts are synchronized.
```

---

### Step 12.4 â€” Test Commit Blocking on Desynchronization

To test that the hook correctly blocks a commit on desynchronization:

```powershell
# 1. Temporarily modify .clinerules to create a desynchronization
Add-Content -Path ".clinerules" -Value "`n# TEST DESYNC"

# 2. Attempt a commit â€” must be blocked
git add .clinerules
git commit -m "test: verify pre-commit hook blocking"
# Expected: "COMMIT BLOCKED: Desynchronization detected in prompts."

# 3. Restore .clinerules
git checkout .clinerules
```

---

### Step 12.5 â€” Version the Scripts and Hook

```powershell
git add scripts/check-prompts-sync.ps1
git commit -m "feat(prompts): check-prompts-sync.ps1 + pre-commit hook â€” automatic consistency verification"
```

> **Note:** The `.git/hooks/pre-commit` hook is NOT versioned in Git (the `.git/` folder is excluded). Each developer who clones the repository must recreate the hook by executing step 12.2.

---

**Phase 12 Validation Criterion:**
- `scripts/check-prompts-sync.ps1` runs without error and displays `6 PASS | 0 FAIL`
- A commit with modified `.clinerules` is blocked by the pre-commit hook
- Restoring `.clinerules` unblocks the commit

---

## Final Summary â€” Complete le workbench System

### Project Tree After the 13 Phases

```
[PROJECT ROOT]
â”œâ”€â”€ .clinerules              # 6 mandatory rules (SP-002) â€” CHECKâ†’CREATEâ†’READâ†’ACT
â”œâ”€â”€ .gitignore               # venv/, .env, __pycache__, *.log
â”œâ”€â”€ .roomodes                # 4 Agile RBAC personas (SP-003 to SP-006)
â”œâ”€â”€ Modelfile                # uadf-agent model (SP-001) â€” T=0.15, ctx=131072
â”œâ”€â”€ proxy.py                 # Gemini Chrome Proxy v2.0 (FastAPI + SSE)
â”œâ”€â”€ requirements.txt         # Python dependencies (fastapi, uvicorn, pyperclip, pydantic)
â”œâ”€â”€ docs/
â”‚   â””â”€â”€ qa/                  # QA reports (written by QA Engineer only)
â”‚       â””â”€â”€ .gitkeep
â”œâ”€â”€ memory-bank/             # Memory Bank â€” 7 Markdown files
â”‚   â”œâ”€â”€ activeContext.md     # Current task, last result, next action
â”‚   â”œâ”€â”€ decisionLog.md       # Timestamped ADRs
â”‚   â”œâ”€â”€ productContext.md    # User Stories, backlog
â”‚   â”œâ”€â”€ progress.md          # le workbench phases checklist + features
â”‚   â”œâ”€â”€ projectBrief.md      # Vision, objectives, Non-Goals
â”‚   â”œâ”€â”€ systemPatterns.md    # Architecture, conventions, patterns
â”‚   â””â”€â”€ techContext.md       # Stack, commands, LLM backend config
â”œâ”€â”€ workbench/               # Planning documents (DOC1, DOC2, DOC3)
â”‚   â”œâ”€â”€ DOC1-PRD-Workbench-Requirements.md
â”‚   â”œâ”€â”€ DOC2-ARCH-Workbench-Technical-Design.md
â”‚   â””â”€â”€ DOC3-BUILD-Workbench-Assembly-Phases.md
â”œâ”€â”€ prompts/                 # Canonical SP registry (SP-001 to SP-007)
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ SP-001-ollama-modelfile-system.md
â”‚   â”œâ”€â”€ SP-002-clinerules-global.md
â”‚   â”œâ”€â”€ SP-003-persona-product-owner.md
â”‚   â”œâ”€â”€ SP-004-persona-scrum-master.md
â”‚   â”œâ”€â”€ SP-005-persona-developer.md
â”‚   â”œâ”€â”€ SP-006-persona-qa-engineer.md
â”‚   â””â”€â”€ SP-007-gem-gemini-roo-agent.md
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ check-prompts-sync.ps1  # Prompt consistency verification
â”‚   â””â”€â”€ start-proxy.ps1         # Gemini Chrome proxy startup
â””â”€â”€ src/                     # Application source code (created by Developer)
```

---

### 3 LLM Modes Dashboard

| Mode | Roo Code Provider | URL / Model | Cost | Automatic | Prerequisites |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1 â€” Local** | Ollama | `http://calypso:11434` / `uadf-agent` | Free | âœ… Yes | Tailscale active + Ollama on `calypso` |
| **2 â€” Proxy** | OpenAI Compatible | `http://localhost:8000/v1` / `gemini-manual` | Free | âŒ Copy-paste | proxy.py + Chrome |
| **3 â€” Cloud** | Anthropic | `api.anthropic.com` / `claude-sonnet-4-6` | Paid | âœ… Yes | API key + Internet |

---

### Final Validation Checklist

- [ ] Phase 0: VS Code + Roo Code cleanly reinstalled
- [ ] Phase 1: Ollama + `uadf-agent` (32B) + `qwen3:7b` installed
- [ ] Phase 2: Git repository initialized with complete `.gitignore`
- [ ] Phase 3: `Modelfile` compiled (`ollama create uadf-agent -f Modelfile`)
- [ ] Phase 4: `.roomodes` with 4 validated RBAC personas
- [ ] Phase 5: Memory Bank (7 files) + `.clinerules` (6 rules) â€” CHECKâ†’CREATEâ†’READâ†’ACT sequence validated
- [ ] Phase 6: `template/proxy.py` v2.0 starts and responds on `/health`
- [ ] Phase 7: Gemini Gem "Roo Code Agent" created and responds with XML tags
- [ ] Phase 8: 3-mode switcher configured in Roo Code
- [ ] Phase 9: End-to-end tests validated (3 modes + RBAC + Memory Bank + Git)
- [ ] Phase 10: Anthropic API configured, key secured in VS Code SecretStorage
- [ ] Phase 11: `prompts/` registry initialized (7 canonical SPs)
- [ ] Phase 12: `check-prompts-sync.ps1` â†’ 6 PASS | 0 FAIL, pre-commit hook active

**The le workbench system is operational when all boxes are checked.**

---

## Appendix A â€” References Table

| Ref. | Type | Title / Identifier | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Internal document | `workbench/DOC1-PRD-Workbench-Requirements.md` | Product Requirements Document v2.0 â€” source of all REQ-xxx requirements implemented in this plan |
| [DOC2] | Internal document | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Architecture, Solution and Technical Stack v2.0 â€” justifies the technical choices of each phase |
| [DOC3] | Internal document | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | This document â€” Complete Sequential Implementation Plan v3.0 (Phases 0â€“12) |
| [DOC4] | Internal document | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | Workbench Deployment Guide for new and existing projects |
| [SP-001] | System Prompt | `template/prompts/SP-001-ollama-modelfile-system.md` | Ollama Modelfile system prompt â€” deployed in Phase 3 |
| [SP-002] | System Prompt | `template/prompts/SP-002-clinerules-global.md` | Canonical content of the `.clinerules` file â€” deployed in Phase 5 |
| [SP-003] | System Prompt | `template/prompts/SP-003-persona-product-owner.md` | Product Owner `roleDefinition` â€” deployed in Phase 4 |
| [SP-004] | System Prompt | `template/prompts/SP-004-persona-scrum-master.md` | Scrum Master `roleDefinition` â€” deployed in Phase 4 |
| [SP-005] | System Prompt | `template/prompts/SP-005-persona-developer.md` | Developer `roleDefinition` â€” deployed in Phase 4 |
| [SP-006] | System Prompt | `template/prompts/SP-006-persona-qa-engineer.md` | QA Engineer `roleDefinition` â€” deployed in Phase 4 |
| [SP-007] | System Prompt | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Gemini Gem "Roo Code Agent" instructions â€” deployed manually in Phase 7 |
| [OLLAMA-DL] | Download | https://ollama.com/download/windows | Ollama installer for Windows â€” used in Phase 1 |
| [QWEN3-32B] | LLM Model | `mychen76/qwen3_cline_roocode:32b` on Ollama Hub | Main model fine-tuned for Roo Code Tool Calling â€” downloaded in Phase 1 |
| [QWEN3-7B] | LLM Model | `qwen3:7b` on Ollama Hub | Secondary model for Boomerang Tasks â€” downloaded in Phase 1 |
| [ROOCODE-EXT] | VS Code Extension | Roo Code (VS Code marketplace) | Agentic extension â€” installed in Phase 0 |
| [FASTAPI] | Python Library | `pip install fastapi uvicorn pyperclip` | Proxy dependencies â€” installed in Phase 6 |
| [ANTHROPIC-KEY] | Documentation | https://console.anthropic.com | Anthropic console for generating the API key â€” used in Phase 10 |
| [ANTHROPIC-MODELS] | Documentation | https://docs.anthropic.com/en/docs/about-claude/models | List of available Claude models â€” to consult for updating `claude-sonnet-4-6` |
| [GEMINI-GEMS] | Interface | https://gemini.google.com > Gems | Gemini Gems creation interface â€” used in Phase 7 |
| [GIT-HOOKS] | Documentation | https://git-scm.com/docs/githooks | Git hooks documentation â€” used in Phase 12 |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | MAJOR.MINOR.PATCH convention for SP files and the workbench |

---

## Appendix B â€” Abbreviations Table

| Abbreviation | Full Form | Explanation |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Timestamped record of an architecture decision. Stored in `memory-bank/decisionLog.md`. |
| **API** | Application Programming Interface | Programming interface. Three APIs in the workbench: Ollama REST (local), OpenAI-compatible (proxy), Anthropic HTTPS (cloud). |
| **ASGI** | Asynchronous Server Gateway Interface | Python standard for asynchronous web servers. FastAPI + Uvicorn = ASGI stack of the proxy (Phase 6). |
| **DA** | Architecture Decision | Identifier for decisions in DOC2 (DA-001 to DA-014). Referenced in phases to justify choices. |
| **GEM** | Gem Gemini | Customized Gemini Web profile with permanent system prompt. Created in Phase 7 with SP-007. |
| **GPU** | Graphics Processing Unit | Graphics processor. `num_gpu 99` in the Modelfile delegates inference to the GPU (Phase 3). |
| **HTTP** | HyperText Transfer Protocol | Communication protocol. The proxy listens on HTTP `localhost:8000` (Phase 6). |
| **JSON** | JavaScript Object Notation | Structured data format. Used for `.roomodes` (Phase 4) and API responses. |
| **LAAW** | Local Agentic Agile Workflow | mychen76 blueprint â€” source of inspiration for the Memory Bank and Agile personas. |
| **LLM** | Large Language Model | Large language model. Three modes in the workbench: Qwen3-32B, Gemini Pro, Claude Sonnet. |
| **MCP** | Model Context Protocol | Roo Code extension protocol. Accessible only to the Developer persona. |
| **MD5** | Message Digest 5 | Hashing algorithm. Used by the proxy to detect clipboard changes (Phase 6). |
| **PO** | Product Owner | Agile persona â€” product vision, User Stories, backlog. `product-owner` mode in `.roomodes`. |
| **PRD** | Product Requirements Document | Product requirements document. DOC1 is the workbench PRD. |
| **RBAC** | Role-Based Access Control | Role-based access control. Matrix defined in Phase 4 and in DOC1 section 4.1. |
| **REQ** | Requirement | Identifier for requirements in DOC1. Each phase of this document references the REQs it implements. |
| **SM** | Scrum Master | Pure facilitator Agile persona â€” Memory Bank + Git only, no code or tests. |
| **SP** | System Prompt | Canonical file in the `template/prompts/` registry with YAML metadata. |
| **SSE** | Server-Sent Events | HTTP serverâ†’client streaming protocol. Implemented in `template/proxy.py` v2.0 (Phase 6). |
| **le workbench** | Agentic Agile Workbench | Name of the system described in this document. |
| **VRAM** | Video Random Access Memory | GPU memory. Qwen3-32B requires 8+ GB of VRAM (Phase 1, prerequisites). |
| **YAML** | YAML Ain't Markup Language | Human-readable serialization format. Used for SP file headers (Phase 11). |

---

## Appendix C â€” Glossary

| Term | Definition |
| :--- | :--- |
| **Workbench** | This repository (`agentic-agile-workbench`). Contains reusable tools, rules, and processes. This implementation plan describes how to install the workbench on a machine. |
| **Roo Code XML Tags** | Roo Code action syntax: `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. Validated in Phase 9 (end-to-end tests). |
| **Boomerang Tasks** | Roo Code mechanism for delegating subtasks to the 7B model. Configured in Phase 8, tested in Phase 9. |
| **Git Commit** | Versioned snapshot of the repository. Each phase ends with a commit with a message in Conventional Commits format. |
| **Conventional Commits** | Commit message convention: `type(scope): description`. Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`. |
| **Determinism** | Stability of LLM responses. Achieved via `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` in the Modelfile (Phase 3). |
| **Context window** | Maximum simultaneous processing capacity of an LLM. Set to 128K tokens (`num_ctx 131072`) in the Modelfile (Phase 3). |
| **Fine-tuning** | Specialized training of an LLM. `mychen76/qwen3_cline_roocode:32b` is fine-tuned for Roo Code Tool Calling (Phase 1). |
| **Gem Gemini** | Gemini Web profile with permanent system prompt (SP-007). Created manually in Phase 7 â€” not versioned in Git. |
| **Pre-commit hook** | Git script executed before each commit. Created in Phase 12 â€” calls `check-prompts-sync.ps1` and blocks if desynchronization. |
| **Memory Bank** | 7 Markdown files in `memory-bank/` persisting context between sessions. Created in Phase 5, used from Phase 9. |
| **Modelfile** | Ollama configuration file. Created in Phase 3, compiled on `calypso` with `ollama create uadf-agent -f Modelfile`. |
| **Cloud Mode** | Roo Code â†’ direct Anthropic API (`claude-sonnet-4-6`). Configured in Phase 10. |
| **Local Mode** | Roo Code (`pc`) â†’ Ollama `calypso:11434` (Tailscale) â†’ Qwen3-32B. Configured in Phase 8. |
| **Proxy Mode** | Roo Code â†’ FastAPI proxy `localhost:8000` â†’ clipboard â†’ Gemini Web. Configured in Phase 8. |
| **Agile Persona** | Roo Code mode simulating a Scrum role. Defined in `.roomodes` in Phase 4. |
| **Polling** | Periodic clipboard check every second in `template/proxy.py` (Phase 6). |
| **Proxy** | Local FastAPI server (`template/proxy.py`) created in Phase 6. Intercepts Roo Code requests and relays them to Gemini Web. |
| **Prompts registry** | `template/prompts/` directory created in Phase 11. Single source of truth for all system prompts. |
| **CHECKâ†’CREATEâ†’READâ†’ACT sequence** | Mandatory protocol at session startup. Defined in RULE 1 of `.clinerules` (Phase 5), validated in Phase 9. |
| **Token** | LLM processing unit â‰ˆ 0.75 words. The 128K token window â‰ˆ 96,000 words. |
| **Tool Calling** | LLM capability to call tools via XML tags. Qwen3-32B is fine-tuned for Roo Code Tool Calling. |
| **VS Code SecretStorage** | Encrypted VS Code storage for the Anthropic API key. Configured in Phase 10 â€” never in Git. |
