# Rapport de Cohérence des System Prompts

**Date :** 2026-03-24

**Phase :** 12 — Vérification automatique de cohérence

**Statut :** Généré automatiquement


---n

## Résultats de Vérification


| SP Canonique | Artefact Déployé | Statut | Notes |

| :--- | :--- | :--- | :--- |

| $spFile | $(System.Collections.Hashtable.Target) SYSTEM | ❌ DÉSYNCHRONISÉ | Contenu différent |

| $spFile | $(System.Collections.Hashtable.Target) Full | ❌ DÉSYNCHRONISÉ | Contenu différent |

| $spFile | $(System.Collections.Hashtable.Target) customModes[2].roleDefinition | ⚠️ HORS GIT | Vérification manuelle requise |

| $spFile | $(System.Collections.Hashtable.Target) customModes[1].roleDefinition | ⚠️ HORS GIT | Vérification manuelle requise |

| $spFile | $(System.Collections.Hashtable.Target) N/A | ⚠️ HORS GIT | Vérification manuelle requise |

| $spFile | $(System.Collections.Hashtable.Target) customModes[0].roleDefinition | ⚠️ HORS GIT | Vérification manuelle requise |

| $spFile | $(System.Collections.Hashtable.Target) customModes[3].roleDefinition | ⚠️ HORS GIT | Vérification manuelle requise |


---n

## Statut Global

- **Cohérence :** ❌ DÉSYNCHRONISATIONS DÉTECTÉES

- **Action requise :** Corriger les désynchronisations

