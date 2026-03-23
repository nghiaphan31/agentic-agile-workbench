# Document 3 (Suite) : Phases 5 (fin) a 10
## Plan d'Implementation Sequentiel UADF — Version 2.0

**Suite de :** DOC3-Plan-Implementation-Windows-VSCode.md
**Phases couvertes :** 5 (fin des 7 fichiers Memory Bank), 6, 7, 8, 9, 10

---

## PHASE 5 (suite) : Contenu des 7 Fichiers Memory Bank

### Fichier 1 : `memory-bank/projectBrief.md`

Ouvrez le fichier et collez :
```markdown
# Project Brief

## Vision du Projet
[Decrivez ici la vision globale de votre projet en 2-3 phrases]

## Objectifs Principaux
1. [Objectif 1]
2. [Objectif 2]
3. [Objectif 3]

## Non-Goals (Ce que ce projet NE fait PAS)
- [Non-goal 1]
- [Non-goal 2]

## Contraintes
- [Contrainte technique ou metier]

## Parties Prenantes
- Product Owner : [Nom]
- Utilisateurs cibles : [Description]
```

### Fichier 2 : `memory-bank/productContext.md`

```powershell
New-Item -Path "memory-bank" -Name "productContext.md" -ItemType File
```
Ouvrez le fichier et collez :
```markdown
# Product Context

## User Stories du Sprint Courant

### Sprint [N] — [Dates]

#### US-001 : [Titre]
**En tant que** [persona]
**Je veux** [action]
**Afin de** [benefice]
**Criteres d'acceptation :**
- [ ] [Critere 1]
- [ ] [Critere 2]

## Backlog (Prochains Sprints)
- [ ] [Feature a venir 1]
- [ ] [Feature a venir 2]
```

### Fichier 3 : `memory-bank/systemPatterns.md`

```powershell
New-Item -Path "memory-bank" -Name "systemPatterns.md" -ItemType File
```
Ouvrez le fichier et collez :
```markdown
# System Patterns

## Architecture des Dossiers
[Collez ici l'arborescence de votre projet]

## Conventions de Nommage
- Fichiers : [convention, ex: kebab-case]
- Variables : [convention, ex: camelCase]
- Classes : [convention, ex: PascalCase]
- Constantes : [convention, ex: UPPER_SNAKE_CASE]

## Patterns Techniques Adoptes
- [Pattern 1 : ex: Repository Pattern pour l'acces aux donnees]
- [Pattern 2 : ex: Service Layer pour la logique metier]

## Anti-Patterns a Eviter
- [Anti-pattern 1]
```

### Fichier 4 : `memory-bank/techContext.md`

```powershell
New-Item -Path "memory-bank" -Name "techContext.md" -ItemType File
```
Ouvrez le fichier et collez :
```markdown
# Tech Context

## Stack Technique
- Langage principal : [ex: Python 3.11]
- Framework : [ex: FastAPI 0.110]
- Base de donnees : [ex: SQLite / PostgreSQL]
- Tests : [ex: pytest]

## Commandes Essentielles
```bash
pip install -r requirements.txt
python main.py
pytest tests/
```

## Variables d'Environnement Requises
- `[VAR_NAME]` : [Description et valeur par defaut]

## Dependances Critiques et Versions
| Package | Version | Raison |
| :--- | :--- | :--- |
| [package] | [version] | [raison] |

## Configuration des Backends LLM (Commutateur UADF)

### Mode 1 : Local Ollama (Souverain et Gratuit)
- API Provider : Ollama
- Base URL : http://localhost:11434
- Model : uadf-agent
- Prerequis : Ollama en cours d'execution (icone zone de notification)

### Mode 2 : Proxy Gemini Chrome (Cloud Gratuit + Copier-Coller)
- API Provider : OpenAI Compatible
- Base URL : http://localhost:8000/v1
- API Key : sk-fake-key-uadf
- Model : gemini-manual
- Prerequis : proxy.py demarre + Chrome ouvert sur Gem "Roo Code Agent"

### Mode 3 : Cloud Direct Claude Sonnet (Payant et Entierement Automatique)
- API Provider : Anthropic
- Model : claude-sonnet-4-5
- API Key : [stockee dans VS Code SecretStorage - ne jamais noter ici]
- Prerequis : Connexion Internet + credit Anthropic disponible
```

### Fichier 5 : `memory-bank/activeContext.md`

```powershell
New-Item -Path "memory-bank" -Name "activeContext.md" -ItemType File
```
Ouvrez le fichier et collez :
```markdown
# Contexte Actif

**Date de mise a jour :** 2026-03-23
**Mode actif :** developer
**Backend LLM actif :** Ollama uadf-agent

## Tache en cours
Initialisation du projet UADF — Configuration de l'environnement de developpement.

## Dernier resultat
Structure initiale du projet creee. Memory Bank initialisee. Depot Git initialise.

## Prochain(s) pas
- [ ] Completer les informations dans projectBrief.md
- [ ] Definir les premieres User Stories dans productContext.md
- [ ] Configurer le proxy Gemini Chrome (proxy.py)
- [ ] Configurer le Gem Gemini Chrome

## Blocages / Questions ouvertes
Aucun blocage identifie pour le moment.

## Dernier commit Git
[A remplir apres le premier commit de la Memory Bank]
```

### Fichier 6 : `memory-bank/progress.md`

```powershell
New-Item -Path "memory-bank" -Name "progress.md" -ItemType File
```
Ouvrez le fichier et collez :
```markdown
# Progression du Projet

**Derniere mise a jour :** 2026-03-23

## Infrastructure UADF

### Phase de Setup
- [x] Phase 0 : Base saine VS Code + Roo Code (reinstallation propre)
- [x] Phase 1 : Installation Ollama + modeles Qwen3-32B et 7B
- [x] Phase 2 : Depot Git initialise avec .gitignore complet
- [x] Phase 3 : Modelfile personnalise (uadf-agent, T=0.15, ctx=131072)
- [x] Phase 4 : .roomodes (4 personas Agile avec regles Git)
- [x] Phase 5 : Memory Bank (7 fichiers) + .clinerules (5 regles dont Git)
- [ ] Phase 6 : proxy.py (serveur Gemini Chrome)
- [ ] Phase 7 : Gem Gemini Chrome configure
- [ ] Phase 8 : Roo Code commutateur 3 modes LLM
- [ ] Phase 9 : Tests end-to-end valides
- [ ] Phase 10 : API Anthropic Claude Sonnet configure

## Features Produit

### Epic 1 : [A definir]
- [ ] [Feature a definir]

## Legende
- [ ] A faire  |  [-] En cours  |  [x] Termine
```

### Fichier 7 : `memory-bank/decisionLog.md`

```powershell
New-Item -Path "memory-bank" -Name "decisionLog.md" -ItemType File
```
Ouvrez le fichier et collez :
```markdown
# Decision Log — Architecture Decision Records (ADR)

---

## ADR-001 : Choix du moteur d'inference local
**Date :** 2026-03-23
**Statut :** Accepte

**Contexte :**
Besoin d'un moteur d'inference LLM local, gratuit et compatible avec l'API OpenAI pour Roo Code.

**Decision :**
Utilisation d'Ollama avec le modele mychen76/qwen3_cline_roocode:32b compile en uadf-agent.

**Consequences :**
- Avantage : Souverainete totale, gratuit, compatible OpenAI
- Avantage : Modele specifiquement optimise pour le Tool Calling Roo Code
- Inconvenient : Necessite 20+ Go de stockage et 16+ Go de RAM

---

## ADR-002 : Architecture du Proxy Gemini Chrome
**Date :** 2026-03-23
**Statut :** Accepte

**Contexte :**
Besoin d'exploiter Gemini Chrome gratuitement depuis Roo Code sans modifier son comportement.

**Decision :**
Serveur FastAPI local emulant l'API OpenAI, avec relay presse-papiers pour l'intervention humaine.

**Consequences :**
- Avantage : Roo Code non modifie, compatibilite native
- Avantage : Gratuite totale de Gemini Chrome
- Inconvenient : Necessite une intervention humaine (copier-coller) a chaque requete

---

## ADR-003 : Versionnement Git integral de tous les artefacts UADF
**Date :** 2026-03-23
**Statut :** Accepte

**Contexte :**
Besoin de tracer l'evolution de tous les artefacts du systeme : code, prompts, scripts, Memory Bank.

**Decision :**
Git versionne TOUT (code, .clinerules, .roomodes, Modelfile, proxy.py, memory-bank/).
La regle de commit est inscrite dans .clinerules (REGLE 5) ET dans les roleDefinitions
du Developer et du Scrum Master pour une defense en profondeur auto-portante.

**Consequences :**
- Avantage : Tracabilite complete de l'evolution du systeme
- Avantage : Possibilite de rollback sur n'importe quel artefact
- Avantage : Comportement auto-portant : l'IA elle-meme maintient le versionnement
- Inconvenient : Necessite une discipline de commit coherente
```

### Etape 5.3 — Commit de la Memory Bank et des Configurations

```powershell
git add .clinerules .roomodes memory-bank/ docs/
git commit -m "feat(uadf): initialisation complete Memory Bank (7 fichiers) + .clinerules (5 regles dont Git)"
```

---

## PHASE 6 : Proxy Gemini Chrome — Fichier `proxy.py`

**Objectif :** Creer le serveur proxy Python qui relaie les requetes Roo Code vers Gemini Chrome via le presse-papiers.
**Exigences adressees :** REQ-2.1.x, REQ-2.2.x, REQ-2.3.x, REQ-2.4.x

### Etape 6.1 — Creer l'Environnement Virtuel Python

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Si erreur de politique d'execution PowerShell :**
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Puis relancez `.\venv\Scripts\Activate.ps1`

Vous devez voir `(venv)` au debut de l'invite de commande.

### Etape 6.2 — Installer les Dependances Python

```powershell
pip install fastapi uvicorn pyperclip
pip freeze > requirements.txt
```

### Etape 6.3 — Creer le Fichier `proxy.py`

```powershell
New-Item -Name "proxy.py" -ItemType File
```

Ouvrez `proxy.py` dans VS Code et collez le code complet suivant :

```python
"""
UADF Proxy -- Pont Roo Code vers Gemini Chrome
Emule l'API OpenAI Chat Completions en local sur localhost:8000.

Usage:
    python proxy.py

Variables d'environnement (fichier .env ou variables systeme):
    USE_GEM_MODE=true       Filtre le system prompt (utiliser avec un Gem Gemini dedie)
    POLLING_INTERVAL=1.0    Intervalle de polling du presse-papiers en secondes
    TIMEOUT_SECONDS=300     Timeout avant HTTP 408 (en secondes)
    PROXY_PORT=8000         Port d'ecoute du serveur

Exigences couvertes:
    REQ-2.1.1 a REQ-2.1.5, REQ-2.2.1 a REQ-2.2.3,
    REQ-2.3.1 a REQ-2.3.4, REQ-2.4.1 a REQ-2.4.3
"""
import asyncio
import hashlib
import os
import time
import uuid
from datetime import datetime
from typing import List, Optional, Union

import pyperclip
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configuration
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

app = FastAPI(title="UADF Proxy", description="Pont Roo Code vers Gemini Chrome", version="1.0.0")

def _hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def _clean_content(content) -> str:
    """Nettoie le contenu : supprime les images base64. REQ-2.1.5"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif item.get("type") == "image_url":
                    parts.append("[IMAGE OMISE - Non supportee par le proxy clipboard]")
                else:
                    parts.append(str(item))
        return "\n".join(parts)
    return str(content)

def _format_prompt(messages: List[MessageContent]) -> str:
    """Formate les messages en texte lisible. REQ-2.1.3, REQ-2.1.4, REQ-2.2.2"""
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if not content.strip():
            continue
        if msg.role == "system":
            if USE_GEM_MODE:
                continue  # Le Gem contient deja le system prompt
            parts.append("[SYSTEM PROMPT]\n" + content)
        elif msg.role == "user":
            parts.append("[USER]\n" + content)
        elif msg.role == "assistant":
            parts.append("[ASSISTANT]\n" + content)
    return "\n\n---\n\n".join(parts)

def _validate_response(text: str) -> bool:
    """Verifie la presence de balises XML Roo Code. REQ-2.3.4"""
    return any(tag in text for tag in ROO_XML_TAGS)

def _build_openai_response(content: str, model: str) -> dict:
    """Construit une reponse au format OpenAI Chat Completions. REQ-2.4.1, REQ-2.4.3"""
    return {
        "id": "chatcmpl-proxy-" + uuid.uuid4().hex[:8],
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop"
        }],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Point d'entree principal. REQ-2.1.1, REQ-2.1.2"""
    ts = datetime.now().strftime("%H:%M:%S")
    print("\n" + "=" * 60)
    print("[" + ts + "] REQUETE RECUE de Roo Code | modele: " + request.model)

    formatted = _format_prompt(request.messages)
    pyperclip.copy(formatted)  # REQ-2.2.1
    initial_hash = _hash(formatted)

    mode_info = "GEM MODE" if USE_GEM_MODE else "MODE COMPLET"
    print("[" + ts + "] Mode: " + mode_info + " | " + str(len(formatted)) + " caracteres")
    print("[" + ts + "] PROMPT COPIE DANS LE PRESSE-PAPIERS !")
    print("[" + ts + "] ACTION REQUISE :")
    print("         1. Allez dans Google Chrome")
    print("         2. Ouvrez votre Gem 'Roo Code Agent' sur gemini.google.com")
    print("         3. Collez le prompt : Ctrl+V")
    print("         4. Attendez la reponse complete de Gemini")
    print("         5. Copiez la reponse : Ctrl+A puis Ctrl+C")
    print("         Timeout dans " + str(TIMEOUT_SECONDS) + " secondes...")

    start_time = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)  # REQ-2.3.1
        current_content = pyperclip.paste()

        if _hash(current_content) != initial_hash:  # REQ-2.3.2
            elapsed = time.time() - start_time
            print("[" + ts + "] REPONSE DETECTEE ! " + str(len(current_content)) + " chars en " + str(round(elapsed, 1)) + "s")

            if not _validate_response(current_content):  # REQ-2.3.4
                print("[" + ts + "] AVERTISSEMENT : Aucune balise XML Roo Code detectee.")
                print("         Verifiez que votre Gem est correctement configure.")

            response = _build_openai_response(current_content, request.model)
            print("[" + ts + "] Reponse transmise a Roo Code (HTTP 200 OK)")
            return JSONResponse(content=response, status_code=200)  # REQ-2.4.2

        elapsed = time.time() - start_time
        if elapsed > TIMEOUT_SECONDS:  # REQ-2.3.3
            print("[" + ts + "] TIMEOUT apres " + str(TIMEOUT_SECONDS) + "s")
            raise HTTPException(status_code=408, detail="Timeout: Relancez votre requete dans Roo Code.")

@app.get("/v1/models")
async def list_models():
    return JSONResponse(content={
        "object": "list",
        "data": [{"id": "gemini-manual", "object": "model", "created": int(time.time()), "owned_by": "uadf-proxy"}]
    })

@app.get("/health")
async def health_check():
    return {"status": "ok", "proxy": "UADF", "gem_mode": USE_GEM_MODE, "version": "1.0.0"}

if __name__ == "__main__":
    print("=" * 60)
    print("  UADF PROXY -- Roo Code vers Gemini Chrome")
    print("=" * 60)
    print("  URL     : http://localhost:" + str(PORT) + "/v1")
    print("  Mode    : " + ("GEM MODE" if USE_GEM_MODE else "MODE COMPLET"))
    print("  Timeout : " + str(TIMEOUT_SECONDS) + "s | Polling : " + str(POLLING_INTERVAL) + "s")
    print("=" * 60)
    print("  Config Roo Code :")
    print("    Base URL : http://localhost:" + str(PORT) + "/v1")
    print("    API Key  : sk-fake-key-uadf")
    print("    Modele   : gemini-manual")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
```

### Etape 6.4 — Creer le Script de Demarrage `scripts/start-proxy.ps1`

```powershell
New-Item -Path "scripts" -Name "start-proxy.ps1" -ItemType File
```

Ouvrez `scripts/start-proxy.ps1` et collez :
```powershell
# UADF Proxy -- Script de demarrage rapide
# Usage: .\scripts\start-proxy.ps1
param(
    [switch]$FullMode  # Utiliser -FullMode pour desactiver le filtrage du system prompt
)

Write-Host "Demarrage du proxy UADF..." -ForegroundColor Cyan

# Activer l'environnement virtuel
& ".\venv\Scripts\Activate.ps1"

# Configurer le mode
if ($FullMode) {
    $env:USE_GEM_MODE = "false"
    Write-Host "Mode: COMPLET (system prompt inclus)" -ForegroundColor Yellow
} else {
    $env:USE_GEM_MODE = "true"
    Write-Host "Mode: GEM (system prompt filtre)" -ForegroundColor Green
}

Write-Host "Proxy disponible sur http://localhost:8000/v1" -ForegroundColor Green
Write-Host "Configurez Roo Code : Base URL = http://localhost:8000/v1" -ForegroundColor Yellow
python proxy.py
```

### Etape 6.5 — Tester le Demarrage du Proxy

```powershell
python proxy.py
```

**Verification dans un second terminal :**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object -ExpandProperty Content
```
Resultat attendu : `{"status":"ok","proxy":"UADF","gem_mode":true,"version":"1.0.0"}`

Arretez le proxy (`Ctrl+C`).

### Etape 6.6 — Versionner le Proxy et ses Scripts

```powershell
git add proxy.py requirements.txt scripts/start-proxy.ps1
git commit -m "feat(proxy): ajout serveur proxy UADF FastAPI + script demarrage PowerShell"
```

---

## PHASE 7 : Configuration Gemini Chrome — Gem Dedie Roo Code

**Objectif :** Creer un profil "Gem" dans Gemini Web avec le system prompt complet de Roo Code.
**Exigences adressees :** REQ-5.1, REQ-5.2, REQ-5.3

### Etape 7.1 — Acceder a Gemini et Creer un Gem

1. Ouvrez **Google Chrome** et allez sur **https://gemini.google.com**
2. Connectez-vous avec votre compte Google
3. Dans le menu de gauche, cherchez **"Gems"** ou **"Mes Gems"**
4. Cliquez sur **"Nouveau Gem"** (ou "New Gem")
5. Donnez-lui le nom : **"Roo Code Agent"**

### Etape 7.2 — Configurer les Instructions du Gem

Dans le champ **"Instructions"** du Gem, collez le texte suivant (en utilisant la vraie syntaxe XML avec chevrons) :

```
Tu es l'agent de codage integre dans Roo Code, un assistant IA expert en developpement logiciel.

REGLES ABSOLUES ET NON-NEGOCIABLES :
1. Tu dois TOUJOURS repondre en utilisant les balises XML de Roo Code.
2. Tu ne dois JAMAIS generer de texte de courtoisie, d'introduction ou de conclusion.
3. Tu ne dois JAMAIS expliquer ce que tu vas faire : tu le fais directement avec les balises XML.
4. Tu dois traiter chaque message comme une instruction directe a executer.
5. Si tu as besoin d'informations supplementaires, utilise ask_followup_question.

BALISES XML DISPONIBLES :
- write_to_file (avec path et content) : creer ou ecrire un fichier complet
- read_file (avec path) : lire un fichier
- execute_command (avec command) : executer une commande terminal
- replace_in_file (avec path et diff) : modifier une partie d'un fichier
- list_files (avec path) : lister les fichiers d'un dossier
- search_files (avec path et regex) : rechercher dans les fichiers
- attempt_completion (avec result) : signaler la completion d'une tache
- ask_followup_question (avec question) : poser une question a l'utilisateur

RAPPEL : Aucun texte avant la premiere balise XML. Aucun texte apres la derniere balise XML.
```

5. Cliquez sur **"Sauvegarder"**

### Etape 7.3 — Documenter le Gem dans la Memory Bank

Ajoutez dans `memory-bank/techContext.md` la section suivante :
```markdown
## Gem Gemini Chrome "Roo Code Agent"
- URL : https://gemini.google.com (section Gems)
- Nom du Gem : "Roo Code Agent"
- Statut : Configure avec system prompt Roo Code complet
- Note : Le proxy (USE_GEM_MODE=true) filtre le system prompt car le Gem le contient deja
```

Puis commitez :
```powershell
git add memory-bank/techContext.md
git commit -m "docs(memory): ajout configuration Gem Gemini dans techContext"
```

---

## PHASE 8 : Configuration Roo Code — Commutateur 3 Modes LLM

**Objectif :** Configurer Roo Code pour basculer entre les 3 backends LLM.
**Exigences adressees :** REQ-2.0, REQ-2.1.2, REQ-6.0

### Etape 8.1 — Configurer le Backend Ollama (Mode Local)

1. Dans VS Code, cliquez sur l'icone **Roo Code** dans la barre laterale
2. Cliquez sur l'icone **Parametres** (engrenage) en haut du panneau Roo Code
3. Dans la section **"API Provider"**, selectionnez **"Ollama"**
4. Configurez :
   - **Base URL :** `http://localhost:11434`
   - **Model :** `uadf-agent`
5. Cliquez sur **"Save"**

### Etape 8.2 — Configurer le Backend Proxy Gemini (Mode Hybride)

Pour basculer vers le proxy Gemini Chrome :
1. Dans les parametres Roo Code, section **"API Provider"**
2. Selectionnez **"OpenAI Compatible"**
3. Configurez :
   - **Base URL :** `http://localhost:8000/v1`
   - **API Key :** `sk-fake-key-uadf`
   - **Model :** `gemini-manual`
4. Cliquez sur **"Save"**

### Etape 8.3 — Configurer le Backend Claude Sonnet (Mode Cloud Direct)

Pour basculer vers l'API Anthropic :
1. Dans les parametres Roo Code, section **"API Provider"**
2. Selectionnez **"Anthropic"**
3. Dans le champ **"API Key"**, collez votre cle `sk-ant-api03-...`
   - Stockee dans VS Code SecretStorage (chiffre, non versionne) — REQ-6.4
4. Dans le champ **"Model"**, tapez : `claude-sonnet-4-5`
5. Cliquez sur **"Save"**

### Tableau de Basculement Rapide

| Mode | API Provider | Base URL | Model | Prerequis |
| :--- | :--- | :--- | :--- | :--- |
| **Local Ollama** | Ollama | `http://localhost:11434` | `uadf-agent` | Ollama en cours |
| **Proxy Gemini** | OpenAI Compatible | `http://localhost:8000/v1` | `gemini-manual` | proxy.py + Chrome |
| **Cloud Claude** | Anthropic | `https://api.anthropic.com` | `claude-sonnet-4-5` | Internet + credit |

---

## PHASE 9 : Tests de Validation End-to-End

**Objectif :** Valider que l'ensemble du systeme fonctionne correctement dans les 3 modes.

### Test 9.1 — Validation du Mode Local (Ollama)

**Prerequis :** Ollama en cours d'execution. Roo Code configure sur Ollama (`uadf-agent`).

1. Selectionnez le mode **"Developer"** dans Roo Code
2. Tapez :
   ```
   Lis la Memory Bank et dis-moi quel est l'etat actuel du projet.
   ```

**Resultat attendu :**
- Roo Code lit `activeContext.md` et `progress.md`
- Il repond avec un resume de l'etat du projet
- Il met a jour `activeContext.md`
- Il effectue un commit Git avec un message descriptif

**Verification :**
```powershell
git log --oneline -5
```
Vous devez voir un commit recent avec un message au format Conventional Commits.

### Test 9.2 — Validation du Mode Proxy Gemini Chrome

**Prerequis :** `python proxy.py` demarre dans un terminal dedie.

1. Configurez Roo Code sur **OpenAI Compatible** (proxy, port 8000)
2. Selectionnez le mode **"Developer"**
3. Tapez :
   ```
   Cree un fichier test-proxy.py qui affiche "Le proxy UADF fonctionne !"
   ```

**Sequence attendue :**

| Etape | Acteur | Action |
| :--- | :--- | :--- |
| 1 | Proxy (terminal) | Affiche "REQUETE RECUE de Roo Code" |
| 2 | Proxy (terminal) | Affiche "PROMPT COPIE DANS LE PRESSE-PAPIERS !" |
| 3 | Vous | Allez dans Chrome, ouvrez le Gem "Roo Code Agent" |
| 4 | Vous | Collez le prompt (Ctrl+V) dans Gemini |
| 5 | Gemini | Genere une reponse avec les balises XML write_to_file |
| 6 | Vous | Copiez la reponse (Ctrl+A puis Ctrl+C) |
| 7 | Proxy (terminal) | Affiche "REPONSE DETECTEE !" |
| 8 | Roo Code (VS Code) | Cree automatiquement le fichier test-proxy.py |
| 9 | Roo Code (VS Code) | Execute un commit Git avec message descriptif |

**Verification :**
```powershell
Test-Path test-proxy.py   # Doit retourner True
git log --oneline -3      # Doit montrer un commit recent
```

### Test 9.3 — Validation des Personas Agile (RBAC)

**Test du Product Owner :**
1. Selectionnez le mode **"Product Owner"**
2. Tapez : `Ecris du code Python pour une API REST.`
3. **Resultat attendu :** Le PO refuse et suggere de basculer vers le mode Developer.

**Test du QA Engineer :**
1. Selectionnez le mode **"QA Engineer"**
2. Tapez : `Modifie le fichier main.py pour corriger ce bug.`
3. **Resultat attendu :** Le QA refuse la modification du code source.

**Test du Developer :**
1. Selectionnez le mode **"Developer"**
2. Tapez : `Cree un fichier src/main.py avec une fonction hello_world().`
3. **Resultat attendu :** Le Developer cree le fichier ET effectue un commit Git.

### Test 9.4 — Validation de la Persistance de la Memory Bank

1. En mode **Developer**, demandez a Roo Code de creer une feature simple
2. Fermez VS Code completement
3. Rouvrez VS Code et le projet
4. En mode **Developer**, tapez :
   ```
   Quel etait le contexte de notre derniere session de travail ?
   ```
5. **Resultat attendu :** Roo Code lit `activeContext.md` et vous resume exactement ce qui a ete fait lors de la session precedente.

### Test 9.5 — Validation du Versionnement Git Auto-Portant

1. En mode **Developer**, demandez a Roo Code de modifier un fichier quelconque
2. **Resultat attendu :** Sans que vous le demandiez explicitement, Roo Code doit :
   - Mettre a jour `memory-bank/activeContext.md`
   - Executer `git add .` et `git commit -m "..."` avec un message au format Conventional Commits
   - Mentionner le commit dans sa reponse `attempt_completion`

**Verification :**
```powershell
git log --oneline -5
```
Chaque commit doit avoir un message au format `type(scope): description`.

---

## PHASE 10 : Mode Cloud Direct — API Anthropic Claude Sonnet

**Objectif :** Configurer Roo Code pour se connecter directement a l'API Anthropic.
**Exigences adressees :** REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4

### Etape 10.1 — Obtenir une Cle API Anthropic

1. Allez sur **https://console.anthropic.com**
2. Connectez-vous ou creez un compte Anthropic
3. Dans le menu de gauche, cliquez sur **"API Keys"**
4. Cliquez sur **"Create Key"** et donnez-lui le nom : `uadf-roo-code`
5. Copiez la cle generee (format `sk-ant-api03-...`) — **affichee une seule fois**
6. Conservez-la dans un gestionnaire de mots de passe

> **Important (REQ-6.4) :** Ne collez JAMAIS cette cle dans un fichier du projet. Elle doit etre stockee exclusivement dans les parametres securises de Roo Code (VS Code SecretStorage).

### Etape 10.2 — Verifier le Solde API

Sur **https://console.anthropic.com/settings/billing** :
- Verifiez que votre compte dispose d'un credit suffisant
- Claude Sonnet est facture a l'usage (tokens entrants + tokens sortants)

### Etape 10.3 — Configurer Roo Code avec le Provider Anthropic

1. Dans les parametres Roo Code, section **"API Provider"**
2. Selectionnez **"Anthropic"**
3. Dans le champ **"API Key"**, collez votre cle `sk-ant-api03-...`
4. Dans le champ **"Model"**, tapez : `claude-sonnet-4-5`
5. Cliquez sur **"Save"**

### Etape 10.4 — Tester la Connexion API

Dans le chat Roo Code (mode Developer), tapez :
```
Dis bonjour en une phrase et confirme que tu es Claude Sonnet.
```

**Resultat attendu :** Roo Code repond instantanement en streaming, sans copier-coller ni proxy.

### Etape 10.5 — Valider le Comportement Agentique Complet avec Git

1. Selectionnez le mode **"Developer"**
2. Tapez :
   ```
   Lis la Memory Bank et cree un fichier test-claude.py qui affiche
   "Mode Cloud Claude Sonnet operationnel dans UADF"
   ```

**Sequence attendue (entierement automatique) :**

| Etape | Acteur | Action |
| :--- | :--- | :--- |
| 1 | Roo Code | Lit `.clinerules` et charge les directives |
| 2 | Roo Code | Envoie la requete directement a `api.anthropic.com` |
| 3 | Claude Sonnet | Repond avec `read_file` pour lire `activeContext.md` |
| 4 | Roo Code | Execute `read_file` et renvoie le contenu |
| 5 | Claude Sonnet | Repond avec `write_to_file` pour creer `test-claude.py` |
| 6 | Roo Code | Cree le fichier `test-claude.py` |
| 7 | Claude Sonnet | Met a jour la Memory Bank et execute un commit Git |
| 8 | Roo Code | Repond avec `attempt_completion` |

**Verification :**
```powershell
Test-Path test-claude.py   # Doit retourner True
git log --oneline -3       # Doit montrer un commit recent
```

### Etape 10.6 — Marquer la Phase 10 Complete dans la Memory Bank

Mettez a jour `memory-bank/progress.md` pour cocher la Phase 10, puis commitez :
```powershell
git add memory-bank/progress.md
git commit -m "docs(memory): phase 10 complete - API Anthropic Claude Sonnet configure et valide"
```

---

## Recapitulatif des Fichiers Crees et Versionnement

A la fin de ce plan, votre depot Git contient :

```
mon-projet-uadf/
|
+-- .clinerules          [VERSIONNE] Directives Memory Bank + REGLE 5 Git
+-- .gitignore           [VERSIONNE] Exclusions Git
+-- .roomodes            [VERSIONNE] Personas Agile RBAC avec regles Git
+-- Modelfile            [VERSIONNE] Config modele Ollama uadf-agent
+-- proxy.py             [VERSIONNE] Serveur proxy Gemini Chrome
+-- requirements.txt     [VERSIONNE] Dependances Python
|
+-- scripts/
|   +-- start-proxy.ps1  [VERSIONNE] Script demarrage proxy
|
+-- memory-bank/         [VERSIONNE] Memoire persistante complete
|   +-- activeContext.md
|   +-- decisionLog.md
|   +-- productContext.md
|   +-- progress.md
|   +-- projectBrief.md
|   +-- systemPatterns.md
|   +-- techContext.md
|
+-- docs/
|   +-- qa/              [VERSIONNE] Rapports QA
|
+-- venv/                [EXCLU de Git via .gitignore]
+-- .env                 [EXCLU de Git via .gitignore]
```

**Historique Git attendu apres installation complete :**
```
git log --oneline
```
```
abc1234 docs(memory): phase 10 complete - API Anthropic configure
def5678 feat(proxy): ajout serveur proxy UADF FastAPI + script demarrage
ghi9012 feat(uadf): initialisation Memory Bank + .clinerules (5 regles dont Git)
jkl3456 feat(agile): ajout personas Agile RBAC avec regles Git (.roomodes)
mno7890 feat: ajout Modelfile Ollama (uadf-agent, T=0.15, ctx=131072)
pqr1234 chore: initialisation depot UADF - squelette projet et .gitignore
```

---

## Guide de Demarrage Quotidien

### Mode Local (Ollama — Souverain et Gratuit)
1. Verifiez que Ollama est en cours d'execution (icone zone de notification)
2. Ouvrez VS Code avec votre projet
3. Dans Roo Code, selectionnez le backend **Ollama** (`uadf-agent`)
4. Selectionnez le mode Agile approprie (Developer, PO, QA...)
5. Commencez a travailler — Roo Code lira la Memory Bank et commitera automatiquement

### Mode Proxy Gemini Chrome (Cloud Gratuit + Copier-Coller)
1. Ouvrez un terminal dans VS Code
2. Activez l'environnement virtuel : `.\venv\Scripts\Activate.ps1`
3. Demarrez le proxy : `.\scripts\start-proxy.ps1`
4. Dans Roo Code, selectionnez le backend **OpenAI Compatible** (port 8000)
5. Ouvrez Chrome avec votre Gem "Roo Code Agent"
6. A chaque requete, le proxy vous guidera pour le copier-coller

### Mode Cloud Claude Sonnet (Payant et Entierement Automatique)
1. Verifiez votre connexion Internet et votre credit Anthropic
2. Dans Roo Code, selectionnez le backend **Anthropic** (`claude-sonnet-4-5`)
3. Commencez a travailler — tout est automatique, Roo Code commitera apres chaque tache

### Tableau de Correspondance Phases / Exigences (Complet)

| Phase | Description | Exigences PRD |
| :--- | :--- | :--- |
| Phase 0 | Base saine VS Code + Roo Code | REQ-000 |
| Phase 1 | Installation Ollama + modeles | REQ-1.0, REQ-1.1, REQ-1.2 |
| Phase 2 | Depot Git + .gitignore complet | REQ-000, REQ-4.1, REQ-4.5 |
| Phase 3 | Modelfile personnalise + commit | REQ-1.2, REQ-1.3 |
| Phase 4 | .roomodes personas Agile + regles Git | REQ-3.1, REQ-3.2, REQ-3.3 |
| Phase 5 | .clinerules (REGLE 5 Git + REGLE 6 Prompts) + 7 fichiers Memory Bank | REQ-4.1 a REQ-4.5 |
| Phase 6 | proxy.py + scripts/ + commit | REQ-2.1.1 a REQ-2.4.3 |
| Phase 7 | Gem Gemini Chrome + doc Memory Bank | REQ-5.1, REQ-5.2, REQ-5.3 |
| Phase 8 | Roo Code commutateur 3 modes LLM | REQ-2.0, REQ-6.0 |
| Phase 9 | Tests end-to-end (dont test Git auto-portant) | REQ-000 |
| Phase 10 | API Anthropic Claude Sonnet | REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4 |
| Phase 11 | Registre central des prompts (prompts/) | REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5 |
| Phase 12 | Verification automatique coherence prompts (script + hook pre-commit) | REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4 |

---

## PHASE 11 : Registre Central des System Prompts

**Objectif :** Creer le repertoire `prompts/` avec les 7 fichiers SP canoniques, initialiser le registre comme source de verite unique pour tous les system prompts du systeme UADF.
**Exigences adressees :** REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5
**Decision architecturale :** DA-012

> **Pourquoi cette phase est importante :** Les system prompts sont disperses dans plusieurs artefacts (.roomodes JSON, .clinerules texte, Modelfile compile, Gemini Web externe). Sans registre centralise, une modification de proxy.py peut rendre le Gem Gemini incoherent sans que personne ne le remarque. Le repertoire `prompts/` resout ce probleme en maintenant une copie canonique et versionnee de chaque prompt avec sa cible de deploiement exacte.

### Etape 11.1 — Creer le Repertoire `prompts/`

```powershell
mkdir prompts
```

### Etape 11.2 — Creer le Fichier Index `prompts/README.md`

```powershell
New-Item -Path "prompts" -Name "README.md" -ItemType File
```

Ouvrez `prompts/README.md` et collez :

```markdown
# Registre Central des System Prompts — UADF
## Source de Verite Unique pour Tous les Prompts du Systeme

**Projet :** Unified Agentic Development Framework (UADF)
**Maintenu par :** Developer / Scrum Master (via REGLE 6 de `.clinerules`)

---

## Principe Fondamental

Ce dossier `prompts/` est la **source de verite unique** pour tous les system prompts du systeme UADF.

**Toute modification d'un prompt doit :**
1. Partir de ce dossier (modifier le fichier SP-XXX canonique)
2. Etre propagee vers sa cible de deploiement (fichier de config ou interface web)
3. Etre commitee dans Git avec un message `chore(prompts): ...`

**Ne jamais modifier directement** `.roomodes`, `.clinerules`, le `Modelfile` ou le Gem Gemini
sans mettre a jour le fichier canonique correspondant dans ce dossier.

---

## Inventaire des Prompts

| ID | Fichier | Nom | Cible de Deploiement | Hors Git |
| :--- | :--- | :--- | :--- | :---: |
| **SP-001** | `SP-001-ollama-modelfile-system.md` | System Prompt Ollama Modelfile | `Modelfile` bloc SYSTEM | Non |
| **SP-002** | `SP-002-clinerules-global.md` | Directives Globales Roo Code | `.clinerules` (fichier entier) | Non |
| **SP-003** | `SP-003-persona-product-owner.md` | Persona Product Owner | `.roomodes` > `customModes[0].roleDefinition` | Non |
| **SP-004** | `SP-004-persona-scrum-master.md` | Persona Scrum Master | `.roomodes` > `customModes[1].roleDefinition` | Non |
| **SP-005** | `SP-005-persona-developer.md` | Persona Developer | `.roomodes` > `customModes[2].roleDefinition` | Non |
| **SP-006** | `SP-006-persona-qa-engineer.md` | Persona QA Engineer | `.roomodes` > `customModes[3].roleDefinition` | Non |
| **SP-007** | `SP-007-gem-gemini-roo-agent.md` | Gem Gemini Chrome "Roo Code Agent" | gemini.google.com > Gems > Instructions | **OUI** |
```

Sauvegardez (`Ctrl+S`).

### Etape 11.3 — Copier les Fichiers SP Canoniques

Si vous avez clone ce depot depuis Git, les fichiers SP sont deja presents dans `prompts/`.
Sinon, creez chaque fichier SP en copiant le contenu depuis les fichiers de reference du projet :

```powershell
# Verifier que tous les fichiers SP sont presents
Get-ChildItem prompts\ | Select-Object Name
```

Vous devez voir :
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

### Etape 11.4 — Verifier la Coherence du Registre

Verifiez que chaque fichier SP correspond bien a l'artefact deploye :

**SP-001 vs Modelfile :**
```powershell
# Afficher le bloc SYSTEM du Modelfile
Select-String -Path "Modelfile" -Pattern "SYSTEM" -Context 0,5
```
Le contenu doit correspondre au "Contenu du Prompt" dans `prompts/SP-001-ollama-modelfile-system.md`.

**SP-002 vs .clinerules :**
```powershell
# Afficher les premieres lignes de .clinerules
Get-Content .clinerules | Select-Object -First 10
```
Le contenu doit correspondre au "Contenu du Prompt" dans `prompts/SP-002-clinerules-global.md`.

**SP-003 a SP-006 vs .roomodes :**
```powershell
# Afficher les roleDefinitions de .roomodes
$modes = Get-Content .roomodes | ConvertFrom-Json
$modes.customModes | ForEach-Object { Write-Host "=== $($_.slug) ===" ; Write-Host $_.roleDefinition }
```
Chaque `roleDefinition` doit correspondre au "Contenu du Prompt" du SP correspondant.

**SP-007 (Gem Gemini) :**
> Ce prompt est externe a Git. Verifier manuellement dans l'interface Gemini que les instructions
> du Gem "Roo Code Agent" correspondent au contenu de `prompts/SP-007-gem-gemini-roo-agent.md`.

### Etape 11.5 — Versionner le Registre

```powershell
git add prompts/
git commit -m "feat(prompts): initialisation registre central SP-001 a SP-007 - source de verite unique"
```

### Etape 11.6 — Tester la REGLE 6 (Coherence Prompts)

Simulez une modification de `proxy.py` pour verifier que REGLE 6 fonctionne :

1. Dans Roo Code, passez en mode **Developer**
2. Demandez : "Modifie le timeout de proxy.py de 300 a 600 secondes"
3. Le Developer doit :
   - Modifier `proxy.py`
   - Verifier si le changement impacte SP-007 (il ne l'impacte pas dans ce cas)
   - Commiter avec `fix(proxy): augmentation timeout 300->600s`
4. Demandez ensuite : "Modifie le format des balises XML dans proxy.py"
5. Le Developer doit cette fois :
   - Modifier `proxy.py`
   - Ouvrir `prompts/README.md` pour identifier SP-007 comme impacte
   - Mettre a jour `prompts/SP-007-gem-gemini-roo-agent.md`
   - Commiter avec `"chore(prompts): mise a jour SP-007 - DEPLOIEMENT MANUEL REQUIS"`

**Critere de validation :** Le Developer applique REGLE 6 sans rappel explicite de l'utilisateur.

---

> **Note Phase 11 :** Avec la Phase 11 completee, le registre `prompts/` est initialise.
> La Phase 12 ajoute la couche de verification automatique qui rend la coherence des prompts
> techniquement garantie (et non seulement comportementalement attendue).

---

## PHASE 12 : Verification Automatique de Coherence des Prompts

**Objectif :** Creer le script `scripts/check-prompts-sync.ps1` et le hook Git pre-commit pour detecter automatiquement toute desynchronisation entre les fichiers SP canoniques du registre et leurs artefacts cibles deployes.
**Exigences adressees :** REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4
**Decision architecturale :** DA-013

> **Pourquoi cette phase est critique :** REGLE 6 dans `.clinerules` est une directive comportementale — un agent LLM peut l'ignorer. Ce script transforme la verification de coherence en contrainte technique : si un artefact est modifie sans mettre a jour le SP canonique correspondant, le commit est bloque automatiquement. C'est le passage de "on espere que l'agent respecte la regle" a "le systeme empeche techniquement la violation".

### Etape 12.1 — Creer le Script de Verification

```powershell
New-Item -Path "scripts" -Name "check-prompts-sync.ps1" -ItemType File
```

Ouvrez `scripts/check-prompts-sync.ps1` et collez le contenu suivant :

```powershell
# check-prompts-sync.ps1
# Verification de coherence entre les SP canoniques (prompts/) et les artefacts deployes
# Usage : .\scripts\check-prompts-sync.ps1
# Retourne exit code 0 si tout est synchronise, 1 si desynchronisation detectee

param(
    [switch]$Verbose = $false
)

$ErrorCount = 0
$WarningCount = 0

function Extract-SpContent {
    param([string]$SpFile)
    $content = Get-Content $SpFile -Raw
    # Extraire le contenu entre les premieres balises de code apres "## Contenu du Prompt"
    if ($content -match '## Contenu du Prompt[\s\S]*?```[\w]*\n([\s\S]*?)```') {
        return $matches[1].Trim()
    }
    return $null
}

function Compare-Content {
    param([string]$Expected, [string]$Actual, [string]$SpId, [string]$Target)
    $expectedNorm = $Expected.Trim() -replace '\r\n', '\n' -replace '\r', '\n'
    $actualNorm = $Actual.Trim() -replace '\r\n', '\n' -replace '\r', '\n'
    if ($expectedNorm -eq $actualNorm) {
        Write-Host "  [SYNC]   $SpId -> $Target" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  [DESYNC] $SpId -> $Target" -ForegroundColor Red
        if ($Verbose) {
            Write-Host "  --- Contenu SP canonique ---" -ForegroundColor Yellow
            Write-Host $Expected.Substring(0, [Math]::Min(200, $Expected.Length)) -ForegroundColor Yellow
            Write-Host "  --- Contenu deploye ---" -ForegroundColor Yellow
            Write-Host $Actual.Substring(0, [Math]::Min(200, $Actual.Length)) -ForegroundColor Yellow
        }
        return $false
    }
}

Write-Host ""
Write-Host "=== VERIFICATION COHERENCE REGISTRE PROMPTS UADF ===" -ForegroundColor Cyan
Write-Host ""

# --- SP-001 : Modelfile bloc SYSTEM ---
Write-Host "SP-001 : Modelfile bloc SYSTEM" -ForegroundColor White
if (Test-Path "Modelfile") {
    $spContent = Extract-SpContent "prompts\SP-001-ollama-modelfile-system.md"
    $modelfileContent = Get-Content "Modelfile" -Raw
    if ($modelfileContent -match 'SYSTEM\s+"""([\s\S]*?)"""') {
        $deployedContent = $matches[1].Trim()
        if (-not (Compare-Content $spContent $deployedContent "SP-001" "Modelfile[SYSTEM]")) {
            $ErrorCount++
        }
    } else {
        Write-Host "  [WARN]   SP-001 : Bloc SYSTEM introuvable dans Modelfile" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host "  [SKIP]   SP-001 : Modelfile absent (normal si Phase 3 non completee)" -ForegroundColor Gray
}

# --- SP-002 : .clinerules ---
Write-Host "SP-002 : .clinerules" -ForegroundColor White
if (Test-Path ".clinerules") {
    $spContent = Extract-SpContent "prompts\SP-002-clinerules-global.md"
    $deployedContent = Get-Content ".clinerules" -Raw
    if (-not (Compare-Content $spContent $deployedContent "SP-002" ".clinerules")) {
        $ErrorCount++
    }
} else {
    Write-Host "  [SKIP]   SP-002 : .clinerules absent (normal si Phase 5 non completee)" -ForegroundColor Gray
}

# --- SP-003 a SP-006 : .roomodes roleDefinitions ---
Write-Host "SP-003 a SP-006 : .roomodes roleDefinitions" -ForegroundColor White
if (Test-Path ".roomodes") {
    $roomodesJson = Get-Content ".roomodes" -Raw | ConvertFrom-Json
    $spRoomodes = @{
        "SP-003" = @{ file = "prompts\SP-003-persona-product-owner.md"; slug = "product-owner"; index = 0 }
        "SP-004" = @{ file = "prompts\SP-004-persona-scrum-master.md";  slug = "scrum-master";  index = 1 }
        "SP-005" = @{ file = "prompts\SP-005-persona-developer.md";     slug = "developer";     index = 2 }
        "SP-006" = @{ file = "prompts\SP-006-persona-qa-engineer.md";   slug = "qa-engineer";   index = 3 }
    }
    foreach ($spId in $spRoomodes.Keys | Sort-Object) {
        $info = $spRoomodes[$spId]
        $spContent = Extract-SpContent $info.file
        $mode = $roomodesJson.customModes | Where-Object { $_.slug -eq $info.slug }
        if ($mode) {
            $deployedContent = $mode.roleDefinition
            if (-not (Compare-Content $spContent $deployedContent $spId ".roomodes[$($info.slug)]")) {
                $ErrorCount++
            }
        } else {
            Write-Host "  [WARN]   $spId : Mode '$($info.slug)' introuvable dans .roomodes" -ForegroundColor Yellow
            $WarningCount++
        }
    }
} else {
    Write-Host "  [SKIP]   SP-003 a SP-006 : .roomodes absent (normal si Phase 4 non completee)" -ForegroundColor Gray
}

# --- SP-007 : Gem Gemini (externe Git — verification manuelle) ---
Write-Host "SP-007 : Gem Gemini Chrome" -ForegroundColor White
Write-Host "  [MANUEL] SP-007 : VERIFICATION MANUELLE REQUISE" -ForegroundColor Magenta
Write-Host "           Verifier que le Gem 'Roo Code Agent' sur gemini.google.com" -ForegroundColor Magenta
Write-Host "           correspond au contenu de prompts\SP-007-gem-gemini-roo-agent.md" -ForegroundColor Magenta
$WarningCount++

# --- Rapport final ---
Write-Host ""
Write-Host "=== RAPPORT FINAL ===" -ForegroundColor Cyan
if ($ErrorCount -eq 0) {
    Write-Host "  RESULTAT : TOUT SYNCHRONISE ($WarningCount avertissement(s))" -ForegroundColor Green
    Write-Host ""
    exit 0
} else {
    Write-Host "  RESULTAT : $ErrorCount DESYNCHRONISATION(S) DETECTEE(S)" -ForegroundColor Red
    Write-Host "  ACTION REQUISE : Mettre a jour les fichiers SP desynchronises dans prompts/" -ForegroundColor Red
    Write-Host "  Voir prompts/README.md pour la procedure de mise a jour." -ForegroundColor Red
    Write-Host ""
    exit 1
}
```

Sauvegardez (`Ctrl+S`).

### Etape 12.2 — Tester le Script Manuellement

```powershell
.\scripts\check-prompts-sync.ps1
```

Si tout est synchronise (ce qui devrait etre le cas apres la Phase 11) :
```
=== VERIFICATION COHERENCE REGISTRE PROMPTS UADF ===

SP-001 : Modelfile bloc SYSTEM
  [SYNC]   SP-001 -> Modelfile[SYSTEM]
SP-002 : .clinerules
  [SYNC]   SP-002 -> .clinerules
SP-003 a SP-006 : .roomodes roleDefinitions
  [SYNC]   SP-003 -> .roomodes[product-owner]
  [SYNC]   SP-004 -> .roomodes[scrum-master]
  [SYNC]   SP-005 -> .roomodes[developer]
  [SYNC]   SP-006 -> .roomodes[qa-engineer]
SP-007 : Gem Gemini Chrome
  [MANUEL] SP-007 : VERIFICATION MANUELLE REQUISE
           Verifier que le Gem 'Roo Code Agent' sur gemini.google.com
           correspond au contenu de prompts\SP-007-gem-gemini-roo-agent.md

=== RAPPORT FINAL ===
  RESULTAT : TOUT SYNCHRONISE (1 avertissement(s))
```

Pour tester le mode verbose (avec diff) :
```powershell
.\scripts\check-prompts-sync.ps1 -Verbose
```

### Etape 12.3 — Creer le Hook Git pre-commit

Le hook pre-commit doit etre cree dans `.git/hooks/` (non versionne par Git lui-meme, mais le script source l'est dans `scripts/`).

```powershell
# Creer le hook pre-commit
$hookContent = @'
#!/bin/sh
# Hook Git pre-commit : verification coherence registre prompts UADF
# Ce hook appelle check-prompts-sync.ps1 avant chaque commit

echo "=== Pre-commit : verification coherence prompts UADF ==="

# Detecter si PowerShell est disponible
if command -v pwsh > /dev/null 2>&1; then
    PWSH=pwsh
elif command -v powershell > /dev/null 2>&1; then
    PWSH=powershell
else
    echo "WARN: PowerShell non disponible, verification ignoree"
    exit 0
fi

$PWSH -ExecutionPolicy Bypass -File scripts/check-prompts-sync.ps1
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "COMMIT BLOQUE : Desynchronisation detectee dans le registre prompts/"
    echo "Mettez a jour les fichiers SP desynchronises avant de commiter."
    echo "Voir prompts/README.md pour la procedure."
    exit 1
fi

exit 0
'@

Set-Content -Path ".git\hooks\pre-commit" -Value $hookContent -Encoding UTF8
Write-Host "Hook pre-commit cree dans .git/hooks/pre-commit"
```

> **Note :** Le hook `.git/hooks/pre-commit` n'est pas versionne par Git (le dossier `.git/` est exclu).
> Pour partager ce hook avec d'autres developpeurs, le script source `scripts/check-prompts-sync.ps1`
> est versionne. Chaque developpeur doit executer l'etape 12.3 apres avoir clone le depot.

### Etape 12.4 — Documenter l'Installation du Hook dans le README

Ajoutez une section dans `README.md` du projet (ou creez-le) :

```markdown
## Installation apres clonage

Apres avoir clone ce depot, executer :

```powershell
# Installer le hook Git pre-commit (verification coherence prompts)
.\scripts\check-prompts-sync.ps1  # Tester d'abord
# Puis creer le hook (voir Phase 12 de DOC3-Plan-Implementation-Windows-VSCode-SUITE.md)
```
```

### Etape 12.5 — Tester le Hook pre-commit

Simulez une desynchronisation pour verifier que le hook bloque bien le commit :

```powershell
# 1. Modifier .clinerules sans mettre a jour SP-002
Add-Content .clinerules "`n# TEST DESYNC"

# 2. Tenter un commit — doit etre bloque
git add .clinerules
git commit -m "test: verification hook pre-commit"
```

Resultat attendu :
```
=== Pre-commit : verification coherence prompts UADF ===
...
  [DESYNC] SP-002 -> .clinerules
...
COMMIT BLOQUE : Desynchronisation detectee dans le registre prompts/
Mettez a jour les fichiers SP desynchronises avant de commiter.
```

Restaurez l'etat propre :
```powershell
git checkout .clinerules
```

**Critere de validation :** Le commit est bloque quand `.clinerules` est modifie sans mettre a jour `prompts/SP-002-clinerules-global.md`.

### Etape 12.6 — Versionner le Script

```powershell
git add scripts/check-prompts-sync.ps1
git commit -m "feat(prompts): ajout script verification coherence + hook pre-commit (DA-013)"
```

---

> **Note finale — Systeme UADF complet :** Avec la Phase 12 completee, toutes les phases (0 a 12)
> sont validees. Le systeme dispose maintenant de trois couches de protection contre la
> desynchronisation des prompts :
>
> 1. **Comportementale** : REGLE 6 dans `.clinerules` (agent LLM)
> 2. **Procedurale** : Fichiers SP canoniques dans `prompts/` avec metadonnees YAML
> 3. **Technique** : Hook Git pre-commit bloquant les commits avec desynchronisation detectee
>
> SP-007 (Gem Gemini) reste le seul point de vigilance manuelle — aucune automatisation
> n'est possible pour un artefact externe a Git.
