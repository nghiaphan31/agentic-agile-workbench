# Rapport de Cohérence des System Prompts — FINAL
**Date :** 2026-03-24
**Script :** `scripts/check-prompts-sync.ps1` v2 (template corrigé — regex triple-backtick en single-quote)
**Contexte :** Phase 11+12 — SP-001..006 synchronisés avec les artefacts déployés + champ `hors_git` ajouté

## Résultat de l'exécution

```
============================================================
  le workbench - Verification Coherence Prompts
============================================================

[SP-001] Modelfile bloc SYSTEM... PASS
[SP-002] .clinerules (fichier entier)... PASS
[SP-003] .roomodes > product-owner roleDefinition... PASS
[SP-004] .roomodes > scrum-master roleDefinition... PASS
[SP-005] .roomodes > developer roleDefinition... PASS
[SP-006] .roomodes > qa-engineer roleDefinition... PASS

[SP-007] Gem Gemini 'Roo Code Agent'... AVERTISSEMENT (deploiement manuel requis)
  -> Verifier manuellement sur https://gemini.google.com > Gems > 'Roo Code Agent'
  -> Comparer avec : prompts/SP-007-gem-gemini-roo-agent.md

============================================================
  RESUME : 6 PASS | 0 FAIL | 1 WARN
============================================================

SUCCES : Tous les prompts verifiables sont synchronises.
```

## Statut par SP

| SP | Fichier | Artefact cible | Résultat |
|----|---------|----------------|----------|
| SP-001 | `prompts/SP-001-ollama-modelfile-system.md` | `Modelfile` bloc SYSTEM | ✅ PASS |
| SP-002 | `prompts/SP-002-clinerules-global.md` | `.clinerules` (fichier entier) | ✅ PASS |
| SP-003 | `prompts/SP-003-persona-product-owner.md` | `.roomodes` > `product-owner` roleDefinition | ✅ PASS |
| SP-004 | `prompts/SP-004-persona-scrum-master.md` | `.roomodes` > `scrum-master` roleDefinition | ✅ PASS |
| SP-005 | `prompts/SP-005-persona-developer.md` | `.roomodes` > `developer` roleDefinition | ✅ PASS |
| SP-006 | `prompts/SP-006-persona-qa-engineer.md` | `.roomodes` > `qa-engineer` roleDefinition | ✅ PASS |
| SP-007 | `prompts/SP-007-gem-gemini-roo-agent.md` | Gem Gemini (EXTERNE) | ⚠️ WARN (déploiement manuel requis) |

## Actions effectuées dans cette session (Phase 11+12)

### Phase 11 — Synchronisation des SP canoniques
- **SP-001** : Ajout `hors_git: false` dans le front matter YAML (contenu déjà synchronisé)
- **SP-002** : Ajout `hors_git: false` + mise à jour du contenu pour correspondre au `.clinerules` déployé (accents français, titre "le workbench", section Notes ajoutée)
- **SP-003** : Ajout `hors_git: false` + mise à jour du contenu avec accents français (roleDefinition `.roomodes`)
- **SP-004** : Ajout `hors_git: false` + mise à jour du contenu avec accents français (roleDefinition `.roomodes`)
- **SP-005** : Ajout `hors_git: false` + mise à jour du contenu avec accents français (roleDefinition `.roomodes`)
- **SP-006** : Ajout `hors_git: false` + mise à jour du contenu avec accents français (roleDefinition `.roomodes`)
- **SP-007** : Vérifié — `hors_git: true` déjà présent, contenu non modifié

### Phase 12 — Script de vérification et hook pre-commit
- **`scripts/check-prompts-sync.ps1`** : Remplacé par la version template corrigée (v2)
  - Correction : regex triple-backtick changée de double-quote en single-quote (fix bug PowerShell 5.1)
  - Suppression du BOM UTF-8 parasite
- **`scripts/check-prompts-sync-fixed.ps1`** : Supprimé (artefact de développement obsolète)
- **`scripts/check-prompts-sync-final.ps1`** : Supprimé (artefact de développement obsolète)
- **`.git/hooks/pre-commit`** : Créé (hook Git actif, appelle `check-prompts-sync.ps1` avant chaque commit)

## Correction technique du script (bug PowerShell 5.1)

**Problème :** La regex dans `Extract-PromptContent` utilisait des triple-backticks (` ``` `) à l'intérieur d'une chaîne double-quote. En PowerShell, le backtick est le caractère d'échappement — trois backticks consécutifs causent une erreur de parsing.

**Solution :** Remplacement de la double-quote par une single-quote pour la chaîne regex :
```powershell
# Avant (cassé) :
if ($content -match "(?s)```(?:markdown|python|)?\r?\n(.*?)\r?\n```") {

# Après (corrigé) :
if ($content -match '(?s)```(?:markdown|python|)?\r?\n(.*?)\r?\n```') {
```

Les single-quotes en PowerShell ne traitent pas le backtick comme caractère d'échappement.

## Critères de validation Phase 11 ✅

- [x] `prompts/` contient exactement 8 fichiers (README.md + SP-001 à SP-007)
- [x] SP-001 à SP-006 ont `hors_git: false` dans le front matter YAML
- [x] SP-007 a `hors_git: true` dans le front matter YAML
- [x] Chaque SP-001 à SP-006 a un contenu synchronisé avec l'artefact déployé (6 PASS)

## Critères de validation Phase 12 ✅

- [x] `scripts/check-prompts-sync.ps1` v2 opérationnel (exit code 0)
- [x] Hook `.git/hooks/pre-commit` créé et actif
- [x] Artefacts obsolètes supprimés (`check-prompts-sync-fixed.ps1`, `check-prompts-sync-final.ps1`)
