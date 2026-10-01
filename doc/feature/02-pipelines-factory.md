# Pipelines & Factory

## Objectif

Des enchaînements de tâches **préconfigurés, réutilisables et personnalisables**, qu'on peut lire en YAML ou voir comme un schéma animé.

## Exemple

```yaml
# pipelines/veille-du-matin/pipeline.yaml
id: veille-du-matin
name: Veille du matin
owner: veilleuse
template: true                     # utilisable comme modèle dans la factory
params:                            # ce que l'utilisateur personnalise
  sources: { type: list, default: [https://news.ycombinator.com/rss] }
  topics:  { type: list, default: [IA, Symfony, Rust] }
  notion_db: { type: secret-ref }
trigger:
  - schedule: "0 8 * * 1-5"
  - manual: true
steps:
  - id: collect
    foreach: ${params.sources}
    tool: rss.fetch                 # outil MCP
    with: { url: ${item}, since_hours: 24 }
  - id: filter
    llm: classify                   # étape LLM étroite → modèle local suffit
    with: { items: ${collect.output.*}, keep_if: "parle de ${params.topics}" }   # aplatit la liste de listes (pas de $flatten en JSONata, cf. T6)
  - id: digest
    agent: { skills: [veille-techno] }   # utilise le SKILL.md
    with: { items: ${filter.output}, style: "5 points max, liens inclus" }
  - id: review
    human: true                     # étape de validation dans la bulle
    when: ${$count(digest.output) > 0}
  - id: publish
    tool: notion.create_page
    with: { database: ${params.notion_db}, content: ${digest.output} }
  - id: notify
    tool: owl.say
    with: { text: "Ta veille est prête", emote: happy }
on_error:
  emote: dizzy
  report: pelote
theme:
  accent: "#7C6CF2"
  icon: moon
```

## La Factory

La factory, c'est le catalogue de pipelines-modèles + l'assistant qui les instancie.

1. **Choisir un template** (« Veille », « Rangement », « Réunion »…).
2. **Remplir les `params`** via un formulaire généré automatiquement depuis le schéma.
3. **Choisir le déclencheur** et l'Owl propriétaire.
4. **Optionnel** : personnaliser le thème (couleur, icône, variante de chouette).
5. → Une nouvelle pipeline instanciée, versionnée dans le dossier utilisateur.

Trois façons de créer une pipeline :

| Méthode | Pour qui |
|---|---|
| Écrire le YAML | Dev, contrôle total |
| Éditeur visuel (nœuds) | Tout le monde |
| Décrire en langage naturel à la Forgeronne | Rapide, puis relecture |

## Fonctionnalités de moteur

- Variables et expressions `${…}` entre étapes.
- `foreach`, `when` (conditions), `parallel`, `retry`, `timeout`.
- Étape `human` : pause jusqu'à validation/saisie de l'utilisateur.
- Étape `agent` : laisse un LLM décider d'une sous-tâche.
- Sous-pipelines (une pipeline appelle une pipeline).
- Mode **dry-run** : simulation sans effet de bord (important pour les pipelines générées par l'IA).
- Historique des runs, relance d'un run à partir d'une étape.

## Enseignements de la veille (30/09/2026)

| Sujet | Décision proposée | Pourquoi |
|---|---|---|
| Moteur | **Maison** (YAML → DAG) au-dessus d'**AI SDK 7** | Contrôle fin des événements pour animer la chouette ; Mastra en plan B (workflows `.step().parallel()`, `suspend`/`waitForEvent`), mais plus lourd, avec des bugs de reprise signalés |
| Expressions `${…}` | **JSONata** | Standard ouvert (AWS Step Functions, Node-RED), fait requête **et** transformation ; perfs suffisantes pour un usage perso |
| Étape `human` | **MRTR MCP** (`input_required`) + `needsApproval` AI SDK | Standard, rien à inventer |
| Étapes longues | Extension **Tasks** MCP | Progression → animation |
| Étape `agent` | `ToolLoopAgent` (AI SDK 7) limité aux outils et Skills de l'Owl | Borné, traçable |
| Import n8n | **Non.** n8n au mieux comme intégration externe via son API | Licence Sustainable Use (pas libre d'embarquer) + modèle de nœuds différent |
| Sécurité | Une étape qui lit du contenu externe marque sa sortie **non fiable** ; tout outil d'action en aval → validation | Anti-injection de prompt (leçons OpenClaw) |

Note sur `foreach` + LLM : préférer **une** étape LLM sur la liste entière (moins d'appels, moins d'erreurs cumulées) quand le contexte le permet.

Sources : [AI SDK 6](https://vercel.com/blog/ai-sdk-6) · [Mastra vs LangGraph vs AI SDK](https://particula.tech/blog/mastra-vs-langgraph-vs-vercel-ai-sdk-typescript-agents) · [JSONata](https://taskjuice.ai/blog/jsonata-data-transformation-workflows) · [MCP 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) · [Licence n8n](https://www.ssdnodes.com/learn/n8n-sustainable-use-license-explained)

## Apports du benchmark agents autonomes (01/10/2026)

| Idée | Source | Traduction Owlcy |
|---|---|---|
| Paramètres typés (`string`, `boolean`, `number`, `date`, `file`) | Goose recipes | Types des `params` → formulaire factory |
| `retry` avec **critère de succès** | Goose recipes | `retry: { max: 2, until: ${…} }` |
| Sous-recettes | Goose | Sous-pipelines (déjà prévu) |
| **Jalons validés** | Factory Missions | Nouvelle étape `validate:` (assertion JSONata ou Owl relectrice) |
| **Plan → approbation → exécution** | Factory Spec Mode | Nouvelle étape `plan:` suivie d'un `human` |
| Workers parallèles isolés | Factory Missions (worktrees) | `parallel` + dossier de travail isolé par branche |
| **Cron « monitor »** : pas de LLM si l'entrée n'a pas changé | Hermes | `schedule: { cron: …, skip_if_unchanged: collect }` → économie de tokens (utile pour la Sentinelle et la veille) |
| **Continuity** : le run se souvient du précédent (dédoublonnage) | Hermes | Variable `${previous.output}` dans chaque run |
| Niveaux d'autonomie | Droid Exec (`--auto low/medium/high`) | Presets de permissions (voir `architecture/02-securite.md`) |

Exemple :

```yaml
trigger:
  - schedule: { cron: "0 8 * * 1-5", skip_if_unchanged: collect }
steps:
  - id: collect
    tool: rss.fetch
  - id: new_only
    llm: none
    expr: ${collect.output.*[$not(link in $$.previous.output.links)]}   # $$ = racine du contexte (cf. T6)
  - id: digest
    agent: { skills: [veille-techno] }
    retry: { max: 2, until: ${$count(digest.output.points) <= 5} }
  - id: check
    validate: ${$count(digest.output.points) > 0}
```

## Questions ouvertes

- Reprise d'un run après redémarrage du PC : nécessaire dès le MVP ? (persister l'état de chaque étape en SQLite)
- Versionner les pipelines (git auto dans `~/.owlcy` ?)
