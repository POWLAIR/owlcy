# Concepts fondamentaux

> **Révision v2 (30/09/2026)** : vocabulaire aligné sur les standards MCP et Agent Skills (voir [`techno/02-standards-agents.md`](../techno/02-standards-agents.md)). Ce qu'on appelait « skill » (action atomique) devient un **Outil**, et « Skill » prend le sens standard (`SKILL.md`).

```
            ┌───────────────┐
 Trigger ──▶│   Pipeline    │──▶ Run (historique, logs, coût)
            │ step → step → │
            └──────┬────────┘
                   │ chaque step appelle
                   ▼
   Owl ─────▶  Outil  (fourni par une Intégration = serveur MCP)
 (persona,      ▲
  skin, LLM,    │ en mode agent, l'Owl choisit ses outils
  Skills)  ◀── Skills (SKILL.md : savoir-faire, procédures)
                   ▲
             Permission Guard (allow / ask / deny, par Owl)
```

## 1. Intégration & Outil — la capacité d'action

- Une **Intégration** = un **serveur MCP** (maison ou existant) qui expose des **Outils** : `rss.fetch`, `notion.create_page`…
- Les **outils internes** (`owl.say`, `fs.*`, `llm.*`, `http.fetch`) tournent **dans le moteur**, sans processus séparé : un serveur MCP coûte ~50 Mo de RAM (test T1).
- Chaque outil a un schéma d'entrée/sortie (JSON Schema), fourni par MCP.
- Une intégration peut exposer des **Cartes** (UI) via **MCP Apps** (`ui://`, iframe sandboxée).
- Un petit fichier `owlcy.yaml` ajoute ce que MCP ne couvre pas : permissions, cible (`windows`/`wsl`), pill, icône.

## 2. Skill — le savoir-faire (standard Agent Skills)

- Un dossier avec `SKILL.md` : « comment faire une bonne veille », « comment migrer Symfony 6 → 7 »…
- Chargé à la demande (divulgation progressive), utilisé par les Owls en mode agent ou par les étapes `agent` d'une pipeline.
- Compatible avec Claude, Cursor et les 40+ outils qui supportent le standard → **tes skills existantes sont réutilisables**.

## 3. Pipeline — l'enchaînement déterministe

Graphe d'étapes (DAG) en YAML, expressions **JSONata**, avec séquence, `foreach`, `when`, `parallel`, étape `human`, étape `agent`.
**Mode par défaut recommandé** : la veille montre qu'enchaîner beaucoup d'appels d'outils via un LLM local est peu fiable (95 % par appel ≈ 66 % sur 8 étapes).

## 4. Owl — le bot spécialisé

Persona = rôle/prompt + modèle LLM + intégrations autorisées + Skills + pipelines + permissions + **skin**.
Modes : `pipeline` · `agent` · `hybrid`.
**Runtime** (v3) : `native` (AI SDK) ou moteur externe (`hermes`, `goose`, `claude-code`) via un adaptateur → [`architecture/03-integration-hermes.md`](../architecture/03-integration-hermes.md).
**Mémoire & apprentissage** : carnet plafonné + archive FTS5 + skills apprises après revue → [`04-apprentissage-memoire.md`](04-apprentissage-memoire.md).

## 5. Trigger — le déclencheur

`manual` · `hotkey` · `schedule` · `file_watch` · `drop` · `hook` (Claude Code, git…) · `voice` · `idle` (PC inactif, cf. mode nuit).
Pas de `webhook` réseau entrant par défaut (sécurité).

## 6. Permission — le garde-fou

Par Owl : `allow` / `ask` / `deny` sur `fs.read`, `fs.write`, `network`, `shell`, `secrets:<nom>`, plus une règle anti-injection `untrusted_input_then_action`. Détail : [`architecture/02-securite.md`](../architecture/02-securite.md).

## 7. Run — l'exécution

Trace de chaque exécution : étapes, entrées/sorties, durée, tokens, décisions de permission, erreurs. C'est la source d'événements de l'animation.

## Vocabulaire

Tous les termes (code, doc, interface) sont définis dans **[`../lexique.md`](../lexique.md)**. Les anciens termes ludiques Nid, Vol, Plume et Nichoir sont abandonnés ; seuls Perchoir, Bulle et Pelote restent dans l'interface.
