# Contexte Actif

**Date de mise à jour :** 2026-03-23
**Mode actif :** developer
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Phase 8 — Configuration du commutateur 3 modes LLM dans Roo Code.

## Dernier résultat
FIX-022 appliqué : proxy.py v2.3.0

**Problème diagnostiqué :** En GEM MODE, le proxy envoyait l'historique complet des messages à Gemini. Gemini continuait alors le contexte de la conversation précédente au lieu de traiter la nouvelle demande indépendamment. Exemple : "Dis bonjour en une phrase." retournait le résumé de la tâche précédente (FIX-020/FIX-021) au lieu de "Bonjour".

**Corrections apportées :**
- **FIX-022** : En GEM MODE, `_format_prompt()` n'envoie plus que le **dernier message [USER]** (pas l'historique complet). Le Gem Gemini a ses propres instructions et chaque conversation est nouvelle — l'historique n'est pas nécessaire et cause une contamination de contexte.
- Le MODE COMPLET (non-GEM) conserve le comportement précédent avec historique complet + troncature.

## Prochain(s) pas
- [ ] Redémarrer le proxy (proxy.py v2.3.0)
- [ ] Tester : envoyer "Dis bonjour en une phrase." → Gemini doit répondre avec `<attempt_completion><result>Bonjour !</result></attempt_completion>`
- [ ] Créer profil "ollama_local" dans Roo Code Settings > Providers
- [ ] Créer profil "gemini_proxy" dans Roo Code Settings > Providers
- [ ] Tester Mode 1 Ollama
- [ ] Tester Mode 2 Proxy Gemini
- [ ] Mettre à jour memory-bank/techContext.md avec URLs réelles (étape 8.4)

## Blocages / Questions ouvertes
Aucun blocage actif.

## Dernier commit Git
[à mettre à jour après commit]
