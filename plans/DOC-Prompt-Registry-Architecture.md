# Registre Central des System Prompts — Architecture UADF
## Prompt Registry Design Document

**Nom du Projet :** Unified Agentic Development Framework (UADF)
**Version :** 1.0
**Date :** 2026-03-23
**Exigence source :** REQ-7.x (voir DOC1)

---

## 1. Probleme Adresse

Dans le systeme UADF, les system prompts sont disperses dans plusieurs endroits :
- Certains sont dans des fichiers de configuration JSON (`.roomodes`)
- Certains sont dans des fichiers de regles texte (`.clinerules`)
- Certains sont dans des fichiers de compilation binaire (Ollama `Modelfile`)
- Certains sont **hors du depot Git** (Gem Gemini Chrome, interface web)

Cette dispersion cree un risque de **desynchronisation** : si le code Python (`proxy.py`) change son comportement, le Gem Gemini doit etre mis a jour manuellement — mais rien ne rappelle a l'utilisateur de le faire, et rien ne documente quelle version du prompt est actuellement deployee.

---

## 2. Solution : Le Registre Central `prompts/`

### 2.1 Principe

Un dossier `prompts/` a la racine du projet contient **un fichier Markdown par system prompt**. Chaque fichier est :
- **Canonique** : c'est la source de verite. Toute modification doit partir de ce fichier.
- **Identifie** : un en-tete YAML de metadonnees precise l'ID, la cible de deploiement, et la version.
- **Versionne** : inclus dans Git comme tout autre artefact du projet.
- **Actionnable** : l'en-tete indique exactement comment deployer le prompt (copier dans quel fichier, quelle interface, quel champ).

### 2.2 Structure du Dossier `prompts/`

```
prompts/
|
+-- README.md                          Index du registre (ce document en resume)
|
+-- SP-001-ollama-modelfile-system.md  System prompt du Modelfile Ollama
+-- SP-002-clinerules-global.md        Directives globales .clinerules (toutes sessions)
+-- SP-003-persona-product-owner.md    roleDefinition du Product Owner (.roomodes)
+-- SP-004-persona-scrum-master.md     roleDefinition du Scrum Master (.roomodes)
+-- SP-005-persona-developer.md        roleDefinition du Developer (.roomodes)
+-- SP-006-persona-qa-engineer.md      roleDefinition du QA Engineer (.roomodes)
+-- SP-007-gem-gemini-roo-agent.md     Instructions du Gem Gemini Chrome "Roo Code Agent"
```

### 2.3 Format Standard d'un Fichier de Prompt

Chaque fichier suit ce format :

```markdown
---
id: SP-XXX
name: [Nom descriptif du prompt]
version: 1.0.0
last_updated: YYYY-MM-DD
status: active | draft | deprecated

# Cible de deploiement (ou ce prompt doit etre place)
target_type: ollama_modelfile | roo_clinerules | roo_roomodes | gemini_gem | anthropic_system
target_file: [chemin relatif du fichier dans le depot, ou "EXTERNE" si hors depot]
target_field: [champ specifique dans le fichier cible, ex: "SYSTEM block", "roleDefinition", "Instructions"]
target_location: [description precise pour l'humain]

# Dependances (autres prompts ou fichiers qui doivent etre coherents avec celui-ci)
depends_on:
  - SP-XXX: [raison de la dependance]

# Historique des modifications
changelog:
  - version: 1.0.0
    date: YYYY-MM-DD
    change: Creation initiale
---

# [Nom du Prompt]

## Contenu du Prompt

[Le texte exact du system prompt, pret a etre copie-colle]

## Notes de Deploiement

[Instructions specifiques pour deployer ce prompt dans sa cible]

## Impact sur les Autres Prompts

[Si ce prompt est modifie, quels autres prompts doivent etre verifies/mis a jour]
```

---

## 3. Inventaire Complet des System Prompts UADF

| ID | Nom | Cible | Fichier Cible | Champ | Hors Git |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **SP-001** | Ollama Modelfile System | Ollama daemon | `Modelfile` | Bloc `SYSTEM` | Non |
| **SP-002** | Directives Globales Roo Code | Roo Code (toutes sessions) | `.clinerules` | Fichier entier | Non |
| **SP-003** | Persona Product Owner | Roo Code mode PO | `.roomodes` | `customModes[0].roleDefinition` | Non |
| **SP-004** | Persona Scrum Master | Roo Code mode SM | `.roomodes` | `customModes[1].roleDefinition` | Non |
| **SP-005** | Persona Developer | Roo Code mode Dev | `.roomodes` | `customModes[2].roleDefinition` | Non |
| **SP-006** | Persona QA Engineer | Roo Code mode QA | `.roomodes` | `customModes[3].roleDefinition` | Non |
| **SP-007** | Gem Gemini Roo Code Agent | Gemini Chrome (web) | EXTERNE | Champ "Instructions" du Gem | **OUI** |

---

## 4. Workflow de Maintenance des Prompts

### 4.1 Modifier un Prompt (Procedure Standard)

```
1. Modifier le fichier canonique dans prompts/SP-XXX-*.md
2. Incrementer la version dans les metadonnees YAML
3. Ajouter une entree dans le changelog
4. Verifier les dependances (champ depends_on) et mettre a jour les prompts lies si necessaire
5. Propager la modification vers la cible de deploiement :
   - Si target_file est dans le depot : copier le contenu dans le fichier cible
   - Si target_type = gemini_gem : copier manuellement dans l'interface Gemini Web
6. Commiter TOUS les fichiers modifies en une seule transaction Git :
   git add prompts/SP-XXX-*.md [fichier_cible_si_dans_depot]
   git commit -m "chore(prompts): mise a jour SP-XXX - [description du changement]"
```

### 4.2 Cas Particulier : Modification de `proxy.py` avec Impact sur SP-007

Si `proxy.py` change le format du prompt envoye a Gemini (ex: nouveau separateur, nouveau contexte) :
1. Modifier `prompts/SP-007-gem-gemini-roo-agent.md`
2. Aller sur https://gemini.google.com > Gems > "Roo Code Agent" > Modifier les instructions
3. Copier-coller le nouveau contenu depuis `SP-007`
4. Commiter `SP-007` avec la note : `DEPLOIEMENT MANUEL REQUIS : Gem Gemini mis a jour le [DATE]`

### 4.3 Verification de Coherence (REGLE 6 dans `.clinerules`)

La REGLE 6 dans `.clinerules` impose a l'agent de verifier la coherence des prompts avant tout commit touchant `proxy.py`, `.roomodes`, `.clinerules` ou `Modelfile`.

---

## 5. Dependances entre Prompts

```
SP-002 (.clinerules)
    |
    +-- depend de SP-005 (Developer) : les regles Git de SP-002 supposent
    |   que le Developer sait commiter (coherence avec roleDefinition)
    |
    +-- depend de SP-007 (Gem Gemini) : le format du prompt copie dans
        le presse-papiers par proxy.py doit correspondre a ce que SP-007
        attend comme input

SP-007 (Gem Gemini)
    |
    +-- depend de proxy.py : le format [USER] / [ASSISTANT] / [SYSTEM PROMPT]
    |   genere par proxy.py doit etre coherent avec les instructions du Gem
    |
    +-- depend de SP-002 : les balises XML attendues par Roo Code (listees
        dans SP-002) doivent etre les memes que celles listees dans SP-007

SP-001 (Modelfile)
    |
    +-- independant des autres SP (niveau bas, generique)
    +-- doit etre recompile avec 'ollama create uadf-agent -f Modelfile'
        apres toute modification
```

---

## 6. Diagramme de Flux de Maintenance

```
Modification detectee
(code, process, HITL)
        |
        v
+-------+--------+
| Quel artefact  |
| est impacte ?  |
+-------+--------+
        |
   +----+----+----+----+
   |         |         |
   v         v         v
proxy.py  .roomodes  .clinerules
   |         |         |
   v         v         v
SP-007    SP-003 a   SP-002
(Gem)     SP-006     (Global)
   |      (Personas)    |
   |         |          |
   v         v          v
Modifier  Modifier   Modifier
SP-XXX    SP-XXX     SP-XXX
canonique canonique  canonique
   |         |          |
   v         v          v
Propager  Propager   Propager
vers      vers       vers
Gemini    .roomodes  .clinerules
(MANUEL)  (fichier)  (fichier)
   |         |          |
   +----+----+----------+
        |
        v
git add prompts/ + fichiers cibles
git commit -m "chore(prompts): ..."
```
