# Contexte Actif

**Date de mise à jour :** 2026-03-24
**Mode actif :** code (Claude Sonnet)
**Backend LLM actif :** Claude Sonnet API

## Tâche en cours
**Phase 11+12 terminées** — Synchronisation des SP canoniques + script de vérification v2 opérationnel.

## Dernier résultat
### Phase 11 — SP canoniques synchronisés ✅
- SP-001 à SP-006 : `hors_git: false` ajouté au front matter YAML
- SP-002 à SP-006 : contenu mis à jour pour correspondre aux artefacts déployés (accents français)
- SP-007 : `hors_git: true` vérifié, contenu non modifié

### Phase 12 — Script de vérification v2 ✅
- `scripts/check-prompts-sync.ps1` : version template corrigée (fix regex triple-backtick PS5.1)
- `.git/hooks/pre-commit` : créé et actif
- Artefacts obsolètes supprimés : `check-prompts-sync-fixed.ps1`, `check-prompts-sync-final.ps1`

### Résultat du script
```
RESUME : 6 PASS | 0 FAIL | 1 WARN
SUCCES : Tous les prompts verifiables sont synchronises.
```

## Prochain(s) pas
- [ ] Vérification manuelle SP-007 : synchroniser le Gem Gemini avec `prompts/SP-007-gem-gemini-roo-agent.md`
- [ ] Phase 10 : Configuration API Anthropic Claude (reportée)

## Blocages / Questions ouvertes
- **SP-007** : Déploiement manuel requis sur https://gemini.google.com > Gems > "Roo Code Agent"
- **Backends LLM** : Ollama, Gemini Proxy et Claude API sont mis en pause sauf Claude Sonnet API (mode actif)

## Dernier commit Git
375978f — feat(prompts): Phase 11+12 — SP-001..006 synced with deployed artifacts + hors_git field + check-prompts-sync.ps1 v2 + pre-commit hook
