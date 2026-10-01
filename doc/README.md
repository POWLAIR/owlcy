# Owlcy — Documentation de conception

> Un assistant autonome qui vit sur ton PC, sous la forme d'une chouette.
> Une base où ajouter une nouvelle tâche, un nouveau bot ou une nouvelle pipeline prend quelques minutes, pas une journée.

Statut : **v4 (01/10/2026) — prêt pour le Sprint 0 (Labo)**. Benchmark refait sur données concrètes, 4 tests exécutés, kit de tests Windows prêt, backlog découpé en 15 sprints.

## Commencer ici

1. **[Lexique](lexique.md)** : le vocabulaire commun (obligatoire avant de lire le reste)
2. [Vision](idee/00-vision.md)
3. [Concepts](feature/00-concepts.md)
4. [Architecture](architecture/00-vue-ensemble.md)
5. [Résultats des tests](techno/03-resultats-tests.md) → [Labo](../poc/README.md)
6. [Méthodologie](gestion/00-methodologie.md) → [Plan de sprints](gestion/03-sprints.md) → [Backlog](gestion/02-backlog.md)

## Plan de la doc

| Dossier | Contenu |
|---|---|
| [`lexique.md`](lexique.md) | Vocabulaire de référence |
| [`idee/`](idee/) | Vision, inspiration Coucou, boîte à idées, benchmarks (concurrents, agents autonomes) |
| [`feature/`](feature/) | Concepts, Owls, pipelines & factory, personnalisation, mémoire & apprentissage |
| [`architecture/`](architecture/) | Vue d'ensemble, système d'extension, sécurité, runtimes externes (Hermes) |
| [`design/`](design/) | Direction artistique, skins, design des pipelines |
| [`techno/`](techno/) | Synthèse de la stack, benchmark concret, standards, **résultats des tests**, portabilité macOS / Linux |
| [`gestion/`](gestion/) | Méthodologie, mise en place GitHub, backlog et sprints (générés) |
| [`roadmap/`](roadmap/) | Vue d'ensemble des phases et releases |
| [`decisions/`](decisions/) | ADR et questions ouvertes |

## En bref (stack retenue, sous réserve des tests du Sprint 0)

Tauri 2 (shell Rust) · moteur TypeScript compilé en sidecar · **MCP** pour les intégrations tierces + **outils internes** dans le moteur · **MCP Apps** pour les cartes · **Agent Skills** (`SKILL.md`) · AI SDK 7 · pipelines YAML + JSONata · Ollama pour les étapes `llm:` étroites (W4 : `qwen3:4b` juste mais lent sur 4 Go de VRAM) + modèle cloud pour le mode agent (fournisseur à choisir, Q26) · React + React Flow · chouette en SVG procédural · SQLite · Windows natif.

## Conventions de la doc

- Un fichier = un sujet ; préfixe numérique = ordre de lecture.
- Vocabulaire : uniquement celui du [lexique](lexique.md).
- Chiffres : toujours avec source et niveau de preuve (🟢 mesuré ici · 🔵 mesuré ailleurs · 🟡 déclaratif · ⚪ à mesurer).
- Décision prise → ADR dans `decisions/`. Idée non validée → `idee/02-boite-a-idees.md`.
- `gestion/02-backlog.md` et `03-sprints.md` sont **générés** : on modifie `gestion/backlog.yaml`.
