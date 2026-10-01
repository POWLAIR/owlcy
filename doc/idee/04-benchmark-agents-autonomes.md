# Benchmark : agents autonomes & « usines à agents »

Veille du 01/10/2026. Complète [`03-benchmark-concurrents.md`](03-benchmark-concurrents.md) avec la catégorie des **agents autonomes** : ceux qui décomposent, délèguent, apprennent et tournent en tâche de fond.

## Vue d'ensemble

| | **Factory (Droids)** | **Hermes Agent** | **Goose** | **Letta** |
|---|---|---|---|---|
| Éditeur | Factory (factory.com) | Nous Research | Block → fondation AAIF / Linux Foundation | Letta |
| Cible | Dev / entreprise, cycle logiciel complet | Assistant perso qui « grandit avec toi » | Agent local généraliste (code + workflows) | Agents à mémoire persistante |
| Code | Propriétaire (CLI, desktop, web) | **Open source MIT**, Python (+ Node 26 requis) | **Open source Apache 2.0**, cœur Rust, desktop Electron | Open source |
| Popularité | Commercial | ≈96 k ★ en 7 semaines (lancé le 25/02/2026) | Large (≈60 % des employés de Block l'utilisent, selon The Agent Report) | Référence mémoire |
| Windows | Oui | **Natif (tier 1 depuis v0.16)**, WSL2 conseillé en prod | Oui | Oui |
| Prix | 20 / 100 / 200 $/mois, pas de gratuit, BYOK limité | Gratuit, tu paies le LLM | Gratuit | Gratuit / cloud payant |

## Factory — le modèle « usine logicielle »

Concepts clés :
- **Droids personnalisés** : fichiers Markdown (`~/.factory/droids/*.md`) avec frontmatter `name`, `description`, `model` (ou `inherit`), `tools` par **catégories** (`read-only`, `edit`, `execute`, `web`, `mcp`), `mcpServers`. Chacun tourne dans un **contexte neuf**, sans pouvoir poser de question ni lancer de sous-agent.
- **Spec Mode** : phase de recherche obligatoire → critères d'acceptation, design, plan → **pause pour approbation** avant d'agir.
- **Missions** : découpage en jalons, workers parallèles (worktrees git), **validation à chaque jalon**.
- **Droid Exec** : mode headless pour cron/CI, **lecture seule par défaut**, niveaux d'autonomie `--auto low | medium | high`.
- **Skills** (instructions + références + scripts) et **AGENTS.md** pour le contexte du projet.
- Philosophie : « ne pas transformer une tâche de 5 minutes en réunion de comité » → proportionner l'outil à la tâche.

**Pour Owlcy** : c'est la meilleure référence pour la *factory* de pipelines et pour les Owls spécialisées. En revanche, c'est un produit fermé, orienté code, payant avec une facturation opaque (crédits sans prix publié) → **à imiter, pas à intégrer**.

## Hermes Agent — le modèle « agent qui apprend »

- **Boucle d'apprentissage** :
  - **Mémoire de prompt** `MEMORY.md` + `USER.md`, plafonnée à ~3 500 caractères (« un post-it, pas un journal »).
  - **Archive de sessions** en SQLite FTS5 (~10 ms sur plus de 10 000 docs) avec résumé LLM à la demande.
  - **Skills** au standard agentskills.io, **créées automatiquement** après 5+ appels d'outils, une récupération d'erreur, une correction de l'utilisateur ou un workflow non évident ; améliorées par **patch ciblé** plutôt que réécrites.
  - Modèle utilisateur optionnel (Honcho).
  - « Nudges » périodiques : l'agent décide lui-même ce qui mérite d'être gardé.
- **Cron intégré** avec *continuity* (dédoublonnage d'un run à l'autre) et **mode monitor** (pas d'appel LLM si rien n'a changé).
- **Approbations « smart »** : un LLM relecteur indépendant juge les commandes signalées ; les règles *deny* restent prioritaires ; **toute écriture dans les skills, la mémoire ou AGENTS.md exige une approbation** (anti-injection).
- **Sécurité** : serveurs MCP stdio examinés contre l'exfiltration, environnement des sous-processus nettoyé, sous-agents en Docker durci.
- **Intégrable** : API compatible OpenAI (`127.0.0.1:8642`, token Bearer obligatoire), **TUI Gateway JSON-RPC** (sessions, approbations, flux d'événements), **ACP** (IDE), import Python.
- **Limites** relevées par la critique :
  - auto-apprentissage **désactivé par défaut** ;
  - les skills ne se transfèrent pas d'un domaine à l'autre ;
  - l'agent « croit presque toujours avoir bien fait » ;
  - la génération auto peut écraser des personnalisations ;
  - mémoire opaque ;
  - 15-25 % de tokens en plus pour la réflexion ;
  - contexte de 64 k conseillé (impossible en local avec 4 Go de VRAM, cf. W4) ;
  - API instable (v0.x, gros refactoring en septembre 2026).

**Pour Owlcy** : candidat n°1 comme **moteur d'Owl optionnel** (voir [`architecture/03-integration-hermes.md`](../architecture/03-integration-hermes.md)), et source d'inspiration pour la mémoire et l'apprentissage.

## Goose — le modèle « recettes »

- **Recipes** YAML/JSON : `instructions`, `prompt`, `extensions` (serveurs MCP), `parameters` typés (`{{ var }}`), `sub_recipes` (multi-étapes), `retry` avec validation de succès, `settings` (modèle, température).
- Planification cron intégrée, vue *Schedules* dans le desktop.
- **Pour Owlcy** : la recette Goose est très proche de notre *pipeline template* → reprendre ses `parameters` typés et son `retry` avec critère de succès. Nuance : une recette reste pilotée par l'agent (le LLM décide), alors que nos pipelines sont déterministes.

## Letta — le modèle « mémoire »

- Mémoire éditable par l'agent, versionnée (**MemFS adossé à git**).
- **Agents « sleep-time »** (le « rêve ») : des sous-agents relisent les conversations récentes **en tâche de fond** pour consolider la mémoire sans bloquer l'agent principal.
- **Pour Owlcy** : colle parfaitement au **mode nuit** de la chouette → consolidation mémoire et amélioration des skills quand le PC est inactif.

## Synthèse : quoi reprendre

| Idée | Source | Où dans Owlcy |
|---|---|---|
| Owls spécialisées en Markdown, outils par catégories | Factory (Droids) | `feature/01-owls.md` |
| **Mode Plan** : plan → validation → exécution | Factory (Spec Mode) | Étape `plan` des pipelines |
| Jalons validés, workers parallèles | Factory (Missions) | Pipelines `parallel` + étapes `validate` |
| **Niveaux d'autonomie** prédéfinis | Factory (Droid Exec) | Presets de permissions |
| Mémoire courte plafonnée + archive FTS5 | Hermes | `feature/04-apprentissage-memoire.md` |
| **Création de skills à partir de l'expérience**, patchs ciblés | Hermes | La Forgeronne |
| Cron *monitor* (pas de LLM si rien n'a changé) + *continuity* | Hermes | Triggers `schedule` |
| Écritures protégées (skills, mémoire) = approbation | Hermes | `architecture/02-securite.md` |
| Recettes paramétrées + retry avec critère de succès | Goose | Pipelines |
| Consolidation en tâche de fond | Letta (sleep-time) | Mode nuit |

## Ce qui distingue toujours Owlcy

Aucun de ces agents n'a de **mascotte qui reflète l'état réel du travail**, ni de **pipelines déterministes visuelles**. Hermes et Goose sont des « cerveaux » ; Owlcy peut être **le corps, le visage et la chaîne de montage** au-dessus de n'importe lequel d'entre eux.

## Sources

- [Factory](https://factory.com/) · [Droids personnalisés](https://docs.factory.com/harness/subagents) · [Droid Exec](https://docs.factory.ai/droid-exec/overview) · [Guide Missions / Skills / Spec Mode](https://sidbharath.com/blog/factory-ai-guide/) · [Tarifs](https://kunavo.com/guides/factory-droid-pricing)
- [Hermes Agent](https://hermes-agent.nousresearch.com/) · [Docs](https://hermes-agent.nousresearch.com/docs) · [API Server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server) · [Intégration programmatique](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration) · [Référence praticien](https://blakecrosley.com/guides/hermes) · [Boucle mémoire / skills](https://agentswarms.fyi/blog/hermes-self-improving-agents-memory-skills-subagents) · [Review 95.6k ★](https://dev.to/tokenmixai/hermes-agent-review-956k-stars-self-improving-ai-agent-april-2026-11le) · [Analyse critique](https://agentconn.com/blog/nousresearch-hermes-agent-self-improving-framework-review/)
- [Goose — recipes & scheduling](https://deepwiki.com/aaif-goose/goose/4-recipes-and-scheduling) · [Goose docs](https://goose-docs.ai/) · [The Agent Report](https://the-agent-report.com/2026/05/block-goose-ai-agent-recipe-runner-scaled-60-percent/)
- [Letta — sleep-time agents](https://docs.letta.com/guides/agents/architectures/sleeptime/) · [Context repositories](https://www.letta.com/blog/context-repositories/)
