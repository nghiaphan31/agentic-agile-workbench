# Changelog — agentic-agile-workbench

Toutes les modifications notables de cet établi sont documentées ici.
Format : [SemVer](https://semver.org) — MAJOR.MINOR.PATCH

## Conventions de Versionnement

- **MAJOR** (v3.0.0) : changement incompatible — ex: nouveau format Memory Bank, restructuration arborescence
- **MINOR** (v2.1.0) : nouvelle fonctionnalité rétrocompatible — ex: nouveau persona, nouveau script
- **PATCH** (v2.0.1) : correction — ex: bug dans `.clinerules`, typo dans un SP

## Comment Mettre à Jour un Projet Applicatif

Quand une nouvelle version de l'établi est publiée :
1. Consulter ce CHANGELOG pour identifier les changements
2. Exécuter `template/scripts/deploy-to-project.ps1 -ProjectPath [chemin] -Update` sur le projet à mettre à jour
3. Vérifier les changements avec `git diff` dans le projet
4. Commiter dans le projet : `chore(workbench): mise à jour établi v[X.Y.Z] — [description]`

---

## [2.0.0] — 2026-03-23

### Ajouté
- `VERSION` et `CHANGELOG.md` à la racine de l'établi
- `README.md` de présentation de l'établi
- Arborescence `workbench/` (documentation) + `template/` (fichiers à déployer)
- `template/scripts/deploy-to-project.ps1` — script de déploiement automatisé
- `template/.workbench-version` — fichier de traçabilité de version dans les projets
- `workbench/DOC4-Guide-Deploiement-Atelier.md` — guide complet de déploiement
- `template/prompts/SP-002-clinerules-global.md` v2.0.0 — séquence VÉRIFIER→CRÉER→LIRE→AGIR
- `template/prompts/SP-004-persona-scrum-master.md` v2.0.0 — Scrum Master pur facilitateur

### Modifié
- `workbench/DOC1-PRD-*.md` → v2.0 : exigences atomiques, 7 arbitrages intégrés
- `workbench/DOC2-Architecture-*.md` → v2.0 : 14 DA, proxy.py v2.0 SSE, matrice traçabilité
- `workbench/DOC3-Plan-Implementation-COMPLETE.md` → v3.0 : phases 0-12 fusionnées (2046 lignes)
- `template/proxy.py` → v2.0 : support SSE (DA-014), streaming transparent pour Roo Code

### Supprimé
- `plans/DOC3-Plan-Implementation-Windows-VSCode.md` — fusionné dans DOC3-COMPLETE
- `plans/DOC3-Plan-Implementation-Windows-VSCode-SUITE.md` — fusionné dans DOC3-COMPLETE
- `plans/DOC-Prompt-Registry-Architecture.md` — contenu intégré dans DOC2 et prompts/README.md

### Renommé
- Dépôt GitHub : `PRE-agentic-agile-dev-framework` → `agentic-agile-workbench`
- `plans/` → `workbench/`
- Fichiers à déployer déplacés dans `template/`

---

## [1.0.0] — 2026-03-23

### Ajouté
- Commit initial — Unified Agentic Development Framework (UADF)
- `plans/` avec DOC1, DOC2, DOC3 (phases 0-10)
- `prompts/` avec SP-001 à SP-007
- `.roomodes` avec 4 personas Agile (Product Owner, Scrum Master, Developer, QA Engineer)
- `.clinerules` avec 6 règles impératives
- `Modelfile` pour `mychen76/qwen3_cline_roocode:32b` (uadf-agent)
