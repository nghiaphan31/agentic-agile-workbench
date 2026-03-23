# ⚠️ DOCUMENT OBSOLÈTE — REDIRECTION

> **Ce fichier est remplacé par [`DOC3-Plan-Implementation-COMPLETE.md`](DOC3-Plan-Implementation-COMPLETE.md)**
>
> **Version :** 3.0 — Document unique fusionné (phases 0-12 en continu)
> **Date de remplacement :** 2026-03-23
>
> **Raison :** Les phases 0-12 ont été fusionnées en un seul document pour éliminer la navigation entre deux fichiers. Le nouveau document intègre également les arbitrages v2.0 : séquence VÉRIFIER→CRÉER→LIRE→AGIR, Scrum Master pur facilitateur, proxy SSE, `claude-sonnet-4-6`.
>
> **Ne pas modifier ce fichier.** Toutes les modifications doivent être apportées à [`DOC3-Plan-Implementation-COMPLETE.md`](DOC3-Plan-Implementation-COMPLETE.md).

---

# Document 3 : Plan d'Implementation Sequentiel
## Systeme Agentique Local Agile, Persistant & Hybride (UADF)

**Nom du Projet :** Unified Agentic Development Framework (UADF)
**Version :** 2.0 (refactorise — base saine + versionnement Git integral)
**Date :** 2026-03-23
**Plateforme cible :** Windows 11 + Visual Studio Code
**References :** DOC1-PRD-Unified-Agentic-Framework.md, DOC2-Architecture-Solution-Stack.md

---

## Prerequis Systeme

Avant de commencer, verifiez que votre machine dispose de :
- Windows 10/11 (64-bit)
- Google Chrome installe avec un compte Google actif
- Au moins 16 Go de RAM (32 Go recommandes pour le modele 32B)
- Au moins 30 Go d'espace disque libre (modeles + projet)
- Une carte graphique NVIDIA avec 8+ Go de VRAM (recommande) OU CPU suffisant
- Connexion Internet pour les telechargements initiaux
- Git installe (`git --version` doit repondre dans PowerShell)
- Python 3.10+ installe (`python --version` doit repondre dans PowerShell)

---

## Vue d'Ensemble des Phases

```
PHASE 0 : Base Saine — Nettoyage et Reinstallation VS Code + Roo Code
    |
    v
PHASE 1 : Infrastructure Systeme (Ollama + Modeles LLM)
    |
    v
PHASE 2 : Creation du Depot Git du Projet UADF
    |
    v
PHASE 3 : Modelfile et Modele Personnalise Ollama
    |
    v
PHASE 4 : Personas Agile (.roomodes) avec Regles Git
    |
    v
PHASE 5 : Memory Bank (.clinerules avec Regles Git + 7 fichiers .md)
    |
    v
PHASE 6 : Proxy Gemini Chrome (proxy.py)
    |
    v
PHASE 7 : Configuration Gemini Chrome (Gem dedie)
    |
    v
PHASE 8 : Configuration Roo Code (Commutateur 3 modes LLM)
    |
    v
PHASE 9 : Tests de Validation End-to-End
    |
    v
PHASE 10 : Mode Cloud Direct — API Anthropic Claude Sonnet
    |
    v
PHASE 11 : Registre Central des System Prompts (prompts/)
    |
    v
PHASE 12 : Verification Automatique de Coherence des Prompts
```

---

## PHASE 0 : Base Saine — Nettoyage et Reinstallation VS Code + Roo Code

**Objectif :** Partir d'un environnement VS Code et Roo Code propre, sans pollution de configurations precedentes, extensions conflictuelles ou parametres corrompus.

> **Pourquoi cette phase est critique :** Un environnement VS Code "pollue" peut causer des comportements impredictibles de Roo Code : parametres API residuels d'anciennes configurations, extensions conflictuelles, cache corrompu, ou anciennes versions de Roo Code (Cline) coexistant avec la nouvelle. Cette phase garantit une ardoise vierge.

### Etape 0.1 — Sauvegarder les Parametres VS Code Actuels (Optionnel)

Si vous avez des configurations VS Code que vous souhaitez conserver (keybindings, themes, etc.) :
```powershell
# Sauvegarder les parametres utilisateur VS Code
$vscodeSettings = "$env:APPDATA\Code\User"
$backup = "$env:USERPROFILE\Desktop\vscode-backup-$(Get-Date -Format 'yyyyMMdd')"
Copy-Item -Path $vscodeSettings -Destination $backup -Recurse
Write-Host "Sauvegarde creee : $backup"
```

### Etape 0.2 — Desinstaller Toutes les Versions de Roo Code / Cline

1. Dans VS Code, ouvrez le panneau Extensions (`Ctrl+Shift+X`)
2. Recherchez **"Roo"** dans la barre de recherche
3. Pour chaque extension trouvee (Roo Code, Roo Cline, Cline, etc.) :
   - Cliquez sur l'engrenage a cote de l'extension
   - Selectionnez **"Uninstall"**
4. Recherchez **"Cline"** et repetez l'operation
5. Rechargez VS Code (`Ctrl+Shift+P` > "Developer: Reload Window")

### Etape 0.3 — Nettoyer le Cache et les Donnees de Roo Code

Fermez VS Code completement, puis dans PowerShell :
```powershell
# Supprimer les donnees stockees de Roo Code / Cline
$extensionsPath = "$env:USERPROFILE\.vscode\extensions"
$globalStoragePath = "$env:APPDATA\Code\User\globalStorage"

# Lister les dossiers Roo/Cline existants avant suppression
Write-Host "=== Extensions Roo/Cline trouvees ==="
Get-ChildItem $extensionsPath | Where-Object { $_.Name -match "roo|cline|saoud" } | Select-Object Name

Write-Host "=== Donnees globales Roo/Cline trouvees ==="
Get-ChildItem $globalStoragePath | Where-Object { $_.Name -match "roo|cline|saoud" } | Select-Object Name
```

Supprimez les dossiers identifies :
```powershell
# Supprimer les extensions Roo/Cline (adapter les noms selon ce qui est trouve)
Get-ChildItem $extensionsPath | Where-Object { $_.Name -match "roo|cline|saoud" } | Remove-Item -Recurse -Force

# Supprimer les donnees globales Roo/Cline
Get-ChildItem $globalStoragePath | Where-Object { $_.Name -match "roo|cline|saoud" } | Remove-Item -Recurse -Force

Write-Host "Nettoyage termine."
```

### Etape 0.4 — Nettoyer les Parametres VS Code Corrompus

```powershell
# Verifier le fichier de parametres VS Code pour des entrees Roo/Cline residuelles
$settingsFile = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $settingsFile) {
    Write-Host "=== Contenu actuel de settings.json ==="
    Get-Content $settingsFile | Select-String -Pattern "roo|cline|ollama|anthropic" -CaseSensitive:$false
}
```

Si des entrees residuelles sont trouvees, ouvrez `settings.json` dans un editeur de texte et supprimez les sections concernees, ou reinitialiser completement :
```powershell
# Option nucleaire : reinitialiser settings.json (ATTENTION : supprime TOUS vos parametres VS Code)
# Decommenter seulement si necessaire :
# Set-Content $settingsFile "{}"
```

### Etape 0.5 — Reinstaller VS Code (Si Necessaire)

Si VS Code lui-meme est instable ou corrompu :
1. Allez dans **Parametres Windows > Applications**
2. Recherchez **"Visual Studio Code"** et cliquez sur **"Desinstaller"**
3. Supprimez les dossiers residuels :
   ```powershell
   Remove-Item "$env:APPDATA\Code" -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item "$env:USERPROFILE\.vscode" -Recurse -Force -ErrorAction SilentlyContinue
   ```
4. Telechargez la derniere version stable sur **https://code.visualstudio.com**
5. Installez avec les options par defaut

### Etape 0.6 — Installer la Derniere Version de Roo Code (Propre)

1. Ouvrez VS Code
2. Ouvrez le panneau Extensions (`Ctrl+Shift+X`)
3. Recherchez **"Roo Code"**
4. Verifiez que l'editeur est **"Roo Coder"** (l'editeur officiel)
5. Cliquez sur **"Install"**
6. Attendez la fin de l'installation

**Verification :** L'icone Roo Code (un kangourou ou logo similaire) doit apparaitre dans la barre laterale gauche de VS Code.

### Etape 0.7 — Verifier l'Etat Propre de Roo Code

1. Cliquez sur l'icone Roo Code dans la barre laterale
2. Le panneau doit s'ouvrir sans erreur
3. Allez dans les parametres Roo Code (engrenage) — aucune cle API ne doit etre pre-remplie
4. La liste des modes doit contenir uniquement les modes par defaut (Code, Architect, Ask, Debug, Orchestrator)

> **Si des modes personnalises ou des cles API apparaissent deja :** Cela indique que des donnees residuelles persistent. Repetez les etapes 0.3 et 0.4.

### Etape 0.8 — Verifier Git et Python

```powershell
git --version
python --version
pip --version
```

Chaque commande doit retourner un numero de version. Si l'une echoue :
- **Git :** Telechargez sur https://git-scm.com/download/win
- **Python :** Telechargez sur https://python.org/downloads (cochez "Add to PATH" lors de l'installation)

---

## PHASE 1 : Infrastructure Systeme — Installation d'Ollama et des Modeles

**Objectif :** Installer le moteur d'inference local et telecharger les modeles LLM.
**Exigences adressees :** REQ-1.0, REQ-1.1, REQ-1.2

### Etape 1.1 — Installer Ollama pour Windows

1. Allez sur **https://ollama.com/download**
2. Cliquez sur **"Download for Windows"** et telechargez l'installateur `.exe`
3. Executez l'installateur (installation standard, pas besoin de modifier les options)
4. Apres installation, Ollama demarre automatiquement en tache de fond
5. Verifiez que l'icone Ollama apparait dans la zone de notification Windows (coin bas-droit)

**Verification :** Ouvrez un terminal PowerShell dans VS Code (`Ctrl+`` `) :
```powershell
ollama --version
```
Resultat attendu : `ollama version 0.x.x`

### Etape 1.2 — Telecharger le Modele Principal (Qwen3 32B optimise Roo Code)

```powershell
ollama pull mychen76/qwen3_cline_roocode:32b
```

> **Note :** Ce telechargement peut prendre 15 a 45 minutes. Le modele pese environ 20 Go.

**Verification :**
```powershell
ollama list
```
Vous devez voir `mychen76/qwen3_cline_roocode:32b` dans la liste.

### Etape 1.3 — Telecharger le Modele Secondaire (Qwen3 7B pour Boomerang)

```powershell
ollama pull qwen3:7b
```

### Etape 1.4 — Verifier que l'API Ollama est Accessible

```powershell
Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method GET | Select-Object -ExpandProperty Content
```

Vous devez voir une reponse JSON listant vos modeles. Si erreur de connexion, relancez Ollama depuis le menu Demarrer.

---

## PHASE 2 : Creation du Depot Git du Projet UADF

**Objectif :** Creer le depot Git qui versionnera TOUT : code, scripts, prompts, configurations, Memory Bank.
**Exigences adressees :** REQ-000, REQ-4.1, REQ-4.5

> **Principe fondamental du versionnement UADF :** Dans ce systeme, Git n'est pas seulement pour le code applicatif. Il versionne l'integralite de l'intelligence du projet : les prompts systeme (`.clinerules`, `.roomodes`), les scripts (proxy.py), la configuration (Modelfile), et la memoire persistante (memory-bank/). Chaque modification significative de l'un de ces elements doit faire l'objet d'un commit Git avec un message descriptif.

### Etape 2.1 — Creer le Dossier du Projet

```powershell
mkdir C:\Users\$env:USERNAME\Projects\mon-projet-uadf
cd C:\Users\$env:USERNAME\Projects\mon-projet-uadf
```

Ouvrez ce dossier dans VS Code :
```powershell
code .
```

### Etape 2.2 — Initialiser Git

Dans le terminal VS Code :
```powershell
git init
git config user.name "Votre Nom"
git config user.email "votre@email.com"
```

### Etape 2.3 — Creer le Fichier `.gitignore` Complet

```powershell
New-Item -Name ".gitignore" -ItemType File
```

Ouvrez `.gitignore` et collez le contenu suivant :
```gitignore
# Environnement Python (jamais versionne)
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/

# Variables d'environnement (contient des cles API — JAMAIS versionne)
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Fichiers temporaires Windows
Thumbs.db
Desktop.ini
*.tmp

# Fichiers VS Code locaux (parametres personnels, pas de projet)
.vscode/settings.json
.vscode/launch.json
.vscode/tasks.json

# IMPORTANT : Les fichiers suivants DOIVENT etre versionnés (ne pas les ajouter ici)
# .roomodes        -> Versionne (personas Agile)
# .clinerules      -> Versionne (regles Memory Bank + Git)
# Modelfile        -> Versionne (config modele Ollama)
# proxy.py         -> Versionne (serveur proxy Gemini)
# memory-bank/     -> Versionne (memoire persistante)
# requirements.txt -> Versionne (dependances Python)
```

Sauvegardez (`Ctrl+S`).

### Etape 2.4 — Creer la Structure de Dossiers du Projet

```powershell
mkdir memory-bank
mkdir docs
mkdir docs\qa
mkdir scripts
```

### Etape 2.5 — Premier Commit : Squelette du Projet

```powershell
git add .gitignore
git commit -m "chore: initialisation depot UADF - squelette projet et .gitignore"
```

---

## PHASE 3 : Modelfile et Modele Personnalise Ollama

**Objectif :** Creer un modele Ollama personnalise avec les parametres de determinisme et la fenetre de contexte etendue.
**Exigences adressees :** REQ-1.2, REQ-1.3

### Etape 3.1 — Creer le Fichier `Modelfile`

```powershell
New-Item -Name "Modelfile" -ItemType File
```

Ouvrez `Modelfile` dans VS Code et collez :
```dockerfile
FROM mychen76/qwen3_cline_roocode:32b

# Parametres de determinisme (anti-hallucination) — REQ-1.3
PARAMETER temperature 0.15
PARAMETER min_p 0.03
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.1

# Fenetre de contexte maximale (128K tokens) — REQ-1.2
PARAMETER num_ctx 131072

# Parametres de performance GPU
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

Sauvegardez (`Ctrl+S`).

### Etape 3.2 — Compiler le Modele Personnalise

```powershell
ollama create uadf-agent -f Modelfile
```

**Verification :**
```powershell
ollama list
```
Vous devez voir `uadf-agent` dans la liste.

### Etape 3.3 — Tester le Modele

```powershell
ollama run uadf-agent "Dis bonjour en une phrase."
```

Tapez `/bye` pour quitter.

### Etape 3.4 — Versionner le Modelfile

```powershell
git add Modelfile
git commit -m "feat: ajout Modelfile Ollama (uadf-agent, T=0.15, ctx=131072)"
```

---

## PHASE 4 : Personas Agile — Fichier `.roomodes` avec Regles Git

**Objectif :** Creer les 4 personas Agile avec leurs permissions RBAC et l'obligation de versionnement Git dans les roleDefinitions du Developer et du Scrum Master.
**Exigences adressees :** REQ-3.1, REQ-3.2, REQ-3.3

> **Pourquoi inscrire Git dans les roleDefinitions ?** Le Developer et le Scrum Master ont acces au terminal. En inscrivant l'obligation de commit Git dans leur `roleDefinition`, on garantit que ce comportement est auto-portant : meme si `.clinerules` n'est pas lu, le persona lui-meme sait qu'il doit versionner. C'est une defense en profondeur.

### Etape 4.1 — Creer le Fichier `.roomodes`

```powershell
New-Item -Name ".roomodes" -ItemType File
```

### Etape 4.2 — Inserer la Configuration des Personas

Ouvrez `.roomodes` dans VS Code et collez le contenu JSON suivant :

```json
{
  "customModes": [
    {
      "slug": "product-owner",
      "name": "Product Owner",
      "roleDefinition": "Tu es le Product Owner de l'equipe Scrum. Ton role est de definir et prioriser le backlog produit. Tu rediges les User Stories au format 'En tant que [persona], je veux [action] afin de [benefice]'. Tu maintiens le fichier memory-bank/productContext.md a jour. Tu ne touches JAMAIS au code source ni aux scripts. Si on te demande d'ecrire du code, tu refuses poliment et suggeres de basculer vers le mode Developer.",
      "groups": [
        "read",
        ["edit", { "fileRegex": "memory-bank/productContext\\.md|docs/.*\\.md|user-stories.*\\.md", "description": "Documentation produit uniquement" }]
      ],
      "source": "project"
    },
    {
      "slug": "scrum-master",
      "name": "Scrum Master",
      "roleDefinition": "Tu es le Scrum Master de l'equipe Scrum. Tu facilites les ceremonies Agile (Sprint Planning, Daily, Review, Retrospective). Tu identifies et supprimes les impediments. Tu maintiens memory-bank/progress.md et memory-bank/activeContext.md a jour. Tu ne touches pas au code source applicatif. Tu peux modifier tous les fichiers de la Memory Bank. REGLE GIT OBLIGATOIRE : Apres chaque mise a jour de la Memory Bank, tu DOIS executer un commit Git avec le message format 'docs(memory): [description de la mise a jour]'.",
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
      "roleDefinition": "Tu es le Developer senior de l'equipe Scrum. Tu implementes les User Stories du backlog. Tu ecris du code propre, teste et documente. PROTOCOLE OBLIGATOIRE EN 3 ETAPES : (1) AVANT de coder : lire memory-bank/activeContext.md, memory-bank/systemPatterns.md et memory-bank/techContext.md. (2) APRES avoir code : mettre a jour memory-bank/activeContext.md et memory-bank/progress.md. (3) AVANT de cloturer la tache : executer 'git add .' puis 'git commit -m [message descriptif au format conventionnel]'. Le versionnement Git est NON NEGOCIABLE : tout fichier cree ou modifie doit etre commite avant attempt_completion.",
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
      "roleDefinition": "Tu es le QA Engineer de l'equipe Scrum. Tu concois et executes les plans de test. Tu analyses les logs et rapports de test. Tu rediges les rapports de bugs avec reproduction steps clairs dans docs/qa/. Tu ne modifies JAMAIS le code source applicatif. Tu peux executer des commandes de test (npm test, pytest, etc.) et lire tous les fichiers.",
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

Sauvegardez (`Ctrl+S`).

### Etape 4.3 — Verifier le Chargement des Modes dans Roo Code

1. Cliquez sur l'icone Roo Code dans la barre laterale
2. Cliquez sur le selecteur de mode en haut du panneau
3. Vous devez voir : "Product Owner", "Scrum Master", "Developer", "QA Engineer"

> **Si les modes n'apparaissent pas :** Rechargez VS Code (`Ctrl+Shift+P` > "Developer: Reload Window").

### Etape 4.4 — Versionner `.roomodes`

```powershell
git add .roomodes
git commit -m "feat(agile): ajout personas Agile RBAC avec regles Git integrees (.roomodes)"
```

---

## PHASE 5 : Memory Bank — `.clinerules` avec Regles Git + 7 Fichiers Markdown

**Objectif :** Creer les directives imperatives (incluant l'obligation de versionnement Git) et les 7 fichiers de la Memory Bank.
**Exigences adressees :** REQ-4.1, REQ-4.2, REQ-4.3, REQ-4.4, REQ-4.5

> **Strategie de versionnement auto-portant :** La REGLE 5 dans `.clinerules` inscrit l'obligation de commit Git au niveau le plus bas du systeme — les directives globales injectees dans chaque session. Combinee avec les `roleDefinition` du Developer et du Scrum Master (Phase 4), cette regle cree une defense en profondeur : meme si un persona oublie sa propre regle, `.clinerules` la rappelle systematiquement.

### Etape 5.1 — Creer le Fichier `.clinerules`

```powershell
New-Item -Name ".clinerules" -ItemType File
```

Ouvrez `.clinerules` et collez le contenu suivant :

```markdown
# PROTOCOLE UADF — DIRECTIVES IMPERATIVES (TOUTES SESSIONS, TOUS MODES)

## REGLE 1 : LECTURE OBLIGATOIRE AU DEMARRAGE DE CHAQUE SESSION
Avant toute action, tu DOIS lire dans cet ordre exact :
1. memory-bank/activeContext.md  (tache en cours, etat actuel)
2. memory-bank/progress.md       (avancement global du projet)

Si ces fichiers n'existent pas encore, tu DOIS les creer immediatement
en utilisant les templates definis ci-dessous.

## REGLE 2 : ECRITURE OBLIGATOIRE A LA CLOTURE DE CHAQUE TACHE
Avant de cloturer toute tache (avant attempt_completion), tu DOIS mettre a jour :
1. memory-bank/activeContext.md  (nouvel etat, prochaine action)
2. memory-bank/progress.md       (cocher les features terminees)

Si une decision d'architecture a ete prise durant la session :
3. memory-bank/decisionLog.md    (ADR avec date, contexte, decision, consequences)

## REGLE 3 : LECTURE CONTEXTUELLE SELON LA TACHE
- Avant de modifier l'architecture : lire memory-bank/systemPatterns.md
- Avant d'executer des commandes build/test : lire memory-bank/techContext.md
- En debut de sprint ou de nouvelle feature : lire memory-bank/productContext.md

## REGLE 4 : AUCUNE EXCEPTION AUX REGLES 1-3
Ces regles s'appliquent a TOUS les modes et a TOUTES les sessions, sans exception.

## REGLE 5 : VERSIONNEMENT GIT OBLIGATOIRE ET AUTO-PORTANT
Cette regle s'applique a tous les modes ayant acces au terminal (developer, scrum-master).

### 5.1 — Ce qui DOIT etre versionne
TOUT doit etre versionne sous Git, sans exception :
- Le code source applicatif (src/, app/, etc.)
- Les scripts systeme (proxy.py, start-proxy.ps1, etc.)
- Les fichiers de configuration (Modelfile, .roomodes, .clinerules, requirements.txt)
- La Memory Bank (memory-bank/*.md)
- Les prompts systeme (ce fichier .clinerules lui-meme)
- Les documents de plans et d'architecture (plans/*.md)
- Les rapports QA (docs/qa/*.md)

### 5.2 — Quand commiter
Tu DOIS executer un commit Git dans les situations suivantes :
- Apres avoir cree ou modifie un fichier de code
- Apres avoir mis a jour la Memory Bank
- Apres avoir modifie .roomodes ou .clinerules
- Apres avoir modifie proxy.py ou tout autre script
- Avant de cloturer une tache (avant attempt_completion)

### 5.3 — Format des messages de commit (Conventional Commits)
Tu DOIS utiliser le format Conventional Commits :
- feat(scope): description     -> Nouvelle fonctionnalite
- fix(scope): description      -> Correction de bug
- docs(memory): description    -> Mise a jour Memory Bank
- docs(plans): description     -> Mise a jour documentation
- chore(config): description   -> Modification de configuration
- refactor(scope): description -> Refactorisation sans changement fonctionnel
- test(scope): description     -> Ajout ou modification de tests

Exemples valides :
- feat(api): ajout endpoint POST /users
- docs(memory): mise a jour activeContext apres implementation login
- chore(config): mise a jour .roomodes avec nouvelle regle Git
- fix(proxy): correction timeout polling presse-papiers

### 5.4 — Commandes Git a utiliser
Pour commiter apres une tache :
  git add .
  git commit -m "type(scope): description concise de ce qui a ete fait"

Pour verifier l'etat avant de commiter :
  git status
  git diff --staged

### 5.5 — Ce qui NE doit PAS etre versionne
- Le dossier venv/ (environnement Python local)
- Les fichiers .env (cles API — JAMAIS dans Git)
- Les fichiers __pycache__/ et *.pyc
- Les logs (*.log)
Ces exclusions sont deja configurees dans .gitignore.

## REGLE 6 : COHERENCE DU REGISTRE DES PROMPTS
Cette regle s'applique au mode developer et scrum-master.

### 6.1 — Avant tout commit touchant un artefact lie a un prompt
Si tu modifies l'un des fichiers suivants : proxy.py, .roomodes, .clinerules, Modelfile
tu DOIS verifier si le changement impacte un system prompt dans prompts/.

### 6.2 — Procedure de verification
1. Lire prompts/README.md pour identifier le prompt concerne
2. Ouvrir le fichier SP-XXX correspondant dans prompts/
3. Si le contenu du prompt doit changer : modifier SP-XXX, incrementer sa version
4. Si SP-007 (Gem Gemini) est impacte : ajouter un avertissement dans le commit :
   "DEPLOIEMENT MANUEL REQUIS : mettre a jour le Gem Gemini avec SP-007"
5. Inclure les fichiers prompts/ modifies dans le meme commit que les fichiers cibles

### 6.3 — Exemple de commit avec mise a jour de prompt
  git add proxy.py prompts/SP-007-gem-gemini-roo-agent.md
  git commit -m "chore(prompts): mise a jour SP-007 suite modification proxy.py - DEPLOIEMENT MANUEL REQUIS"

## TEMPLATES DE FICHIERS MEMORY BANK

### Template activeContext.md
---
# Contexte Actif
**Date de mise a jour :** [DATE]
**Mode actif :** [MODE]
**Backend LLM actif :** [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]

## Tache en cours
[Description de la tache en cours]

## Dernier resultat
[Resultat de la derniere action]

## Prochain(s) pas
- [ ] [Prochaine action immediate]

## Blocages / Questions ouvertes
[Aucun | Description du blocage]

## Dernier commit Git
[Hash court et message du dernier commit]
---

### Template progress.md
---
# Progression du Projet
**Derniere mise a jour :** [DATE]

## Infrastructure UADF
- [ ] Phase 0 : Base saine VS Code + Roo Code
- [ ] Phase 1 : Ollama + modeles
- [ ] Phase 2 : Depot Git initialise
- [ ] Phase 3 : Modelfile personnalise
- [ ] Phase 4 : .roomodes (personas Agile)
- [ ] Phase 5 : Memory Bank + .clinerules
- [ ] Phase 6 : proxy.py (Gemini Chrome)
- [ ] Phase 7 : Gem Gemini configure
- [ ] Phase 8 : Roo Code commutateur 3 modes
- [ ] Phase 9 : Tests end-to-end valides
- [ ] Phase 10 : API Anthropic Claude configure
- [ ] Phase 11 : Registre prompts/ initialise
- [ ] Phase 12 : Verification coherence prompts (script + hook pre-commit)

## Features Produit

### Epic 1 : [A definir]
- [ ] [Feature a definir]

## Legende
- [ ] A faire  |  [-] En cours  |  [x] Termine
---
```

Sauvegardez (`Ctrl+S`).

### Etape 5.2 — Creer les 7 Fichiers de la Memory Bank

**Fichier 1 : `memory-bank/projectBrief.md`**
```powershell
New-Item -Path "memory-bank" -Name "projectBrief.md" -ItemType File