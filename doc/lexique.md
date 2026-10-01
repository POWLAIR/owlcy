# Lexique Owlcy

**La référence unique du vocabulaire.** Un concept = un mot. Si un terme n'est pas ici, on ne l'utilise pas dans le code, la doc, les issues ni les commits. Pour ajouter ou changer un terme : une PR qui modifie ce fichier (label `doc`).

## Règles

1. **Le code est en anglais**, avec le terme de la colonne « Code » (`Owl`, `Pipeline`, `Step`…).
2. **La doc et les issues sont en français**, avec le terme de la colonne « Terme ».
3. **Le vocabulaire « chouette »** (colonne « Nom affiché ») n'apparaît **que dans l'interface**. Il n'est jamais utilisé dans le code ni dans la doc technique.
4. On n'invente pas de synonyme : on dit « Run », pas « exécution », « job » ni « vol ».

## Concepts principaux

| Terme (doc) | Code | Nom affiché (UI) | Définition | À ne pas confondre avec |
|---|---|---|---|---|
| **Owlcy** | `owlcy` | Owlcy | L'application dans son ensemble | — |
| **Owl** | `Owl` | une chouette | Un bot spécialisé : rôle, modèle LLM, intégrations autorisées, skills, pipelines, permissions, skin | Agent (terme générique hors Owlcy) |
| **Intégration** | `Integration` | — | Un fournisseur d'outils : un serveur MCP (externe) ou un module interne | Outil |
| **Outil** | `Tool` | — | Une action unitaire typée exposée par une intégration (`rss.fetch`, `fs.move`) | Skill, Intégration |
| **Outil interne** | `BuiltinTool` | — | Outil exécuté dans le moteur, sans processus séparé (`owl.say`, `fs.*`, `llm.*`, `http.fetch`) | Intégration MCP |
| **Skill** | `Skill` | savoir-faire | Un savoir-faire au format standard `SKILL.md` (instructions, références, scripts), chargé à la demande | Outil (une skill *explique comment faire*, un outil *fait*) |
| **Pipeline** | `Pipeline` | — | Un enchaînement déterministe d'étapes, décrit en YAML | Workflow, recette |
| **Modèle de pipeline** | `PipelineTemplate` | modèle | Une pipeline paramétrable, instanciable depuis la Factory | — |
| **Factory** | `Factory` | Factory | Le catalogue de modèles de pipelines + l'assistant qui les instancie | Forgeronne |
| **Étape** | `Step` | — | Un nœud de pipeline. Types : `tool`, `llm`, `agent`, `human`, `plan`, `validate`, `pipeline` | Run |
| **Déclencheur** | `Trigger` | — | Ce qui lance une pipeline ou réveille une Owl : `manual`, `schedule`, `hotkey`, `file_watch`, `drop`, `hook`, `idle`, `voice` | Événement |
| **Run** | `Run` | — | Une exécution d'une pipeline ou d'une Owl, tracée dans l'historique | Pipeline (la définition) |
| **Événement** | `Event` | — | Un message sur le bus interne (`run.started`, `step.done`, `permission.requested`…) | Déclencheur |
| **Permission** | `Permission` | — | Le droit d'une Owl sur une capacité (`fs.write`, `network`, `shell`, `secrets:<nom>`…) avec `allow` / `ask` / `deny` | Preset |
| **Preset d'autonomie** | `AutonomyPreset` | niveau d'autonomie | Jeu de permissions prédéfini : `observe`, `low`, `medium`, `high` | — |
| **Demande de validation** | `ApprovalRequest` | — | Une question posée à l'utilisateur avant une action (permission `ask`, étape `human`) | — |
| **Runtime** | `Runtime` | — | Le moteur qui fait « réfléchir » une Owl : `native` (AI SDK), `hermes`, `goose`, `claude-code` | Moteur (le processus Owlcy) |
| **Moteur** | `engine` | — | Le processus TypeScript qui exécute pipelines, runtimes et permissions (sidecar) | Runtime |
| **Shell** | `shell` | — | La partie Rust/Tauri : fenêtres, hotkeys, secrets, supervision du moteur | L'outil `shell.run` |
| **Fonction de plateforme** | `PlatformFeature` | — | Une fonction du shell qui dépend de l'OS (curseur global, fenêtre active, hotkeys, tray…), déclarée disponible ou non au démarrage | Permission (le droit d'une Owl, pas une possibilité de l'OS) |
| **Carnet** | `Notebook` | carnet | La mémoire courte d'une Owl, toujours dans le prompt, **plafonnée** | Archive |
| **Archive** | `Archive` | historique | Tous les runs et conversations, en SQLite FTS5, cherchés à la demande | Carnet |
| **Profil utilisateur** | `UserProfile` | — | `USER.md` : préférences de l'utilisateur, partagées entre Owls | — |
| **Paquet** | `Package` | — | Une archive partageable d'Owls, pipelines, skills, skins, avec permissions déclarées et signature | — |

## Interface & design

| Terme (doc) | Code | Nom affiché (UI) | Définition |
|---|---|---|---|
| **Perchoir** | `Perch` | — | La petite fenêtre overlay, toujours au-dessus, où vivent les chouettes |
| **Bulle** | `Bubble` | — | Le phylactère au-dessus d'une chouette : messages, demandes de validation |
| **Carte** | `Card` | — | Une vue riche d'une intégration (MCP App, iframe sandboxée) |
| **Pill** | `Pill` | — | Un badge compact de statut (ex. « 12 articles ») |
| **Dashboard** | `Dashboard` | Tableau de bord | La fenêtre principale : Owls, pipelines, runs, réglages, éditeurs |
| **Skin** | `Skin` | apparence | Les paramètres visuels d'une chouette (forme, couleurs, motif, accessoires, sons) |
| **Emote** | `Emote` | — | Un état expressif : `idle`, `curious`, `thinking`, `working`, `ask`, `happy`, `dizzy`, `sleepy`, `annoyed` |
| **Pelote** | `ErrorReport` | pelote | Le rapport d'erreur d'un run échoué, que la chouette « recrache » (seul terme ludique conservé dans l'UI pour une erreur) |
| **Mode vivant** | `LiveView` | — | L'affichage animé d'une pipeline pendant un run |
| **Mode nuit** | `NightMode` | mode nuit | Les tâches de consolidation (mémoire, skills) lancées quand le PC est inactif |

## Owls prévues

| Nom | Rôle |
|---|---|
| **Owlcy** | L'Owl principale : répond et oriente vers les autres Owls |
| **Veilleuse** | Veille techno (cas d'usage du MVP) |
| **Scribe** | Écriture, reformulation, dictée |
| **Mécano** | Surveille Claude Code / Cursor / Docker, relaie les validations |
| **Intendante** | Agenda, rappels, tâches |
| **Archiviste** | Rangement et indexation de fichiers |
| **Sentinelle** | Surveillance (sites, prix, déploiements) |
| **Forgeronne** | Crée des intégrations, skills et pipelines à partir d'une description |

## Gestion de projet

| Terme | Définition |
|---|---|
| **Epic** | Un grand bloc fonctionnel (ex. « E2 — Perchoir & chouette »). Une issue GitHub avec le label `epic` |
| **US** (User Story) | Un besoin utilisateur livrable en un sprint, avec critères d'acceptation |
| **Spike** | Une US d'exploration technique dont le livrable est un résultat chiffré et une décision |
| **Sprint** | 2 semaines. Un milestone GitHub `Sprint N — <objectif>` |
| **DoR / DoD** | *Definition of Ready* / *Definition of Done* (voir [`gestion/00-methodologie.md`](gestion/00-methodologie.md)) |
| **ADR** | *Architecture Decision Record* : une décision technique écrite (`decisions/ADR-xxx`) |
| **Go / no-go** | La décision prise à la fin d'un spike |

## Termes abandonnés (ne plus utiliser)

| Ancien terme | Remplacé par | Pourquoi |
|---|---|---|
| Nid | Owlcy / Dashboard | Doublon |
| Vol | Run | Doublon ludique inutile |
| Plume | Paquet | Doublon |
| Nichoir | Intégration | Doublon |
| Skill (au sens d'action atomique, v1 de la doc) | Outil | Conflit avec le standard `SKILL.md` |
| Exécution, job | Run | Un seul mot |
