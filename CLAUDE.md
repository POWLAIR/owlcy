# Owlcy

Assistant personnel autonome pour Windows (une chouette sur le bureau). Statut : conception terminée, **Sprint 0 (Labo)** : tests techniques avant tout développement.

## À lire avant toute modification

1. [`doc/lexique.md`](doc/lexique.md) : **la référence unique du vocabulaire**. Un concept = un mot. Si un terme n'y est pas, on ne l'utilise pas. Pas de synonyme (on dit « Run », pas « exécution » ni « vol »).
2. [`doc/README.md`](doc/README.md) : plan de la doc et conventions.

## Règles

- **Langues** : code en anglais (colonne « Code » du lexique), doc et issues en français. Le vocabulaire « chouette » n'apparaît que dans l'interface.
- **Rien sans preuve** : tout chiffre porte sa source et son niveau de preuve (🟢 mesuré ici · 🔵 mesuré ailleurs · 🟡 déclaratif · ⚪ à mesurer). Les résultats des tests sont dans [`doc/techno/03-resultats-tests.md`](doc/techno/03-resultats-tests.md), et le code des tests dans `poc/`.
- **Décisions** : une décision prise va dans un ADR (`doc/decisions/`). Une question ouverte va dans `doc/decisions/questions-ouvertes.md`. Une idée non validée va dans `doc/idee/02-boite-a-idees.md`, pas dans le périmètre.
- **Périmètre du MVP** : « la Veilleuse publie ma veille ». Le reste attend.
- **Backlog** : la source de vérité est `gestion/backlog.yaml`. Les fichiers `doc/gestion/02-backlog.md` et `03-sprints.md` sont **générés** (`python scripts/github_bootstrap.py docs`) : ne pas les éditer à la main.
- **Cohérence** : après une décision (version de lib, chiffre, choix d'architecture), mettre à jour tous les fichiers qui la citent, pas seulement l'ADR.

## Vérification dans le navigateur (IronBee DevTools)

Dès qu'une interface web tourne, toute interaction navigateur passe **uniquement** par le serveur MCP `ironbee-dt-browser` (déclaré dans `.mcp.json`), et jamais par un autre MCP navigateur (`playwright` compris). Les plateformes Node et Backend d'IronBee sont désactivées.

Pour vérifier un changement d'UI : ouvrir la page (`navigation_go-to`), utiliser vraiment la fonctionnalité, confirmer par un snapshot ARIA ou une capture, puis consulter `o11y_get-console-messages`. Préférer un script `execute` dès que le parcours dépasse 2 ou 3 appels. Les changements qui ne touchent que la doc n'ont pas besoin de vérification.
