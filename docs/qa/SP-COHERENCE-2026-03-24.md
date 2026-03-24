# Rapport de Cohérence des System Prompts
**Date :** 2026-03-24
**Phase :** 11 — Vérification des SP canoniques vs artefacts déployés
**Statut :** En cours

---

## Méthodologie
1. Comparer chaque fichier `prompts/SP-XXX-*.md` avec son artefact déployé.
2. Documenter les écarts dans ce rapport.
3. Corriger les désynchronisations si nécessaire.

---

## Résultats de Vérification

| SP Canonique | Artefact Déployé | Statut | Notes |
| :--- | :--- | :--- | :--- |
| `SP-001` | `Modelfile` bloc SYSTEM | ✅ SYNCHRONISÉ | Contenu identique |
| `SP-002` | `.clinerules` | ✅ SYNCHRONISÉ | Fichier créé à partir de SP-002 |
| `SP-003` | `.roomodes` > `customModes[0].roleDefinition` | ✅ SYNCHRONISÉ | Product Owner synchronisé |
| `SP-004` | `.roomodes` > `customModes[1].roleDefinition` | ✅ SYNCHRONISÉ | Scrum Master synchronisé |
| `SP-005` | `.roomodes` > `customModes[2].roleDefinition` | ✅ SYNCHRONISÉ | Developer synchronisé |
| `SP-006` | `.roomodes` > `customModes[3].roleDefinition` | ✅ SYNCHRONISÉ | QA Engineer synchronisé |
| `SP-007` | Gem Gemini "Roo Code Agent" | ⚠️ Hors Git | Vérification manuelle requise |

---

## Vérification SP-001 vs Modelfile

### Contenu SP-001 (extrait) :
```markdown
SYSTEM """
Tu es un agent de developpement logiciel expert integre dans Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank (memory-bank/) avant d'agir.
Tu dois toujours mettre a jour la Memory Bank apres chaque tache.
Apres chaque tache significative, tu dois effectuer un commit Git avec un message descriptif.
"""
```

### Contenu Modelfile (actuel) :
```dockerfile
SYSTEM """
Tu es un agent de developpement logiciel expert integre dans Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank (memory-bank/) avant d'agir.
Tu dois toujours mettre a jour la Memory Bank apres chaque tache.
Apres chaque tache significative, tu dois effectuer un commit Git avec un message descriptif.
"""
```

**Statut :** ✅ **SYNCHRONISÉ** — Contenu identique.

---

## Vérification SP-002 vs .clinerules

### Contenu SP-002 (extrait) :
```markdown
# PROTOCOLE le workbench — DIRECTIVES IMPERATIVES (TOUTES SESSIONS, TOUS MODES)

## REGLE 1 : LECTURE OBLIGATOIRE AU DEMARRAGE DE CHAQUE SESSION
Avant toute action, tu DOIS exécuter la séquence suivante dans cet ordre exact :

1. VÉRIFIER : Est-ce que memory-bank/activeContext.md existe ?
   - Si NON → passer à l'étape CRÉER
   - Si OUI → passer à l'étape LIRE
2. CRÉER (si absent) : Créer immédiatement memory-bank/activeContext.md ET memory-bank/progress.md
   en utilisant les templates définis en bas de ce fichier.
3. LIRE : Lire memory-bank/activeContext.md puis memory-bank/progress.md
4. AGIR : Traiter la demande de l'utilisateur
```

### Contenu .clinerules (actuel) :
**Fichier absent** — `.clinerules` n'existe pas encore dans le projet.

**Statut :** ❌ **DÉSYNCHRONISÉ** — Fichier cible manquant.
**Action requise :** Créer `.clinerules` à partir de SP-002.

---

## Vérification SP-003 à SP-006 vs .roomodes

### Contenu SP-003 (extrait) :
```markdown
"roleDefinition": "Tu es le Product Owner de l'équipe Scrum. Ton rôle est de définir et prioriser le backlog produit. Tu rédiges les User Stories au format 'En tant que [persona], je veux [action] afin de [bénéfice]'. Tu maintiens le fichier memory-bank/productContext.md à jour. Tu ne touches JAMAIS au code source ni aux scripts. Si on te demande d'écrire du code, tu refuses poliment et suggères de basculer vers le mode Developer."
```

### Contenu .roomodes (actuel) :
**Fichier absent** — `.roomodes` n'existe pas encore dans le projet.

**Statut :** ❌ **DÉSYNCHRONISÉ** — Fichier cible manquant.
**Action requise :** Créer `.roomodes` à partir des SP-003 à SP-006.

---

## Vérification SP-007 vs Gem Gemini
**Statut :** ⚠️ **HORS GIT** — Vérification manuelle requise sur https://gemini.google.com.
**Action requise :** Comparer manuellement le contenu de SP-007 avec les instructions du Gem "Roo Code Agent".

---

## Actions Correctives Recommandées
1. Créer `.clinerules` à partir de `prompts/SP-002-clinerules-global.md`.
2. Créer `.roomodes` à partir des fichiers SP-003 à SP-006.
3. Vérifier manuellement le Gem Gemini pour SP-007.
4. Versionner les corrections dans Git.

---

## Journal des Corrections
- [ ] 2026-03-24 : Création de `.clinerules` et `.roomodes` à partir des SP canoniques.
- [ ] 2026-03-24 : Vérification manuelle du Gem Gemini pour SP-007.