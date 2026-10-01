# Benchmark de la stack — v3 (données concrètes)

Révision du 01/10/2026. La v2 contenait des notes pondérées subjectives : **elles sont supprimées**. Chaque chiffre porte maintenant sa source, sa date et son **niveau de preuve** :

| Niveau | Signification |
|---|---|
| 🟢 **Mesuré ici** | Test exécuté pendant la conception (voir [`03-resultats-tests.md`](03-resultats-tests.md)) |
| 🔵 **Mesuré (source publique)** | Benchmark reproductible publié, méthode connue |
| 🟡 **Déclaratif** | Chiffre annoncé par un article, un éditeur ou un retour d'expérience, sans méthode vérifiable |
| ⚪ **À mesurer** | Test prévu sur ton PC (kit `poc/windows`) |

---

## 1. Shell desktop : Tauri 2 vs Electron

### Ce que disent les mesures

| Mesure (Windows x64) | Tauri | Electron | Preuve | Source |
|---|---|---|---|---|
| Taille du build | **≈ 3 Mo** | ≈ 384 Mo | 🔵 | Elanis, CI GitHub, maj. 09/2026 |
| Temps de démarrage (release) | ≈ 711 ms | **≈ 206 ms** | 🔵 | Elanis |
| **Mémoire (release)** | **≈ 317 Mo** | ≈ 278 Mo | 🔵 | Elanis — méthode : « mémoire du processus principal et de ses enfants » |
| Mémoire (Linux, release) | **≈ 94 Mo** | ≈ 586 Mo | 🔵 | Elanis |
| Overlay Tauri en production (Windows 11) | 14 Mo, < 1 % CPU | — | 🟡 | Manasight (on ignore si les processus WebView2 sont comptés) |
| « Tauri = 5× moins de RAM » | — | — | 🟡 | Articles comparatifs, sans méthode |

**Correction importante par rapport à la v2** : sur Windows, l'avantage mémoire de Tauri **n'est pas démontré**. WebView2 est un Chromium multi-processus (browser, GPU, renderer, utility), comme Electron. Les « 14 Mo » viennent probablement du seul processus principal. Des applis WebView2 montent à 800 Mo-1,5 Go quand la page est lourde (issues publiques de Kybern, Hoppscotch, corral-desktop).

### Ce qui reste vrai

- **Taille** : 3 Mo contre 384 Mo (🔵). Avec notre moteur TS compilé : ~30-40 Mo d'installeur (🟢 T4), toujours ~10× plus léger.
- **Rust natif** pour les appels Win32 (styles de fenêtre, hotkeys, secrets) sans module natif Node.
- **Écosystème overlay** : Tauri est le choix d'OpenAkita, NekoAI, de l'app desktop QwenPaw et de l'overlay Manasight (🟡 constat de veille).

### Pièges Windows documentés (tous concrets, 2026)

| Piège | Source | Parade |
|---|---|---|
| Une fenêtre transparente **plein écran** est vue comme une appli plein écran : Focus Assist s'active, la barre des tâches auto-masquée ne se révèle plus, ShareX et Wallpaper Engine réagissent | carnac #12 (28/09/2026), tauri #7328 | **Fenêtre petite, dimensionnée au contenu** ; propriété `NonRudeHWND` ; décaler des bords |
| Pas de click-through natif dans Tauri | tauri #13070 | Hit-test ~60 Hz + `set_ignore_cursor_events` |
| Une fenêtre `focusable(false)` **s'active quand même** à `set_visible(true)` | tao PR #1358 (ouverte le 30/09/2026) | Style `WS_EX_NOACTIVATE` + `ShowWindow(SW_SHOWNOACTIVATE)` en Win32 |
| Réaffirmer « topmost » trop souvent perturbe les autres applis | carnac #12 | Ne le réaffirmer que sur événement |
| Barre de titre fantôme sur les fenêtres transparentes | tauri #14764 | À vérifier en W1 |

**Verdict : Tauri 2 reste le choix**, pour la taille, Rust/Win32 et l'écosystème, **mais pas pour la RAM**. Le critère RAM (< 150 Mo privés au repos, tous processus) est à mesurer ⚪ en W1/W2 : c'est un go / no-go.

## 2. Moteur : TypeScript (sidecar) vs Rust vs Python

| Critère | TS (Bun compilé) | Rust dans Tauri | Python |
|---|---|---|---|
| SDK MCP officiel | **v2 supporte la spec 2026-07-28** (MRTR, `serveStdio`, compatibilité avec les serveurs 2025) — statut v2 alpha/bêta 🔵 docs | `rmcp` (SDK officiel) en bêta 🟡 | SDK 1.27 = spec **2025-11-25** 🟢 T1 |
| Démarrage | 19 ms cloud · **24 ms Windows** 🟢 | ~0 (dans le binaire) | ~400 ms avec le SDK 🟢 |
| RAM | 74 Mo cloud · **75 Mo privés Windows** 🟢 | ~0 en plus | 54 Mo par serveur 🟢 |
| Taille ajoutée | +102 Mo brut / ~26 Mo compressé (cloud) · **84,7 Mo brut / 29,9 Mo xz (Windows)** 🟢 | ~0 | runtime complet à embarquer |
| Frameworks LLM | AI SDK 7, Mastra 🔵 | pauvres | riches |

**Verdict** : moteur TS en sidecar **maintenu**. Plan B si la taille ou la RAM posent problème : moteur Rust + `rmcp` (à réévaluer quand le SDK Rust sort de bêta).

## 3. Couche LLM / agents

| Option | Faits vérifiés | Preuve |
|---|---|---|
| **AI SDK 6** (déc. 2025), remplacé par la **v7** (ADR-001) | `ToolLoopAgent`, `needsApproval`, MCP stable (`@ai-sdk/mcp`, OAuth, élicitation) | 🔵 annonce officielle |
| Mastra | Apache 2.0, workflows avec suspend/resume, MCP client et serveur ; bug ouvert sur la reprise d'un workflow détenu par un agent (#15734) | 🔵 |
| Retour d'expérience « même agent : 41 h LangGraph TS contre 18 h Mastra » | 🟡 un seul témoignage |

Testé 🟢 en T5 avec **AI SDK 7** (la v6 n'est plus qu'une branche de maintenance) + provider Ollama + client MCP, sur modèle simulé ; reste à valider avec un vrai modèle Ollama. Voir `techno/03-resultats-tests.md`.

## 4. Modèles locaux (données publiques sur carte 8 Go ; ta carte : 4 Go)

| Donnée | Valeur | Preuve | Source |
|---|---|---|---|
| Test sur carte 8 Go (Jetson Orin Nano), 17 petits modèles, 50 tests d'outils (simples, parallèles, chaînés) | Granite 4.0-3B **96,2 %** · Hammer2.1-3B 94,2 % · **Gemma 4 E4B 92,3 %, seul 8/8 en chaîné** · Granite 4.1-3B 92,3 % | 🔵 dépôt public, évaluation AST déterministe | bfcl-jetson-test-v2 |
| BFCL v4 (sans fine-tuning) | Qwen3-4B-Instruct-2507 : « haut des 80 % » · Gemma 4 E4B : « milieu-haut des 80 % » · Phi-4-mini : « bas-milieu des 80 % » | 🟡 fourchettes, pas de chiffre exact | Ertas (08/2026) |
| Quantification < Q4_K_M → fiabilité des outils dégradée avant la qualité du chat | | 🟡 | PromptQuorum |
| Composition : 95 %/appel sur 8 étapes ≈ 66 % | | calcul (0,95⁸) | |

**Changement par rapport à la v2** : `qwen3:8b` n'est plus le choix par défaut. Les petits modèles spécialisés **3-4B (Granite 4, Gemma 4 E4B, Qwen3-4B-2507)** font aussi bien ou mieux en appel d'outils, tiennent largement en 8 Go et laissent de la VRAM pour le contexte.
**Décision reportée au test W4**, sur ton GPU (RTX 500 Ada, **4 Go de VRAM**), avec nos scénarios (dont le refus d'injection). W4 (01/10) arrêté après `qwen3:4b` : juste sur les appels simples, mais ~1,5 min par appel et timeout en chaîné. Modèle par défaut toujours à choisir (Q26).

## 5. Protocoles

| Sujet | Fait | Preuve |
|---|---|---|
| MCP stdio : latence | 2,7 ms p50 | 🟢 T1 |
| MCP : validation humaine | Élicitation fonctionnelle aujourd'hui (spec 2025-11-25) | 🟢 T1 |
| MCP 2026-07-28 : MRTR, stateless | Spec GA ; SDK TS v2 compatible ; SDK Python 1.x non | 🔵 / 🟢 |
| MCP Apps : sandbox iframe + postMessage | Fonctionne dans Chromium 141 ; DOM hôte, réseau et stockage bloqués | 🟢 T2 |
| MCP Apps : hôte officiel | `AppBridge` (ext-apps) : l'hôte gère `ui/initialize`, `tools/call`, notifications, CSP selon les domaines déclarés | 🔵 docs |
| Agent Skills (`SKILL.md`) | Standard ouvert, adopté par Claude, Codex, Copilot, Cursor, Hermes… | 🔵 |

## 6. Mascotte

| Option | Fait | Preuve |
|---|---|---|
| **SVG procédural** | 3 chouettes à 60 fps : 37 ms/s de thread principal ; 0,1 ms/s en pause ; skins générés par paramètres | 🟢 T3 |
| Rive | Runtime **MIT** ; data binding couleurs, nombres, enums, artboards ; éditeur gratuit pour un individu | 🔵 docs |
| Sprites | Un fichier par skin (NekoAI : 32 px ×1-4) | 🔵 |

**Verdict : SVG procédural confirmé** pour le MVP. Rive = option du Sprint 10 (skins avancés).

## 7. UI & éditeur de graphe

- React Flow et Svelte Flow sont à parité fonctionnelle depuis Svelte Flow 1.0 (14/05/2025) 🔵.
- **React retenu** : l'AppBridge MCP Apps et les hooks AI SDK sont d'abord publiés pour React/TS 🔵, et c'est la stack de NekoAI et OpenAkita.

## 8. Windows vs WSL

- WSL : l'accès `/mnt/c` reste lent sur de nombreux petits fichiers ; Microsoft annonce des améliorations en 2026 🟡.
- Latence `wsl.exe` + stdio : **⚪ W3**.
- **Verdict (inchangé)** : Owlcy natif Windows ; intégrations `target: wsl` sous réserve de W3.

---

## Sources

- [Elanis — web-to-desktop-framework-comparison](https://github.com/Elanis/web-to-desktop-framework-comparison) (mesures CI, maj. 09/2026)
- [Manasight — Tauri v2 pour un overlay](https://blog.manasight.gg/why-i-chose-tauri-v2-for-a-desktop-overlay/)
- [carnac #12 — overlay plein écran et Focus Assist](https://github.com/doggy8088/carnac/issues/12) · [tauri #7328](https://github.com/tauri-apps/tauri/issues/7328) · [tauri #13070](https://github.com/tauri-apps/tauri/issues/13070) · [tao PR #1358](https://github.com/tauri-apps/tao/pull/1358)
- WebView2 et mémoire : [corral-desktop #198](https://github.com/Florious95/corral-desktop/issues/198) · [Hoppscotch #6340](https://github.com/hoppscotch/hoppscotch/issues/6340) · [Kybern #14](https://github.com/Tresnanda/kybern/issues/14)
- [SDK MCP TS v2 — support 2026-07-28](https://ts.sdk.modelcontextprotocol.io/v2/migration/support-2026-07-28) · [MCP Apps — overview](https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/overview.md)
- [bfcl-jetson-test-v2 (8 Go)](https://github.com/drwjkirkpatrick-web/bfcl-jetson-test-v2) · [Ertas — tool calling on-device 2026](https://www.ertas.ai/blog/on-device-tool-calling-2026-qwen3-gemma4-phi4) · [BFCL v4 (BenchLM)](https://benchlm.ai/benchmarks/bfcl-v4) · [PromptQuorum](https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026)
- [AI SDK 6](https://vercel.com/blog/ai-sdk-6) · [Mastra #15734](https://github.com/mastra-ai/mastra/issues/15734) · [Mastra vs LangGraph vs AI SDK](https://particula.tech/blog/mastra-vs-langgraph-vs-vercel-ai-sdk-typescript-agents)
- [Rive — data binding](https://rive.app/docs/runtimes/web/data-binding) · [Svelte Flow 1.0](https://xyflow.com/blog/svelte-flow-release)
- [WSL — améliorations 2026](https://www.windowslatest.com/2026/03/31/microsoft-to-upgrade-windows-subsystem-for-linux-wsl-with-faster-file-access-better-networking-and-easier-setup/)
