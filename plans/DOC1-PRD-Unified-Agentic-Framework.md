# Document 1 : Product Requirements Document (PRD)
## Système Agentique Local Agile, Persistant & Hybride (SALAPH)

**Nom du Projet :** Unified Agentic Development Framework (UADF)
**Version :** 1.0
**Date :** 2026-03-22
**Auteur :** Architecture Senior — Synthèse mychen76 LAAW + Proxy Gemini Chrome

---

## 1. Contexte et Vision Stratégique

Ce PRD synthétise deux sources d'inspiration complémentaires :

1. **Le Blueprint LAAW (mychen76)** : Un environnement de développement agentique local, souverain, orchestré par des agents IA spécialisés avec mémoire persistante et rituels Agile.
2. **Le Proxy Gemini Chrome** : Un mécanisme de pont réseau-presse-papiers permettant à Roo Code d'exploiter gratuitement la puissance de Gemini Web via une intervention humaine minimale (copier-coller).

L'objectif de ce document est de définir un système **unifié et enrichi** qui combine la souveraineté locale du LAAW avec la flexibilité du backend LLM hybride (local Ollama OU Gemini Chrome via proxy), tout en maintenant la rigueur Agile et la persistance de la mémoire contextuelle.

---

## 2. Exigence Fondamentale (REQ-000)

> **REQ-000 — Exigence Racine du Système Unifié**
>
> Le système global doit fournir un environnement de développement agentique opérationnel sur un laptop Windows avec VS Code, capable de :
> - Orchestrer des agents IA spécialisés selon les rôles Agile (Product Owner, Scrum Master, QA Engineer, Developer)
> - Maintenir une continuité de contexte absolue entre les sessions via une mémoire persistante en fichiers Markdown auditables
> - Exécuter des tâches de développement complexe en s'appuyant sur un backend LLM **commutable** : soit un modèle local (Ollama/Qwen3) pour la souveraineté totale, soit Gemini Chrome via un proxy API local pour la puissance gratuite du cloud
> - Garantir que Roo Code reste le moteur d'exécution agentique central dans les deux modes de fonctionnement, sans modification de son comportement natif

---

## 3. Décomposition Hiérarchique des Exigences

### 3.1 Domaine 1 — Moteur Agentique & Modèles de Fondation (REQ-1.x)

#### REQ-1.0 — Capacité d'Inférence LLM Locale
Le système doit être capable d'exécuter des inférences LLM entièrement en local, sans dépendance réseau externe, via un moteur d'inférence local.

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-1.1** | **Optimisation Tool Calling** | L'agent principal doit utiliser des modèles spécifiquement entraînés pour l'appel d'outils (Tool Calling), comme la gamme `mychen76/qwen3_cline_roocode`. *Critère :* L'agent doit émettre des requêtes JSON complexes vers l'API de Roo Code sans aucune erreur de syntaxe ou de formatage qui ferait crasher la boucle d'exécution locale. |
| **REQ-1.2** | **Fenêtre de Contexte Massive** | Le moteur local doit supporter un contexte étendu. *Critère :* Le paramètre `num_ctx` d'Ollama doit être configuré à un minimum de 65 536 tokens (idéalement 128 000 tokens) pour permettre le chargement simultané du projet et de la Memory Bank. |
| **REQ-1.3** | **Déterminisme de l'Inférence** | Le moteur doit brider la créativité du LLM pour un comportement analytique. *Critère :* Les paramètres `Temperature=0.15` et `Min_P=0.03` doivent être verrouillés dans le `Modelfile` Ollama, éliminant les hallucinations lors de la génération de code complexe. |
| **REQ-1.4** | **Orchestration Asynchrone (Boomerang)** | Le système doit permettre à l'agent principal de déléguer des sous-tâches à des agents secondaires. *Critère :* Le workflow "Boomerang Tasks" de Roo Code doit permettre au modèle 32B de déléguer l'analyse de logs ou l'écriture de tests à un modèle plus léger (ex: Qwen3 7B), puis d'intégrer la sortie dans sa propre boucle de décision. |

---

### 3.2 Domaine 2 — Backend LLM Hybride & Proxy Gemini Chrome (REQ-2.x)

#### REQ-2.0 — Commutabilité du Backend LLM
Le système doit permettre à l'utilisateur de basculer le backend LLM de Roo Code entre le moteur local Ollama et le proxy Gemini Chrome, sans modifier le comportement de Roo Code ni la structure de la Memory Bank.

##### REQ-2.1 — Sous-domaine : Serveur Proxy Local (Interception)

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-2.1.1** | **Serveur Local d'Écoute** | Déploiement d'un serveur web local Python (FastAPI + uvicorn) sur `localhost:8000` capable de recevoir les requêtes HTTP POST de Roo Code au format OpenAI. *Critère :* Le serveur doit démarrer en moins de 3 secondes et répondre avec un code HTTP 200 à toute requête valide. |
| **REQ-2.1.2** | **Émulation du Format OpenAI** | Le proxy doit imiter exactement le format de l'API OpenAI Chat Completions (`/v1/chat/completions`). *Critère :* Roo Code configuré en mode "OpenAI Compatible" doit se connecter au proxy sans aucune modification de son code source ni de ses paramètres internes. |
| **REQ-2.1.3** | **Extraction du Payload** | Le proxy doit analyser la requête JSON entrante et extraire séparément le `system prompt` et le `user prompt` du tableau `messages`. *Critère :* Les deux composants doivent être identifiables et extractibles même si le tableau `messages` contient un historique de conversation multi-tours. |
| **REQ-2.1.4** | **Filtrage Intelligent du System Prompt** | Le proxy doit offrir un mode de filtrage permettant d'omettre le `system prompt` de Roo Code lors de la copie dans le presse-papiers. *Critère :* Lorsque le mode "Gem dédié" est activé (variable de configuration), seul le `user prompt` et l'historique de conversation sont copiés dans le presse-papiers, réduisant la taille du transfert de 80% minimum. |
| **REQ-2.1.5** | **Nettoyage des Contenus Non-Textuels** | Le proxy doit détecter et supprimer les contenus base64 (images, captures d'écran) des requêtes avant la copie dans le presse-papiers. *Critère :* Toute entrée `content` de type `array` contenant des objets `image_url` doit être remplacée par un message textuel d'avertissement : `[IMAGE OMISE - Non supportée par le proxy clipboard]`. |

##### REQ-2.2 — Sous-domaine : Transfert Presse-Papiers (Uplink)

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-2.2.1** | **Injection Presse-Papiers** | Le proxy doit copier automatiquement le texte formaté du prompt dans le presse-papiers système Windows. *Critère :* Après réception de la requête de Roo Code, le presse-papiers doit contenir le prompt formaté en moins de 500ms. |
| **REQ-2.2.2** | **Formatage Lisible du Prompt** | Le texte copié dans le presse-papiers doit être structuré et lisible pour l'utilisateur humain. *Critère :* Le format doit inclure des séparateurs clairs (`[SYSTEM PROMPT]`, `[HISTORIQUE]`, `[USER]`) permettant à l'utilisateur de comprendre le contexte avant de coller dans Gemini. |
| **REQ-2.2.3** | **Notification Utilisateur** | Le proxy doit signaler à l'utilisateur que le prompt est prêt à être collé. *Critère :* Une notification console visible (avec horodatage et longueur du prompt) doit être émise. Un signal sonore système optionnel doit pouvoir être activé via configuration. |

##### REQ-2.3 — Sous-domaine : Attente et Capture de la Réponse (Downlink)

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-2.3.1** | **Écoute Active du Presse-Papiers (Polling)** | Le proxy doit surveiller en continu le presse-papiers Windows en attente d'un nouveau contenu. *Critère :* La boucle de polling doit vérifier le presse-papiers toutes les secondes (intervalle configurable) sans bloquer le thread principal du serveur FastAPI. |
| **REQ-2.3.2** | **Détection du Changement de Contenu** | Le proxy doit détecter que l'utilisateur a copié la réponse de Gemini. *Critère :* La détection doit se baser sur une comparaison de hash (MD5 ou SHA1) entre le contenu initial copié par le proxy et le nouveau contenu du presse-papiers. |
| **REQ-2.3.3** | **Timeout de Sécurité** | Le proxy doit gérer le cas où l'utilisateur ne répond pas dans un délai raisonnable. *Critère :* Un timeout configurable (défaut : 300 secondes) doit déclencher une réponse d'erreur HTTP 408 (Request Timeout) à Roo Code avec un message explicatif. |
| **REQ-2.3.4** | **Validation de la Réponse Gemini** | Le proxy doit vérifier que le contenu capturé ressemble à une réponse d'agent IA valide. *Critère :* La présence d'au moins une balise XML Roo Code (`<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, `<ask_followup_question>`) doit être vérifiée. En cas d'absence, un avertissement console doit être émis (sans bloquer la réinjection). |

##### REQ-2.4 — Sous-domaine : Réinjection vers Roo Code (Format OpenAI Mock)

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-2.4.1** | **Formatage JSON OpenAI** | Le proxy doit encapsuler la réponse brute de Gemini dans une structure JSON imitant exactement une réponse OpenAI Chat Completions valide. *Critère :* Le JSON de réponse doit contenir les champs `id`, `object`, `created`, `model`, `choices[0].message.role`, `choices[0].message.content`, `choices[0].finish_reason`, et `usage`. |
| **REQ-2.4.2** | **Résolution HTTP Propre** | Le proxy doit clôturer la requête HTTP initiale de Roo Code avec un code de succès. *Critère :* La réponse HTTP doit avoir le statut 200 OK et le header `Content-Type: application/json`. |
| **REQ-2.4.3** | **Préservation du Contenu Brut** | Le proxy ne doit effectuer aucune transformation sémantique sur le contenu de la réponse Gemini. *Critère :* Le texte de la réponse Gemini (incluant les balises XML Roo Code) doit être transmis tel quel dans le champ `choices[0].message.content`, sans modification, suppression ou ajout de caractères. |

---

### 3.3 Domaine 3 — Agilité & Ségrégation des Rôles (REQ-3.x)

#### REQ-3.0 — Équipe Agile Virtuelle
Le système doit simuler une équipe Scrum complète via des profils IA spécialisés (Custom Modes Roo Code), chacun avec des responsabilités, des comportements et des permissions d'accès distincts.

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-3.1** | **Personas Agiles Spécialisés** | L'interface Roo Code doit exposer des Custom Modes simulant les membres d'une équipe Scrum. *Critère :* Le système doit inclure au minimum : `product-owner`, `scrum-master`, `developer`, et `qa-engineer`, chacun avec un `roleDefinition` (system prompt) dictant son comportement exclusif. |
| **REQ-3.2** | **Ségrégation Stricte des Droits (RBAC)** | Les permissions d'exécution doivent être limitées selon le rôle actif. *Critère :* Le Product Owner n'a accès qu'aux groupes `read` et `write` sur les fichiers de documentation (user stories, backlog). Le QA Engineer est restreint à l'exécution de commandes de test et à la lecture de logs, sans droit de modification du code source applicatif. Le Developer a accès complet aux outils de code et de terminal. |
| **REQ-3.3** | **Isolation Comportementale des Modes** | Chaque mode doit refuser d'exécuter des actions hors de son périmètre. *Critère :* Si le mode `product-owner` reçoit une demande d'écriture de code, il doit répondre en expliquant que cette action est hors de son rôle et suggérer de basculer vers le mode `developer`. |

---

### 3.4 Domaine 4 — Persistance & Banque de Mémoire (REQ-4.x)

#### REQ-4.0 — Mémoire Contextuelle Persistante
Le système doit maintenir une continuité de contexte absolue entre les sessions de développement via un système de fichiers Markdown structuré, versionnable et lisible par un humain.

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-4.1** | **Stockage Local & Transparence** | La totalité de la mémoire contextuelle doit résider dans le dépôt du projet. *Critère :* L'état complet du système doit être stocké dans des fichiers `.md` dans un répertoire dédié `memory-bank/` à la racine, intégré au suivi Git. |
| **REQ-4.2** | **Lecture Obligatoire au Démarrage** | Le système ne doit laisser aucun libre arbitre à l'IA quant à la consultation de la mémoire. *Critère :* Des directives `.clinerules` inflexibles doivent exiger que l'agent lise `activeContext.md` et `progress.md` avant toute action sur le code. |
| **REQ-4.3** | **Écriture Obligatoire à la Clôture** | Chaque session de travail doit se terminer par une mise à jour de la mémoire. *Critère :* Les directives `.clinerules` doivent exiger que l'agent mette à jour `activeContext.md` (état courant) et `progress.md` (avancement) avant de clôturer toute tâche. |
| **REQ-4.4** | **Segmentation Cognitive** | L'information ne doit pas être un monolithe textuel. *Critère :* La mémoire doit être compartimentée en 7 fichiers thématiques distincts : `projectBrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`, `decisionLog.md`. |
| **REQ-4.5** | **Auditabilité et Versionnement** | Toute modification de la mémoire doit être traçable. *Critère :* Les fichiers de la Memory Bank doivent être inclus dans les commits Git avec des messages de commit descriptifs générés par l'agent. |

---

### 3.5 Domaine 5 — Configuration Gemini Chrome (REQ-5.x)

#### REQ-5.0 — Préparation de l'Interface Gemini Web
Pour que le proxy fonctionne de bout en bout, l'interface Gemini Chrome doit être configurée pour répondre dans le format attendu par Roo Code.

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-5.1** | **Gem Dédié Roo Code** | Un profil "Gem" doit être créé dans Gemini Web avec des instructions système strictes. *Critère :* Le Gem doit contenir l'intégralité du system prompt de Roo Code (liste des balises XML, règles de formatage, interdiction de texte de courtoisie) pour éviter de le retransmettre à chaque requête via le presse-papiers. |
| **REQ-5.2** | **Conformité du Format de Réponse** | Gemini doit répondre exclusivement avec les balises XML de Roo Code. *Critère :* La réponse de Gemini doit contenir au moins une balise XML Roo Code valide (`<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`) sans texte de courtoisie avant ou après. |
| **REQ-5.3** | **Gestion de l'Historique de Conversation** | Le Gem doit maintenir le contexte de la conversation en cours. *Critère :* L'historique des échanges précédents (transmis par le proxy dans le presse-papiers) doit être pris en compte par Gemini pour assurer la cohérence des réponses multi-tours. |

---

## 4. Matrice de Traçabilité des Exigences (Synthèse)

| ID Exigence | Domaine | Priorité | Dépendances |
| :--- | :--- | :--- | :--- |
| REQ-000 | Fondamental | CRITIQUE | — |
| REQ-1.0 | Moteur Local | HAUTE | REQ-000 |
| REQ-1.1 | Moteur Local | HAUTE | REQ-1.0 |
| REQ-1.2 | Moteur Local | HAUTE | REQ-1.0 |
| REQ-1.3 | Moteur Local | HAUTE | REQ-1.0 |
| REQ-1.4 | Moteur Local | MOYENNE | REQ-1.1 |
| REQ-2.0 | Proxy Hybride | HAUTE | REQ-000 |
| REQ-2.1.1 | Proxy — Serveur | CRITIQUE | REQ-2.0 |
| REQ-2.1.2 | Proxy — Serveur | CRITIQUE | REQ-2.1.1 |
| REQ-2.1.3 | Proxy — Serveur | HAUTE | REQ-2.1.1 |
| REQ-2.1.4 | Proxy — Serveur | MOYENNE | REQ-2.1.3 |
| REQ-2.1.5 | Proxy — Serveur | MOYENNE | REQ-2.1.3 |
| REQ-2.2.1 | Proxy — Uplink | CRITIQUE | REQ-2.1.3 |
| REQ-2.2.2 | Proxy — Uplink | HAUTE | REQ-2.2.1 |
| REQ-2.2.3 | Proxy — Uplink | HAUTE | REQ-2.2.1 |
| REQ-2.3.1 | Proxy — Downlink | CRITIQUE | REQ-2.2.1 |
| REQ-2.3.2 | Proxy — Downlink | CRITIQUE | REQ-2.3.1 |
| REQ-2.3.3 | Proxy — Downlink | HAUTE | REQ-2.3.1 |
| REQ-2.3.4 | Proxy — Downlink | MOYENNE | REQ-2.3.2 |
| REQ-2.4.1 | Proxy — Réinjection | CRITIQUE | REQ-2.3.2 |
| REQ-2.4.2 | Proxy — Réinjection | CRITIQUE | REQ-2.4.1 |
| REQ-2.4.3 | Proxy — Réinjection | HAUTE | REQ-2.4.1 |
| REQ-3.0 | Agilité | HAUTE | REQ-000 |
| REQ-3.1 | Agilité — Personas | HAUTE | REQ-3.0 |
| REQ-3.2 | Agilité — RBAC | HAUTE | REQ-3.1 |
| REQ-3.3 | Agilité — Isolation | MOYENNE | REQ-3.2 |
| REQ-4.0 | Mémoire | HAUTE | REQ-000 |
| REQ-4.1 | Mémoire — Stockage | CRITIQUE | REQ-4.0 |
| REQ-4.2 | Mémoire — Lecture | CRITIQUE | REQ-4.1 |
| REQ-4.3 | Mémoire — Écriture | CRITIQUE | REQ-4.1 |
| REQ-4.4 | Mémoire — Structure | HAUTE | REQ-4.1 |
| REQ-4.5 | Mémoire — Audit | MOYENNE | REQ-4.1 |
| REQ-5.0 | Gemini Config | HAUTE | REQ-2.0 |
| REQ-5.1 | Gemini — Gem | CRITIQUE | REQ-5.0 |
| REQ-5.2 | Gemini — Format | CRITIQUE | REQ-5.1 |
| REQ-5.3 | Gemini — Historique | HAUTE | REQ-5.1 |
| REQ-6.0 | Cloud API Directe | HAUTE | REQ-000 |
| REQ-6.1 | Cloud — Clé API Anthropic | CRITIQUE | REQ-6.0 |
| REQ-6.2 | Cloud — Modèle Claude Sonnet | CRITIQUE | REQ-6.0 |
| REQ-6.3 | Cloud — Compatibilité Native Roo | CRITIQUE | REQ-6.0 |
| REQ-6.4 | Cloud — Sécurité Clé API | HAUTE | REQ-6.1 |

---

### 3.6 Domaine 6 — Mode Cloud Direct via API Anthropic (REQ-6.x)

#### REQ-6.0 — Connexion Directe à l'API Anthropic Claude
Le système doit permettre à Roo Code de se connecter directement à l'API officielle Anthropic pour utiliser Claude Sonnet 3.5 comme backend LLM, sans proxy intermédiaire ni intervention humaine, offrant ainsi une expérience agentique entièrement automatisée avec un modèle cloud de haute qualité.

| ID | Exigence | Description Détaillée et Critères d'Acceptation |
| :--- | :--- | :--- |
| **REQ-6.1** | **Clé API Anthropic** | L'utilisateur doit disposer d'une clé API Anthropic valide (`sk-ant-...`). *Critère :* La clé doit être stockée de manière sécurisée dans les paramètres de Roo Code (non versionnée dans Git, non exposée dans les fichiers du projet). |
| **REQ-6.2** | **Modèle Claude Sonnet 3.5** | Roo Code doit être configuré pour utiliser le modèle `claude-sonnet-4-5` (ou la version stable la plus récente de la gamme Sonnet). *Critère :* Le modèle doit répondre aux requêtes de Roo Code avec les balises XML attendues, sans configuration supplémentaire du format de réponse. |
| **REQ-6.3** | **Compatibilité Native Roo Code** | La connexion à l'API Anthropic doit utiliser le fournisseur natif Roo Code, sans aucun proxy ou middleware. *Critère :* Roo Code doit se connecter directement à `https://api.anthropic.com` via le fournisseur "Anthropic" intégré, garantissant la compatibilité totale avec les fonctionnalités avancées (streaming, vision, tool use natif). |
| **REQ-6.4** | **Sécurité de la Clé API** | La clé API Anthropic ne doit jamais être exposée dans les fichiers du projet. *Critère :* La clé doit être stockée exclusivement dans les paramètres chiffrés de l'extension Roo Code (stockage VS Code SecretStorage), jamais dans `.env`, `.clinerules`, `.roomodes` ou tout autre fichier versionné. |

---

### 3.7 Domaine 7 — Registre Central des Prompts Systeme (REQ-7.x)

#### REQ-7.0 — Registre Centralise des System Prompts
Le systeme doit maintenir un repertoire `prompts/` contenant une version canonique et a jour de chaque system prompt utilise dans UADF, avec identification precise de sa cible de deploiement, afin de garantir la coherence permanente entre le code, les scripts et les comportements des agents LLM.

| ID | Exigence | Description Detaillee et Criteres d'Acceptation |
| :--- | :--- | :--- |
| **REQ-7.1** | **Fichier canonique par prompt** | Chaque system prompt doit avoir un fichier canonique unique dans `prompts/` (format `SP-XXX-nom.md`) avec un en-tete YAML identifiant : ID, version, cible de deploiement exacte (fichier + champ), et dependances. *Critere :* 7 fichiers SP-001 a SP-007 presents dans `prompts/`, chacun avec un en-tete YAML valide. |
| **REQ-7.2** | **Identification de la cible de deploiement** | Chaque fichier SP doit specifier sans ambiguite ou deployer le prompt : fichier cible, champ exact, et procedure de deploiement. *Critere :* Les champs `target_file`, `target_field` et `target_location` sont renseignes dans chaque SP. Les prompts externes (Gem Gemini) sont marques `hors_git: true` avec procedure manuelle documentee. |
| **REQ-7.3** | **Coherence obligatoire avant commit** | Toute modification d'un artefact impactant un prompt (proxy.py, .roomodes, .clinerules, Modelfile) doit declencher une verification et mise a jour du fichier SP correspondant dans `prompts/`. *Critere :* REGLE 6 dans `.clinerules` impose cette verification. Le commit doit inclure les fichiers `prompts/` modifies. |
| **REQ-7.4** | **Versionnement des prompts** | Chaque fichier SP doit maintenir un changelog avec numero de version semantique (MAJOR.MINOR.PATCH) et description des modifications. *Critere :* Champ `changelog` present dans chaque SP avec au moins une entree. La version est incrementee a chaque modification. |
| **REQ-7.5** | **Deploiement manuel documente pour SP-007** | Le Gem Gemini (SP-007) etant externe a Git, sa procedure de deploiement manuel doit etre documentee et tout commit modifiant SP-007 doit inclure la mention "DEPLOIEMENT MANUEL REQUIS". *Critere :* SP-007 marque `hors_git: true`, procedure de deploiement dans le fichier, REGLE 6.2 dans `.clinerules` impose la mention dans le message de commit. |

---

### Matrice de Tracabilite — Domaine 7

| ID | Domaine | Priorite | Depend de |
| :--- | :--- | :--- | :--- |
| REQ-7.0 | Registre Prompts | HAUTE | REQ-000 |
| REQ-7.1 | Registre Prompts — Fichiers canoniques | HAUTE | REQ-7.0 |
| REQ-7.2 | Registre Prompts — Cibles | CRITIQUE | REQ-7.1 |
| REQ-7.3 | Registre Prompts — Coherence | CRITIQUE | REQ-7.1, REQ-5.x |
| REQ-7.4 | Registre Prompts — Versionnement | HAUTE | REQ-7.1 |
| REQ-7.5 | Registre Prompts — Deploiement manuel SP-007 | HAUTE | REQ-7.2, REQ-5.x |

---

### 3.8 Domaine 8 — Verification Automatique de Coherence des Prompts (REQ-8.x)

#### REQ-8.0 — Detection Automatique de Desynchronisation Prompt/Artefact
Le systeme doit fournir un mecanisme automatique de detection des desynchronisations entre les fichiers SP canoniques du registre `prompts/` et leurs artefacts cibles deployes (.clinerules, .roomodes, Modelfile), afin de garantir que le registre reste la source de verite effective et non seulement theorique.

| ID | Exigence | Description Detaillee et Criteres d'Acceptation |
| :--- | :--- | :--- |
| **REQ-8.1** | **Script de verification de coherence** | Un script `scripts/check-prompts-sync.ps1` doit comparer le contenu de chaque fichier SP canonique avec son artefact cible deploye et produire un rapport PASS/FAIL. *Critere :* Le script compare SP-001 vs Modelfile, SP-002 vs .clinerules, SP-003 a SP-006 vs .roomodes. Il affiche les differences si desynchronisation detectee. |
| **REQ-8.2** | **Hook Git pre-commit** | Un hook Git `.git/hooks/pre-commit` doit appeler automatiquement le script de verification avant chaque commit et bloquer le commit si une desynchronisation est detectee. *Critere :* Un commit avec artefact modifie mais SP non mis a jour est bloque avec un message explicatif indiquant quel SP est desynchronise. |
| **REQ-8.3** | **Rapport de verification lisible** | Le script de verification doit produire un rapport clair avec : statut par SP (SYNC / DESYNC), nom du fichier SP, nom de l'artefact cible, et extrait du diff si desynchronise. *Critere :* Un utilisateur peut identifier en moins de 10 secondes quel prompt est desynchronise et quelle est la difference. |
| **REQ-8.4** | **Exclusion SP-007 de la verification automatique** | SP-007 (Gem Gemini, externe Git) doit etre exclu de la verification automatique avec un avertissement rappelant la verification manuelle requise. *Critere :* Le script affiche "SP-007 : VERIFICATION MANUELLE REQUISE (Gem Gemini externe)" sans bloquer le commit. |

---

### Matrice de Tracabilite — Domaine 8

| ID | Domaine | Priorite | Depend de |
| :--- | :--- | :--- | :--- |
| REQ-8.0 | Verification Coherence Prompts | HAUTE | REQ-7.0 |
| REQ-8.1 | Verification — Script PowerShell | HAUTE | REQ-7.1, REQ-7.2 |
| REQ-8.2 | Verification — Hook pre-commit | HAUTE | REQ-8.1 |
| REQ-8.3 | Verification — Rapport lisible | MOYENNE | REQ-8.1 |
| REQ-8.4 | Verification — Exclusion SP-007 | HAUTE | REQ-7.5, REQ-8.1 |

---

## 5. Contraintes et Non-Goals

### Contraintes
- Le système doit fonctionner sur un laptop Windows avec VS Code sans nécessiter de serveur dédié ou d'infrastructure cloud payante (sauf pour le Mode Cloud qui implique des coûts API Anthropic à l'usage).
- Le proxy Gemini Chrome repose sur une intervention humaine minimale (copier-coller) : ce n'est pas un système entièrement automatisé.
- La qualité des réponses en mode Gemini Chrome dépend de la disponibilité et du comportement de l'interface web Gemini (hors contrôle du système).
- Le Mode Cloud (Claude API) implique des coûts à l'usage selon la tarification Anthropic en vigueur.

### Non-Goals
- Ce système ne vise PAS à automatiser entièrement le copier-coller vers Gemini Chrome (pas d'automatisation de navigateur type Selenium).
- Ce système ne vise PAS à gérer des projets multi-utilisateurs ou des environnements distribués.
- Ce système ne vise PAS à supporter des modèles LLM autres qu'Ollama (local), Gemini Chrome (via proxy) et Claude Sonnet via API Anthropic (cloud direct) dans cette version 1.0.

### Tableau Comparatif des 3 Modes LLM

| Critère | Mode Local (Ollama) | Mode Proxy (Gemini Chrome) | Mode Cloud (Claude API) |
| :--- | :--- | :--- | :--- |
| **Coût** | Gratuit | Gratuit | Payant (à l'usage) |
| **Intervention humaine** | Aucune | Copier-coller à chaque requête | Aucune |
| **Qualité du raisonnement** | Haute (32B local) | Très haute (Gemini Pro) | Très haute (Claude Sonnet) |
| **Vitesse** | Dépend du hardware | Dépend de l'humain | Rapide (API directe) |
| **Souveraineté des données** | Totale (100% local) | Partielle (données envoyées à Google) | Partielle (données envoyées à Anthropic) |
| **Disponibilité** | Toujours (hors ligne) | Nécessite Chrome + compte Google | Nécessite Internet + clé API |
| **Configuration Roo Code** | Provider: Ollama | Provider: OpenAI Compatible | Provider: Anthropic |
| **Exigences PRD** | REQ-1.x | REQ-2.x, REQ-5.x | REQ-6.x |
