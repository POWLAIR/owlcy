# ADR-004 — Moteur de pipelines maison, sur AI SDK 7 et JSONata

- **Date** : 2026-10-01
- **Statut** : proposé
- **Questions liées** : Q13, Q6

## Contexte

Les pipelines YAML d'Owlcy (voir [feature/02](../feature/02-pipelines-factory.md)) enchaînent des étapes `tool`, `llm`, `human`, `when`, `foreach`, `retry` et `validate`, avec des expressions `${…}`. Il faut décider entre écrire ce moteur ou adopter un framework de workflows.

## Options envisagées

1. **Mastra** : workflows avec suspend/resume et MCP intégrés. Mais on ne maîtrise ni le format ni la persistance, et un bug est ouvert sur la reprise d'un workflow porté par un agent (#15734).
2. **Moteur maison** : un interpréteur YAML qui appelle l'AI SDK pour les étapes `llm` et agent, et JSONata pour les expressions. On maîtrise le format de fichier, la reprise et la validation humaine.
3. LangGraph TS : plus lourd, et le seul témoignage disponible le donne 2 fois plus long à mettre en œuvre que Mastra. Écarté.

## Décision

**Option 2.** Les briques testées couvrent les besoins, et ce qui reste à écrire (ordonnancement, persistance par étape) est ce qu'Owlcy doit de toute façon contrôler :

| Brique | Preuve | Source |
|---|---|---|
| Étapes `llm` / agent + validation humaine | AI SDK 7 : boucle d'outils, `needsApproval`, outils MCP | T5 |
| Validation demandée par une intégration | MRTR `input_required` (SDK MCP TS v2) | T7 |
| Expressions `${…}` | JSONata 2.2.2 : 8 cas sur 10 de la doc OK tels quels, **~25 µs** par évaluation | T6 |

## Conséquences

- **Corrections à faire dans la doc de pipelines (T6)** :
  - `$flatten` n'existe pas en JSONata (erreur T1006). Soit le moteur l'enregistre comme fonction maison, soit on écrit `collect.output.*`.
  - Le dédoublonnage `collect.output[link in $not(previous.output.links)]` renvoie `undefined` **sans erreur**. La forme correcte est `collect.output.*[$not(link in $$.previous.output.links)]` (`$$` est nécessaire dans un prédicat).
- **Règle pour le moteur** : une expression qui renvoie `undefined` dans `with:`, `when:`, `until:` ou `validate:` doit faire échouer l'étape de façon explicite, jamais passer en silence.
- La persistance de l'état par étape (Q15) est à notre charge : prévue au Sprint 4.
- **Critère de réexamen** : si à la fin du Sprint 4 (étapes tool, llm et human livrées) l'interpréteur dépasse ~1 000 lignes hors tests, ou si la reprise après redémarrage devient un chantier à elle seule, refaire un spike avec Mastra.
