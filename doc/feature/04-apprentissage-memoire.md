# Apprentissage & mémoire

Objectif : qu'une Owl **s'améliore avec l'usage**, sans devenir opaque ni dangereuse. Inspiré de Hermes (boucle d'apprentissage), Letta (consolidation en tâche de fond) et Factory (skills packagées). Détails des sources : [`idee/04-benchmark-agents-autonomes.md`](../idee/04-benchmark-agents-autonomes.md).

## Les 4 couches de mémoire (par Owl)

| Couche | Contenu | Format | Chargement |
|---|---|---|---|
| 1. **Carnet** | L'essentiel durable (préférences, contexte) | `memory/<owl>/CARNET.md`, **plafonné** (~3 500 caractères, comme Hermes) | Toujours dans le prompt |
| 2. **Archive** | Tous les runs et conversations | SQLite **FTS5** (+ vecteurs plus tard) | Recherche à la demande, résultats résumés |
| 3. **Skills** | Savoir-faire procédural | `SKILL.md` (standard) | Divulgation progressive |
| 4. **Profil** | Ce que l'utilisateur aime / refuse | `USER.md` partagé entre Owls | Toujours |

Différence clé avec Hermes : **tout reste lisible et éditable** (Markdown + SQLite consultable dans le dashboard). La critique principale de Hermes est justement une mémoire « automatique mais opaque ».

## La boucle d'apprentissage

```
Run terminé ──▶ Critère déclenché ? ──non──▶ rien
                    │ oui (5+ outils, erreur récupérée,
                    │      correction de l'utilisateur, workflow nouveau)
                    ▼
         La Forgeronne propose :
           • une nouvelle Skill, ou un PATCH ciblé d'une skill existante
           • une ligne pour le Carnet
                    ▼
         Brouillon ──▶ revue dans le dashboard (diff) ──▶ validé / rejeté
```

- **Jamais d'écriture automatique** dans les skills ou la mémoire sans validation (règle Hermes « fichiers protégés ») → protège contre l'injection de prompt.
- **Patchs ciblés** plutôt que réécritures complètes (historique propre, pas d'écrasement des personnalisations).
- **Évaluation objective** quand c'est possible : une skill proposée est rejouée en dry-run sur le run d'origine. On ne se fie pas à l'auto-évaluation du LLM (l'agent « croit presque toujours avoir réussi »).

## Mode nuit (consolidation « sleep-time »)

Trigger `idle` / `schedule` nocturne :
1. Relire les runs du jour.
2. Dédupliquer et condenser le Carnet (rester sous le plafond).
3. Proposer des améliorations de skills → file de revue pour le matin.
4. La chouette le matin : « J'ai appris 2 choses cette nuit, tu veux voir ? »

Coût : la réflexion coûte 15-25 % de tokens en plus chez Hermes → **désactivable par Owl**, modèle local possible pour la condensation.

## Réutiliser plutôt que tout réinventer

- Une Owl en `runtime: hermes` utilise la mémoire de Hermes ; Owlcy n'affiche que ce qu'elle expose.
- Les Owls natives utilisent ce modèle maison, volontairement simple.

## Questions ouvertes

- Carnet par Owl, ou un carnet global + un par Owl ?
- Seuil de déclenchement réglable ?
- Export et suppression de la mémoire (« oublie ça ») dès le MVP ?
