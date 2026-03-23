# Contexte Actif

**Date de mise à jour :** 2026-03-23
**Mode actif :** developer
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Phase 8 — Configuration du commutateur 3 modes LLM dans Roo Code.

## Dernier résultat
Phases 0 à 7 complètes. Phase 8 en cours.
- Étape 8.1 : Profil "ollama_local" à créer dans Roo Code (Ollama, http://calypso:11434, uadf-agent)
- Étape 8.2 : Profil "gemini_proxy" à créer dans Roo Code (OpenAI Compatible, http://localhost:8000/v1, gemini-manual)
- FIX-019 appliqué : proxy.py v2.1.1 — force UTF-8 stdout Windows (UnicodeEncodeError cp1252 corrigé)

## Prochain(s) pas
- [ ] Créer profil "ollama_local" dans Roo Code Settings > Providers
- [ ] Créer profil "gemini_proxy" dans Roo Code Settings > Providers
- [ ] Tester Mode 1 Ollama (envoyer message depuis Roo Code, vérifier logs Ollama sur calypso)
- [ ] Tester Mode 2 Proxy Gemini (proxy affiche PROMPT COPIE !)
- [ ] Mettre à jour memory-bank/techContext.md avec URLs réelles (étape 8.4)

## Blocages / Questions ouvertes
Aucun blocage actif.

## Dernier commit Git
193a7b1 — fix(proxy): v2.1.1 FIX-019 — force UTF-8 stdout Windows pour eviter UnicodeEncodeError cp1252
