# Méthodologie de développement

Objectif : **avancer sur un seul sujet à la fois, toujours avec une version qui marche**, et garder la maîtrise de tout ce qui est codé.

## Principes

1. **Rien ne démarre sans preuve.** Tout point technique risqué passe d'abord par un *spike* (Sprint 0) avec un critère go / no-go chiffré.
2. **Un sprint = un objectif.** Chaque sprint a une phrase d'objectif ; ce qui ne sert pas cet objectif attend.
3. **`main` marche toujours.** Chaque PR laisse une application qui se lance. Pas de branche « grand chantier » qui vit 3 semaines.
4. **Tout se trace.** Pas de code sans issue ; pas d'issue sans critères d'acceptation ; pas de décision technique sans ADR.
5. **Un seul vocabulaire** : [`../lexique.md`](../lexique.md).
6. **Le backlog vit dans un fichier** ([`gestion/backlog.yaml`](../../gestion/backlog.yaml)). GitHub est synchronisé depuis ce fichier, pas l'inverse, sauf pour le statut des issues.

## Cadence (sprints de 2 semaines)

| Moment | Durée | Contenu |
|---|---|---|
| **Planning** (lundi J1) | 30 min | Relire l'objectif, vérifier que chaque item est *Ready*, s'engager sur ≤ capacité |
| **Suivi** (chaque session de travail) | 2 min | Déplacer les cartes du board ; noter les blocages (`status:blocked`) |
| **Revue** (vendredi J12) | 30 min | Démo réelle de ce qui marche ; critères d'acceptation cochés un par un |
| **Rétro** (vendredi J12) | 15 min | 1 chose à garder, 1 à changer → notée dans la milestone |
| **Clôture** | 10 min | Items non finis → sprint suivant (jamais « presque fini ») ; mise à jour de la vélocité |

Capacité de départ : **12 points / sprint** (hypothèse pour un rythme d'alternance). À recalculer après le Sprint 1 : moyenne des points réellement livrés.

## Types d'items

| Type | Label | Quand | Livrable |
|---|---|---|---|
| Epic | `type:epic` | Un grand bloc (E0-E14) | Une issue parente avec la liste de ses items |
| User story | `type:us` | Un besoin utilisateur livrable en un sprint | Code + tests + doc |
| Spike | `type:spike` | Une inconnue technique | Résultat chiffré + décision (ADR) |
| Chore | `type:chore` | Outillage, CI, dette | Changement technique |
| Bug | `type:bug` | Anomalie | Correctif + test de non-régression |
| Doc | `type:doc` | Doc seule | Doc à jour |

**Estimation** : points de Fibonacci (1, 2, 3, 5, 8). Au-delà de 8 : on découpe.

## Definition of Ready (DoR)

Un item peut entrer dans un sprint si :
- [ ] l'histoire suit « En tant que…, je veux…, afin de… » ;
- [ ] les critères d'acceptation sont vérifiables (oui / non) ;
- [ ] il est estimé (≤ 8 points) ;
- [ ] ses dépendances sont terminées ou dans le même sprint ;
- [ ] aucun point technique inconnu (sinon : un spike d'abord).

## Definition of Done (DoD)

Un item est *Done* si :
- [ ] tous les critères d'acceptation sont cochés ;
- [ ] le code est mergé dans `main` via une PR, CI verte (Windows) ;
- [ ] les tests couvrent le comportement ajouté (unitaires pour le moteur, test manuel décrit pour l'UI) ;
- [ ] l'application se lance et la démo de l'item fonctionne sur le PC ;
- [ ] la doc concernée est à jour (et le lexique si un terme apparaît) ;
- [ ] aucun secret dans le code, les logs ou les commits.

Pour un **spike**, la DoD devient : résultat chiffré dans [`../techno/03-resultats-tests.md`](../techno/03-resultats-tests.md) + décision go / no-go + ADR si une décision en découle.

## Git

- **Branches** : `type/US-020-perchoir-overlay` (ex. `feat/US-020-…`, `fix/US-061-…`, `spike/US-002-…`, `chore/US-011-…`).
- **Commits** : [Conventional Commits](https://www.conventionalcommits.org/fr/) avec l'id : `feat(shell): perchoir sans vol de focus (US-020)`.
- **PR** : une PR par item (ou sous-partie d'un item de 5-8 pts), liée par `Closes #N`, modèle de PR obligatoire.
- **Merge** : *squash merge* ; `main` protégée (PR + CI verte).
- **Versions** : SemVer ; une release GitHub à la fin des sprints 5, 8, 11, 14 (voir [`03-sprints.md`](03-sprints.md)).

## Décisions (ADR)

Toute décision qui engage l'architecture → `doc/decisions/ADR-xxx-titre.md` (modèle : `ADR-000-template.md`), référencée depuis l'issue qui l'a provoquée. Les questions encore ouvertes restent dans [`../decisions/questions-ouvertes.md`](../decisions/questions-ouvertes.md).

## Garder la maîtrise quand une IA code

Owlcy sera largement co-développé avec des assistants IA. Règles :
- l'IA travaille **sur une issue précise**, dans une branche dédiée ;
- chaque PR est **relue et comprise** avant merge ; si une partie n'est pas comprise, elle n'est pas mergée ;
- `AGENTS.md` / `CLAUDE.md` à la racine renvoient vers le lexique, cette méthodologie et l'architecture ;
- les tests et la CI sont le filet de sécurité, pas la relecture seule.
