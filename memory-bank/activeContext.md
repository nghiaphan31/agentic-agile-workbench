# Contexte Actif

**Date de mise à jour :** 2026-03-24
**Mode actif :** developer
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Phase 8 — Configuration du commutateur 3 modes LLM dans Roo Code.

## Dernier résultat
FIX-025 appliqué : proxy.py v2.5.1

**Problème diagnostiqué :** La structure réelle d'un message Roo Code contient un tag `<user_message>` qui encapsule le contexte de conversation précédent, **avant** `<environment_details>`. FIX-024 coupait à `<environment_details>` mais pas à `<user_message>`, donc le contenu de la conversation précédente passait quand même.

**Structure réelle d'un message Roo Code :**
```
Dis moi bonjour en une seule phrase
<user_message>
...contexte conversation precedente...
</user_message>
<environment_details>
...
</environment_details>
====

REMINDERS
...
```

**Correction FIX-025 :** Ajout de `<user_message>` dans `_ROO_INJECTION_START_TAGS`. Le proxy coupe maintenant au premier tag parmi : `<environment_details`, `<user_message>`, `<SYSTEM>`, `<task>`, `<feedback>`.

## Prochain(s) pas
- [ ] Redémarrer le proxy (proxy.py v2.5.1)
- [ ] Tester : envoyer "Dis moi bonjour en une seule phrase." → Gemini doit recevoir `[USER]\nDis moi bonjour en une seule phrase.`
- [ ] Créer profil "ollama_local" dans Roo Code Settings > Providers
- [ ] Créer profil "gemini_proxy" dans Roo Code Settings > Providers
- [ ] Tester Mode 1 Ollama
- [ ] Tester Mode 2 Proxy Gemini
- [ ] Mettre à jour memory-bank/techContext.md avec URLs réelles (étape 8.4)

## Blocages / Questions ouvertes
Aucun blocage actif.

## Dernier commit Git
38659b9 — fix(proxy): v2.5.1 FIX-025 — ajout <user_message> dans _ROO_INJECTION_START_TAGS pour couper avant contexte conversation precedent
