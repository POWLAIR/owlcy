# Boîte à idées

Idées en vrac, non validées. Quand une idée est retenue → elle part dans `feature/` et on la raye ici.

## Owls (bots) possibles

| Owl | Rôle | Exemples de tâches |
|---|---|---|
| **Veilleuse** | Veille techno / info | Agrège flux RSS, GitHub trending, newsletters → digest quotidien |
| **Scribe** | Écriture | Reformule, résume, rédige des mails, dictée vocale (lien avec Handy AI Overlay) |
| **Mécano** | Dev | Observe Claude Code / Cursor, remonte les permissions, lance les tests, surveille Docker |
| **Intendante** | Organisation | Agenda, rappels, tâches Notion, préparation de la journée |
| **Archiviste** | Fichiers | Range les téléchargements, renomme, indexe les docs pour recherche |
| **Sentinelle** | Surveillance | Surveille un site, un prix, un déploiement, un repo |
| **Forgeronne** | Méta | Crée de nouvelles skills / pipelines à partir d'une description |
| *Setup tech* (nom à définir) | Démarrage de projet | À partir d'un sujet, prépare un dossier projet à l'endroit choisi : structure, `.claude/`, `.cursor/`, `.mcp.json`, `AGENTS.md`/`CLAUDE.md`, skills et MCP adaptés, APIs publiques utiles |
| *DB* (nom à définir) | Bibliothèque perso | Gère le catalogue de skills, MCP et pages (Notion ?) : ajouter une skill, une page, retrouver ce qui a déjà servi |
| *Voyage* (nom à définir) | Voyages | Prépare un programme de voyage (étapes, durées, budget) et cherche les prix les plus bas ; surveille les prix et alerte quand ils baissent |
| *Overture* (ancien projet abandonné, nom à confirmer) | Loisirs | À partir des jeux de la bibliothèque Steam, trouve les concerts orchestraux live de leurs musiques, alerte, propose l'ajout au calendrier et la date d'ouverture de la billetterie |

## Owls « Setup tech » et « DB » (idée du 01/10/2026)

**Setup tech** — « prépare-moi un projet sur <sujet> dans <dossier> » :
1. Déclencheur `manual` / `hotkey` / `voice` ; paramètres : sujet, emplacement cible.
2. Étape `plan:` : l'Owl propose la structure, les skills, les MCP et les APIs retenus → validation dans la bulle.
3. Elle pioche dans **ton catalogue** (skills et MCP déjà utilisés ou créés) via l'Owl DB (`owl.<id>.ask`).
4. Elle peut proposer des APIs gratuites issues de [public-apis](https://github.com/public-apis/public-apis) (`http.fetch`, sortie marquée **non fiable**).
5. Écriture du dossier : `fs.write` en `ask`, et `AGENTS.md`/`CLAUDE.md` sont des **fichiers protégés** → approbation obligatoire.
- Cas réel : le dossier `owlcy` lui-même contient des skills GCP identiques dupliquées dans `.claude/skills` et `.cursor/skills`, sans rapport avec le projet. Exactement ce que cette Owl éviterait.

**DB** — gérer ses bases :
- Ajouter / retrouver une skill, un MCP, une page ; tagger « déjà utilisé dans tel projet ».
- Ajout d'une skill = écriture protégée (brouillon + revue), comme pour la Forgeronne.

**À trancher :**
- Source de vérité : fichiers locaux (`%APPDATA%/Owlcy/skills`, `integrations/`, déjà versionnables) **ou** Notion. Piste : fichiers = source, Notion = vue / index, pour éviter deux catalogues qui divergent.
- Recoupements : la Forgeronne crée des skills et intégrations, l'Archiviste range des fichiers, le catalogue MCP graphique (ci-dessous) liste les MCP. DB pourrait être le propriétaire unique de ce catalogue.
- Noms des deux Owls à ajouter au lexique.
- Prérequis : mode agent (cloud, cf. W4), Skills et Notion (S5-S8), Forgeronne (S13).

## Owl « Voyage » (idée du 01/10/2026)

- **Programme** : mode agent + skill `SKILL.md` « organiser un voyage » ; étape `plan:` → itinéraire proposé dans la bulle → publication Notion.
- **Prix au plus bas** : recoupe la **Sentinelle** (surveillance de prix). Pipeline planifiée avec `skip_if_unchanged` (pas d'appel LLM si le prix n'a pas bougé) et `previous.output` pour détecter une baisse → `owl.say` + alerte.
- **Sources de prix** : aucune intégration prévue. Il faut des serveurs MCP vols / hôtels / trains existants, ou les faire générer par la Forgeronne. Contenu web = sortie **non fiable**.
- **Réservation / paiement** : action distante → preset `high` et validation humaine systématique. Pas de données de carte dans Owlcy ; au mieux, ouvrir la page de réservation.
- Modèle : mode agent en cloud (cf. W4) ; la surveillance planifiée peut tourner en local la nuit.
- À trancher : Owl à part ou simple pipeline de la Sentinelle pour la partie prix.

## Owl « Overture » (idée du 01/10/2026, reprise d'un ancien projet)

Pipeline planifiée, typique de la surveillance (proche de la Sentinelle) :

```
schedule (hebdo, skip_if_unchanged)
  → steam : liste des jeux            (intégration à trouver / créer)
  → concerts : recherche par jeu      (intégration ou http.fetch, sortie non fiable)
  → llm : rapprocher jeux ↔ concerts  (étape étroite → modèle local OK, la nuit)
  → nouveaux seulement                (previous.output, dédoublonnage)
  → owl.say : alerte + emote happy
  → human : « Ajouter au calendrier ? » / « Me rappeler l'ouverture de la billetterie ? »
  → calendar : création de l'événement (intégration à trouver)
```

- Briques **déjà prévues** : `schedule`, `skip_if_unchanged`, `previous.output`, étape `llm`, étape `human`, `owl.say`.
- **Manquent** : intégrations Steam, sources de concerts, calendrier (aucune prévue ; MCP existants ou Forgeronne).
- Ajout au calendrier = écriture distante → validation humaine (`ask`).
- Rappel de la billetterie : le plus simple est un 2e événement de calendrier ; un déclencheur créé dynamiquement par un run n'est pas prévu.
- Bon candidat de **modèle de Factory** (« Alertes concerts de mes jeux ») et de **paquet partageable**.

## Pipelines « factory » possibles

- **Veille du matin** : collecter sources → filtrer par centres d'intérêt → résumer → publier dans Notion → notifier.
- **Téléchargement → rangement** : nouveau fichier → détecter type → renommer → déplacer → indexer.
- **Réunion** : transcription → résumé → actions → création de tâches.
- **Montée de version** : lire changelog → lister breaking changes → plan → PR (lien avec les skills Symfony existantes).
- **Nouvelle skill** : description → génération → tests en sandbox → revue humaine → installation.

## Idées d'interaction

- Glisser un fichier sur la chouette = « fais quelque chose avec ça » (elle propose les pipelines compatibles).
- Glisser la chouette sur une fenêtre = ajouter la fenêtre en contexte (repris de Coucou).
- Raccourci clavier global + commande vocale.
- La chouette tourne la tête vers la fenêtre concernée quand elle a besoin de toi.
- Plusieurs Owls actives = plusieurs chouettes sur le perchoir.
- Mode « nuit » : la chouette est plus active la nuit (tâches de fond planifiées pendant que le PC est inutilisé) — cohérent avec l'animal.

## Intégrations

- **Catalogue MCP graphique** (idée du 01/10/2026) : un écran du dashboard où l'on parcourt les serveurs MCP disponibles (nom, description, outils exposés, permissions demandées) et où on en active un en un clic.
  - Simple passe-plat : le catalogue ne fait que générer le `owlcy.yaml` (cas 1 de [`architecture/01-systeme-extension.md`](../architecture/01-systeme-extension.md)) et ouvrir le formulaire des secrets (`secret-ref`) ; aucun nouveau mécanisme dans le moteur.
  - Garde-fous inchangés : écran des permissions avant activation, secrets dans le Credential Manager, démarrage à la demande.
  - Comble le manque pour un nouvel utilisateur : aujourd'hui, ajouter un MCP passe par un fichier YAML ou par la Forgeronne.
  - À trancher : source de la liste (registre MCP officiel, liste maintenue dans le dépôt…) et vérification des serveurs proposés (leçon ClawHub).

## Compagnon mobile (idée du 01/10/2026, non prioritaire)

Pas de portage Android (perchoir Win32, sidecar Windows, MCP stdio, Credential Manager : rien ne se transpose). À la place, **suivre depuis le téléphone ce qui se passe sur le PC** :
- **Niveau 1 (lecture seule)** : runs en cours et historique, alertes (`owl.say`), état de la chouette (emote). Le téléphone n'est qu'un abonné de plus du bus d'événements ; tout s'exécute sur le PC.
- **Niveau 2 (plus tard)** : répondre aux demandes de validation (bulle) à distance → c'est une action, donc authentification forte et journalisation.
- **Contrainte** : la doc impose **aucun port réseau ouvert par défaut** (leçon OpenClaw) et pas de cloud multi-utilisateurs. Il faut donc un canal conçu exprès (connexion sortante vers un relais chiffré, ou réseau privé) : chantier sécurité à part entière.

## Idées communauté (plus tard)

- Partage d'Owls, skills, pipelines et skins sous forme de paquets (un catalogue communautaire).
- Import de workflows n8n comme pipelines.
- Compatibilité avec les skills / plugins Claude existants.

## Idées fun

- Plumes à collectionner à chaque pipeline réussie (récompense cosmétique uniquement, pas un concept technique — cf. lexique).
- Pelotes de réjection = rapports d'erreur (la chouette « recrache » ce qui n'a pas marché). Pédagogique et drôle.
- Accessoires de saison pour les skins.
