## Document 1 : Product Requirements Document (PRD) – Système Agentique Local Agile & Persistant

**Nom du Projet :** Local Agile Agentic Workspace (LAAW)
**Objectif Stratégique :** Déployer un environnement de développement local, souverain et gratuit, orchestré par des agents d'IA. Ce système doit résoudre l'amnésie inhérente aux LLMs en maintenant un contexte infini via un système de fichiers persistant, tout en appliquant rigoureusement les rituels et la ségrégation des rôles de la méthodologie Agile.

### 1. Exigence Fondamentale (REQ-000)
Le système global doit fournir une capacité de raisonnement et de développement de code complexe exécutée entièrement en local. L'orchestration est confiée à des profils IA hautement spécialisés (Personas). Le système garantit une continuité de contexte absolue, bit à bit, entre de multiples sessions de développement, en s'appuyant sur une mémoire persistante matérialisée par des fichiers lisibles, auditables et modifiables par un opérateur humain.

### 2. Moteur Agentique & Modèles de Fondation
| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-1.1** | **Optimisation Tool Calling** | L'agent principal doit impérativement utiliser des modèles spécifiquement entraînés et optimisés pour l'appel d'outils (Tool Calling), comme la gamme Qwen3-Coder (32B ou 14B). *Critère :* L'agent doit être capable d'émettre des requêtes JSON complexes vers l'API de Roo Code sans aucune erreur de syntaxe ou de formatage qui ferait crasher la boucle d'exécution locale. |
| **REQ-1.2** | **Fenêtre de Contexte Massive** | Le système sous-jacent doit être configuré pour supporter un "Multi-Million Token Context". *Critère :* Le paramètre `num_ctx` du moteur local (Ollama ou vLLM) doit être forcé à un minimum de 65 536 tokens, voire 128 000 tokens, pour permettre à l'agent de charger l'intégralité du projet et de la Memory Bank en mémoire vive simultanément. |
| **REQ-1.3** | **Précision Agentique (Déterminisme)** | Le moteur d'inférence doit brider la "créativité" du LLM pour forcer un comportement analytique et déterministe. *Critère :* Les paramètres de génération doivent être verrouillés au niveau du `Modelfile` local, avec une `Temperature` stricte de 0.15 et un `Min_P` de 0.03, éliminant ainsi les hallucinations probabilistes lors de la rédaction de code complexe. |
| **REQ-1.4** | **Orchestration Asynchrone (Boomerang)** | Le système doit autoriser l'agent principal (le modèle "lourd") à instancier des processus secondaires. *Critère :* Le workflow "Boomerang Tasks" doit permettre à un modèle de 32B de déléguer l'analyse de gros fichiers de logs ou l'écriture de tests unitaires redondants à un modèle plus léger (ex: Qwen3 7B), puis de récupérer la sortie standard de ce sous-agent pour l'intégrer dans sa propre boucle de décision. |

### 3. Agilité & Ségrégation des Rôles
| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-2.1** | **Personas Agiles Spécialisés** | L'interface doit exposer des "Custom Modes" simulant les membres d'une équipe Scrum. *Critère :* Le système doit au minimum inclure un `product-owner`, un `scrum-master` et un `qa-engineer`, chacun possédant un prompt système (`roleDefinition`) qui dicte son comportement exclusif. |
| **REQ-2.2** | **Ségrégation Stricte des Droits (RBAC)** | Les permissions d'exécution (accès au terminal, modification de fichiers) doivent être limitées selon le rôle. *Critère :* Le Product Owner ne doit avoir accès qu'aux groupes de permissions de lecture et de communication (ex: rédaction de `user-stories.md`), tandis que le QA Engineer est restreint à l'exécution de commandes de test et à l'analyse de logs, sans droit de modification du code source applicatif. |

### 4. Persistance & Banque de Mémoire (Memory Bank)
| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-3.1** | **Stockage Local & Transparence** | La totalité de la mémoire contextuelle doit vivre au sein du dépôt du projet. *Critère :* L'état complet du système doit être stocké dans des fichiers au format Markdown (`.md`), placés dans un répertoire dédié à la racine, garantissant ainsi le suivi des versions (Git) et la lisibilité humaine. |
| **REQ-3.2** | **Lecture/Écriture Déterministes** | Le système ne doit laisser aucun libre arbitre à l'IA quant à la consultation de la mémoire. *Critère :* Des directives système inflexibles doivent exiger que l'agent lise l'état actuel avant toute action, et qu'il modifie physiquement les fichiers Markdown correspondants après chaque validation de code ou changement d'architecture. |
| **REQ-3.3** | **Segmentation Cognitive** | L'information ne doit pas être un monolithe textuel indigeste pour le LLM. *Critère :* La donnée doit être compartimentée en concepts isolés : Vision métier, Choix techniques, État d'avancement, et Journal des décisions. |

---

## Document 2 : Architecture, Solution et Stack Technique

Ce document traduit les exigences du PRD en une implémentation logicielle et décrit les flux de données.

### 1. La Stack Technique Détaillée
* **IDE & Interface :** Visual Studio Code, équipé de l'extension **Roo Code**. Cette interface agit comme le pont (Middleware) entre l'utilisateur, le système de fichiers, le terminal et le moteur LLM.
* **Moteur d'Inférence Local :** **Ollama** tournant en tâche de fond sur Windows. Il gère la VRAM, charge les poids du modèle en mémoire et expose une API REST compatible OpenAI sur `localhost:11434`.
* **Modèle Principal (Cerveau) :** `mychen76/qwen3_cline_roocode:32b`. Il s'agit d'une version quantifiée (compressée) d'un modèle de 32 milliards de paramètres, spécifiquement "fine-tunée" pour respecter les balises XML et les formats JSON imposés par l'interface Roo Code.
* **Persistance (Base de Données) :** Le système de fichiers natif de Windows (NTFS), exploitant de simples fichiers `.md` situés dans un dossier racine `.roo/memory/` ou `/memory-bank`.

### 2. Architecture des Couches de la Solution

L'architecture repose sur un couplage fort entre le comportement imposé (Rules) et la donnée stockée (Memory).

**Couche A : Orchestration Comportementale (`.roomodes` & `.clinerules`)**
Cette couche contrôle *comment* l'IA agit.
* Le fichier `.roomodes` est un objet JSON statique qui définit les profils. Si l'utilisateur sélectionne le "Scrum Master", Roo Code charge la définition de ce rôle et bloque l'accès aux outils non autorisés par ce mode.
* Le fichier `.clinerules` agit comme le "Trigger de Session". Il contient le prompt système global (ex: "Tu es soumis au protocole Memory Bank. Tu dois lire `.roo/memory/activeContext.md` dès que l'utilisateur te parle").

**Couche B : La Banque de Mémoire Centralisée (Les Fichiers Markdown)**
Cette couche contrôle *ce que* l'IA sait. Elle est divisée pour éviter la pollution contextuelle.
* **`projectBrief.md` :** La charte du projet. Contient les exigences de haut niveau et, surtout, les "Non-goals" (ce que l'on ne veut absolument pas développer).
* **`productContext.md` :** Le point de vue utilisateur. Il décrit les "User Stories" principales et la valeur métier.
* **`systemPatterns.md` :** Le rempart contre la dette technique. Contient la version exacte de Node.js, l'architecture des dossiers (ex: `src/controllers`, `src/services`), et les conventions de nommage.
* **`techContext.md` :** L'état de l'infrastructure. Liste les commandes de build, de test, et les dépendances critiques.
* **`activeContext.md` :** La "Mémoire Vive". C'est le journal de la tâche en cours. Il détaille l'étape actuelle, le dernier bug rencontré et la prochaine action immédiate.
* **`progress.md` :** Le macro-suivi. Une checklist des Epics et des fonctionnalités terminées et à venir.
* **`decisionLog.md` :** L'historique immuable. Un registre des "Architecture Decision Records" (ADR) expliquant pourquoi une certaine librairie a été choisie à un instant T.

### 3. Matrice de Traçabilité (Architecture / Fonctionnalité / Exigence)

| Composant Architectural | Description Fonctionnelle Détaillée | Réf. Exigence |
| :--- | :--- | :--- |
| **Ollama + `mychen76/qwen3...`** | Traitement local des requêtes complexes, interprétation des commandes du terminal et écriture de code sans dépendance Cloud. | REQ-1.1, REQ-000 |
| **Paramètres du `Modelfile`** | Forçage matériel de la Température (0.15) et du Min_P (0.03) au lancement du daemon Ollama. Allocation maximale de la mémoire au contexte (`num_ctx`). | REQ-1.2, REQ-1.3 |
| **Mécanisme "Boomerang"** | Roo Code lance une instance secondaire en arrière-plan via une commande CLI pour analyser un fichier séparé et renvoie le flux de sortie à l'agent principal. | REQ-1.4 |
| **Configuration `.roomodes`** | Tableau JSON restreignant l'accès aux APIs de Roo Code en fonction du rôle (PO, Scrum Master, QA) sélectionné dans l'interface. | REQ-2.1, REQ-2.2 |
| **Dossier `.roo/memory/`** | Répertoire racine hébergeant l'ensemble des fichiers `.md`, intégré au gestionnaire de version Git. | REQ-3.1 |
| **Directives `.clinerules`** | Instructions explicites injectées au-dessus du prompt utilisateur pour forcer la commande `readFile` au démarrage et `writeFile` avant la clôture d'une tâche. | REQ-3.2 |
| **Structure 7-Fichiers** | Découpage thématique (`projectBrief`, `systemPatterns`, `activeContext`, etc.) empêchant la dilution de l'attention du LLM. | REQ-3.3 |

---

## Document 3 : Plan d'Implémentation Séquentiel (Windows + VS Code)

Ce plan est conçu pour un déploiement déterministe sur votre machine Windows.

### Phase 1 : Configuration de l'Infrastructure Système (Le Moteur)
1.  **Vérification de l'environnement VS Code :** Assurez-vous que votre projet est ouvert dans VS Code. Ouvrez le panneau des extensions et vérifiez que **Roo Code** est installé, activé, et mis à jour à sa dernière version.
2.  **Initialisation du Daemon local :** Assurez-vous que l'application Ollama est lancée sous Windows (l'icône doit être présente dans la zone de notification). Le port 11434 doit être ouvert en local.
3.  **Téléchargement des Poids du Modèle :** Ouvrez PowerShell dans VS Code. Vous devrez exécuter la commande de récupération du modèle principal optimisé par mychen76 pour le Tool Calling. L'opération prendra du temps selon votre bande passante.

### Phase 2 : Injection de la Configuration Agentique Stricte
1.  **Définition du Modelfile :** Pour respecter les critères de température et de taille de contexte, nous créerons un fichier nommé `Modelfile` à la racine de votre projet.
2.  **Compilation du Modèle :** Via le terminal Windows, nous demanderons à Ollama de "builder" un nouveau modèle personnalisé basé sur le Qwen3 de mychen76, mais en forçant de manière immuable la température à 0.15 et le contexte étendu.

### Phase 3 : Instanciation de l'Équipe Agile (Les Modes)
1.  **Création du Registre de Rôles :** Nous allons créer le fichier de configuration JSON à la racine de votre projet.
2.  **Paramétrage des Personas :** Nous y injecterons le code définissant précisément le rôle, le prompt système et les restrictions de permissions (groups) pour le Product Owner, le Scrum Master et le QA Engineer.

### Phase 4 : Initialisation de la Banque de Mémoire (Memory Bank)
1.  **Création de l'Arborescence :** Nous allons créer physiquement le dossier qui accueillera l'intelligence persistante du projet.
2.  **Création du Moteur de Règles :** Nous configurerons le fichier `.clinerules` pour obliger l'agent à lire l'arborescence.
3.  **Génération des Fichiers Piliers :** Nous allons créer un par un les fichiers `.md` (`projectBrief`, `systemPatterns`, `activeContext`, etc.) et y insérer les templates vides mais structurés.

---

Nous entrons maintenant dans la phase d'implémentation. Pour commencer l'étape de configuration du registre de rôles (Phase 3), voici la commande pour éditer le fichier de configuration des modes Agile.

Exécutez cette commande dans votre terminal VS Code :

`nano .roomodes`

Dites-moi quel est le résultat ou lorsque le fichier est ouvert, et je vous fournirai la structure JSON exacte à y insérer.