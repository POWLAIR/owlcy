# Owls — les bots spécialisés

## Objectif

Pouvoir créer une nouvelle Owl **sans écrire de code** : un fichier YAML ou un formulaire dans l'app.

## Exemple de définition

```yaml
# owls/veilleuse/owl.yaml
id: veilleuse
name: Veilleuse
role: >
  Tu fais la veille techno de Paul. Tu es concise, tu cites toujours tes sources,
  tu privilégies IA, dev web, Symfony et outils dev.
personality:
  tone: calme, un peu malicieuse
  language: fr
model:
  provider: ollama          # ou anthropic, openai, lmstudio…
  name: qwen3:4b           # provisoire : seul modèle mesuré en W4 (4 Go de VRAM) ; défaut à trancher (Q26)
  agent_model: { provider: anthropic, name: claude-sonnet }   # pour le mode agent
mode: pipeline              # pipeline | agent | hybrid
integrations:               # serveurs MCP autorisés (outils)
  - rss
  - web
  - notion
skills:                     # SKILL.md chargés à la demande
  - veille-techno
pipelines:
  - veille-du-matin
permissions:
  network: allow
  secrets: [notion]
  fs.write: ask
  untrusted_input_then_action: ask
skin: veilleuse-nuit         # voir design/01-systeme-mascottes.md
```

## Fonctionnalités

- **Création** : depuis un template, depuis zéro, ou demandée à la Forgeronne (« crée-moi une Owl qui surveille mes PR GitLab »).
- **Mode agent** : la chouette reçoit une demande libre et choisit parmi ses skills (tool calling).
- **Mode pipeline** : elle déroule une pipeline fixe, prévisible, pas cher.
- **Mode hybride** : pipeline fixe avec des étapes « agent » ponctuelles.
- **Mémoire par Owl** : notes persistantes propres à chaque Owl (préférences apprises, contexte).
- **Délégation** : une Owl peut appeler une autre Owl comme une skill (`owl.call: scribe`).

## Owls livrées de base (proposition MVP)

1. **Owlcy** (la chouette principale) : routeur, répond au chat et oriente vers la bonne Owl.
2. **Veilleuse** : veille (cas d'usage prioritaire).
3. **Forgeronne** : génère skills et pipelines.

## Enseignements de la veille (30/09/2026)

- **Fiabilité des modèles locaux** : sur une carte 8 Go, les modèles 7-8B sont corrects pour *une* action structurée, mais une chaîne d'outils se dégrade vite (95 % par appel ≈ 66 % sur 8 étapes). ➜ Mode `pipeline` par défaut, modèle local pour les étapes étroites, **cloud pour le mode agent**.
- Modèles sur carte 8 Go (mise à jour v4, données concrètes) : les petits modèles **3-4B** spécialisés font aussi bien que les 8B en appels d'outils — Granite 4.0-3B 96 %, Gemma 4 E4B 92 % (seul 8/8 en chaîné), Qwen3-4B-2507 « haut des 80 % » BFCL. Ta carte n'a que 4 Go : W4 n'a mesuré que `qwen3:4b` (juste mais ~1,5 min par appel, NO-GO en chaîné). Rester en Q4_K_M minimum. Voir `techno/01-benchmark-stack.md` §4.
- Ollama expose une API compatible Anthropic → possibilité de faire tourner certains outils prévus pour Claude sur des modèles locaux.
- **Délégation entre Owls** : pattern « agents as tools » (Mastra, OpenAkita). À implémenter simplement : une Owl est exposée aux autres comme un outil `owl.<id>.ask`.
- **Humeur** : NekoAI fait varier l'énergie de son chat selon l'heure, l'inactivité et l'appli active → à reprendre pour les emotes (chouette plus vive la nuit).
- Pour le routage de l'Owl principale : classifieur local léger (les 8B savent bien faire une classification unique) + règles explicites (`drop` d'un PDF → Scribe).

Sources : [PromptQuorum](https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026) · [LocalAIMaster](https://localaimaster.com/blog/best-ollama-models-tool-calling) · [NekoAI](https://github.com/nucket/NekoAI) · [Mastra](https://dev.to/gabrielanhaia/mastra-in-2026-what-it-is-when-to-use-it-and-how-it-compares-2go1)

## Apports du benchmark agents autonomes (01/10/2026)

- **Runtime par Owl** : `runtime: native | hermes | goose | claude-code`, pour déléguer le « cerveau » à un moteur externe. Voir [`architecture/03-integration-hermes.md`](../architecture/03-integration-hermes.md).
- **Format inspiré des Droids Factory** : une Owl simple peut aussi s'écrire en Markdown (frontmatter `name`, `description`, `model`/`inherit`, `tools` par catégories `read-only | edit | execute | web | mcp`) + prompt en corps. Le YAML reste la forme complète.
- **Sous-Owls** : une Owl déléguée tourne dans un contexte neuf, sans poser de question ni déléguer à son tour (règle Factory) → pas de récursion incontrôlée.
- **Mode Plan** (Spec Mode de Factory) : pour une demande complexe, l'Owl produit un plan (critères, étapes, fichiers touchés) → bulle d'approbation → exécution.
- **Apprentissage** : voir [`04-apprentissage-memoire.md`](04-apprentissage-memoire.md).
- Proportionner : une petite tâche = une Owl seule ; plan + sous-Owls seulement quand c'est justifié.

## Questions ouvertes

- Une Owl = un processus isolé, ou toutes dans le même runtime ?
- Comment l'Owl principale route-t-elle ? (classification LLM, règles, ou les deux)
- Limite de coût / tokens par Owl ?
