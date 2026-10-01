<!-- Fichier GÉNÉRÉ par scripts/github_bootstrap.py depuis gestion/backlog.yaml — ne pas modifier à la main -->

# Backlog

52 items · 160 points · 15 epics. Source : [`gestion/backlog.yaml`](../../gestion/backlog.yaml). Vocabulaire : [`lexique.md`](../lexique.md).

| Epic | Titre | Items | Points | Sprints |
|---|---|---|---|---|
| E0 | Labo & décisions | 8 | 16 | S0 |
| E1 | Fondations | 5 | 13 | S1, S5 |
| E2 | Perchoir & chouette | 4 | 12 | S2 |
| E3 | Moteur & intégrations | 4 | 12 | S3 |
| E4 | Pipelines | 6 | 16 | S4, S7, S8 |
| E5 | La Veilleuse (MVP) | 4 | 9 | S5 |
| E6 | Sécurité & secrets | 3 | 8 | S5, S6, S8 |
| E7 | Dashboard | 2 | 8 | S6 |
| E8 | Factory & déclencheurs | 2 | 8 | S7 |
| E9 | Mode agent & skills | 2 | 7 | S8 |
| E10 | Mécano | 2 | 6 | S9 |
| E11 | Design avancé | 4 | 19 | S10, S11 |
| E12 | Runtimes externes | 2 | 8 | S12 |
| E13 | Mémoire & Forgeronne | 2 | 10 | S13 |
| E14 | Partage | 2 | 8 | S14 |

## E0 — Labo & décisions

Tests techniques go / no-go et ADR avant tout développement.

### US-001 · Créer le dépôt, le GitHub Project et importer le backlog

`chore` · **1 pts** · P0 · Sprint 0 · devops

> En tant que développeur, je veux un dépôt et un board GitHub prêts, afin de suivre le projet sprint par sprint.

**Critères d'acceptation**

- [ ] Le dépôt POWLAIR/owlcy existe avec la doc (dossier doc/) et le labo (poc/)
- [ ] Labels, milestones (sprints) et issues sont créés par scripts/github_bootstrap.py
- [ ] Le GitHub Project a les champs Status, Priority, Estimate, Epic et 3 vues (Board du sprint, Table backlog, Roadmap)

### US-002 · W1 — Perchoir Tauri sous Windows (overlay, focus, click-through)

`spike` · **5 pts** · P0 · Sprint 0 · shell

> En tant que développeur, je veux prouver qu'une chouette peut vivre au-dessus du bureau Windows sans gêner, afin de valider le cœur de l'expérience.

**Critères d'acceptation**

- [ ] Le spike poc/windows/w1-perchoir-tauri compile et se lance (corrections notées)
- [ ] Les vérifications 1.1 à 1.15 de poc/README.md sont renseignées
- [ ] Critères GO — focus jamais volé, click-through hors chouette, pas de Focus Assist, < 150 Mo privés et < 1 % CPU au repos
- [ ] Décision GO / NO-GO écrite dans doc/techno/03-resultats-tests.md

### US-003 · W2 — Mesurer la mémoire réelle (processus + WebView2)

`spike` · **1 pts** · P0 · Sprint 0 · shell

> En tant que développeur, je veux la RAM réelle de l'overlay, afin de trancher le débat 14 Mo / 317 Mo.

**Critères d'acceptation**

- [ ] mesure-memoire.ps1 exécuté 60 s sur le spike W1 et sur une appli Electron de référence
- [ ] Résultats (privé, working set, nb de processus, CPU) reportés dans 03-resultats-tests.md

### US-004 · W3 — Intégrations WSL via wsl.exe (latence stdio, /mnt/c)

`spike` · **1 pts** · P1 · Sprint 0 · integrations

> En tant que développeur, je veux savoir si une intégration peut tourner dans WSL, afin de réutiliser mes outils Linux.

**Critères d'acceptation**

- [ ] wsl_stdio_bench.py exécuté côté Windows
- [ ] GO si RTT p95 < 5 ms et démarrage à froid < 1,5 s

### US-005 · W4 — Fiabilité des appels d'outils des modèles locaux (RTX 500 Ada, 4 Go de VRAM)

`spike` · **2 pts** · P0 · Sprint 0 · llm

> En tant que développeur, je veux mesurer mes modèles locaux sur nos scénarios, afin de choisir le modèle par défaut des étapes llm.

**Critères d'acceptation**

- [ ] bench_ollama_tools.py exécuté sur au moins 4 modèles (dont un 3-4B et un 8B)
- [ ] Tableau score global, par type (simple, choix, parallèle, chaîné, refus) et tokens/s publié
- [ ] Modèle par défaut choisi (ADR) ; décision « mode agent local ou cloud »

### US-006 · W5 — Secrets dans le Windows Credential Manager

`spike` · **1 pts** · P1 · Sprint 0 · security

> En tant qu'utilisateur, je veux que mes clés API soient dans le coffre de Windows, afin qu'elles ne traînent jamais dans un fichier.

**Critères d'acceptation**

- [ ] test_keyring.py réussi, entrée visible puis supprimée dans le Gestionnaire d'identification

### US-007 · T5-T7 — AI SDK 7 + Ollama + MCP, JSONata, SDK MCP TS v2

`spike` · **3 pts** · P0 · Sprint 0 · engine, llm

> En tant que développeur, je veux valider la chaîne TypeScript du moteur, afin de confirmer le choix sidecar TS.

**Critères d'acceptation**

- [ ] Un script TS appelle un modèle Ollama avec un outil MCP (stdio) via AI SDK 7 et affiche le résultat
- [ ] needsApproval déclenche bien une demande avant exécution
- [ ] 5 expressions JSONata de doc/feature/02 évaluées (dont $count, filtrage, aplatissement)
- [ ] Un serveur MCP TS v2 renvoie inputRequired (MRTR) et le client le gère
- [ ] Binaire Bun compilé pour Windows (--target=bun-windows-x64) démarré sur le PC

### US-008 · Écrire les ADR des décisions bloquantes (Q1, Q2, Q7, Q13)

`chore` · **2 pts** · P0 · Sprint 0 · doc

> En tant que développeur, je veux des décisions écrites et justifiées par les tests, afin de ne plus les rediscuter.

**Critères d'acceptation**

- [ ] ADR-001 moteur TS sidecar vs Rust ; ADR-002 MCP + outils internes ; ADR-003 Windows natif + WSL ; ADR-004 moteur de pipelines maison
- [ ] Chaque ADR cite les résultats de tests qui la justifient

## E1 — Fondations

Dépôt, conventions, CI, squelette shell + moteur, packaging.

### US-010 · Monorepo et conventions de code

`chore` · **2 pts** · P0 · Sprint 1 · devops

> En tant que développeur, je veux une structure de dépôt claire, afin de savoir où va chaque chose.

**Critères d'acceptation**

- [ ] apps/shell (Tauri), apps/engine (TS), packages/ui, packages/schemas, integrations/, examples/
- [ ] Lint + format (Biome ou ESLint/Prettier, rustfmt/clippy), commits conventionnels, .editorconfig
- [ ] AGENTS.md / CLAUDE.md à la racine qui renvoie vers doc/lexique.md

### US-011 · CI GitHub Actions (Windows) — lint, tests, build

`chore` · **3 pts** · P0 · Sprint 1 · devops

> En tant que développeur, je veux que chaque PR soit vérifiée automatiquement sur Windows, afin de ne jamais casser main.

**Critères d'acceptation**

- [ ] Workflow sur windows-latest - lint, tests unitaires moteur, cargo check, build Tauri
- [ ] L'installeur NSIS est publié en artefact sur main
- [ ] Protection de branche - PR obligatoire + CI verte

### US-012 · Le shell lance le moteur et ils se parlent

`us` · **5 pts** · P0 · Sprint 1 · shell, engine

> En tant que développeur, je veux que Tauri démarre le moteur TS compilé et échange des messages avec lui, afin d'avoir le squelette de l'application.

**Critères d'acceptation**

- [ ] Le moteur (binaire Bun) est embarqué comme sidecar et lancé au démarrage
- [ ] Canal JSON-RPC shell <-> moteur (stdio), ping aller-retour affiché dans une fenêtre de debug
- [ ] Si le moteur plante, le shell le relance et le signale (événement engine.restarted)
- [ ] Aucun port réseau ouvert (vérifié avec netstat)

### US-013 · Journalisation unifiée (shell + moteur)

`chore` · **2 pts** · P1 · Sprint 1 · engine, shell

> En tant que développeur, je veux des logs lisibles au même endroit, afin de diagnostiquer vite.

**Critères d'acceptation**

- [ ] Logs JSON dans %APPDATA%/Owlcy/logs, rotation, niveau réglable
- [ ] Aucun secret dans les logs (test)

### US-055 · Release v0.1.0 (installeur + notes)

`chore` · **1 pts** · P0 · Sprint 5 · devops

> En tant qu'utilisateur, je veux installer Owlcy en un clic, afin de l'utiliser au quotidien.

**Critères d'acceptation**

- [ ] Installeur NSIS publié en GitHub Release, notes générées depuis les PR
- [ ] Critère de sortie du MVP vérifié pendant 5 jours ouvrés d'affilée

## E2 — Perchoir & chouette

Overlay Windows, chouette SVG, emotes, bulle, tray.

### US-020 · Voir la chouette sur mon bureau sans qu'elle me gêne

`us` · **5 pts** · P0 · Sprint 2 · shell, ui

> En tant qu'utilisateur, je veux une chouette en bas de l'écran qui ne vole jamais le focus et laisse passer mes clics, afin de l'avoir toujours là sans être dérangé.

**Critères d'acceptation**

- [ ] Reprise du code validé en W1 (fenêtre petite, WS_EX_NOACTIVATE, NonRudeHWND, hit-test)
- [ ] Position réglable (coin, écran) et mémorisée
- [ ] Pas dans Alt+Tab ni la barre des tâches ; icône dans le tray (Quitter, Masquer)

### US-021 · Une chouette vivante (respiration, clignements, regard)

`us` · **3 pts** · P0 · Sprint 2 · design, ui

> En tant qu'utilisateur, je veux une chouette qui respire, cligne des yeux et me suit du regard, afin qu'elle paraisse vivante.

**Critères d'acceptation**

- [ ] Composant React Owl en SVG procédural, paramétré par un skin (couleurs, formes)
- [ ] Yeux qui suivent le curseur sur tout l'écran (position envoyée par le shell)
- [ ] 30 fps en idle, animation coupée quand la chouette est masquée (mesure < 0,5 ms/s en pause)

### US-022 · Des emotes qui reflètent ce qui se passe

`us` · **2 pts** · P1 · Sprint 2 · design, ui

> En tant qu'utilisateur, je veux voir si la chouette réfléchit, travaille, est contente ou en erreur, afin de comprendre l'état sans ouvrir de fenêtre.

**Critères d'acceptation**

- [ ] Emotes idle, thinking, working, ask, happy, dizzy, sleepy
- [ ] Pilotées par des événements (emote.set) — testables depuis la fenêtre de debug

### US-023 · Bulle avec demande de validation

`us` · **2 pts** · P0 · Sprint 2 · ui

> En tant qu'utilisateur, je veux que la chouette me pose une question dans une bulle avec Autoriser / Refuser, afin de garder le contrôle sur ses actions.

**Critères d'acceptation**

- [ ] Événement approval.requested -> bulle ; réponse -> approval.answered
- [ ] La bulle ne vole pas le focus ; fermeture auto configurable ; file d'attente si plusieurs demandes

## E3 — Moteur & intégrations

Configuration, bus d'événements, hôte MCP, outils internes.

### US-030 · Configuration en fichiers YAML validés et rechargés à chaud

`us` · **3 pts** · P0 · Sprint 3 · engine

> En tant qu'utilisateur avancé, je veux décrire Owls, intégrations et pipelines en YAML, afin de tout personnaliser sans coder.

**Critères d'acceptation**

- [ ] Dossier %APPDATA%/Owlcy avec owls/, integrations/, skills/, pipelines/, skins/
- [ ] JSON Schemas publiés dans packages/schemas ; erreur de validation -> pelote avec la ligne fautive
- [ ] Modification d'un fichier -> rechargement sans redémarrer

### US-031 · Bus d'événements moteur -> shell -> UI

`us` · **2 pts** · P0 · Sprint 3 · engine, ui

> En tant que développeur, je veux que tout passe par des événements typés, afin d'ajouter des fonctionnalités sans toucher au cœur.

**Critères d'acceptation**

- [ ] Événements typés (run.*, step.*, approval.*, emote.*, engine.*) partagés entre moteur et UI
- [ ] La chouette s'anime uniquement via ces événements

### US-032 · Hôte MCP (démarrage à la demande, arrêt après inactivité)

`us` · **5 pts** · P0 · Sprint 3 · engine, integrations

> En tant qu'utilisateur, je veux brancher n'importe quel serveur MCP via un owlcy.yaml, afin d'étendre Owlcy sans coder.

**Critères d'acceptation**

- [ ] Intégration déclarée (command, args, env, target windows|wsl) -> outils listés
- [ ] Processus lancé au premier appel, arrêté après N minutes d'inactivité (mesure RAM avant/après)
- [ ] Élicitation MCP relayée en demande de validation (bulle)

### US-033 · Outils internes de base

`us` · **2 pts** · P1 · Sprint 3 · engine

> En tant que développeur, je veux des outils courants intégrés au moteur, afin d'éviter un processus de 50 Mo par petit outil.

**Critères d'acceptation**

- [ ] owl.say, http.fetch, fs.read, fs.write, fs.move disponibles sans processus séparé
- [ ] Même interface (schéma d'entrée/sortie) que les outils MCP

## E4 — Pipelines

Moteur de pipelines YAML, étapes, expressions, runs.

### US-040 · Exécuter une pipeline YAML séquentielle

`us` · **5 pts** · P0 · Sprint 4 · pipelines

> En tant qu'utilisateur, je veux lancer une pipeline décrite en YAML, afin d'automatiser une tâche répétitive.

**Critères d'acceptation**

- [ ] Étapes tool et llm ; foreach ; when ; variables entre étapes en JSONata
- [ ] Événements step.* émis ; la chouette passe en working pendant le run
- [ ] Dry-run disponible (aucun effet de bord)

### US-041 · Étape humaine dans une pipeline

`us` · **2 pts** · P0 · Sprint 4 · pipelines, ui

> En tant qu'utilisateur, je veux qu'une pipeline puisse s'arrêter pour me demander mon avis, afin de valider avant une action.

**Critères d'acceptation**

- [ ] Étape human -> bulle -> reprise ou arrêt selon la réponse
- [ ] Délai d'expiration configurable

### US-042 · Étapes LLM avec Ollama et Claude

`us` · **3 pts** · P0 · Sprint 4 · llm

> En tant qu'utilisateur, je veux choisir le modèle de chaque Owl (local ou cloud), afin d'arbitrer coût, confidentialité et qualité.

**Critères d'acceptation**

- [ ] Provider Ollama et Anthropic via AI SDK ; modèle par défaut = celui choisi en W4
- [ ] Sortie structurée validée par schéma + 1 retry automatique
- [ ] Tokens et durée enregistrés dans le run

### US-043 · Historique des runs en SQLite

`us` · **2 pts** · P1 · Sprint 4 · engine

> En tant qu'utilisateur, je veux garder la trace de chaque run, afin de comprendre ce qui s'est passé.

**Critères d'acceptation**

- [ ] Runs, étapes, entrées/sorties, durées, décisions de permission stockés
- [ ] Commande CLI owlcy runs list / show <id>

### US-072 · skip_if_unchanged et continuity

`us` · **2 pts** · P2 · Sprint 7 · pipelines

> En tant qu'utilisateur, je veux qu'une pipeline planifiée n'appelle pas le LLM si rien n'a changé, afin d'économiser des tokens.

**Critères d'acceptation**

- [ ] Option skip_if_unchanged sur un step
- [ ] Variable previous.output disponible

### US-083 · Étapes plan et validate

`us` · **2 pts** · P2 · Sprint 8 · pipelines

> En tant qu'utilisateur, je veux voir un plan avant exécution et des contrôles entre étapes, afin d'éviter les dérives.

**Critères d'acceptation**

- [ ] Étape plan -> bulle d'approbation du plan
- [ ] Étape validate (assertion JSONata) -> arrêt propre si faux

## E5 — La Veilleuse (MVP)

Première Owl utile de bout en bout.

### US-050 · Intégration RSS

`us` · **2 pts** · P0 · Sprint 5 · integrations

> En tant qu'utilisateur, je veux lister les articles de mes flux, afin d'alimenter ma veille.

**Critères d'acceptation**

- [ ] Outil rss.fetch(url, since_hours) ; sortie marquée non fiable (untrusted-output)
- [ ] Tests sur 3 flux réels (RSS et Atom)

### US-051 · Publication dans Notion

`us` · **2 pts** · P0 · Sprint 5 · integrations, security

> En tant qu'utilisateur, je veux que le digest soit publié dans ma base Notion, afin de le retrouver avec le reste.

**Critères d'acceptation**

- [ ] Serveur MCP Notion officiel branché via owlcy.yaml
- [ ] Token Notion stocké dans le Credential Manager (secret-ref)

### US-052 · Pipeline « Veille du matin » + skill veille-techno

`us` · **3 pts** · P0 · Sprint 5 · pipelines, llm

> En tant qu'utilisateur, je veux un digest de 5 points avec sources chaque matin, afin de rester à jour en 2 minutes.

**Critères d'acceptation**

- [ ] Pipeline collect -> filtre -> digest -> validation -> publication -> owl.say
- [ ] Skill veille-techno (SKILL.md) utilisée pour le digest
- [ ] Changer ses sources et sujets = modifier les params, sans code

### US-053 · Déclencheur planifié

`us` · **2 pts** · P0 · Sprint 5 · engine

> En tant qu'utilisateur, je veux que la veille tourne seule à 8 h en semaine, afin de ne pas y penser.

**Critères d'acceptation**

- [ ] Trigger schedule (cron) ; rattrapage si le PC était éteint (option)
- [ ] Lancement automatique d'Owlcy au démarrage de Windows (option)

## E6 — Sécurité & secrets

Permissions, coffre de secrets, anti-injection, audit.

### US-054 · Permissions par Owl (allow / ask / deny)

`us` · **2 pts** · P0 · Sprint 5 · security

> En tant qu'utilisateur, je veux décider ce que chaque Owl peut faire seule, afin qu'elle n'agisse jamais sans mon accord sur l'important.

**Critères d'acceptation**

- [ ] Le Permission Guard intercepte chaque appel d'outil selon permissions dans owl.yaml
- [ ] ask -> bulle ; deny -> pelote explicite ; décision journalisée dans le run

### US-062 · Réglages et gestion des secrets

`us` · **3 pts** · P1 · Sprint 6 · ui, security

> En tant qu'utilisateur, je veux gérer mes clés et réglages dans une fenêtre, afin de ne pas éditer de fichiers pour ça.

**Critères d'acceptation**

- [ ] Ajout/suppression de secrets (Credential Manager), jamais réaffichés en clair
- [ ] Modèle par défaut, position du perchoir, démarrage auto

### US-082 · Presets d'autonomie et anti-injection

`us` · **3 pts** · P1 · Sprint 8 · security

> En tant qu'utilisateur, je veux choisir un niveau d'autonomie et être protégé contre les contenus piégés, afin de déléguer sans risque.

**Critères d'acceptation**

- [ ] Presets observe/low/medium/high
- [ ] Sortie non fiable suivie d'une action sensible -> validation obligatoire (test avec un RSS piégé)

## E7 — Dashboard

Fenêtre principale : runs, Owls, réglages.

### US-060 · Liste et détail des runs

`us` · **5 pts** · P1 · Sprint 6 · ui

> En tant qu'utilisateur, je veux voir mes runs et le détail de chaque étape, afin de comprendre ce qu'a fait une Owl.

**Critères d'acceptation**

- [ ] Liste filtrable (Owl, pipeline, statut, date)
- [ ] Détail - entrées/sorties par étape, durée, tokens, décisions

### US-061 · Pelote : rapport d'erreur lisible et relance

`us` · **3 pts** · P1 · Sprint 6 · ui, pipelines

> En tant qu'utilisateur, je veux comprendre une erreur et relancer depuis l'étape fautive, afin de ne pas tout refaire.

**Critères d'acceptation**

- [ ] Clic sur la chouette étourdie -> pelote
- [ ] Bouton relancer depuis l'étape N

## E8 — Factory & déclencheurs

Modèles de pipelines, formulaires, nouveaux déclencheurs.

### US-070 · Instancier une pipeline depuis un modèle

`us` · **5 pts** · P1 · Sprint 7 · ui, pipelines

> En tant qu'utilisateur, je veux créer une pipeline à partir d'un modèle et d'un formulaire, afin de ne pas écrire de YAML.

**Critères d'acceptation**

- [ ] Formulaire généré depuis le JSON Schema des params (types string, number, bool, date, file, list, secret-ref)
- [ ] La pipeline créée est un fichier YAML lisible

### US-071 · Déclencheurs hotkey, drop et file_watch

`us` · **3 pts** · P1 · Sprint 7 · shell, engine

> En tant qu'utilisateur, je veux lancer une pipeline par raccourci, en glissant un fichier sur la chouette ou quand un fichier arrive, afin d'aller vite.

**Critères d'acceptation**

- [ ] Raccourci global configurable
- [ ] Glisser-déposer sur la chouette -> choix des pipelines compatibles
- [ ] Surveillance d'un dossier (ex. Téléchargements)

## E9 — Mode agent & skills

ToolLoopAgent, SKILL.md, presets d'autonomie, plan/validate.

### US-080 · Mode agent (ToolLoopAgent) borné aux outils de l'Owl

`us` · **5 pts** · P1 · Sprint 8 · llm, engine

> En tant qu'utilisateur, je veux demander librement quelque chose à une Owl, afin qu'elle choisisse elle-même les outils.

**Critères d'acceptation**

- [ ] Limite d'étapes et de budget tokens
- [ ] needsApproval branché sur le Permission Guard

### US-081 · Chargement des Skills (SKILL.md)

`us` · **2 pts** · P1 · Sprint 8 · llm

> En tant qu'utilisateur, je veux réutiliser mes skills Claude existantes, afin de ne pas les réécrire.

**Critères d'acceptation**

- [ ] Divulgation progressive - frontmatter toujours, corps à la demande
- [ ] Mes skills Symfony fonctionnent telles quelles

## E10 — Mécano

Hooks Claude Code, relais des validations.

### US-090 · Recevoir les hooks Claude Code

`us` · **3 pts** · P2 · Sprint 9 · engine, security

> En tant que développeur, je veux que la chouette voie mes sessions Claude Code, afin de suivre ce qu'elles font.

**Critères d'acceptation**

- [ ] Endpoint 127.0.0.1 + token, installé avec sauvegarde et diff de la config Claude Code
- [ ] Si Owlcy ne répond pas, Claude Code n'est jamais bloqué

### US-091 · Valider les permissions Claude Code depuis la bulle

`us` · **3 pts** · P2 · Sprint 9 · ui

> En tant que développeur, je veux autoriser ou refuser une commande Claude Code depuis la chouette, afin de ne pas basculer de fenêtre.

**Critères d'acceptation**

- [ ] PermissionRequest -> bulle -> allow/deny renvoyé
- [ ] Délai dépassé -> décision laissée à Claude Code

## E11 — Design avancé

Skins, sons, éditeur de pipelines, mode vivant.

### US-100 · Skins paramétriques + éditeur live

`us` · **5 pts** · P2 · Sprint 10 · design, ui

> En tant qu'utilisateur, je veux personnaliser l'apparence de chaque Owl, afin de les reconnaître d'un coup d'œil.

**Critères d'acceptation**

- [ ] skin.yaml (forme, couleurs, motif, accessoires) avec bornes et contrôle de contraste
- [ ] Aperçu live de toutes les emotes

### US-101 · Sons et humeur contextuelle

`us` · **3 pts** · P3 · Sprint 10 · design

> En tant qu'utilisateur, je veux des sons discrets et une chouette dont l'humeur suit l'heure et mon activité, afin qu'elle paraisse vivante.

**Critères d'acceptation**

- [ ] Pack de sons désactivable
- [ ] Humeur - plus vive la nuit, somnolente après inactivité

### US-110 · Éditeur visuel de pipelines (React Flow)

`us` · **8 pts** · P2 · Sprint 11 · ui, pipelines

> En tant qu'utilisateur, je veux voir et modifier une pipeline sous forme de schéma, afin de la comprendre sans lire le YAML.

**Critères d'acceptation**

- [ ] Aller-retour YAML <-> graphe sans perte
- [ ] Nœuds par type d'étape, validation en direct

### US-111 · Mode vivant

`us` · **3 pts** · P3 · Sprint 11 · design, ui

> En tant qu'utilisateur, je veux voir la chouette avancer d'étape en étape pendant un run, afin de suivre l'exécution.

**Critères d'acceptation**

- [ ] Animation pilotée par step.*
- [ ] Erreur -> chute + pelote cliquable

## E12 — Runtimes externes

Adaptateur de runtime, Hermes.

### US-120 · W6 — Spike Owl Hermes (TUI Gateway dans WSL)

`spike` · **3 pts** · P2 · Sprint 12 · engine

> En tant que développeur, je veux tester Hermes comme cerveau d'une Owl, afin de décider de son intégration.

**Critères d'acceptation**

- [ ] Progression et approbations Hermes affichées dans la bulle
- [ ] Mesures - latence, RAM, stabilité sur 1 semaine ; ADR

### US-121 · Interface Runtime + adaptateur Hermes

`us` · **5 pts** · P3 · Sprint 12 · engine

> En tant qu'utilisateur, je veux choisir le runtime de chaque Owl, afin de profiter d'autres agents sans quitter Owlcy.

**Critères d'acceptation**

- [ ] runtime - native | hermes dans owl.yaml
- [ ] Les skills créées par Hermes arrivent en brouillon

## E13 — Mémoire & Forgeronne

Carnet, archive, apprentissage, génération d'intégrations.

### US-130 · Carnet et archive par Owl

`us` · **5 pts** · P2 · Sprint 13 · engine, llm

> En tant qu'utilisateur, je veux qu'une Owl se souvienne de l'essentiel, afin de ne pas tout lui réexpliquer.

**Critères d'acceptation**

- [ ] Carnet Markdown plafonné, éditable dans le dashboard
- [ ] Archive FTS5 cherchable
- [ ] Écriture uniquement via le moteur, après validation

### US-131 · La Forgeronne génère une intégration

`us` · **5 pts** · P3 · Sprint 13 · llm, integrations

> En tant qu'utilisateur, je veux décrire une intégration et la voir générée, afin d'étendre Owlcy en quelques minutes.

**Critères d'acceptation**

- [ ] Cherche d'abord un serveur MCP existant
- [ ] Génère code + owlcy.yaml + test ; dry-run ; diff ; validation humaine

## E14 — Partage

Mode nuit, paquets signés.

### US-140 · Mode nuit : consolidation et propositions de skills

`us` · **3 pts** · P3 · Sprint 14 · llm

> En tant qu'utilisateur, je veux qu'Owlcy apprenne pendant que le PC est inactif, afin de trouver des améliorations le matin.

**Critères d'acceptation**

- [ ] Trigger idle ; condensation du carnet ; propositions en file de revue
- [ ] Désactivable par Owl

### US-141 · Paquets partageables signés

`us` · **5 pts** · P3 · Sprint 14 · security

> En tant qu'utilisateur, je veux installer ou partager des Owls et pipelines en paquet, afin de réutiliser le travail des autres sans risque.

**Critères d'acceptation**

- [ ] package.yaml + signature ; écran de permissions avant installation
- [ ] Scan statique des scripts inclus
