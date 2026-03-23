# Document 5 : Manuel du Processus Agile Applicatif
## Comment dÃ©velopper un projet applicatif avec l'Agentic Agile Workbench

**Nom du Projet :** Agentic Agile Workbench
**Version :** 1.0
**Date :** 2026-03-23
**References :** DOC1-PRD v2.0, DOC2-Architecture v2.0, DOC3-Plan v3.0, DOC4-Guide-Deploiement v1.0

---

## Preambule : Pourquoi ce Document ?

Les documents DOC1 a DOC4 decrivent **l'atelier lui-meme** : ses exigences, son architecture, son installation, son deploiement. Ils ne decrivent pas **comment travailler avec l'atelier** pour produire un logiciel applicatif ou metier.

Ce document repond a la question : **"J'ai l'atelier operationnel. Comment je developpe mon projet ?"**

Il couvre :
1. Le **processus Agile** adapte au developpement agentique
2. La **nomenclature et les templates** de tous les artifacts d'un projet applicatif
3. Les **mecanismes anti-risques** specifiques au developpement agentique (perte de memoire, hallucination, multi-sessions sur plusieurs mois)
4. La **phase amont ouverte** : comment transformer des idees narratives non-structurees en artifacts structures
5. La **tracabilite et le versionnement** de tout le processus

---

## Table des Matieres

1. Vue d'Ensemble du Processus
2. Phase 0 - Amont Ouvert : De l'Idee aux Artifacts
3. Phase 1 - Cadrage : Initialisation du Projet
4. Phase 2 - Sprints de Developpement
5. Phase 3 - Livraison et Maintenance
6. Nomenclature des Artifacts
7. Templates des Artifacts
8. Mecanismes Anti-Risques Agentiques
9. Protocoles de Session
10. Tableau de Bord du Projet

---

## 1. Vue d'Ensemble du Processus

### 1.1 Principes Fondamentaux

Le processus repose sur **quatre principes non-negociables** :

| Principe | Description | Mecanisme de l'Atelier |
| :--- | :--- | :--- |
| **Memoire Persistante** | Tout contexte est ecrit, jamais suppose memorise | Memory Bank (7 fichiers `.md`) |
| **Tracabilite Totale** | Tout artifact est versionne avec son historique | Git + Conventional Commits |
| **Convergence Progressive** | Les entrees narratives maturent vers des artifacts structures | Phase 0 -> Phase 1 -> Phase 2 |
| **Defense en Profondeur** | Chaque regle est redondante (`.clinerules` + `roleDefinition` + protocoles) | `.clinerules` + `.roomodes` |

### 1.2 Carte du Processus

```
+-------------------------------------------------------------------------+
|                    PHASE 0 - AMONT OUVERT                               |
|                                                                          |
|  Entrees narratives, non-structurees, desordonnees                      |
|  (emails, notes, conversations, code existant, idees vagues)            |
|                                                                          |
|  -> Artifact : BRIEF-001 (Vision Narrative Brute)                       |
|  -> Artifact : BRIEF-002 (Synthese Structuree)                          |
|  -> Artifact : BRIEF-003 (Decision de Lancement)                        |
+----------------------------------+--------------------------------------+
                                   | Convergence
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 1 - CADRAGE                                     |
|                                                                          |
|  Initialisation du projet, Memory Bank, backlog initial                 |
|                                                                          |
|  -> Artifact : PRJ-001 (Project Brief)                                  |
|  -> Artifact : PRJ-002 (Architecture Initiale)                          |
|  -> Artifact : PRJ-003 (Backlog Initial)                                |
|  -> Artifact : PRJ-004 (Tech Context)                                   |
+----------------------------------+--------------------------------------+
                                   | Iteration
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 2 - SPRINTS (repetee N fois)                   |
|                                                                          |
|  Sprint Planning -> Developpement -> Tests -> Review -> Retrospective   |
|                                                                          |
|  -> Artifact : SPR-XXX-001 (Sprint Backlog)                             |
|  -> Artifact : SPR-XXX-002 (User Stories)                               |
|  -> Artifact : SPR-XXX-003 (Code Source)                                |
|  -> Artifact : SPR-XXX-004 (Rapport de Tests)                           |
|  -> Artifact : SPR-XXX-005 (Sprint Review)                              |
|  -> Artifact : SPR-XXX-006 (Retrospective)                              |
+----------------------------------+--------------------------------------+
                                   | Livraison
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 3 - LIVRAISON & MAINTENANCE                    |
|                                                                          |
|  -> Artifact : REL-XXX-001 (Release Notes)                              |
|  -> Artifact : REL-XXX-002 (Documentation Utilisateur)                  |
|  -> Artifact : REL-XXX-003 (Runbook de Deploiement)                     |
+-------------------------------------------------------------------------+
```

### 1.3 Roles et Responsabilites par Phase

| Phase | Persona Principal | Personas Secondaires | Livrables |
| :--- | :--- | :--- | :--- |
| Phase 0 - Amont | Product Owner | Developer | BRIEF-001, BRIEF-002, BRIEF-003 |
| Phase 1 - Cadrage | Product Owner | Developer, Scrum Master | PRJ-001 a PRJ-004 |
| Phase 2 - Sprint Planning | Product Owner | Scrum Master | SPR-XXX-001, SPR-XXX-002 |
| Phase 2 - Developpement | Developer | â€” | SPR-XXX-003 |
| Phase 2 - Tests | QA Engineer | Developer | SPR-XXX-004 |
| Phase 2 - Review | Product Owner | Scrum Master | SPR-XXX-005 |
| Phase 2 - Retrospective | Scrum Master | Tous | SPR-XXX-006 |
| Phase 3 - Livraison | Developer | QA Engineer | REL-XXX-001 a REL-XXX-003 |

---

## 2. Phase 0 - Amont Ouvert : De l'Idee aux Artifacts

### 2.1 Pourquoi une Phase Amont Ouverte ?

Le developpement logiciel commence rarement par un cahier des charges structure. Il commence par :
- Un email de 3 lignes : "Il faudrait un outil pour gerer nos commandes clients"
- Une conversation : "Le probleme c'est que les commerciaux saisissent les donnees deux fois"
- Un code existant sans documentation : "Voila ce qu'on a, il faut le refaire proprement"
- Des notes desordonnees sur plusieurs documents
- Une idee vague qui evolue au fil des discussions

**L'atelier doit accepter ces entrees telles quelles** et les transformer progressivement en artifacts structures. C'est le role de la Phase 0.

> **Regle d'or de la Phase 0 :** Ne jamais forcer une structure prematuree. Laisser la comprehension murir avant de structurer.

### 2.2 Entrees Acceptees en Phase 0

| Type d'Entree | Exemple | Traitement |
| :--- | :--- | :--- |
| **Texte narratif libre** | Email, note, compte-rendu de reunion | Copier tel quel dans BRIEF-001 |
| **Code existant** | Depot legacy, scripts, prototypes | Audit Developer -> BRIEF-002 |
| **Conversation orale** | Retranscription, notes de reunion | Copier tel quel dans BRIEF-001 |
| **Document Word/PDF** | Cahier des charges partiel, spec fonctionnelle | Extraire le texte -> BRIEF-001 |
| **Maquettes/Wireframes** | Images, captures d'ecran | Decrire en texte -> BRIEF-001 |
| **Idee vague** | "Je veux quelque chose comme Trello mais pour..." | Dialogue Product Owner -> BRIEF-001 |

### 2.3 Processus de Maturation Phase 0

```
ETAPE 0.1 - COLLECTE (Mode Product Owner)

  Instruction a Roo Code :
  "Je vais te donner des informations brutes sur mon projet.
   Cree le fichier docs/brief/BRIEF-001-vision-narrative.md
   et copie-y exactement ce que je te donne, sans reformuler.
   [Coller ici toutes les entrees brutes]"

  -> Artifact cree : BRIEF-001-vision-narrative.md

ETAPE 0.2 - ANALYSE (Mode Developer)

  Instruction a Roo Code :
  "Lis docs/brief/BRIEF-001-vision-narrative.md.
   Identifie et liste dans docs/brief/BRIEF-002-synthese-structuree.md :
   - Les fonctionnalites mentionnees (meme implicitement)
   - Les utilisateurs cibles identifiables
   - Les contraintes techniques ou metier
   - Les ambiguites et questions ouvertes
   - Ce qui est hors perimetre apparent
   Ne prends aucune decision. Documente seulement ce que tu comprends."

  -> Artifact cree : BRIEF-002-synthese-structuree.md

ETAPE 0.3 - CLARIFICATION (Mode Product Owner)

  Instruction a Roo Code :
  "Lis docs/brief/BRIEF-002-synthese-structuree.md.
   Pour chaque ambiguite listee, pose-moi une question precise.
   Attends ma reponse avant de passer a la suivante."

  -> Dialogue iteratif jusqu'a resolution des ambiguites
  -> BRIEF-002 mis a jour avec les reponses

ETAPE 0.4 - DECISION DE LANCEMENT (Mode Product Owner)

  Instruction a Roo Code :
  "Sur la base de BRIEF-001 et BRIEF-002, cree
   docs/brief/BRIEF-003-decision-lancement.md avec :
   - La decision GO / NO-GO / ATTENTE
   - Les conditions de lancement si ATTENTE
   - La date de decision
   - Les risques identifies
   Commite les 3 fichiers BRIEF avec le message :
   'docs(brief): phase amont complete - decision [GO/NO-GO]'"

  -> Artifact cree : BRIEF-003-decision-lancement.md
  -> Commit Git des 3 artifacts BRIEF
```

### 2.4 Critere de Sortie de Phase 0

La Phase 0 est terminee quand :
- [ ] BRIEF-001 existe et contient toutes les entrees brutes
- [ ] BRIEF-002 existe et liste fonctionnalites, utilisateurs, contraintes, ambiguites
- [ ] Toutes les ambiguites critiques sont resolues (ou documentees comme acceptees)
- [ ] BRIEF-003 contient une decision GO
- [ ] Les 3 fichiers sont commites dans Git

> **Si la decision est NO-GO ou ATTENTE :** Archiver les fichiers BRIEF dans `docs/brief/archive/` et commiter. Le projet peut reprendre plus tard en repartant de ces artifacts.

---

## 3. Phase 1 - Cadrage : Initialisation du Projet

### 3.1 Objectif

Transformer la decision GO de la Phase 0 en une base de projet structuree et operationnelle : Memory Bank remplie, architecture initiale definie, backlog initial cree.

### 3.2 Sequence de Cadrage

#### Etape 1.1 - Initialisation de la Memory Bank (Mode Product Owner)

```
Instruction a Roo Code :
"Lis docs/brief/BRIEF-002-synthese-structuree.md et
 docs/brief/BRIEF-003-decision-lancement.md.

 Remplis les fichiers Memory Bank suivants :

 1. memory-bank/projectBrief.md :
    - Vision du projet (2-3 phrases synthetiques)
    - Objectifs principaux (mesurables)
    - Non-Goals explicites
    - Contraintes identifiees
    - Parties prenantes

 2. memory-bank/productContext.md :
    - Personas utilisateurs identifies
    - Premieres User Stories (format standard)
    - Backlog initial priorise

 Commite avec : 'feat(memory): initialisation Memory Bank depuis phase amont'"
```

#### Etape 1.2 - Architecture Initiale (Mode Developer)

```
Instruction a Roo Code :
"Lis memory-bank/projectBrief.md et memory-bank/productContext.md.

 Propose une architecture initiale dans docs/architecture/PRJ-002-architecture-initiale.md :
 - Stack technique recommandee (avec justification)
 - Structure des dossiers du projet
 - Patterns architecturaux retenus
 - Decisions d'architecture (ADR format)
 - Dependances externes identifiees

 Mets a jour memory-bank/systemPatterns.md et memory-bank/techContext.md.
 Mets a jour memory-bank/decisionLog.md avec les ADR.
 Commite avec : 'feat(architecture): architecture initiale + Memory Bank mise a jour'"
```

#### Etape 1.3 - Validation de l'Architecture (Mode Product Owner)

```
Instruction a Roo Code :
"Lis docs/architecture/PRJ-002-architecture-initiale.md.
 Verifie que l'architecture proposee est coherente avec :
 - La vision dans memory-bank/projectBrief.md
 - Les contraintes identifiees
 - Les Non-Goals

 Si des incoherences existent, liste-les.
 Si l'architecture est validee, mets a jour BRIEF-003 avec la mention
 'Architecture validee le [DATE]' et commite."
```

#### Etape 1.4 - Backlog Initial Structure (Mode Product Owner)

```
Instruction a Roo Code :
"Sur la base de memory-bank/productContext.md et de l'architecture validee,
 cree docs/backlog/PRJ-003-backlog-initial.md avec :

 - Les Epics identifiees (regroupements fonctionnels)
 - Les User Stories de chaque Epic (format standard)
 - La priorisation MoSCoW (Must/Should/Could/Won't)
 - Les dependances entre User Stories
 - L'estimation de complexite (T-shirt sizing : XS/S/M/L/XL)

 Mets a jour memory-bank/productContext.md avec le backlog structure.
 Commite avec : 'feat(backlog): backlog initial structure avec priorisation MoSCoW'"
```

### 3.3 Critere de Sortie de Phase 1

- [ ] `memory-bank/projectBrief.md` rempli et valide
- [ ] `memory-bank/productContext.md` contient le backlog initial
- [ ] `memory-bank/systemPatterns.md` contient l'architecture initiale
- [ ] `memory-bank/techContext.md` contient la stack et les commandes
- [ ] `docs/architecture/PRJ-002-architecture-initiale.md` existe
- [ ] `docs/backlog/PRJ-003-backlog-initial.md` existe avec priorisation MoSCoW
- [ ] Tous les fichiers commites dans Git

---

## 4. Phase 2 - Sprints de Developpement

### 4.1 Structure d'un Sprint

Un sprint dure **1 a 2 semaines**. Il suit le cycle Scrum standard adapte au developpement agentique :

```
SPRINT PLANNING (Debut de sprint)
  Duree : 1-2 heures
  Personas : Product Owner + Scrum Master
  Artifact : SPR-XXX-001 (Sprint Backlog)

DEVELOPPEMENT (Corps du sprint)
  Duree : 80% du sprint
  Persona : Developer
  Artifact : SPR-XXX-003 (Code Source + commits)
  Regle : 1 User Story = N commits = 1 livraison

TESTS (Fin de developpement)
  Duree : 15% du sprint
  Persona : QA Engineer
  Artifact : SPR-XXX-004 (Rapport de Tests)

SPRINT REVIEW (Fin de sprint)
  Duree : 1 heure
  Personas : Product Owner + Scrum Master
  Artifact : SPR-XXX-005 (Sprint Review)

RETROSPECTIVE (Apres la review)
  Duree : 30 minutes
  Persona : Scrum Master
  Artifact : SPR-XXX-006 (Retrospective)

MISE A JOUR MEMORY BANK (Obligatoire avant cloture)
  Persona : Scrum Master
  Fichiers : activeContext.md, progress.md
  Commit : 'docs(memory): cloture sprint XXX'
```

### 4.2 Sprint Planning (Mode Product Owner + Scrum Master)

```
Instruction Product Owner :
"Lis memory-bank/productContext.md et memory-bank/progress.md.

 Cree docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md avec :
 - L'objectif du sprint (Sprint Goal - 1 phrase)
 - Les User Stories selectionnees du backlog (avec leur ID)
 - La capacite estimee (en points ou en jours)
 - Les criteres d'acceptation de chaque US
 - Les dependances techniques identifiees

 Mets a jour memory-bank/activeContext.md avec le Sprint Goal.
 Commite avec : 'feat(sprint-[NNN]): sprint planning - [Sprint Goal]'"
```

### 4.3 Developpement d'une User Story (Mode Developer)

**Protocole obligatoire en 5 etapes :**

```
ETAPE D.1 - LECTURE MEMORY BANK (obligatoire)
  Lire : activeContext.md, systemPatterns.md, techContext.md

ETAPE D.2 - COMPREHENSION DE LA USER STORY
  Lire : docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md
  Identifier : criteres d'acceptation, dependances

ETAPE D.3 - IMPLEMENTATION
  Coder la User Story
  Commiter apres chaque sous-tache significative
  Format commit : 'feat(US-XXX): [description]'

ETAPE D.4 - MISE A JOUR MEMORY BANK
  Mettre a jour : activeContext.md (etat courant)
  Si decision d'architecture : mettre a jour decisionLog.md

ETAPE D.5 - COMMIT FINAL
  git add .
  git commit -m 'feat(US-XXX): implementation complete - [description]'
```

**Instruction type pour le Developer :**

```
"Lis memory-bank/activeContext.md, memory-bank/systemPatterns.md
 et memory-bank/techContext.md.

 Implemente la User Story US-[XXX] definie dans
 docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md.

 Respecte les conventions de memory-bank/systemPatterns.md.
 Commite apres chaque sous-tache avec le format 'feat(US-XXX): [description]'.
 Mets a jour memory-bank/activeContext.md apres chaque sous-tache.
 Avant de cloturer, commite memory-bank/ avec 'docs(memory): US-XXX implementee'."
```

### 4.4 Tests (Mode QA Engineer)

```
Instruction QA Engineer :
"Lis docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md
 pour connaitre les criteres d'acceptation de chaque US.

 Pour chaque User Story du sprint :
 1. Execute les tests automatises existants
 2. Verifie chaque critere d'acceptation
 3. Documente les resultats dans
    docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md

 Commite avec : 'test(sprint-[NNN]): rapport de tests - [NNN] US testees'"
```

### 4.5 Sprint Review (Mode Product Owner)

```
Instruction Product Owner :
"Lis docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md.

 Cree docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md avec :
 - Les US livrees (validees par les tests)
 - Les US non livrees (avec raison)
 - La velocite du sprint (points livres / points planifies)
 - Les feedbacks sur les fonctionnalites livrees
 - Les ajustements du backlog (nouvelles US, repriorisation)

 Mets a jour memory-bank/productContext.md avec les ajustements backlog.
 Commite avec : 'docs(sprint-[NNN]): sprint review - velocite [X]%'"
```

### 4.6 Retrospective (Mode Scrum Master)

```
Instruction Scrum Master :
"Lis docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md
 et memory-bank/activeContext.md.

 Cree docs/sprints/sprint-[NNN]/SPR-[NNN]-006-retrospective.md avec :
 - Ce qui a bien fonctionne (Keep)
 - Ce qui doit etre ameliore (Improve)
 - Ce qui doit etre arrete (Stop)
 - Les actions concretes pour le prochain sprint
 - Les impediments identifies et leur resolution

 Mets a jour memory-bank/progress.md (cocher les US terminees).
 Mets a jour memory-bank/activeContext.md (etat fin de sprint).
 Commite avec : 'docs(memory): cloture sprint [NNN] - [X] US livrees'"
```

---

## 5. Phase 3 - Livraison et Maintenance

### 5.1 Preparation d'une Release

```
Instruction Developer :
"Lis memory-bank/progress.md pour identifier les features livrees
 depuis la derniere release.

 Cree docs/releases/REL-[VERSION]-001-release-notes.md avec :
 - La version (format SemVer : MAJOR.MINOR.PATCH)
 - La date de release
 - Les nouvelles fonctionnalites (avec reference aux US)
 - Les corrections de bugs
 - Les changements breaking (si MAJOR)
 - Les instructions de migration (si applicable)

 Commite avec : 'docs(release): release notes v[VERSION]'"
```

### 5.2 Documentation Utilisateur

```
Instruction Developer :
"Sur la base des features livrees dans REL-[VERSION]-001-release-notes.md,
 cree ou mets a jour docs/releases/REL-[VERSION]-002-documentation-utilisateur.md.

 La documentation doit couvrir :
 - Guide de demarrage rapide
 - Description de chaque fonctionnalite
 - Exemples d'utilisation
 - FAQ

 Commite avec : 'docs(release): documentation utilisateur v[VERSION]'"
```

### 5.3 Runbook de Deploiement

```
Instruction Developer :
"Cree docs/releases/REL-[VERSION]-003-runbook-deploiement.md avec :
 - Les prerequis systeme
 - Les etapes de deploiement (numerotees, precises)
 - Les variables d'environnement requises
 - Les commandes de verification post-deploiement
 - La procedure de rollback

 Commite avec : 'docs(release): runbook deploiement v[VERSION]'"
```

---

## 6. Nomenclature des Artifacts

### 6.1 Convention de Nommage

**Format general :** `[CATEGORIE]-[NUMERO]-[DESCRIPTION-COURTE].[ext]`

**Categories :**

| Prefixe | Categorie | Phase | Emplacement |
| :--- | :--- | :--- | :--- |
| `BRIEF` | Artifacts de phase amont | Phase 0 | `docs/brief/` |
| `PRJ` | Artifacts de cadrage projet | Phase 1 | `docs/architecture/`, `docs/backlog/` |
| `SPR` | Artifacts de sprint | Phase 2 | `docs/sprints/sprint-[NNN]/` |
| `QA` | Rapports de tests | Phase 2 | `docs/sprints/sprint-[NNN]/` ou `docs/qa/` |
| `REL` | Artifacts de release | Phase 3 | `docs/releases/` |
| `ADR` | Architecture Decision Records | Toutes | `memory-bank/decisionLog.md` |
| `US` | User Stories | Phase 1-2 | `memory-bank/productContext.md` |

### 6.2 Nomenclature Complete des Artifacts

#### Artifacts Phase 0 - Amont

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `BRIEF-001` | `BRIEF-001-vision-narrative.md` | Entrees brutes non-structurees | Product Owner |
| `BRIEF-002` | `BRIEF-002-synthese-structuree.md` | Analyse structuree des entrees | Developer |
| `BRIEF-003` | `BRIEF-003-decision-lancement.md` | Decision GO/NO-GO avec conditions | Product Owner |

#### Artifacts Phase 1 - Cadrage

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `PRJ-001` | `memory-bank/projectBrief.md` | Vision, objectifs, Non-Goals | Product Owner |
| `PRJ-002` | `PRJ-002-architecture-initiale.md` | Architecture, stack, ADR initiaux | Developer |
| `PRJ-003` | `PRJ-003-backlog-initial.md` | Epics, US, priorisation MoSCoW | Product Owner |
| `PRJ-004` | `memory-bank/techContext.md` | Stack, commandes, variables d'env | Developer |

#### Artifacts Phase 2 - Sprint

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `SPR-[NNN]-001` | `SPR-[NNN]-001-sprint-backlog.md` | US selectionnees, Sprint Goal | Product Owner |
| `SPR-[NNN]-002` | `SPR-[NNN]-002-user-stories.md` | Detail des US (si non dans backlog) | Product Owner |
| `SPR-[NNN]-003` | Code source dans `src/` | Implementation des US | Developer |
| `SPR-[NNN]-004` | `SPR-[NNN]-004-rapport-tests.md` | Resultats des tests, bugs | QA Engineer |
| `SPR-[NNN]-005` | `SPR-[NNN]-005-sprint-review.md` | Velocite, US livrees, feedbacks | Product Owner |
| `SPR-[NNN]-006` | `SPR-[NNN]-006-retrospective.md` | Keep/Improve/Stop, actions | Scrum Master |

#### Artifacts Phase 3 - Release

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `REL-[VER]-001` | `REL-[VER]-001-release-notes.md` | Changelog, nouvelles features | Developer |
| `REL-[VER]-002` | `REL-[VER]-002-documentation-utilisateur.md` | Guide utilisateur | Developer |
| `REL-[VER]-003` | `REL-[VER]-003-runbook-deploiement.md` | Procedure de deploiement | Developer |

#### Artifacts Memory Bank (Persistants)

| Fichier | Frequence de Mise a Jour | Persona Responsable |
| :--- | :--- | :--- |
| `memory-bank/projectBrief.md` | Rare (changement de vision) | Product Owner |
| `memory-bank/productContext.md` | Chaque sprint (backlog) | Product Owner |
| `memory-bank/systemPatterns.md` | Apres decision d'architecture | Developer |
| `memory-bank/techContext.md` | Apres changement de stack | Developer |
| `memory-bank/activeContext.md` | **A chaque session** | Tous |
| `memory-bank/progress.md` | **A chaque fin de sprint** | Scrum Master |
| `memory-bank/decisionLog.md` | Apres chaque ADR | Developer |

### 6.3 Structure des Dossiers d'un Projet Applicatif

```
[RACINE DU PROJET]
|-- .clinerules                    # Regles atelier (copie depuis workbench)
|-- .gitignore                     # Exclusions Git
|-- .roomodes                      # Personas Agile (copie depuis workbench)
|-- .workbench-version             # Version de l'atelier deployee
|-- Modelfile                      # Config Ollama (si Mode Local)
|-- proxy.py                       # Proxy Gemini (si Mode Proxy)
|-- requirements.txt               # Dependances Python proxy
|
|-- docs/                          # Tous les artifacts documentaires
|   |-- brief/                     # Phase 0 - Amont
|   |   |-- BRIEF-001-vision-narrative.md
|   |   |-- BRIEF-002-synthese-structuree.md
|   |   |-- BRIEF-003-decision-lancement.md
|   |   +-- archive/               # Projets NO-GO archives
|   |
|   |-- architecture/              # Phase 1 - Cadrage
|   |   +-- PRJ-002-architecture-initiale.md
|   |
|   |-- backlog/                   # Phase 1 - Backlog
|   |   +-- PRJ-003-backlog-initial.md
|   |
|   |-- sprints/                   # Phase 2 - Sprints
|   |   |-- sprint-001/
|   |   |   |-- SPR-001-001-sprint-backlog.md
|   |   |   |-- SPR-001-004-rapport-tests.md
|   |   |   |

|   |   |   |-- SPR-001-005-sprint-review.md
|   |   |   +-- SPR-001-006-retrospective.md
|   |   +-- sprint-002/
|   |       +-- ...
|   |
|   |-- qa/                        # Rapports QA (ecrits par QA Engineer)
|   |   +-- .gitkeep
|   |
|   +-- releases/                  # Phase 3 - Releases
|       |-- REL-1.0.0-001-release-notes.md
|       |-- REL-1.0.0-002-documentation-utilisateur.md
|       +-- REL-1.0.0-003-runbook-deploiement.md
|
|-- memory-bank/                   # Memory Bank - 7 fichiers persistants
|   |-- activeContext.md
|   |-- decisionLog.md
|   |-- productContext.md
|   |-- progress.md
|   |-- projectBrief.md
|   |-- systemPatterns.md
|   +-- techContext.md
|
|-- prompts/                       # Registre prompts (copie depuis workbench)
|   |-- README.md
|   +-- SP-001 a SP-007
|
|-- scripts/                       # Scripts utilitaires (copie depuis workbench)
|   |-- check-prompts-sync.ps1
|   +-- start-proxy.ps1
|
+-- src/                           # Code source applicatif
    +-- [structure specifique au projet]
```

---

## 7. Templates des Artifacts

### 7.1 Template BRIEF-001 - Vision Narrative

```markdown
# BRIEF-001 - Vision Narrative Brute
**Date de creation :** [DATE]
**Cree par :** Product Owner
**Statut :** Brouillon

---

## Entrees Brutes

> Ce fichier contient les entrees TELLES QUELLES, sans reformulation.
> Ne pas modifier le contenu original. Ajouter de nouvelles entrees a la suite.

### Entree 1 - [Source : email / reunion / note / code existant]
**Date :** [DATE]
**Auteur :** [NOM]

[COLLER ICI LE TEXTE BRUT SANS MODIFICATION]

---

### Entree 2 - [Source]
**Date :** [DATE]

[COLLER ICI]

---

## Historique des Ajouts
| Date | Source | Resume |
| :--- | :--- | :--- |
| [DATE] | [SOURCE] | [RESUME EN 1 LIGNE] |
```

### 7.2 Template BRIEF-002 - Synthese Structuree

```markdown
# BRIEF-002 - Synthese Structuree
**Date de creation :** [DATE]
**Base sur :** BRIEF-001-vision-narrative.md
**Statut :** En cours d'analyse

---

## Fonctionnalites Identifiees

### Fonctionnalites Explicites (mentionnees clairement)
- [F-001] [Description]
- [F-002] [Description]

### Fonctionnalites Implicites (deduites du contexte)
- [F-I-001] [Description] - *Deduit de : "[citation de BRIEF-001]"*

---

## Utilisateurs Cibles Identifies

| Persona | Description | Besoins Principaux |
| :--- | :--- | :--- |
| [Nom] | [Description] | [Besoins] |

---

## Contraintes Identifiees

### Contraintes Techniques
- [CT-001] [Description]

### Contraintes Metier / Legales
- [CM-001] [Description]

---

## Perimetre Apparent

### Dans le Perimetre
- [Description]

### Hors Perimetre (apparent)
- [Description]

---

## Ambiguites et Questions Ouvertes

| ID | Question | Criticite | Statut |
| :--- | :--- | :--- | :--- |
| [Q-001] | [Question precise] | CRITIQUE / HAUTE / BASSE | Ouverte / Resolue |

### Reponses aux Questions
**Q-001 :** [Reponse obtenue le DATE]

---

## Risques Identifies
- [R-001] [Description du risque] - Probabilite : [H/M/B] - Impact : [H/M/B]
```

### 7.3 Template BRIEF-003 - Decision de Lancement

```markdown
# BRIEF-003 - Decision de Lancement
**Date de decision :** [DATE]
**Decideur :** [NOM]

---

## Decision

**[ ] GO** - Le projet est lance
**[ ] NO-GO** - Le projet est abandonne
**[ ] ATTENTE** - Le projet est suspendu jusqu'a [CONDITION]

---

## Justification
[Pourquoi cette decision ?]

---

## Conditions de Lancement (si ATTENTE)
- [ ] [Condition 1]
- [ ] [Condition 2]

---

## Risques Acceptes
- [R-001] [Description] - Mitigation : [Plan]

---

## Perimetre Valide pour le Lancement
[Description du perimetre initial valide]

---

## Historique
| Date | Decision | Raison |
| :--- | :--- | :--- |
| [DATE] | [GO/NO-GO/ATTENTE] | [Raison] |
```

### 7.4 Template SPR-[NNN]-001 - Sprint Backlog

```markdown
# SPR-[NNN]-001 - Sprint [NNN] Backlog
**Sprint :** [NNN]
**Dates :** [DATE DEBUT] -> [DATE FIN]
**Sprint Goal :** [UNE PHRASE DECRIVANT L'OBJECTIF DU SPRINT]
**Capacite :** [X] points / [Y] jours

---

## User Stories Selectionnees

### US-[XXX] - [Titre]
**Epic :** [Nom de l'Epic]
**Priorite :** Must / Should / Could
**Complexite :** XS / S / M / L / XL ([X] points)
**Assigne a :** Developer

**En tant que** [persona]
**Je veux** [action]
**Afin de** [benefice]

**Criteres d'Acceptation :**
- [ ] [CA-001] [Critere mesurable]
- [ ] [CA-002] [Critere mesurable]

**Dependances :** [US-XXX ou Aucune]
**Notes techniques :** [Contraintes d'implementation]

---

## Recapitulatif

| US | Titre | Points | Statut |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Titre] | [X] | A faire / En cours / Termine |

**Total points planifies :** [X]
**Total points livres :** [Y] *(mis a jour en fin de sprint)*
**Velocite :** [Y/X * 100]% *(mis a jour en fin de sprint)*
```

### 7.5 Template SPR-[NNN]-004 - Rapport de Tests

```markdown
# SPR-[NNN]-004 - Rapport de Tests Sprint [NNN]
**Sprint :** [NNN]
**Date de test :** [DATE]
**QA Engineer :** [Mode QA Engineer - Roo Code]
**Backend LLM utilise :** [Ollama / Proxy Gemini / Claude API]

---

## Resume Executif

| Metrique | Valeur |
| :--- | :--- |
| US testees | [X] / [Y] planifiees |
| Tests passes | [X] |
| Tests echoues | [X] |
| Bugs critiques | [X] |
| Bugs mineurs | [X] |
| Couverture de code | [X]% |

---

## Resultats par User Story

### US-[XXX] - [Titre]
**Statut global :** VALIDEE / REJETEE / PARTIELLE

| Critere d'Acceptation | Resultat | Notes |
| :--- | :--- | :--- |
| CA-001 : [Description] | PASS / FAIL | [Notes] |
| CA-002 : [Description] | PASS / FAIL | [Notes] |

**Commande de test executee :**
```bash
[commande]
```
**Sortie :**
```
[sortie de la commande]
```

---

## Bugs Identifies

### BUG-[NNN]-001 - [Titre]
**Severite :** CRITIQUE / HAUTE / MOYENNE / BASSE
**US concernee :** US-[XXX]
**Steps de reproduction :**
1. [Etape 1]
2. [Etape 2]
**Comportement attendu :** [Description]
**Comportement observe :** [Description]
**Statut :** Ouvert / Corrige / Accepte

---

## Recommandation QA
**[ ] Sprint valide** - Toutes les US critiques passent les tests
**[ ] Sprint rejete** - Des bugs critiques bloquent la livraison
**[ ] Livraison partielle** - [X] US validees sur [Y]
```

### 7.6 Template SPR-[NNN]-005 - Sprint Review

```markdown
# SPR-[NNN]-005 - Sprint Review Sprint [NNN]
**Sprint :** [NNN]
**Date :** [DATE]
**Participants :** Product Owner, Scrum Master

---

## Sprint Goal
[Rappel du Sprint Goal]
**Atteint :** OUI / NON / PARTIELLEMENT

---

## User Stories Livrees

| US | Titre | Points | Validee par QA |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Titre] | [X] | OUI / NON |

**Velocite :** [X] points livres / [Y] points planifies = [Z]%

---

## User Stories Non Livrees

| US | Titre | Raison | Action |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Titre] | [Raison] | Reporter sprint suivant / Abandonner |

---

## Feedbacks sur les Fonctionnalites
[Observations sur les fonctionnalites livrees]

---

## Ajustements du Backlog
- [US-XXX] : Repriorisee de Should -> Must (raison : [])
- [US-YYY] : Nouvelle US ajoutee (raison : [])
- [US-ZZZ] : Abandonnee (raison : [])

---

## Decision de Release
**[ ] Release planifiee** pour la version [X.Y.Z]
**[ ] Pas de release** - Continuer les sprints
```

### 7.7 Template SPR-[NNN]-006 - Retrospective

```markdown
# SPR-[NNN]-006 - Retrospective Sprint [NNN]
**Sprint :** [NNN]
**Date :** [DATE]
**Facilite par :** Scrum Master

---

## Keep - Ce qui a bien fonctionne
- [Description]
- [Description]

## Improve - Ce qui doit etre ameliore
- [Description] -> Action : [Action concrete]
- [Description] -> Action : [Action concrete]

## Stop - Ce qui doit etre arrete
- [Description]

---

## Actions pour le Prochain Sprint

| Action | Responsable | Echeance |
| :--- | :--- | :--- |
| [Description] | [Persona] | Sprint [NNN+1] |

---

## Impediments Identifies

| Impediment | Impact | Resolution |
| :--- | :--- | :--- |
| [Description] | [Impact] | [Plan de resolution] |

---

## Metriques du Sprint
- Velocite : [X] points
- Velocite moyenne (3 derniers sprints) : [Y] points
- Tendance : En hausse / Stable / En baisse
```

---

## 8. Mecanismes Anti-Risques Agentiques

### 8.1 Catalogue des Risques Agentiques

Le developpement agentique presente des risques specifiques absents du developpement humain classique. Ce catalogue les identifie et decrit les contre-mesures integrees dans l'atelier.

| ID Risque | Risque | Probabilite | Impact | Contre-mesure Principale |
| :--- | :--- | :--- | :--- | :--- |
| **RA-001** | Perte de contexte entre sessions | TRES HAUTE | CRITIQUE | Memory Bank + Sequence VERIFIER->CREER->LIRE->AGIR |
| **RA-002** | Hallucination de code | HAUTE | CRITIQUE | Temperature 0.15 + Modelfile deterministe |
| **RA-003** | Derive de l'architecture sur plusieurs mois | HAUTE | HAUTE | `systemPatterns.md` + ADR dans `decisionLog.md` |
| **RA-004** | Incoherence entre sessions longues | HAUTE | HAUTE | `activeContext.md` mis a jour a chaque session |
| **RA-005** | Regression silencieuse | MOYENNE | CRITIQUE | Tests QA obligatoires + rapports versionnes |
| **RA-006** | Perte de la vision produit | MOYENNE | HAUTE | `projectBrief.md` immuable sauf decision explicite |
| **RA-007** | Duplication de code non detectee | MOYENNE | MOYENNE | `systemPatterns.md` + revue Developer |
| **RA-008** | Decisions d'architecture non tracees | HAUTE | HAUTE | `decisionLog.md` + REGLE 2 `.clinerules` |
| **RA-009** | Prompt injection / derive comportementale | BASSE | CRITIQUE | `.clinerules` + RBAC `.roomodes` |
| **RA-010** | Travail sur mauvaise version du code | MOYENNE | HAUTE | Git obligatoire + commits frequents |

---

### 8.2 RA-001 - Perte de Contexte entre Sessions

**Description du risque :** Un LLM n'a aucune memoire entre deux sessions. Sans mecanisme explicite, chaque session repart de zero. Sur un projet de plusieurs mois, cela conduit a des incoherences, des reimplementations, des contradictions.

**Contre-mesures integrees :**

```
NIVEAU 1 - Sequence obligatoire au demarrage (REGLE 1 .clinerules)
  L'agent DOIT lire activeContext.md et progress.md avant toute action
  Si les fichiers n'existent pas, il les cree depuis les templates

NIVEAU 2 - Mise a jour obligatoire a la cloture (REGLE 2 .clinerules)
  L'agent DOIT mettre a jour activeContext.md avant attempt_completion
  activeContext.md contient : tache en cours, dernier resultat, prochaine action

NIVEAU 3 - Contexte thematique selon la tache (REGLE 3 .clinerules)
  Avant modification architecture : lire systemPatterns.md
  Avant commandes build/test : lire techContext.md
  En debut de sprint : lire productContext.md

NIVEAU 4 - Redondance dans les roleDefinitions (.roomodes)
  Le Developer a le protocole LIRE->CODER->METTRE A JOUR->COMMITER inscrit
  dans son roleDefinition - meme si .clinerules n'est pas lu
```

**Protocole de reprise apres longue interruption (> 1 semaine) :**

```
Instruction a Roo Code (Mode Scrum Master) :
"Je reprends le projet apres [X] jours d'interruption.
 Lis dans cet ordre :
 1. memory-bank/activeContext.md
 2. memory-bank/progress.md
 3. memory-bank/projectBrief.md
 4. memory-bank/productContext.md

 Puis genere un resume de l'etat du projet :
 - Ou en est-on ?
 - Quelle etait la derniere tache en cours ?
 - Quelles sont les prochaines actions ?
 - Y a-t-il des blocages identifies ?

 Mets a jour activeContext.md avec la date de reprise."
```

---

### 8.3 RA-002 - Hallucination de Code

**Description du risque :** Un LLM peut generer du code syntaxiquement correct mais fonctionnellement faux, inventer des APIs inexistantes, ou produire des implementations qui semblent plausibles mais ne fonctionnent pas.

**Contre-mesures integrees :**

```
NIVEAU 1 - Parametres de determinisme (Modelfile Ollama)
  temperature 0.15 (quasi-deterministe)
  min_p 0.03, top_p 0.95, repeat_penalty 1.1
  Reduit drastiquement les reponses "creatives" non fondees

NIVEAU 2 - Tests QA obligatoires apres chaque US
  Le QA Engineer execute les tests reels (pas simules)
  Les criteres d'acceptation sont verifies un par un
  Les bugs sont documentes dans SPR-[NNN]-004

NIVEAU 3 - Commits frequents avec messages descriptifs
  Chaque sous-tache est commitee separement
  En cas d'hallucination detectee : git revert vers le dernier commit sain

NIVEAU 4 - Lecture de la Memory Bank avant de coder
  systemPatterns.md contient les patterns REELS du projet
  techContext.md contient les commandes REELLES testees
  L'agent code en coherence avec ce qui existe, pas ce qu'il imagine
```

**Detection d'une hallucination :**

```
Signes d'alerte :
- L'agent importe une bibliotheque qui n'est pas dans requirements.txt
- L'agent appelle une fonction qui n'existe pas dans le code
- L'agent decrit une architecture differente de systemPatterns.md
- Les tests QA echouent systematiquement sur une US

Action corrective :
1. git log --oneline -10  (identifier le dernier commit sain)
2. git diff HEAD~1        (voir ce qui a change)
3. git revert [hash]      (revenir en arriere si necessaire)
4. Mettre a jour activeContext.md avec la description du probleme
5. Relancer le Developer avec un contexte plus precis
```

---

### 8.4 RA-003 - Derive Architecturale sur Plusieurs Mois

**Description du risque :** Sur un projet long, les decisions d'architecture prises en Phase 1 peuvent etre oubliees ou contredites par des decisions ulterieures. Sans tracabilite, le code devient incoherent.

**Contre-mesures integrees :**

```
NIVEAU 1 - decisionLog.md comme registre des ADR
  Chaque decision d'architecture est documentee avec :
  Date, contexte, decision prise, consequences
  Format : ADR-[NNN] avec numerotation sequentielle

NIVEAU 2 - systemPatterns.md comme reference vivante
  Mis a jour apres chaque decision d'architecture
  Contient les patterns ACTUELS (pas les patterns initiaux)
  L'agent lit ce fichier avant toute modification architecturale

NIVEAU 3 - REGLE 2 .clinerules
  Si une decision d'architecture est prise durant la session :
  obligatoirement mettre a jour decisionLog.md

NIVEAU 4 - Revue architecturale en Sprint Review
  Le Product Owner verifie la coherence avec la vision initiale
  Les derives sont identifiees et documentees
```

**Protocole de revue architecturale (tous les 3 sprints) :**

```
Instruction a Roo Code (Mode Developer) :
"Lis memory-bank/systemPatterns.md, memory-bank/decisionLog.md
 et docs/architecture/PRJ-002-architecture-initiale.md.

 Compare l'architecture initiale avec l'architecture actuelle.
 Identifie :
 - Les derives par rapport a l'architecture initiale
 - Les decisions implicites non documentees dans decisionLog.md
 - Les patterns incoherents entre modules

 Documente tes conclusions dans docs/architecture/ARCH-REVIEW-[DATE].md.
 Mets a jour decisionLog.md avec les ADR manquants.
 Commite avec : 'docs(architecture): revue architecturale sprint [NNN]'"
```

---

### 8.5 RA-004 - Incoherence sur Sessions Longues (Multi-Mois)

**Description du risque :** Sur un projet de plusieurs mois avec des dizaines de sessions, les informations dans la Memory Bank peuvent devenir obsoletes, contradictoires ou incompletes.

**Contre-mesures integrees :**

```
NIVEAU 1 - activeContext.md comme "memoire vive"
  Mis a jour a CHAQUE session (debut et fin)
  Contient toujours l'etat le plus recent
  Inclut le hash du dernier commit Git

NIVEAU 2 - progress.md comme "tableau de bord"
  Checklist des phases et features
  Mis a jour a chaque fin de sprint
  Permet de voir d'un coup d'oeil ou en est le projet

NIVEAU 3 - Versionnement Git de la Memory Bank
  git log --oneline -- memory-bank/ montre l'historique complet
  En cas de doute : git show [hash]:memory-bank/activeContext.md

NIVEAU 4 - Audit de coherence periodique (mensuel)
```

**Protocole d'audit de coherence Memory Bank (mensuel) :**

```
Instruction a Roo Code (Mode Scrum Master) :
"Effectue un audit de coherence de la Memory Bank.

 Pour chaque fichier, verifie :
 1. projectBrief.md : La vision est-elle toujours valide ?
 2. productContext.md : Le backlog est-il a jour avec les sprints livres ?
 3. systemPatterns.md : Les patterns correspondent-ils au code actuel ?
 4. techContext.md : Les commandes et versions sont-elles a jour ?
 5. activeContext.md : L'etat decrit correspond-il a la realite Git ?
 6. progress.md : Les cases cochees correspondent-elles aux commits ?
 7. decisionLog.md : Toutes les decisions recentes sont-elles documentees ?

 Pour chaque incoherence trouvee, corrige le fichier concerne.
 Commite avec : 'docs(memory): audit coherence mensuel [DATE]'"
```

---

### 8.6 RA-005 - Regression Silencieuse

**Description du risque :** Une modification du Developer peut casser une fonctionnalite existante sans que personne ne le detecte, surtout si les tests ne couvrent pas toutes les fonctionnalites.

**Contre-mesures integrees :**

```
NIVEAU 1 - Tests QA obligatoires apres chaque US
  Le QA Engineer teste non seulement la nouvelle US
  Mais aussi les US precedentes potentiellement impactees

NIVEAU 2 - Commits atomiques
  Chaque US = serie de commits lies
  git bisect permet d'identifier le commit qui a introduit la regression

NIVEAU 3 - Rapport de tests versionne
  SPR-[NNN]-004 documente l'etat des tests a chaque sprint
  Comparaison possible entre sprints pour detecter les regressions

NIVEAU 4 - Criteres d'acceptation dans le Sprint Backlog
  Chaque US a des criteres d'acceptation precis et testables
  Le QA Engineer verifie chaque critere individuellement
```

---

### 8.7 RA-008 - Decisions d'Architecture Non Tracees

**Description du risque :** L'agent prend des decisions d'architecture implicites (choix d'une bibliotheque, pattern d'implementation) sans les documenter. Ces decisions sont perdues entre les sessions.

**Contre-mesures integrees :**

```
NIVEAU 1 - REGLE 2 .clinerules (obligatoire)
  Si une decision d'architecture a ete prise durant la session :
  OBLIGATOIREMENT mettre a jour memory-bank/decisionLog.md

NIVEAU 2 - Format ADR standardise
  Chaque ADR contient : Date, Contexte, Decision, Consequences
  Numerotation sequentielle : ADR-001, ADR-002, ...

NIVEAU 3 - Detection proactive par le Developer
  Avant de choisir une bibliotheque : verifier decisionLog.md
  Si une decision similaire existe : la respecter ou la reviser explicitement
```

**Format ADR standard :**

```markdown
## ADR-[NNN] : [Titre de la decision]
**Date :** [DATE]
**Statut :** Propose / Accepte / Deprecie / Remplace par ADR-[YYY]

**Contexte :**
[Pourquoi cette decision etait necessaire]

**Decision :**
[Ce qui a ete decide]

**Consequences :**
- Avantage : [Description]
- Inconvenient : [Description]
- Impact sur : [Fichiers/modules concernes]
```

---

### 8.8 Tableau de Synthese Anti-Risques

| Risque | Mecanisme Preventif | Mecanisme Detectif | Mecanisme Correctif |
| :--- | :--- | :--- | :--- |
| RA-001 Perte contexte | Memory Bank + REGLE 1 | Sequence VERIFIER->CREER->LIRE | Protocole reprise longue interruption |
| RA-002 Hallucination | T=0.15 + Modelfile | Tests QA + git diff | git revert + relance avec contexte precis |
| RA-003 Derive archi | decisionLog.md + REGLE 2 | Revue archi tous les 3 sprints | ARCH-REVIEW + mise a jour ADR |
| RA-004 Incoherence multi-mois | activeContext.md a chaque session | Audit mensuel Memory Bank | Correction + commit docs(memory) |
| RA-005 Regression | Tests QA obligatoires | SPR-[NNN]-004 compare aux precedents | git bisect + fix + re-test |
| RA-008 ADR non traces | REGLE 2 .clinerules | Audit decisionLog.md | Retro-documentation des decisions |

---

## 9. Protocoles de Session

### 9.1 Protocole de Demarrage de Session

**Applicable a toutes les sessions, tous modes, tous personas.**

```
ETAPE 1 - VERIFICATION (automatique via .clinerules REGLE 1)
  L'agent verifie l'existence de :
  - memory-bank/activeContext.md
  - memory-bank/progress.md

ETAPE 2 - CREATION si absents
  Si l'un des fichiers est absent :
  L'agent le cree depuis le template defini dans .clinerules
  Puis passe a l'etape 3

ETAPE 3 - LECTURE
  L'agent lit dans cet ordre :
  1. memory-bank/activeContext.md  (etat courant)
  2. memory-bank/progress.md       (avancement global)

ETAPE 4 - LECTURE CONTEXTUELLE (selon la tache)
  Si modification d'architecture prevue : lire systemPatterns.md
  Si commandes build/test prevues : lire techContext.md
  Si debut de sprint : lire productContext.md

ETAPE 5 - ACTION
  L'agent traite la demande de l'utilisateur
```

**Instruction de demarrage de session recommandee :**

```
"[Decrire ici la tache a accomplir]

 Note : Avant d'agir, lis memory-bank/activeContext.md et
 memory-bank/progress.md pour te remettre dans le contexte du projet."
```

---

### 9.2 Protocole de Cloture de Session

**Applicable avant tout `attempt_completion`, tous modes, tous personas.**

```
ETAPE 1 - MISE A JOUR activeContext.md (obligatoire)
  Contenu a mettre a jour :
  - Date de mise a jour
  - Tache accomplie durant cette session
  - Etat actuel du projet
  - Prochaine(s) action(s) recommandee(s)
  - Blocages eventuels
  - Hash du dernier commit Git

ETAPE 2 - MISE A JOUR progress.md (si features terminees)
  Cocher les US ou phases terminees durant la session

ETAPE 3 - MISE A JOUR decisionLog.md (si decision d'architecture)
  Documenter toute decision d'architecture prise durant la session
  Format ADR standard (voir section 8.7)

ETAPE 4 - COMMIT GIT (obligatoire)
  git add .
  git commit -m "docs(memory): [description de la session]"
  Le hash de ce commit doit etre note dans activeContext.md
```

---

### 9.3 Protocole de Reprise apres Interruption

**Utiliser ce protocole apres toute interruption > 1 semaine.**

```
Instruction a Roo Code (Mode Scrum Master) :
"Je reprends le projet apres [X] jours/semaines d'interruption.

 Effectue un bilan de reprise :

 1. Lis memory-bank/activeContext.md
    -> Quelle etait la derniere tache en cours ?
    -> Quel etait l'etat du projet ?

 2. Lis memory-bank/progress.md
    -> Quelles phases/features sont terminees ?
    -> Quelles sont en cours ?

 3. Execute : git log --oneline -10
    -> Quels sont les derniers commits ?
    -> Y a-t-il des commits non documentes dans la Memory Bank ?

 4. Lis memory-bank/projectBrief.md
    -> La vision du projet est-elle toujours valide ?

 5. Genere un rapport de reprise dans docs/sprints/REPRISE-[DATE].md :
    - Etat du projet au moment de la reprise
    - Prochaines actions recommandees
    - Risques identifies apres l'interruption

 6. Mets a jour memory-bank/activeContext.md avec la date de reprise.
 7. Commite avec : 'docs(memory): reprise projet apres [X] jours - [DATE]'"
```

---

### 9.4 Protocole de Changement de Backend LLM

**Utiliser ce protocole lors du basculement entre les 3 modes LLM.**

```
AVANT LE BASCULEMENT :
  1. Commiter l'etat actuel de la Memory Bank
     git add memory-bank/
     git commit -m "docs(memory): sauvegarde avant changement backend LLM"

  2. Noter dans activeContext.md le nouveau backend utilise
     "Backend LLM actif : [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]"

APRES LE BASCULEMENT :
  3. Tester le nouveau backend avec une requete simple
     "Lis memory-bank/activeContext.md et resume l'etat du projet."

  4. Verifier que la Memory Bank est correctement lue
     Le resume doit correspondre au contenu reel des fichiers

POURQUOI CE PROTOCOLE :
  Chaque backend LLM a des caracteristiques differentes :
  - Ollama (local) : deterministe, peut etre plus lent sur taches complexes
  - Proxy Gemini : haute qualite, necessite copier-coller humain
  - Claude API : haute qualite, entierement automatique, payant
  La Memory Bank garantit la continuite du contexte quel que soit le backend.
```

---

### 9.5 Protocole de Gestion des Conflits Git

**Utiliser ce protocole si des conflits Git apparaissent (rare mais possible).**

```
Instruction a Roo Code (Mode Developer) :
"Un conflit Git a ete detecte.

 1. Execute : git status
    -> Identifier les fichiers en conflit

 2. Pour chaque fichier en conflit :
    - Si conflit dans memory-bank/ : privilegier la version la plus recente
    - Si conflit dans src/ : analyser les deux versions et choisir la meilleure
    - Si conflit dans docs/ : fusionner les deux versions si possible

 3. Apres resolution :
    git add [fichiers resolus]
    git commit -m 'fix(git): resolution conflit [description]'

 4. Mettre a jour memory-bank/activeContext.md avec la description du conflit
    et sa resolution."
```

---

### 9.6 Protocole de Gestion des Erreurs d'Agent

**Utiliser ce protocole si l'agent produit des resultats incorrects ou incoherents.**

```
DIAGNOSTIC :
  1. Identifier le type d'erreur :
     - Hallucination (code invente, API inexistante)
     - Incoherence avec la Memory Bank (ignore les conventions)
     - Depassement de contexte (oublie le debut de la conversation)
     - Erreur de permission RBAC (tente une action hors perimetre)

CORRECTION SELON LE TYPE :

  Hallucination :
  -> git revert [dernier commit problematique]
  -> Relancer avec un contexte plus precis et des exemples concrets
  -> Verifier que systemPatterns.md et techContext.md sont a jour

  Incoherence avec Memory Bank :
  -> Verifier que .clinerules est a la racine du projet
  -> Recharger VS Code (Ctrl+Shift+P > "Developer: Reload Window")
  -> Relancer en rappelant explicitement de lire la Memory Bank

  Depassement de contexte :
  -> Commencer une nouvelle session Roo Code
  -> La nouvelle session relira la Memory Bank depuis le debut
  -> C'est pour cela que la Memory Bank doit etre a jour avant chaque cloture

  Erreur RBAC :
  -> Verifier que le bon persona est selectionne dans Roo Code
  -> Verifier que .roomodes est a la racine du projet
  -> Si le persona tente une action hors perimetre, il doit refuser
     et suggerer le persona approprie
```

---

## 10. Tableau de Bord du Projet

### 10.1 Indicateurs de Sante du Projet

Le tableau de bord est maintenu dans `memory-bank/progress.md`. Il doit refleter en permanence l'etat reel du projet.

**Indicateurs a surveiller :**

| Indicateur | Source | Frequence de Mise a Jour | Seuil d'Alerte |
| :--- | :--- | :--- | :--- |
| Velocite du sprint | SPR-[NNN]-005 | Fin de sprint | < 50% de la velocite cible |
| Couverture de tests | SPR-[NNN]-004 | Fin de sprint | < 70% |
| Bugs critiques ouverts | SPR-[NNN]-004 | Continu | > 0 |
| ADR non documentes | decisionLog.md | Continu | > 0 |
| Memory Bank a jour | activeContext.md | Chaque session | > 48h sans mise a jour |
| Commits sans message | git log | Continu | > 0 commits "WIP" ou vides |

---

### 10.2 Template progress.md Etendu pour Projet Applicatif

```markdown
# Progression du Projet [NOM DU PROJET]
**Derniere mise a jour :** [DATE]
**Sprint courant :** [NNN]
**Backend LLM actif :** [Ollama / Proxy Gemini / Claude API]

---

## Infrastructure Atelier
- [x] Phase 0 : Amont ouvert - Decision GO
- [x] Phase 1 : Cadrage - Memory Bank initialisee
- [x] Phase 1 : Architecture initiale validee
- [x] Phase 1 : Backlog initial cree
- [ ] Phase 2 : Sprint 001 en cours
- [ ] Phase 3 : Premiere release

---

## Backlog par Epic

### Epic 1 : [Nom de l'Epic]
- [x] US-001 : [Titre] - Sprint 001 - LIVREE
- [-] US-002 : [Titre] - Sprint 001 - EN COURS
- [ ] US-003 : [Titre] - Sprint 002 - PLANIFIEE
- [ ] US-004 : [Titre] - Backlog - NON PLANIFIEE

### Epic 2 : [Nom de l'Epic]
- [ ] US-010 : [Titre] - Backlog - NON PLANIFIEE

---

## Historique des Sprints

| Sprint | Dates | Goal | US Planifiees | US Livrees | Velocite |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sprint 001 | [DATE]->[DATE] | [Goal] | [X] | [Y] | [Z]% |

---

## Bugs Ouverts

| ID | Severite | US | Description | Sprint Cible |
| :--- | :--- | :--- | :--- | :--- |
| BUG-001-001 | HAUTE | US-002 | [Description] | Sprint 002 |

---

## Decisions d'Architecture Recentes
- ADR-001 : [Titre] - [DATE] - Accepte
- ADR-002 : [Titre] - [DATE] - Accepte

---

## Legende
- [ ] A faire  |  [-] En cours  |  [x] Termine
```

---

### 10.3 Checklist de Qualite par Sprint

A verifier en fin de chaque sprint avant de commencer le suivant :

**Qualite du Code :**
- [ ] Toutes les US du sprint ont des tests QA documentes
- [ ] Aucun bug critique ouvert
- [ ] Le code respecte les conventions de `systemPatterns.md`
- [ ] Toutes les dependances sont dans `requirements.txt` / `package.json`

**Qualite de la Memory Bank :**
- [ ] `activeContext.md` mis a jour avec l'etat fin de sprint
- [ ] `progress.md` mis a jour (US cochees)
- [ ] `decisionLog.md` contient tous les ADR du sprint
- [ ] `productContext.md` reflÃ¨te les ajustements backlog de la Sprint Review

**Qualite du Versionnement :**
- [ ] Tous les fichiers modifies sont commites
- [ ] Les messages de commit suivent le format Conventional Commits
- [ ] Aucun fichier `.env` ou `venv/` dans Git
- [ ] `git log --oneline -10` montre des commits descriptifs

**Qualite des Artifacts :**
- [ ] `SPR-[NNN]-001` (Sprint Backlog) existe et est complet
- [ ] `SPR-[NNN]-004` (Rapport de Tests) existe et est signe par QA Engineer
- [ ] `SPR-[NNN]-005` (Sprint Review) existe avec la velocite calculee
- [ ] `SPR-[NNN]-006` (Retrospective) existe avec les actions du prochain sprint

---

### 10.4 Commandes de Diagnostic Rapide

Ces commandes permettent de verifier rapidement l'etat du projet :

```powershell
# Etat Git du projet
git log --oneline -10
git status

# Verifier que la Memory Bank est a jour
Get-Content memory-bank/activeContext.md | Select-Object -First 10

# Lister tous les artifacts du projet
Get-ChildItem docs/ -Recurse -Filter "*.md" | Select-Object Name, LastWriteTime

# Verifier les bugs ouverts dans les rapports QA
Select-String -Path "docs/sprints/**/*.md" -Pattern "Statut : Ouvert"

# Verifier la coherence des prompts (atelier)
powershell -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"

# Historique de la Memory Bank
git log --oneline -- memory-bank/

# Derniere mise a jour de activeContext.md
git log --oneline -3 -- memory-bank/activeContext.md
```

---

### 10.5 Signaux d'Alerte et Actions Correctives

| Signal d'Alerte | Cause Probable | Action Corrective |
| :--- | :--- | :--- |
| L'agent ignore la Memory Bank | `.clinerules` absent ou mal place | Verifier que `.clinerules` est a la racine, recharger VS Code |
| L'agent hallucine du code | Contexte insuffisant, temperature trop haute | Lire `systemPatterns.md` + `techContext.md` avant de coder |
| Les tests echouent systematiquement | Regression introduite, hallucination | `git bisect` pour identifier le commit fautif, `git revert` |
| La velocite chute de > 30% | Complexite sous-estimee, impediments | Retrospective immediate, revoir les estimations |
| `activeContext.md` date de > 48h | Sessions sans mise a jour Memory Bank | Audit Memory Bank (protocole 9.3) |
| Conflits Git frequents | Plusieurs sessions paralleles | Toujours commiter avant de changer de session |
| Bugs critiques s'accumulent | Tests insuffisants, US trop larges | Decouper les US, renforcer les criteres d'acceptation |
| L'architecture derive | ADR non documentes, Memory Bank obsolete | Revue architecturale (protocole 8.4) |

---

## Annexe A - Correspondance Artifacts / Memory Bank / Git

| Artifact | Fichier | Commit Format | Persona |
| :--- | :--- | :--- | :--- |
| BRIEF-001 | `docs/brief/BRIEF-001-*.md` | `docs(brief): vision narrative initiale` | Product Owner |
| BRIEF-002 | `docs/brief/BRIEF-002-*.md` | `docs(brief): synthese structuree` | Developer |
| BRIEF-003 | `docs/brief/BRIEF-003-*.md` | `docs(brief): decision lancement [GO/NO-GO]` | Product Owner |
| PRJ-001 | `memory-bank/projectBrief.md` | `feat(memory): initialisation projectBrief` | Product Owner |
| PRJ-002 | `docs/architecture/PRJ-002-*.md` | `feat(architecture): architecture initiale` | Developer |
| PRJ-003 | `docs/backlog/PRJ-003-*.md` | `feat(backlog): backlog initial MoSCoW` | Product Owner |
| SPR-NNN-001 | `docs/sprints/sprint-NNN/SPR-NNN-001-*.md` | `feat(sprint-NNN): sprint planning` | Product Owner |
| SPR-NNN-004 | `docs/sprints/sprint-NNN/SPR-NNN-004-*.md` | `test(sprint-NNN): rapport de tests` | QA Engineer |
| SPR-NNN-005 | `docs/sprints/sprint-NNN/SPR-NNN-005-*.md` | `docs(sprint-NNN): sprint review` | Product Owner |
| SPR-NNN-006 | `docs/sprints/sprint-NNN/SPR-NNN-006-*.md` | `docs(sprint-NNN): retrospective` | Scrum Master |
| REL-VER-001 | `docs/releases/REL-VER-001-*.md` | `docs(release): release notes vVER` | Developer |
| ADR-NNN | `memory-bank/decisionLog.md` | `docs(memory): ADR-NNN [titre]` | Developer |

---

## Annexe B - Glossaire du Processus

| Terme | Definition |
| :--- | :--- |
| **Artifact** | Document produit par le processus Agile. Chaque artifact a un ID unique, un template, un persona responsable et un emplacement defini dans la structure du projet. |
| **Amont Ouvert** | Phase 0 du processus. Accepte des entrees non-structurees (emails, notes, code existant) et les transforme progressivement en artifacts structures via BRIEF-001, BRIEF-002, BRIEF-003. |
| **Convergence Progressive** | Principe selon lequel les entrees narratives brutes (Phase 0) maturent vers des artifacts de plus en plus structures (Phase 1, Phase 2) sans forcer une structure prematuree. |
| **Defense en Profondeur** | Principe de securite agentique : chaque regle critique est inscrite a plusieurs niveaux (`.clinerules`, `roleDefinition`, protocoles de session) pour qu'elle soit respectee meme si un niveau est ignore. |
| **Epic** | Regroupement fonctionnel de User Stories partageant un objectif metier commun. Une Epic peut s'etendre sur plusieurs sprints. |
| **Hallucination** | Comportement d'un LLM qui genere du contenu plausible mais incorrect (code invente, API inexistante, architecture fictive). Contre-mesure principale : temperature 0.15 + tests QA obligatoires. |
| **Impediment** | Obstacle qui empeche l'equipe de progresser. Identifie par le Scrum Master dans la Retrospective. Doit avoir un plan de resolution documente. |
| **MoSCoW** | Methode de priorisation : Must (obligatoire), Should (important), Could (souhaitable), Won't (hors perimetre). Utilisee pour le backlog initial (PRJ-003). |
| **Perte de Contexte** | Risque agentique RA-001. Un LLM n'a aucune memoire entre deux sessions. La Memory Bank est le mecanisme principal de contre-mesure. |
| **Protocole de Session** | Sequence d'actions obligatoires au demarrage et a la cloture de chaque session Roo Code. Garantit la continuite du contexte entre les sessions. |
| **Regression Silencieuse** | Bug introduit par une modification qui casse une fonctionnalite existante sans etre detecte immediatement. Contre-mesure : tests QA apres chaque US. |
| **Sprint Goal** | Objectif en une phrase du sprint. Definit ce que l'equipe s'engage a livrer. Inscrit dans SPR-NNN-001 et dans `activeContext.md`. |
| **T-shirt Sizing** | Methode d'estimation de complexite : XS (< 1h), S (1-4h), M (4-8h), L (1-3j), XL (> 3j). Utilisee pour le backlog initial. |
| **User Story** | Description d'une fonctionnalite du point de vue de l'utilisateur. Format : "En tant que [persona], je veux [action] afin de [benefice]". Identifiee par US-NNN. |
| **Velocite** | Nombre de points livres par sprint. Indicateur de la capacite de l'equipe. Calculee dans SPR-NNN-005. |

---

## Annexe C - Table des References

| Ref. | Type | Titre / Identifiant | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Document interne | `workbench/DOC1-PRD-Workbench-Requirements.md` | Exigences de l'atelier - REQ-xxx references dans ce document |
| [DOC2] | Document interne | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Architecture technique de l'atelier - DA-xxx references |
| [DOC3] | Document interne | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | Plan d'installation de l'atelier (Phases 0-12) |
| [DOC4] | Document interne | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | Guide de deploiement de l'atelier sur projets |
| [DOC5] | Document interne | `workbench/DOC5-GUIDE-Project-Development-Process.md` | Ce document - Manuel du processus Agile applicatif |
| [SCRUM] | Standard | Scrum Guide (scrumguides.org) | Guide officiel Scrum - reference pour les ceremonies et roles |
| [MOSCOW] | Methode | MoSCoW Prioritization | Methode de priorisation Must/Should/Could/Won't |
| [ADR] | Pattern | Architecture Decision Records (adr.github.io) | Format standard pour documenter les decisions d'architecture |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | Convention MAJOR.MINOR.PATCH pour les releases |
| [CONVCOMMITS] | Standard | Conventional Commits (conventionalcommits.org) | Convention de messages de commit : type(scope): description |
| [MEMORY-BANK] | Composant Atelier | `memory-bank/` (7 fichiers .md) | Systeme de memoire persistante - contre-mesure principale RA-001 |
| [CLINERULES] | Composant Atelier | `.clinerules` (6 regles imperatives) | Directives de session - REGLE 1 a REGLE 6 |
| [ROOMODES] | Composant Atelier | `.roomodes` (4 personas Agile) | Personas Product Owner, Scrum Master, Developer, QA Engineer |
