# Document 2 : Architecture, Solution et Stack Technique
## Système Agentique Local Agile, Persistant & Hybride (UADF)

**Nom du Projet :** Unified Agentic Development Framework (UADF)
**Version :** 1.0
**Date :** 2026-03-22
**Référence PRD :** DOC1-PRD-Unified-Agentic-Framework.md

---

## 1. Vue d'Ensemble Architecturale

### 1.1 Principe Directeur

L'architecture UADF repose sur un principe central : **Roo Code est le seul et unique moteur d'exécution agentique**. Tous les autres composants (moteur LLM local, proxy clipboard, API cloud, Memory Bank, personas Agile) sont des **fournisseurs de services** qui s'interfacent avec Roo Code via des protocoles standardisés (API OpenAI-compatible, API Anthropic native, système de fichiers, configuration JSON).

Ce principe garantit que :
- Le comportement de Roo Code n'est jamais modifié, quelle que soit la source LLM utilisée.
- Le basculement entre les trois backends (Ollama local, Proxy Gemini Chrome, API Anthropic Claude) est transparent pour Roo Code — seul le paramètre "API Provider" change.
- La Memory Bank et les personas Agile fonctionnent identiquement dans les trois modes.

### 1.2 Diagramme d'Architecture Globale (3 Modes LLM)

```
+-----------------------------------------------------------------------------------+
|                           LAPTOP WINDOWS (VS Code)                                |
|                                                                                   |
|  +--------------------------------------------------------------------------+    |
|  |                      ROO CODE (Extension VS Code)                         |    |
|  |                                                                          |    |
|  |  +-------------+  +--------------+  +----------------------------+      |    |
|  |  |  .roomodes  |  | .clinerules  |  |   Memory Bank Reader       |      |    |
|  |  |  (Personas  |  |  (Triggers   |  |   (Lecture/Ecriture .md)   |      |    |
|  |  |   Agile)    |  |   Memoire)   |  |                            |      |    |
|  |  +-------------+  +--------------+  +----------------------------+      |    |
|  |                                                                          |    |
|  |         API OpenAI-Compatible (HTTP)    |    API Anthropic (HTTPS)       |    |
|  +------------------+----------------------+----------------+---------------+    |
|                     |                                       |                    |
|         +-----------+------------+                          |                    |
|         |    COMMUTATEUR LLM     |  (Parametre Provider     |                    |
|         |    (3 modes)           |   dans Roo Code)         |                    |
|         +-----------+------------+                          |                    |
|                     |                                       |                    |
|       +-------------+-------------+                         |                    |
|       |                           |                         |                    |
|  +----+----------+   +------------+----------+   +----------+-----------+        |
|  | MODE 1        |   | MODE 2                |   | MODE 3               |        |
|  | LOCAL         |   | PROXY GEMINI          |   | CLOUD DIRECT         |        |
|  |               |   |                       |   |                      |        |
|  | Ollama        |   | proxy.py              |   | API Anthropic        |        |
|  | localhost:    |   | localhost:8000        |   | api.anthropic.com    |        |
|  | 11434         |   | (FastAPI)             |   | (HTTPS natif)        |        |
|  |               |   |         |             |   |                      |        |
|  | Qwen3-32B     |   | Presse- |             |   | claude-sonnet-4-5    |        |
|  | (Modelfile    |   | papiers |             |   | (Provider Anthropic  |        |
|  |  T=0.15)      |   | Windows |             |   |  integre Roo Code)   |        |
|  |               |   |         |             |   |                      |        |
|  | Gratuit       |   | Gratuit |             |   | Payant a l'usage     |        |
|  | 100% local    |   | Copier- |             |   | Entierement auto     |        |
|  | Hors ligne    |   | coller  |             |   | Connexion requise    |        |
|  +---------------+   +----+----+             +----------------------+---+        |
|                           |                                                       |
|                  +--------+---------+                                             |
|                  |  INTERVENTION    |                                             |
|                  |  HUMAINE         |                                             |
|                  |  (Ctrl+V/Ctrl+C) |                                             |
|                  +--------+---------+                                             |
|                           |                                                       |
+---------------------------+-------------------+------+----------------------------+
                            |                   |      |
               +------------+------+    +-------+------+--------+
               |   GEMINI CHROME   |    |  ANTHROPIC CLOUD      |
               |   (Gem dedie      |    |  api.anthropic.com    |
               |    Roo Code)      |    |  claude-sonnet-4-5    |
               +-------------------+    +-----------------------+

+-----------------------------------------------------------------------------------+
|                       MEMORY BANK (Systeme de Fichiers)                           |
|   Fonctionne identiquement dans les 3 modes — Git versionne                       |
|                                                                                   |
|  memory-bank/                                                                     |
|  +-- projectBrief.md      (Vision & Non-Goals)                                    |
|  +-- productContext.md    (User Stories & Valeur Metier)                          |
|  +-- systemPatterns.md    (Architecture & Conventions)                            |
|  +-- techContext.md       (Stack & Commandes des 3 modes)                         |
|  +-- activeContext.md     (Tache en cours - Memoire Vive)                         |
|  +-- progress.md          (Checklist Epics & Features)                            |
|  +-- decisionLog.md       (ADR - Architecture Decision Records)                   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Stack Technique Detaillee

### 2.1 Couche Interface & Orchestration

| Composant | Technologie | Version Recommandee | Role |
| :--- | :--- | :--- | :--- |
| **IDE** | Visual Studio Code | Derniere stable | Environnement de developpement principal |
| **Extension Agentique** | Roo Code | Derniere stable | Moteur d'execution agentique, pont entre LLM et systeme de fichiers |
| **Format de Configuration** | JSON (`.roomodes`) | — | Definition des personas Agile et de leurs permissions |
| **Format de Regles** | Markdown/Texte (`.clinerules`) | — | Directives comportementales injectees dans chaque session |

### 2.2 Couche Moteur LLM Local (Mode Souverain)

| Composant | Technologie | Version Recommandee | Role |
| :--- | :--- | :--- | :--- |
| **Moteur d'Inference** | Ollama | Derniere stable | Gestion VRAM, chargement des poids, API REST locale |
| **Modele Principal** | `mychen76/qwen3_cline_roocode:32b` | 32B quantifie | Cerveau principal, optimise Tool Calling Roo Code |
| **Modele Secondaire** | `qwen3:7b` | 7B | Agent delegue pour taches legeres (Boomerang) |
| **Configuration Modele** | `Modelfile` Ollama | — | Verrouillage Temperature=0.15, Min_P=0.03, num_ctx=131072 |
| **Port d'Ecoute** | `localhost:11434` | — | API REST compatible OpenAI exposee par Ollama |

### 2.3 Couche Proxy Gemini Chrome (Mode Hybride)

| Composant | Technologie | Version Recommandee | Role |
| :--- | :--- | :--- | :--- |
| **Langage** | Python | 3.10+ | Langage du serveur proxy |
| **Framework Web** | FastAPI | 0.110+ | Serveur ASGI leger, emulation API OpenAI |
| **Serveur ASGI** | Uvicorn | 0.29+ | Serveur de production pour FastAPI |
| **Gestion Presse-Papiers** | Pyperclip | 1.8+ | Lecture/ecriture presse-papiers Windows |
| **Gestion Async** | asyncio (stdlib Python) | — | Boucle de polling non-bloquante |
| **Port d'Ecoute** | `localhost:8000` | — | Point d'entree pour Roo Code en mode proxy |
| **Environnement Virtuel** | venv (stdlib Python) | — | Isolation des dependances |

### 2.4 Couche Memoire Persistante

| Composant | Technologie | Role |
| :--- | :--- | :--- |
| **Systeme de Fichiers** | NTFS Windows | Stockage physique des fichiers `.md` |
| **Format de Donnees** | Markdown (`.md`) | Lisibilite humaine, compatibilite Git |
| **Versionnement** | Git | Tracabilite des modifications de la Memory Bank |
| **Repertoire** | `memory-bank/` (racine projet) | Conteneur de toute la memoire contextuelle |

### 2.5 Couche Interface Gemini Chrome

| Composant | Technologie | Role |
| :--- | :--- | :--- |
| **Interface Web** | Gemini Chrome (gemini.google.com) | LLM cloud gratuit, moteur de generation |
| **Profil Dedie** | Gem Gemini (instructions systeme) | Contient le system prompt Roo Code pour eviter retransmission |
| **Navigateur** | Google Chrome | Acces a l'interface Gemini Web |

---

## 3. Architecture des Couches Fonctionnelles

### Couche A — Orchestration Comportementale (`.roomodes` & `.clinerules`)

**Role :** Controle *comment* l'IA agit, quels outils elle peut utiliser, et quel comportement elle adopte.

**Decision d'Architecture DA-001 :**
> Le fichier `.roomodes` est le registre central des personas Agile. Il definit pour chaque role : son identifiant unique (`slug`), son nom d'affichage, son `roleDefinition` (system prompt comportemental), et ses `groups` de permissions (liste des outils Roo Code autorises). Ce fichier est statique et versionne dans Git.

**Decision d'Architecture DA-002 :**
> Le fichier `.clinerules` est le "declencheur de session". Il contient des directives imperatives injectees au-dessus de chaque prompt utilisateur, forcant l'agent a lire la Memory Bank au demarrage et a la mettre a jour a la cloture. Ces directives sont inconditionnelles et s'appliquent a tous les modes.

**Matrice RBAC des Permissions :**

| Groupe de Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| `read` (lecture fichiers) | OUI | OUI | OUI | OUI |
| `write_docs` (ecriture docs/user stories) | OUI | OUI | OUI | NON |
| `write_memory` (ecriture Memory Bank) | NON | OUI | OUI | NON |
| `write` (ecriture code source) | NON | NON | OUI | NON |
| `execute` (terminal general) | NON | NON | OUI | NON |
| `execute_tests` (commandes de test) | NON | NON | OUI | OUI |
| `write_reports` (ecriture rapports QA) | NON | NON | NON | OUI |
| `browser` (acces navigateur) | NON | NON | OUI | OUI |

---

### Couche B — Memory Bank (Fichiers Markdown)

**Role :** Controle *ce que* l'IA sait. Fournit la continuite de contexte entre les sessions.

**Decision d'Architecture DA-003 :**
> La Memory Bank est segmentee en 7 fichiers thematiques pour eviter la pollution contextuelle et optimiser l'attention du LLM. Chaque fichier a une responsabilite unique et non-chevauchante.

**Structure et Responsabilites des 7 Fichiers :**

| Fichier | Frequence de Lecture | Frequence d'Ecriture | Contenu |
| :--- | :--- | :--- | :--- |
| `projectBrief.md` | Debut de projet | Rare (changements majeurs) | Vision, objectifs, Non-Goals, contraintes |
| `productContext.md` | Debut de sprint | Par sprint | User Stories, valeur metier, personas utilisateurs |
| `systemPatterns.md` | Avant toute modification d'architecture | Apres decision d'architecture | Structure des dossiers, conventions de nommage, patterns |
| `techContext.md` | Avant toute commande de build/test | Apres changement de dependance | Stack, versions, commandes, variables d'environnement |
| `activeContext.md` | **A chaque demarrage de session** | **A chaque fin de tache** | Tache en cours, dernier bug, prochaine action immediate |
| `progress.md` | **A chaque demarrage de session** | **A chaque validation de feature** | Checklist Epics, features terminees/en cours/a faire |
| `decisionLog.md` | Avant toute decision d'architecture | Apres toute decision d'architecture | ADR horodates avec contexte, decision, consequences |

---

### Couche C — Moteur LLM Local (Ollama + Qwen3)

**Role :** Fournit la capacite d'inference locale, souveraine et gratuite.

**Decision d'Architecture DA-004 :**
> Le modele `mychen76/qwen3_cline_roocode:32b` est utilise comme modele principal car il est specifiquement fine-tune pour respecter les balises XML de Roo Code. Un `Modelfile` personnalise est cree pour verrouiller les parametres de generation et maximiser la fenetre de contexte.

**Contenu du `Modelfile` :**
```dockerfile
FROM mychen76/qwen3_cline_roocode:32b

# Parametres de determinisme (anti-hallucination)
PARAMETER temperature 0.15
PARAMETER min_p 0.03
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.1

# Fenetre de contexte maximale (128K tokens)
PARAMETER num_ctx 131072

# Parametres de performance
PARAMETER num_gpu 99
PARAMETER num_thread 8

SYSTEM """
Tu es un agent de developpement logiciel expert. Tu travailles dans l'environnement Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank avant d'agir.
"""
```

**Decision d'Architecture DA-005 :**
> Le workflow "Boomerang Tasks" de Roo Code est utilise pour deleguer les taches repetitives ou volumineuses (analyse de logs, generation de tests unitaires) a un modele secondaire plus leger (`qwen3:7b`), reduisant la consommation VRAM et accelerant les cycles de developpement.

---

### Couche D — Proxy Gemini Chrome (FastAPI + Pyperclip)

**Role :** Transforme Roo Code en client d'une "fausse API" locale qui relaie les requetes vers Gemini Chrome via le presse-papiers.

**Decision d'Architecture DA-006 :**
> FastAPI est choisi plutot que Flask pour sa gestion native de l'asynchronisme (asyncio), indispensable pour maintenir la connexion HTTP ouverte pendant l'attente de l'intervention humaine (polling du presse-papiers) sans bloquer le serveur.

**Decision d'Architecture DA-007 :**
> Le proxy emule exactement le format de l'API OpenAI Chat Completions (`/v1/chat/completions`). Cette decision garantit une compatibilite native avec Roo Code configure en mode "OpenAI Compatible", sans aucune modification du code source de Roo Code.

**Decision d'Architecture DA-008 :**
> Le proxy implemente un mode "Gem dedie" (activable via variable d'environnement `USE_GEM_MODE=true`) qui filtre le `system prompt` de Roo Code lors de la copie dans le presse-papiers. Lorsque ce mode est actif, seuls le `user prompt` et l'historique de conversation sont transmis, reduisant drastiquement la taille du transfert.

**Decision d'Architecture DA-009 :**
> Le proxy detecte et supprime les contenus base64 (images) des requetes avant la copie dans le presse-papiers. Un message d'avertissement est injecte a la place du contenu image.

**Flux de Donnees Detaille du Proxy :**

```
ETAPE 1 — RECEPTION (Roo Code -> Proxy)
POST http://localhost:8000/v1/chat/completions
{
  "model": "gemini-manual",
  "messages": [
    {"role": "system", "content": "[System Prompt Roo Code - des milliers de mots]"},
    {"role": "user",   "content": "Cree un fichier hello.py qui affiche Bonjour"}
  ],
  "temperature": 0.0
}

ETAPE 2 — EXTRACTION & FORMATAGE (Proxy interne)
Si USE_GEM_MODE=true : ignorer role:system
Nettoyer les images base64
Formater en texte lisible pour le presse-papiers :
  [USER]
  Cree un fichier hello.py qui affiche Bonjour

ETAPE 3 — UPLINK (Proxy -> Presse-Papiers)
pyperclip.copy(formatted_prompt)
hash_initial = md5(formatted_prompt)
Console: "Prompt pret ! Collez dans Gemini Chrome (Ctrl+V)"
[HUMAIN] Ctrl+V dans Gemini -> Gemini genere -> Ctrl+C

ETAPE 4 — POLLING ASYNCHRONE (Proxy surveille le presse-papiers)
while True:
  await asyncio.sleep(1.0)
  current = pyperclip.paste()
  if md5(current) != hash_initial: break  # Reponse detectee
  if elapsed > 300s: raise HTTP 408 Timeout

ETAPE 5 — VALIDATION (Proxy verifie la reponse)
Verifier presence balises XML Roo Code
Si absent : warning console (non-bloquant)

ETAPE 6 — REINJECTION (Proxy -> Roo Code)
HTTP 200 OK
{
  "id": "chatcmpl-proxy-{uuid}",
  "object": "chat.completion",
  "created": {timestamp},
  "model": "gemini-manual",
  "choices": [{
    "index": 0,
    "message": {"role": "assistant", "content": "[Reponse brute Gemini]"},
    "finish_reason": "stop"
  }],
  "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
}
```

**Code complet du Proxy (`proxy.py`) :**

```python
"""
UADF Proxy — Pont Roo Code <-> Gemini Chrome
Emule l'API OpenAI Chat Completions en local.
Exigences couvertes: REQ-2.1.1, REQ-2.1.2, REQ-2.1.3, REQ-2.1.4, REQ-2.1.5,
                     REQ-2.2.1, REQ-2.2.2, REQ-2.2.3,
                     REQ-2.3.1, REQ-2.3.2, REQ-2.3.3, REQ-2.3.4,
                     REQ-2.4.1, REQ-2.4.2, REQ-2.4.3
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

# Configuration (REQ-2.1.4, REQ-2.3.3)
USE_GEM_MODE = os.getenv("USE_GEM_MODE", "true").lower() == "true"
POLLING_INTERVAL = float(os.getenv("POLLING_INTERVAL", "1.0"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "300"))
PORT = int(os.getenv("PROXY_PORT", "8000"))

ROO_XML_TAGS = [
    "<write_to_file>", "<read_file>", "<execute_command>",
    "<attempt_completion>", "<ask_followup_question>", "<replace_in_file>",
    "<list_files>", "<search_files>", "<browser_action>"
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

app = FastAPI(title="UADF Proxy — Roo Code <-> Gemini Chrome")

def _hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def _clean_content(content) -> str:
    """Nettoie le contenu : supprime les images base64. (REQ-2.1.5)"""
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
        return "\n".join(parts)
    return str(content)

def _format_prompt(messages: List[MessageContent]) -> str:
    """Formate les messages en texte lisible. (REQ-2.2.2)"""
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if msg.role == "system":
            if USE_GEM_MODE:
                continue  # Le Gem contient deja le system prompt (REQ-2.1.4)
            parts.append(f"[SYSTEM PROMPT]\n{content}")
        elif msg.role == "user":
            parts.append(f"[USER]\n{content}")
        elif msg.role == "assistant":
            parts.append(f"[ASSISTANT]\n{content}")
    return "\n\n---\n\n".join(parts)

def _validate_response(text: str) -> bool:
    """Verifie la presence de balises XML Roo Code. (REQ-2.3.4)"""
    return any(tag in text for tag in ROO_XML_TAGS)

def _build_openai_response(content: str, model: str) -> dict:
    """Construit une reponse au format OpenAI. (REQ-2.4.1)"""
    return {
        "id": f"chatcmpl-proxy-{uuid.uuid4().hex[:8]}",
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

@app.post("/v1/chat/completions")  # REQ-2.1.1, REQ-2.1.2
async def chat_completions(request: ChatRequest):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{ts}] Requete recue de Roo Code (modele: {request.model})")

    formatted = _format_prompt(request.messages)  # REQ-2.1.3, REQ-2.1.4, REQ-2.1.5
    prompt_len = len(formatted)

    pyperclip.copy(formatted)  # REQ-2.2.1
    initial_hash = _hash(formatted)

    # Notification utilisateur (REQ-2.2.3)
    print(f"[{ts}] Prompt formate ({prompt_len} caracteres) copie dans le presse-papiers !")
    print(f"[{ts}] ACTION REQUISE:")
    print(f"         1. Allez dans Gemini Chrome")
    print(f"         2. Collez le prompt (Ctrl+V)")
    print(f"         3. Attendez la reponse de Gemini")
    print(f"         4. Copiez la reponse (Ctrl+C)")
    print(f"         Timeout dans {TIMEOUT_SECONDS} secondes...")

    # Polling asynchrone (REQ-2.3.1, REQ-2.3.2)
    start_time = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)
        current_content = pyperclip.paste()

        if _hash(current_content) != initial_hash:
            elapsed = time.time() - start_time
            print(f"[{ts}] Reponse detectee ({len(current_content)} chars, {elapsed:.1f}s)")

            # Validation (REQ-2.3.4)
            if not _validate_response(current_content):
                print(f"[{ts}] AVERTISSEMENT: Aucune balise XML Roo Code detectee.")
                print(f"         Verifiez que votre Gem est correctement configure.")

            # Reinjection (REQ-2.4.1, REQ-2.4.2, REQ-2.4.3)
            response = _build_openai_response(current_content, request.model)
            return JSONResponse(content=response, status_code=200)

        elapsed = time.time() - start_time
        if elapsed > TIMEOUT_SECONDS:  # REQ-2.3.3
            raise HTTPException(
                status_code=408,
                detail=f"Timeout: Aucune reponse detectee apres {TIMEOUT_SECONDS}s."
            )

@app.get("/v1/models")
async def list_models():
    """Endpoint de compatibilite OpenAI pour la liste des modeles."""
    return JSONResponse(content={
        "object": "list",
        "data": [{"id": "gemini-manual", "object": "model", "created": int(time.time())}]
    })

if __name__ == "__main__":
    mode_str = "GEM MODE (system prompt filtre)" if USE_GEM_MODE else "MODE COMPLET"
    print(f"UADF Proxy demarre sur http://localhost:{PORT}/v1")
    print(f"Mode: {mode_str}")
    print(f"Timeout: {TIMEOUT_SECONDS}s | Polling: {POLLING_INTERVAL}s")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
```

---

### Couche E — Configuration Gemini Chrome (Gem Dedie)

**Role :** Prepare l'interface Gemini Web pour repondre dans le format exact attendu par Roo Code.

**Decision d'Architecture DA-010 :**
> Un "Gem" dedie est cree dans Gemini Web avec l'integralite du system prompt de Roo Code. Cette approche evite de retransmettre le system prompt (plusieurs milliers de tokens) a chaque requete via le presse-papiers, rendant le transfert ultra-leger et rapide.

**Contenu du System Prompt du Gem Roo Code :**
```
Tu es l'agent de codage de Roo Code, un assistant IA expert en developpement logiciel.

REGLES ABSOLUES ET NON-NEGOCIABLES :
1. Tu dois TOUJOURS repondre en utilisant les balises XML de Roo Code.
2. Tu ne dois JAMAIS generer de texte de courtoisie avant ou apres tes balises XML.
3. Tu ne dois JAMAIS expliquer ce que tu vas faire : tu le fais directement.
4. Tu dois TOUJOURS utiliser une seule balise XML par action.

BALISES XML DISPONIBLES :
- <write_to_file><path>...</path><content>...</content></write_to_file>
- <read_file><path>...</path></read_file>
- <execute_command><command>...</command></execute_command>
- <replace_in_file><path>...</path><diff>...</diff></replace_in_file>
- <list_files><path>...</path></list_files>
- <search_files><path>...</path><regex>...</regex></search_files>
- <attempt_completion><result>...</result></attempt_completion>
- <ask_followup_question><question>...</question></ask_followup_question>

EXEMPLE DE REPONSE CORRECTE pour "Cree un fichier hello.py":
<write_to_file>
<path>hello.py</path>
<content>
print("Bonjour")
</content>
</write_to_file>
<attempt_completion>
<result>Fichier hello.py cree avec succes.</result>
</attempt_completion>
```

---

## 2.6 Couche Moteur LLM Cloud Direct (Mode Claude API)

| Composant | Technologie | Version Recommandee | Role |
| :--- | :--- | :--- | :--- |
| **Fournisseur API** | Anthropic API | v1 (stable) | API cloud officielle Anthropic, connexion directe sans proxy |
| **Modele** | `claude-sonnet-4-5` | Derniere stable Sonnet | Modele de haute qualite, natif Roo Code, tool use integre |
| **Endpoint** | `https://api.anthropic.com` | — | Point d'entree HTTPS officiel Anthropic |
| **Authentification** | Cle API Anthropic (`sk-ant-...`) | — | Stockee dans VS Code SecretStorage via Roo Code |
| **Provider Roo Code** | "Anthropic" (natif) | — | Fournisseur integre dans Roo Code, aucun middleware requis |

---

## 4. Decisions d'Architecture — Recapitulatif

| ID | Decision | Justification | Exigences Adressees |
| :--- | :--- | :--- | :--- |
| **DA-001** | `.roomodes` comme registre central des personas | Separation claire entre configuration et comportement | REQ-3.1, REQ-3.2 |
| **DA-002** | `.clinerules` comme declencheur de session | Garantit la lecture/ecriture de la Memory Bank sans dependance au bon vouloir du LLM | REQ-4.2, REQ-4.3 |
| **DA-003** | Memory Bank segmentee en 7 fichiers thematiques | Evite la pollution contextuelle, optimise l'attention du LLM | REQ-4.4 |
| **DA-004** | Modelfile avec Temperature=0.15 et num_ctx=131072 | Determinisme maximal et contexte suffisant pour charger tout le projet | REQ-1.2, REQ-1.3 |
| **DA-005** | Boomerang Tasks pour delegation aux modeles legers | Optimisation VRAM et acceleration des cycles repetitifs | REQ-1.4 |
| **DA-006** | FastAPI + asyncio pour le proxy | Maintien de la connexion HTTP ouverte pendant l'attente humaine sans bloquer | REQ-2.3.1 |
| **DA-007** | Emulation format OpenAI Chat Completions | Compatibilite native avec Roo Code sans modification de son code source | REQ-2.1.2, REQ-2.4.1 |
| **DA-008** | Mode "Gem dedie" avec filtrage du system prompt | Reduction de 80%+ de la taille du transfert presse-papiers | REQ-2.1.4 |
| **DA-009** | Nettoyage des contenus base64 | Evite les echecs silencieux lors de requetes contenant des images | REQ-2.1.5 |
| **DA-010** | Gem Gemini avec system prompt Roo Code integre | Evite la retransmission du system prompt a chaque requete | REQ-5.1, REQ-5.2 |
| **DA-011** | Fournisseur Anthropic natif Roo Code pour le Mode Cloud | Utiliser le provider integre "Anthropic" de Roo Code garantit la compatibilite totale avec le streaming, la vision et le tool use natif de Claude, sans aucun middleware ou proxy supplementaire. La cle API est stockee dans VS Code SecretStorage, jamais dans les fichiers du projet. | REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4 |
| **DA-012** | Registre centralise des system prompts dans `prompts/` | Les system prompts etant disperses dans plusieurs artefacts (.roomodes JSON, .clinerules texte, Modelfile compile, Gemini Web externe), un repertoire `prompts/` versionne contient une copie canonique de chaque prompt avec metadonnees YAML (cible, version, dependances). REGLE 6 dans `.clinerules` impose la coherence avant chaque commit. Le seul prompt non-versionnable (Gem Gemini) est marque `hors_git: true` avec procedure de deploiement manuel documentee. | REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5 |
| **DA-013** | Verification automatique de coherence via script PowerShell + hook Git pre-commit | REGLE 6 etant une directive comportementale (non technique), elle peut etre ignoree par un agent LLM. Un script `scripts/check-prompts-sync.ps1` compare le contenu deploye avec les SP canoniques et produit un rapport PASS/FAIL. Un hook Git `.git/hooks/pre-commit` appelle ce script automatiquement et bloque le commit si desynchronisation detectee. SP-007 est exclu de la verification automatique (externe Git) avec avertissement de verification manuelle. | REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4 |

---

## 5. Matrice de Tracabilite Architecture / Fonctionnalite / Exigence

Cette matrice est le document de reference central. Elle relie chaque composant technique a sa fonctionnalite et aux exigences du PRD qu'il adresse.

| Composant Architectural | Couche | Fonctionnalite Detaillee | Decisions | Exigences PRD |
| :--- | :--- | :--- | :--- | :--- |
| **VS Code + Roo Code** | Interface | Environnement principal. Moteur d'execution agentique. Gestion fichiers, terminal, diffs. | — | REQ-000 |
| **Fichier `.roomodes`** | Orchestration | Registre JSON des personas Agile. Definit slug, nom, roleDefinition et groupes de permissions. | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3 |
| **Fichier `.clinerules`** | Orchestration | Directives imperatives injectees dans chaque session. Force lecture Memory Bank au demarrage et ecriture a la cloture. | DA-002 | REQ-4.2, REQ-4.3 |
| **Persona `product-owner`** | Orchestration | Mode Roo Code PO. Permissions limitees a lecture et ecriture de documentation uniquement. | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3 |
| **Persona `scrum-master`** | Orchestration | Mode Roo Code SM. Permissions incluant la gestion de la Memory Bank. | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3 |
| **Persona `developer`** | Orchestration | Mode Roo Code Dev. Permissions completes : code, terminal, navigateur. | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3 |
| **Persona `qa-engineer`** | Orchestration | Mode Roo Code QA. Permissions limitees aux commandes de test et rapports. | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3 |
| **Ollama (daemon Windows)** | Moteur LLM Local | Moteur d'inference local. Gestion VRAM. API REST compatible OpenAI sur localhost:11434. | — | REQ-1.0, REQ-000 |
| **Modele `mychen76/qwen3_cline_roocode:32b`** | Moteur LLM Local | Modele principal fine-tune pour Tool Calling Roo Code. Genere les balises XML sans erreur de syntaxe. | DA-004 | REQ-1.1 |
| **`Modelfile` (Temperature=0.15, Min_P=0.03)** | Moteur LLM Local | Verrouillage du determinisme. Elimination des hallucinations lors de la generation de code. | DA-004 | REQ-1.3 |
| **`Modelfile` (num_ctx=131072)** | Moteur LLM Local | Fenetre de contexte 128K tokens. Chargement simultane du projet et de la Memory Bank. | DA-004 | REQ-1.2 |
| **Modele secondaire `qwen3:7b` + Boomerang** | Moteur LLM Local | Delegation des taches repetitives au modele leger. Recuperation de la sortie par l'agent principal. | DA-005 | REQ-1.4 |
| **`proxy.py` — Route POST `/v1/chat/completions`** | Proxy Hybride | Point d'entree unique. Intercepte les requetes HTTP POST de Roo Code au format OpenAI. | DA-006, DA-007 | REQ-2.1.1, REQ-2.1.2 |
| **`proxy.py` — Fonction `_format_prompt()`** | Proxy Hybride | Extraction et formatage du payload. Separe system prompt, historique et user prompt. | DA-008 | REQ-2.1.3, REQ-2.1.4 |
| **`proxy.py` — Fonction `_clean_content()`** | Proxy Hybride | Nettoyage des contenus base64. Remplace les images par un message d'avertissement textuel. | DA-009 | REQ-2.1.5 |
| **`proxy.py` — `pyperclip.copy()`** | Proxy Hybride | Injection du prompt formate dans le presse-papiers Windows. | — | REQ-2.2.1 |
| **`proxy.py` — Formatage avec separateurs** | Proxy Hybride | Structure lisible avec balises [SYSTEM PROMPT], [USER], [ASSISTANT] pour l'utilisateur humain. | DA-008 | REQ-2.2.2 |
| **`proxy.py` — Messages console horodates** | Proxy Hybride | Notification utilisateur avec timestamp, taille du prompt et instructions d'action claires. | — | REQ-2.2.3 |
| **`proxy.py` — Boucle `asyncio` + `pyperclip.paste()`** | Proxy Hybride | Polling asynchrone du presse-papiers toutes les secondes. Non-bloquant grace a asyncio. | DA-006 | REQ-2.3.1 |
| **`proxy.py` — Comparaison de hash MD5** | Proxy Hybride | Detection du changement de contenu du presse-papiers. Identifie le moment ou l'humain a copie la reponse Gemini. | — | REQ-2.3.2 |
| **`proxy.py` — Timeout 300s + HTTP 408** | Proxy Hybride | Gestion du cas de non-reponse. Retourne HTTP 408 avec message explicatif apres le delai configure. | — | REQ-2.3.3 |
| **`proxy.py` — Fonction `_validate_response()`** | Proxy Hybride | Verification de la presence de balises XML Roo Code dans la reponse Gemini. Avertissement console si absent. | — | REQ-2.3.4 |
| **`proxy.py` — Fonction `_build_openai_response()`** | Proxy Hybride | Construction du JSON de reponse au format OpenAI Chat Completions avec tous les champs requis. | DA-007 | REQ-2.4.1 |
| **`proxy.py` — `JSONResponse(status_code=200)`** | Proxy Hybride | Cloture propre de la requete HTTP avec code 200 OK et Content-Type application/json. | — | REQ-2.4.2 |
| **`proxy.py` — Transmission du contenu brut** | Proxy Hybride | Contenu de la reponse Gemini transmis tel quel dans choices[0].message.content sans modification. | — | REQ-2.4.3 |
| **Repertoire `memory-bank/`** | Memoire | Conteneur de toute la memoire contextuelle. Integre au depot Git pour versionnement. | DA-003 | REQ-4.1, REQ-4.5 |
| **`memory-bank/projectBrief.md`** | Memoire | Vision, objectifs, Non-Goals et contraintes du projet. Lu en debut de projet. | DA-003 | REQ-4.4 |
| **`memory-bank/productContext.md`** | Memoire | User Stories, valeur metier, personas utilisateurs. Lu en debut de sprint. | DA-003 | REQ-4.4 |
| **`memory-bank/systemPatterns.md`** | Memoire | Architecture des dossiers, conventions de nommage, patterns techniques. | DA-003 | REQ-4.4 |
| **`memory-bank/techContext.md`** | Memoire | Stack technique, versions, commandes de build/test, variables d'environnement. | DA-003 | REQ-4.4 |
| **`memory-bank/activeContext.md`** | Memoire | Memoire vive de la session. Tache en cours, dernier bug, prochaine action. Lu et ecrit a chaque session. | DA-002, DA-003 | REQ-4.2, REQ-4.3, REQ-4.4 |
| **`memory-bank/progress.md`** | Memoire | Checklist macro des Epics et features. Lu et mis a jour a chaque validation de feature. | DA-002, DA-003 | REQ-4.2, REQ-4.3, REQ-4.4 |
| **`memory-bank/decisionLog.md`** | Memoire | Registre des ADR horodates. Mis a jour apres chaque decision d'architecture. | DA-003 | REQ-4.4, REQ-4.5 |
| **Gem Gemini Chrome** | Gemini Config | Profil dedie dans Gemini Web contenant l'integralite du system prompt Roo Code. Evite la retransmission a chaque requete. | DA-010 | REQ-5.1, REQ-5.2 |
| **Instructions du Gem (balises XML)** | Gemini Config | Regles strictes imposant a Gemini de repondre uniquement avec les balises XML Roo Code, sans texte de courtoisie. | DA-010 | REQ-5.2 |
| **Historique de conversation dans le presse-papiers** | Gemini Config | Transmission de l'historique multi-tours pour maintenir la coherence des reponses Gemini. | DA-008 | REQ-5.3 |
| **Configuration Roo Code (Base URL)** | Commutateur LLM | Parametre permettant de basculer entre Ollama (port 11434), le proxy (port 8000) et l'API Anthropic sans modifier Roo Code. | DA-007, DA-011 | REQ-2.0 |
| **Variable `USE_GEM_MODE`** | Proxy Hybride | Commutateur de comportement du proxy. Active le filtrage du system prompt quand le Gem est configure. | DA-008 | REQ-2.1.4 |
| **Provider "Anthropic" dans Roo Code** | Cloud Direct | Fournisseur natif Roo Code pour l'API Anthropic. Connexion directe a api.anthropic.com sans proxy ni middleware. | DA-011 | REQ-6.3 |
| **Cle API Anthropic (VS Code SecretStorage)** | Cloud Direct | Authentification aupres de l'API Anthropic. Stockee dans le gestionnaire de secrets chiffre de VS Code, jamais dans les fichiers du projet. | DA-011 | REQ-6.1, REQ-6.4 |
| **Modele `claude-sonnet-4-5`** | Cloud Direct | Modele Claude Sonnet de haute qualite. Repond nativement aux balises XML Roo Code sans configuration supplementaire du format. | DA-011 | REQ-6.2 |
| **Tableau comparatif 3 modes (DOC1 section 5)** | Commutateur LLM | Reference documentaire permettant a l'utilisateur de choisir le mode LLM adapte a son contexte (cout, vitesse, souverainete). | DA-011 | REQ-6.0, REQ-2.0 |
| **Repertoire `prompts/`** | Registre Prompts | Dossier versionne contenant les 7 fichiers SP canoniques. Source de verite unique pour tous les system prompts du systeme. | DA-012 | REQ-7.1 |
| **Fichiers `prompts/SP-XXX-*.md`** | Registre Prompts | Fichiers canoniques avec en-tete YAML (id, version, target_file, target_field, depends_on, changelog). Un fichier par prompt. | DA-012 | REQ-7.1, REQ-7.2, REQ-7.4 |
| **`prompts/README.md`** | Registre Prompts | Index de tous les prompts avec tableau ID / fichier / cible / flag Hors Git. Point d'entree du registre. | DA-012 | REQ-7.2 |
| **REGLE 6 dans `.clinerules`** | Registre Prompts | Directive imperative imposant la verification de coherence du registre avant tout commit touchant proxy.py, .roomodes, .clinerules ou Modelfile. | DA-012 | REQ-7.3 |
| **Flag `hors_git: true` dans SP-007** | Registre Prompts | Marqueur identifiant le Gem Gemini comme le seul prompt a deploiement manuel. Declenche l'obligation de mention "DEPLOIEMENT MANUEL REQUIS" dans le commit. | DA-012 | REQ-7.5 |
| **`scripts/check-prompts-sync.ps1`** | Verification Prompts | Script PowerShell comparant le contenu deploye de chaque artefact (Modelfile, .clinerules, .roomodes) avec le SP canonique correspondant. Produit un rapport PASS/FAIL avec diff si desynchronisation. SP-007 exclu avec avertissement manuel. | DA-013 | REQ-8.1, REQ-8.3, REQ-8.4 |
| **`.git/hooks/pre-commit`** | Verification Prompts | Hook Git appelant automatiquement check-prompts-sync.ps1 avant chaque commit. Bloque le commit avec message explicatif si desynchronisation detectee entre un SP canonique et son artefact cible. | DA-013 | REQ-8.2 |