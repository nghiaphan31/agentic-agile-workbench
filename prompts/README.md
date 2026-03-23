# Registre Central des System Prompts — UADF
## Source de Verite Unique pour Tous les Prompts du Systeme

**Projet :** Unified Agentic Development Framework (UADF)
**Maintenu par :** Developer / Scrum Master (via REGLE 6 de `.clinerules`)
**Derniere mise a jour :** 2026-03-23

---

## Principe Fondamental

Ce dossier `prompts/` est la **source de verite unique** pour tous les system prompts du systeme UADF.

**Toute modification d'un prompt doit :**
1. Partir de ce dossier (modifier le fichier SP-XXX canonique)
2. Etre propagee vers sa cible de deploiement (fichier de config ou interface web)
3. Etre commitee dans Git avec un message `chore(prompts): ...`

**Ne jamais modifier directement** `.roomodes`, `.clinerules`, le `Modelfile` ou le Gem Gemini sans mettre a jour le fichier canonique correspondant dans ce dossier.

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
| **SP-007** | `SP-007-gem-gemini-roo-agent.md` | Gem Gemini Chrome "Roo Code Agent" | gemini.google.com > Gems > "Roo Code Agent" > Instructions | **OUI** |

---

## Procedure de Modification d'un Prompt

```
1. Ouvrir le fichier SP-XXX-*.md correspondant dans ce dossier
2. Modifier le contenu du prompt
3. Incrementer la version (ex: 1.0.0 -> 1.1.0)
4. Ajouter une entree dans le changelog du fichier
5. Verifier les dependances (champ depends_on) et mettre a jour les prompts lies
6. Propager vers la cible :
   - Fichier dans le depot : copier le contenu dans le fichier cible
   - Gem Gemini (SP-007) : copier manuellement dans l'interface web Gemini
7. Commiter TOUS les fichiers modifies :
   git add prompts/ .clinerules .roomodes Modelfile  (selon ce qui a change)
   git commit -m "chore(prompts): mise a jour SP-XXX - [description]"
```

---

## Dependances Critiques

- **SP-007 depend de `proxy.py`** : si le format du prompt change dans proxy.py, SP-007 doit etre mis a jour ET re-deploye manuellement dans Gemini
- **SP-002 depend de SP-005** : les regles Git de .clinerules supposent que le Developer connait le protocole de commit
- **SP-007 depend de SP-002** : les balises XML listees dans le Gem doivent etre identiques a celles attendues par Roo Code
- **SP-001 necessite recompilation** : apres modification, executer `ollama create uadf-agent -f Modelfile`
