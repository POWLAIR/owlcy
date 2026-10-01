# Intégration d'agents externes (Hermes & co.)

## Idée

Owlcy n'a pas à réinventer un cerveau d'agent. Une **Owl** peut déléguer sa « réflexion » à un moteur externe, tandis qu'Owlcy garde ce qui fait sa valeur : **la chouette, les pipelines, les permissions, l'historique**.

```yaml
# owls/chercheuse/owl.yaml
id: chercheuse
runtime:
  type: hermes            # native | hermes | goose | claude-code
  transport: tui-gateway  # json-rpc (stdio/ws) — ou api (OpenAI-compatible)
  profile: owlcy         # profil Hermes dédié, isolé du reste
skin: chercheuse-lunettes
permissions:
  shell: ask              # appliqué côté Owlcy ET relayé aux approbations Hermes
```

## Les 3 options étudiées

| Option | Description | + | − |
|---|---|---|---|
| **A. Hermes = cerveau central** | Owlcy n'est plus qu'une UI au-dessus de Hermes | Rapide, profite de la mémoire et de l'apprentissage de Hermes | Dépendance forte à une v0.x (refactoring majeur en sept. 2026), Python + Node 26 obligatoires, perte de contrôle sur les pipelines |
| **B. Adaptateur de runtime par Owl** ✅ | Chaque Owl choisit son moteur ; Hermes en est un parmi d'autres | Découplé, remplaçable, on garde nos pipelines déterministes | Un adaptateur à maintenir par moteur |
| C. Inspiration seulement | On réimplémente mémoire et apprentissage nous-mêmes | Aucune dépendance | Beaucoup de travail |

**Recommandation : B**, et **C pour la mémoire de base** (voir [`feature/04-apprentissage-memoire.md`](../feature/04-apprentissage-memoire.md)), de sorte qu'Owlcy fonctionne aussi sans Hermes.

## Comment brancher Hermes

Hermes propose 3 transports (même cœur `AIAgent`) :

| Transport | Usage pour Owlcy |
|---|---|
| **TUI Gateway JSON-RPC** (stdio / WebSocket) | ✅ **Recommandé** : sessions, **approbations**, flux d'événements fin → la chouette peut s'animer et les demandes d'approbation remontent dans la bulle |
| API compatible OpenAI (`127.0.0.1:8642`, Bearer) | Simple ; SSE avec événements `hermes.tool.progress` ; `/v1/runs` pour les sessions longues. Moins de contrôle sur les approbations. |
| ACP (JSON-RPC stdio) | Pensé pour les IDE ; utile si on veut aussi piloter d'autres agents compatibles ACP |

Correspondance des événements :

| Hermes | Owlcy |
|---|---|
| progression d'outil | `step.progress` → emote `working` |
| demande d'approbation | `permission.requested` → bulle |
| fin de run | `run.done` → emote `happy` |
| erreur | `run.failed` → `dizzy` + pelote |
| skill créée | `skill.proposed` → **revue obligatoire** dans le dashboard |

## Garde-fous spécifiques

- Profil Hermes **dédié** à Owlcy, `API_SERVER_KEY` stockée dans le Credential Manager, jamais de CORS ouvert.
- Hermes a **accès au terminal** : sous Windows, préférer l'exécution en **WSL2** (recommandation Hermes elle-même pour la prod) ou le backend Docker.
- Les skills auto-créées par Hermes arrivent en **brouillon** dans Owlcy ; activation après revue (les critiques relèvent que l'agent surestime ses réussites et que la génération auto peut écraser des personnalisations).
- Version de Hermes **épinglée** (API v0.x instable).
- Contexte de 64 k conseillé par Hermes → avec 4 Go de VRAM (RTX 500 Ada, cf. W4), une Owl Hermes = **modèle cloud** en pratique.

## Autres moteurs possibles (même adaptateur)

| Moteur | Transport | Intérêt |
|---|---|---|
| **Claude Code** | Hooks (`http`) + CLI headless | Owl « Mécano » : surveiller et valider (façon Coucou) |
| **Goose** | CLI / API, recettes YAML | Recettes réutilisables |
| **Factory Droid** | `droid exec --output-format json` / `stream-jsonrpc` | Possible (headless, autonomie réglable), mais payant et fermé → **non prioritaire** |
| **Natif Owlcy** | AI SDK 7 | Par défaut, léger, marche avec Ollama |

## Spike proposé

« Owl Hermes » minimale : lancer Hermes en TUI Gateway dans WSL, l'envelopper dans une Owl, afficher progression et approbations dans la bulle, puis mesurer la latence et la RAM, et la stabilité sur une semaine.

## Sources

- [Hermes — intégration programmatique](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration) · [API Server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server) · [Référence praticien](https://blakecrosley.com/guides/hermes) · [Analyse critique](https://agentconn.com/blog/nousresearch-hermes-agent-self-improving-framework-review/)
- [Droid Exec](https://docs.factory.ai/droid-exec/overview) · [Goose](https://goose-docs.ai/)
