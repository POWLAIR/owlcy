# Vision

## Le pitch

**Owlcy** (owl + Jarvis) est un assistant personnel qui tourne en local sur le PC. Il se présente sous la forme d'une petite chouette animée, discrète quand il n'y a rien à faire et expressive quand elle travaille.

Derrière la mascotte, il y a un **moteur de tâches extensible** :

- des **Owls** : des bots spécialisés, chacun avec son rôle, sa personnalité et son apparence ;
- des **Outils** : des actions unitaires exposées par les intégrations (lire un mail, résumer un PDF, lancer un script, appeler une API) ;
- des **Skills** : des savoir-faire au format standard `SKILL.md`, chargés à la demande (une skill *explique comment faire*, un outil *fait*) ;
- des **Pipelines** : des enchaînements d'étapes préconfigurés, qu'on peut dupliquer et adapter comme dans une « factory ».

## Le problème

Les assistants actuels sont soit :

- **fermés** : on ne peut pas leur ajouter ses propres tâches facilement ;
- **génériques** : un chat où il faut tout réexpliquer à chaque fois ;
- **austères** : des outils d'automatisation puissants (n8n, scripts, cron) sans aucune âme, qu'on oublie d'ouvrir.

## Les principes directeurs

1. **Ajouter une feature doit être trivial.** Un dossier + un fichier manifeste = une nouvelle skill. Pas besoin de toucher au cœur.
2. **Le bot peut s'étendre lui-même.** On décrit une tâche en langage naturel, Owlcy génère la skill ou la pipeline, on relit, on valide.
3. **Tout est configuration.** Owls, pipelines, thèmes, déclencheurs : des fichiers lisibles (YAML), versionnables, partageables.
4. **Le design fait partie du produit.** La mascotte n'est pas un gadget : c'est l'interface de statut, de validation et d'humeur du système.
5. **Local d'abord, privé par défaut.** Pas de télémétrie, secrets dans le coffre de l'OS, modèles locaux possibles.
6. **Autonome mais sous contrôle.** Chaque action sensible passe par un niveau de permission ; la chouette demande avant d'agir.
7. **Invisible au repos.** Zéro CPU quand rien ne tourne (principe repris de Coucou).

## Ce qu'Owlcy n'est pas (pour l'instant)

- Pas un remplaçant de Claude Code / Cursor : il peut les observer ou les piloter, pas les refaire.
- Pas une plateforme cloud multi-utilisateurs.
- Pas un outil no-code grand public en v1 : la cible initiale, c'est un développeur qui veut son propre Jarvis.

## Positionnement (après benchmark du 30/09/2026)

| | Mascotte / âme | Automatisation sérieuse | Desktop natif | Sécurité pensée dès le départ |
|---|---|---|---|---|
| Agents perso (OpenClaw, QwenPaw, OpenAkita) | ✗ | ✓ | ~ | ✗ (incidents début 2026) |
| Desktop pets (NekoAI, OpenPets, Shimeji) | ✓ | ✗ | ✓ | — |
| Coucou | ✓ | ~ (Claude Code seulement, macOS) | ✓ | ✓ |
| **Owlcy** | ✓ | ✓ | ✓ (Windows d'abord) | ✓ |

Détail : [`03-benchmark-concurrents.md`](03-benchmark-concurrents.md).

## Cible

1. **Moi (Paul)** : dev, Windows + WSL2, veut automatiser sa veille, son quotidien pro et perso.
2. **Plus tard** : devs et power-users qui veulent un assistant qu'ils peuvent modeler, et partager leurs Owls / pipelines / skins.

## Vision produit final : le point de vue client

La v1 vise un développeur (voir « Cible »). Le produit final, lui, doit être utilisable par **quelqu'un qui n'ouvrira jamais un fichier YAML**. Les fichiers restent la source de vérité, mais chacun a son écran.

### Règle de conception

**Tout ce qui se fait en YAML doit aussi pouvoir se faire depuis l'interface.** Le YAML reste l'option experte, jamais un passage obligé.

| Besoin du client | Réponse prévue | Statut |
|---|---|---|
| Créer une automatisation | Factory : modèle + formulaire généré | Prévu S7 (v0.2) |
| Voir / modifier une pipeline | Éditeur visuel (React Flow) | Prévu S11 (v0.3) |
| Connecter un service (Notion, GitHub…) | **Catalogue MCP graphique**, activation en un clic | Idée (`02-boite-a-idees.md`) |
| Gérer ses comptes et clés | Écran réglages + secrets | Prévu S6 |
| Réutiliser le travail des autres | Paquets signés ; catalogue communautaire | Paquets S14 (v0.4) ; catalogue : idée |
| Changer l'apparence | Éditeur de skin | Prévu S10 |
| Ajouter une capacité inédite | Forgeronne (description en langage naturel) | Prévu S13 |

### Parcours cible d'un nouvel utilisateur

1. Il installe Owlcy : la chouette apparaît sur le bureau.
2. Il ouvre la Factory et choisit un modèle (« Veille de la semaine », « Récap de ma journée »…).
3. Le modèle indique les services nécessaires ; il les connecte depuis le catalogue (compte + permissions).
4. Il remplit le formulaire (sources, horaires, page Notion) et choisit le déclencheur.
5. La chouette lui annonce le premier run et lui demande validation avant toute action sensible.

### Cas d'usage client à couvrir (testés le 01/10/2026)

| Cas | Faisabilité avec la conception actuelle |
|---|---|
| Synthèse hebdomadaire des infos importantes à partir de flux RSS | ✅ Modèle « Veille » + `schedule` hebdo |
| Owl « Pro » : récap des tâches de la veille dans Notion à partir du suivi du temps, ouverture de liens | 🟡 Briques prévues ; manque une intégration pour l'outil de suivi du temps et un outil d'ouverture de liens |
| Mode « au bureau » qui suit les pages Chrome (tickets ouverts, temps passé) | ❌ Non prévu ; à étudier (vie privée, permissions) |
| Atelier pour connecter facilement des MCP | 🟡 YAML ou Forgeronne aujourd'hui ; catalogue graphique en idée |
| Workflows de la communauté prêts à l'emploi, il suffit de connecter les bons MCP | 🟡 Paquets signés prévus ; catalogue public non planifié |

### Manques identifiés pour la vision client

- Un catalogue MCP graphique (passe-plat vers `owlcy.yaml`).
- Réutiliser la sortie d'une pipeline dans une autre (ex. agréger les veilles quotidiennes en une synthèse hebdo).
- À l'installation d'un paquet : détecter les intégrations manquantes et proposer de les connecter.
- Un catalogue communautaire vérifié (après signature et scan).
- Un premier lancement guidé (onboarding).

## Critères de réussite de la conception

- On peut expliquer en une phrase comment ajouter une skill.
- On peut créer une nouvelle Owl sans écrire de code.
- La chouette donne envie de l'ouvrir.
