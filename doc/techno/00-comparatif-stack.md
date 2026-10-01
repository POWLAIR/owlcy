# Stack — synthèse des choix

> Ce fichier est le **résumé** (v4, 01/10/2026). Les résultats de tests sont dans [`03-resultats-tests.md`](03-resultats-tests.md). Les comparatifs sourcés sont dans [`01-benchmark-stack.md`](01-benchmark-stack.md), et les standards dans [`02-standards-agents.md`](02-standards-agents.md).

| Brique | Choix recommandé | Alternative / plan B | Statut |
|---|---|---|---|
| Shell desktop | **Tauri 2** (taille, Rust/Win32) — ⚠️ avantage RAM non démontré sous Windows | Electron | 🟡 tests W1/W2 |
| Core OS | **Rust** (fin) | — | ✅ |
| Moteur | **TypeScript en sidecar** (binaire Bun sous Windows : 24 ms au démarrage, 75 Mo privés, installeur +29,9 Mo en xz — T4 Windows) | Rust + `rmcp` | 🟡 T5-T7 |
| Protocole des capacités | **MCP** pour les intégrations tierces + **outils internes** dans le moteur (T1 : ~50 Mo par serveur MCP) | — | ✅ T1 |
| UI des plugins | **MCP Apps** | Cartes maison | ✅ T2 (reste W1.11-12) |
| Savoir-faire | **Agent Skills (`SKILL.md`)** | — | ✅ |
| Couche LLM / agent | **AI SDK 7** (`ToolLoopAgent`, `needsApproval`, `@ai-sdk/mcp`) | Mastra | ✅ |
| Moteur de pipelines | **Maison (YAML → DAG)** | Mastra workflows | 🟡 ADR Sprint 0 |
| Expressions | **JSONata** | CEL pour les conditions seules | 🟡 T6 |
| LLM local | **Ollama** — petit modèle 3-8B choisi par le test W4 (candidats : Gemma 4 E4B, Granite 4 3B, Qwen3-4B-2507, Qwen3 8B) | LM Studio | 🟡 test W4 |
| LLM cloud | **Claude** pour le mode agent | Autres via AI SDK | ✅ |
| Mascotte | **SVG procédural** | Rive (Sprint 10) | ✅ T3 |
| UI | **React** | Svelte (parité xyflow) | ✅ |
| Éditeur de graphe | **React Flow (xyflow)** | — | ✅ |
| Config | **YAML + JSON Schema** | — | ✅ |
| Données | **SQLite** (plein texte + vecteurs plus tard) | — | ✅ |
| Secrets | **Windows Credential Manager** via `keyring` | — | 🟡 W5 |
| Intégrations Python | **uv** | — | ✅ |
| Cible OS | **Windows natif**, intégrations `wsl` possibles | — | 🟡 W3 |
| Runtimes d'Owl externes | **Adaptateur** : Hermes (TUI Gateway JSON-RPC), Claude Code (hooks), Goose | Factory Droid Exec (payant, fermé) | 🟡 spike Hermes |
| Mémoire | Carnet Markdown plafonné + SQLite FTS5 (modèle Hermes, en lisible) | Letta | ✅ recommandé |

## Projets à surveiller

Coucou · OpenClaw · QwenPaw · OpenAkita · NekoAI · Mastra · spec MCP · Rive · **Hermes Agent · Factory · Goose · Letta**. Détails dans [`idee/03-benchmark-concurrents.md`](../idee/03-benchmark-concurrents.md) et [`idee/04-benchmark-agents-autonomes.md`](../idee/04-benchmark-agents-autonomes.md).
