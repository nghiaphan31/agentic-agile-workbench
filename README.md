# agentic-agile-workbench

> **L'établi de développement agentique et agile** — un template versionné pour développer des projets logiciels avec des agents IA (Roo Code) et une méthode Agile (Scrum).

**Version courante :** `2.0.0` (voir [CHANGELOG.md](CHANGELOG.md))

---

## Ce que c'est

Cet établi (`workbench`) est un **template réutilisable**, pas un projet applicatif. Il contient :

- Les **personas Agile** (Product Owner, Scrum Master, Developer, QA Engineer) configurés pour Roo Code
- Les **règles impératives** (Memory Bank, Git, cohérence des prompts) injectées à chaque session
- Le **proxy Gemini Chrome** pour utiliser Gemini gratuitement depuis Roo Code
- Les **system prompts canoniques** versionnés pour tous les composants
- Les **scripts utilitaires** dont le script de déploiement vers un projet applicatif

Il est conçu pour être déployé sur n'importe quel projet — nouveau ou existant — en copiant le contenu de `template/` dans le dépôt du projet.

---

## Structure

```
agentic-agile-workbench/
│
├── VERSION                        ← Version courante de l'établi (SemVer)
├── CHANGELOG.md                   ← Historique des versions
├── README.md                      ← Ce fichier
│
├── workbench/                     ← Documentation de l'établi (ne va PAS dans les projets)
│   ├── DOC1-PRD-Unified-Agentic-Framework.md
│   ├── DOC2-Architecture-Solution-Stack.md
│   ├── DOC3-Plan-Implementation-COMPLETE.md
│   └── DOC4-Guide-Deploiement-Atelier.md
│
└── template/                      ← Fichiers à copier dans les projets applicatifs
    ├── .roomodes                  ← 4 personas Agile RBAC
    ├── .clinerules                ← 6 règles impératives (Memory Bank, Git, Prompts)
    ├── .workbench-version         ← Version de l'établi utilisée dans le projet
    ├── Modelfile                  ← Modèle Ollama uadf-agent (T=0.15, ctx=131072)
    ├── proxy.py                   ← Proxy Gemini Chrome v2.0 (FastAPI + SSE)
    ├── requirements.txt           ← Dépendances Python du proxy
    ├── prompts/                   ← Registre SP canoniques (SP-001 à SP-007)
    └── scripts/
        ├── start-proxy.ps1        ← Démarrage du proxy Gemini Chrome
        ├── check-prompts-sync.ps1 ← Vérification cohérence prompts
        └── deploy-to-project.ps1  ← Déploiement de l'établi vers un projet
```

---

## Déploiement Rapide

### Nouveau projet

```powershell
# 1. Créer le projet
git init C:\Projets\mon-projet
cd C:\Projets\mon-projet

# 2. Déployer l'établi
$Workbench = "C:\chemin\vers\agentic-agile-workbench"
& "$Workbench\template\scripts\deploy-to-project.ps1" -ProjectPath "C:\Projets\mon-projet"

# 3. Remplir la vision du projet
# Ouvrir memory-bank/projectBrief.md et décrire le projet

# 4. Ouvrir dans VS Code
code C:\Projets\mon-projet
```

### Projet existant (code legacy)

```powershell
# 1. Commiter l'état initial
cd C:\Projets\mon-projet-legacy
git add . && git commit -m "chore(init): état initial avant intégration établi agentique"

# 2. Déployer l'établi
$Workbench = "C:\chemin\vers\agentic-agile-workbench"
& "$Workbench\template\scripts\deploy-to-project.ps1" -ProjectPath "C:\Projets\mon-projet-legacy"

# 3. Audit du code existant (dans Roo Code, mode Developer)
# "Analyse le code source et documente l'architecture dans memory-bank/systemPatterns.md"
```

---

## Les 3 Modes LLM

| Mode | Provider Roo Code | Coût | Automatique |
| :--- | :--- | :--- | :--- |
| **1 — Ollama local** | Ollama / `uadf-agent` | Gratuit | ✅ Oui |
| **2 — Proxy Gemini** | OpenAI Compatible / `gemini-manual` | Gratuit | ❌ Copier-coller |
| **3 — Claude API** | Anthropic / `claude-sonnet-4-6` | Payant | ✅ Oui |

---

## Documentation Complète

| Document | Contenu |
| :--- | :--- |
| [`workbench/DOC1-PRD-Unified-Agentic-Framework.md`](workbench/DOC1-PRD-Unified-Agentic-Framework.md) | Exigences fonctionnelles et non-fonctionnelles |
| [`workbench/DOC2-Architecture-Solution-Stack.md`](workbench/DOC2-Architecture-Solution-Stack.md) | Architecture technique, décisions, matrice de traçabilité |
| [`workbench/DOC3-Plan-Implementation-COMPLETE.md`](workbench/DOC3-Plan-Implementation-COMPLETE.md) | Guide d'installation pas à pas (phases 0-12) |
| [`workbench/DOC4-Guide-Deploiement-Atelier.md`](workbench/DOC4-Guide-Deploiement-Atelier.md) | Comment déployer l'établi sur un projet |

---

## Versionnement de l'Établi

Cet établi suit [SemVer](https://semver.org) :
- **MAJOR** : changement incompatible (ex: nouveau format Memory Bank)
- **MINOR** : nouvelle fonctionnalité (ex: nouveau persona)
- **PATCH** : correction (ex: bug dans `.clinerules`)

Chaque projet applicatif contient un fichier `.workbench-version` indiquant quelle version de l'établi a été déployée. Pour mettre à jour un projet vers une nouvelle version de l'établi, utilisez `deploy-to-project.ps1 -Update`.
