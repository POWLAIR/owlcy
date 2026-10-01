# Inspiration : Coucou

Source : https://github.com/Louis-CFM/coucou (licence MIT, auteur Louis Raillé).

## Ce que c'est

Une app **macOS** : un petit personnage animé, **Mochi**, vit dans l'encoche (notch) du MacBook et surveille les sessions Claude Code.

- Affiche chaque session pas à pas (fichiers lus, édités, commandes lancées).
- Remonte les demandes de permission avec des boutons d'action directement dans l'encoche.
- Chat intégré avec Claude, glisser-déposer de fichiers, glisser Mochi sur une fenêtre pour l'ajouter en contexte.
- Intégrations (Stripe, GitHub, Vercel, n8n, Resend, Notion, Cal.com) sous forme de petits « pollers ».

## Architecture (ce qu'on en retient)

- **Hooks non bloquants** : un petit script (`nb-hook`) capte les événements Claude Code et les envoie à l'app via un socket Unix. Si l'app ne tourne pas, le hook sort immédiatement → Claude Code n'est jamais bloqué.
- **Intégration = 3 morceaux** : un *poller* (récupère les données), une *pill* (badge compact), une *carte de détail*. Modèle simple et reproductible.
- **Pollers qui se mettent en pause** quand personne ne regarde → zéro CPU au repos.
- **Secrets dans le Keychain**, jamais sur disque. Pas de télémétrie, pas de compte.
- **Zéro dépendance tierce**, Swift 6 + SwiftUI + AppKit.

## Design (ce qui plaît)

- Personnage **procédural** : dessiné en code (Canvas + TimelineView, 60 fps), pas d'images ni de lib d'animation.
- Forme simple : un « squircle » doux avec de grands yeux.
- Vie au repos : respiration, clignements, **yeux qui suivent le curseur**.
- Émotions : content, agacé, étourdi… + ~28 sons faits main.
- **Variations de couleur par intégration** → le personnage change de teinte selon le contexte.
- « Invisible au repos » : caché quand rien ne tourne, pointe le bout du nez au survol.

## Ce qu'on garde / adapte / laisse

| Idée Coucou | Pour Owlcy |
|---|---|
| Mascotte procédurale expressive | **On garde** — mais une chouette originale, et paramétrable (skins) |
| Vit dans l'encoche | **On adapte** — pas d'encoche sur Windows : « perchoir » en bord d'écran / au-dessus de la barre des tâches |
| Hooks non bloquants + socket | **On garde** le principe pour observer des outils externes (Claude Code, Cursor, git…) |
| Intégration = poller + pill + carte | **On généralise** : toute skill peut déclarer une pill et une carte |
| Validation inline des permissions | **On garde** — c'est le cœur du « autonome mais sous contrôle » |
| Zéro dépendance, 100 % natif macOS | **On laisse** — on veut du multi-OS (Windows d'abord) et un écosystème de plugins |
| Focus Claude Code uniquement | **On élargit** — Claude Code devient *une* Owl parmi d'autres |
| Couleur par intégration | **On étend** — thème par Owl et par pipeline |

## Mise à jour après veille (30/09/2026)

- Les hooks Claude Code ont désormais un handler **`http`** : pour Owlcy, plus besoin d'un script intermédiaire comme `nb-hook`, Claude Code peut POSTer directement vers un endpoint local. On garde la règle d'or de Coucou : ne jamais bloquer si l'app ne répond pas.
- Le modèle « poller + pill + carte » se traduit dans les standards : poller = intégration MCP, carte = **MCP App**, pill = champ `ui.pill` de `owlcy.yaml`.
- Coucou est le seul projet du benchmark qui combine mascotte expressive et utilité réelle (voir [`03-benchmark-concurrents.md`](03-benchmark-concurrents.md)).

## À creuser dans le code source

- [ ] Comment est structuré le rendu de Mochi (construction de la forme, système d'états/émotions).
- [ ] Format des événements hook → app.
- [ ] Gestion du dossier `design/` (assets, tokens ?).
- [ ] Le fichier `CLAUDE.md` du repo : bonne pratique pour qu'un agent contribue au projet.
