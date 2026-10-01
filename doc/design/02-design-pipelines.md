# Design des pipelines

## Objectif

Qu'une pipeline soit **aussi agréable à regarder qu'à utiliser**, et reconnaissable au premier coup d'œil, dans la même DA que les chouettes.

## Métaphore visuelle : l'arbre et le vol

- Une pipeline = une **branche** ; chaque étape = un **perchoir** (nœud) sur la branche.
- Pendant un run, la chouette de l'Owl propriétaire **vole de perchoir en perchoir**.
- Étape humaine = la chouette se tourne vers toi et attend.
- Erreur = la chouette tombe du perchoir, étourdie, et laisse une pelote cliquable (le rapport d'erreur).
- Branches parallèles = le tronc se divise ; plusieurs petites chouettes (ou plumes) parcourent chaque branche.

Deux modes d'affichage :

1. **Mode éditeur** : nœuds clairs, lisibles, connexions nettes (style éditeur de graphe classique mais arrondi et doux).
2. **Mode vivant** : la même pipeline en illustration animée pendant l'exécution (vue « branche »).

## Thème d'une pipeline

```yaml
theme:
  accent: "#7C6CF2"      # couleur de la branche et des nœuds
  icon: moon             # icône de la pipeline
  owl_variant: default   # ou un skin spécifique pour cette pipeline
  background: night      # night | dawn | forest | minimal
```

## Nœuds

| Type | Forme / visuel |
|---|---|
| Outil (`tool`) | Nœud rond avec l'icône de l'intégration |
| LLM / agent | Nœud avec aura (plume lumineuse) |
| Condition | Embranchement en Y |
| Boucle | Nœud avec petit compteur |
| Humain | Nœud avec silhouette / bulle |
| Sous-pipeline | Nœud « boîte » (cliquable pour descendre dedans) |
| Déclencheur | Racine / départ de la branche |

États : attente (gris doux) · en cours (pulse accent) · réussi (plein) · erreur (rouge chaud + pelote) · ignoré (pointillés).

## Cartes de la factory

Chaque template = une carte : illustration de la chouette dans une petite scène liée à la tâche (chouette avec journal pour la veille, avec cartons pour le rangement…), titre, 1 phrase, params principaux, bouton « Utiliser ».

## Choix technique (30/09/2026)

- **React Flow (xyflow)** pour le mode éditeur : nœuds 100 % custom en React → nos « perchoirs » stylés. Svelte Flow a atteint la parité en 1.0, mais on reste sur React (voir `techno/01-benchmark-stack.md`). Utilisé en production par des moteurs de workflows (Windmill…).
- **Mode vivant** : même graphe, rendu illustré en SVG ; la chouette (le même composant que sur le perchoir) se déplace le long des arêtes au rythme des événements `step.*`.
- Éditeurs de flux existants (n8n, Node-RED) : efficaces mais austères → ce sont eux qu'on veut dépasser sur l'émotion, pas sur le nombre de nœuds.

Sources : [Svelte Flow 1.0 / xyflow](https://xyflow.com/blog/svelte-flow-release)

## À faire

- [ ] Wireframe de l'éditeur de pipelines.
- [ ] Maquette du mode vivant pour la veille du matin.
- [x] Choisir la lib de graphe → React Flow.
