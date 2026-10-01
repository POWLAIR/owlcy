# Résultats des tests techniques

> Règle du projet : **aucun développement ne démarre sur un point non prouvé.** Chaque test a un critère go / no-go. Code et protocoles : [`poc/README.md`](../../poc/README.md).

Dernière mise à jour : 01/10/2026.

## Tableau de bord

| Test | Sujet | Où | Statut | Verdict |
|---|---|---|---|---|
| T1 | MCP stdio : 10 serveurs, latence, mémoire, validation humaine | Cloud | ✅ fait | **GO**, avec contrainte mémoire |
| T2 | Carte MCP Apps dans une iframe sandboxée (Chromium 141 ≈ moteur WebView2) | Cloud | ✅ fait | **GO** (à confirmer dans Tauri : W1.11-12) |
| T3 | Chouette SVG procédurale : coût CPU | Cloud | ✅ fait | **GO** |
| T4 | Moteur TS compilé (Bun) : taille, démarrage | Cloud + ton PC | ✅ fait | **GO** : binaire Windows validé (24 ms, 75 Mo) |
| T5 | AI SDK 7 + provider Ollama + MCP (TS) + `needsApproval` | WSL | 🟡 chaîne OK (modèle simulé) | **GO provisoire** : relancer avec Ollama réel |
| T6 | JSONata : expressions des pipelines | WSL | ✅ fait | **GO**, 2 expressions de la doc à corriger |
| T7 | SDK MCP TypeScript v2 (spec 2026-07-28, MRTR) | WSL | ✅ fait | **GO** |
| W1 | **Perchoir Tauri sous Windows** | Ton PC | 🟡 compilé, contrôles automatiques OK | 1 bug tao corrigé ; reste les vérifications manuelles |
| W2 | Mémoire réelle Tauri (processus + WebView2) | Ton PC | 🔲 à faire | |
| W3 | Intégrations WSL via `wsl.exe` | Ton PC | ✅ fait | **GO** (p95 1,6 ms) ; `/mnt/c` 115× plus lent |
| W4 | Appels d'outils des modèles locaux (RTX 500 Ada, 4 Go de VRAM) | Ton PC | ✅ arrêté, pris comme résultat | **Local OK pour les étapes simples, NO-GO pour le mode agent** |
| W5 | Windows Credential Manager | Ton PC | ✅ fait | **GO** |
| W6 | Spike Hermes (TUI Gateway dans WSL) | Ton PC | 🔲 plus tard (Sprint 12) | |

T5 à T7 ont été lancés depuis WSL sur ton PC (registre npm accessible). Machine de test : Dell Precision 3490, Windows 11 Pro, 32 Go de RAM, RTX 500 Ada Laptop 4 Go, WebView2 154. Décisions associées : [ADR-001](../decisions/ADR-001-moteur-ts-sidecar.md) à [ADR-004](../decisions/ADR-004-moteur-pipelines-maison.md).

---

## T1 — MCP stdio (SDK Python officiel 1.27.0)

Environnement : Linux, 2 vCPU, 8 Go, Python 3.11.

| Mesure | Résultat |
|---|---|
| Version de protocole négociée | `2025-11-25` (le SDK Python 1.x **ne parle pas encore** la spec 2026-07-28) |
| Démarrage d'un serveur (spawn → initialize → list_tools) | **~400 ms** |
| **RAM par serveur Python (FastMCP)** | **~54 Mo** (dont ~45 Mo dus à l'import du SDK ; Python nu ≈ 8 Mo) |
| 10 serveurs en parallèle | ~540 Mo au total |
| Latence d'un appel d'outil (p50 / p95) | **2,7 / 3,2 ms** |
| 500 éléments structurés renvoyés | 19 ms, `structuredContent` OK |
| Appel simultané sur les 10 serveurs | 20 ms |
| **Validation humaine via *elicitation*** (outil qui demande « Déplacer … ? ») | ✅ fonctionne, aller-retour 4,8 ms (hors temps humain) |

**Conséquences de design :**
1. La latence de MCP est négligeable, ce n'est pas un problème.
2. **La mémoire l'est** : un processus par intégration coûte ~50 Mo. Donc :
   - démarrage **à la demande** + arrêt après inactivité (déjà prévu, désormais **obligatoire**) ;
   - les **outils de base d'Owlcy** (`owl.say`, `fs.*`, `llm.*`, `http.fetch`) tournent **dans le moteur**, pas en processus MCP séparés ;
   - MCP en processus séparé seulement pour les intégrations tierces ou isolées.
3. La validation humaine peut s'appuyer **dès maintenant sur l'elicitation** (spec 2025-11-25, supportée) ; MRTR (2026-07-28) viendra avec le SDK TS v2.

## T2 — MCP Apps (mécanisme)

Serveur MCP réel qui expose un outil `digest` avec `_meta.ui.resourceUri = ui://veille/digest` et une ressource `text/html;profile=mcp-app`. Page hôte Chromium : iframe `sandbox="allow-scripts"` (origine opaque), dialogue JSON-RPC par `postMessage`.

| Vérification | Résultat |
|---|---|
| L'hôte découvre la ressource UI via les métadonnées de l'outil | ✅ |
| La carte reçoit le résultat initial (`ui/notifications/tool-result`) | ✅ 3 éléments affichés |
| La carte appelle un outil via l'hôte (`tools/call`) → serveur MCP réel | ✅ 8,7 ms, 5 éléments affichés |
| Accès au DOM de l'hôte depuis la carte | ✅ **bloqué** |
| Requête réseau depuis la carte (CSP `connect-src 'none'`) | ✅ **bloquée** |
| `localStorage` depuis la carte | ✅ **bloqué** |

Limites : protocole simplifié écrit à la main (l'AppBridge officiel `@modelcontextprotocol/ext-apps` n'était pas installable). **Reste à vérifier dans Tauri/WebView2** : la CSP de l'app peut bloquer les scripts d'une iframe `srcdoc` (W1.11-12). Si c'est le cas → servir les cartes depuis une origine dédiée (proxy sandbox, comme le fait l'AppBridge officiel).

## T3 — Chouette SVG procédurale

3 chouettes animées à 60 fps (respiration, clignements, yeux qui suivent le curseur, emotes), Chromium 141 headless (rendu logiciel, 2 vCPU lents : pessimiste).

| Situation | Travail du thread principal |
|---|---|
| 3 chouettes, idle | **37 ms/s** (≈ 3,7 % d'un cœur) |
| + suivi du curseur | 42 ms/s |
| + emotes actives | 36 ms/s |
| **Animation en pause** (fenêtre cachée) | **0,1 ms/s** ✅ |
| Tas JS | ~1,5 Mo |

Captures : `poc/cloud/t3-chouette-svg/capture-*.png`. Les skins (`owlcy`, `veilleuse`, `mecano`) sont bien générés par paramètres.
**Optimisations prévues** : 30 fps en idle, animation par CSS/transform uniquement, une seule chouette animée à la fois. À mesurer sur WebView2 avec GPU (W1.14).

## T4 — Moteur TypeScript compilé (sidecar)

Serveur JSON-RPC stdio minimal, Bun 1.3.13.

| Variante | Démarrage → 1re réponse | RAM | RTT p50 |
|---|---|---|---|
| **Bun compilé (binaire unique)** | 19 ms | 74 Mo | 0,02 ms |
| Node 22 (script) | 32 ms | 55 Mo | 0,04 ms |
| Bun (script) | 26 ms | 59 Mo | 0,07 ms |

| Taille du binaire Bun compilé | Valeur |
|---|---|
| Brut | **102 Mo** |
| gzip -9 | 39 Mo |
| xz (≈ compression de l'installeur NSIS/LZMA) | **26 Mo** |

**Conséquence** : l'argument « Tauri = 3 Mo » ne tient plus avec un sidecar TS. Installeur estimé **~30-40 Mo**, ce qui reste 10× plus léger qu'Electron (~384 Mo mesurés sur Windows par Elanis). Alternative à garder en tête : moteur en Rust (≈ 5-10 Mo, mais SDK MCP Rust `rmcp` encore en bêta côté officiel).

### T4 bis — Le même binaire sous Windows (01/10/2026)

Compilé depuis WSL (`bun build --compile --target=bun-windows-x64`, Bun 1.4.0), lancé sous Windows 11 par `poc/cloud/t4-bun-sidecar/bench-windows.ps1`. Détails : `result-windows.json`.

| Mesure | Valeur |
|---|---|
| Taille `.exe` | 84,7 Mo brut, **29,9 Mo en xz** |
| Démarrage → 1re réponse | **~24 ms** (96 ms au tout premier lancement : analyse Defender) |
| RAM | **75 Mo privés**, 26 Mo de working set |
| RTT p50 / p95 | 0,03 / 0,04 ms |

**Verdict : GO.** Le sidecar se compile pour Windows depuis WSL, sans toolchain Windows (Q14 : Bun compile).

## T5 — AI SDK 7 + Ollama + MCP stdio + `needsApproval`

Code : `poc/cloud/t5-t7-moteur-ts/` (`t5-aisdk-ollama-mcp.ts`, `t5-server.ts`). Versions : `ai` 7.0.126, `@ai-sdk/mcp` 2.0.65, `ai-sdk-ollama` 4.4.0, SDK MCP serveur 2.2.0.

**Changement de version** : l'AI SDK 6 est désormais une branche de maintenance (`ai-v6`). `latest` est la **v7**, et les deux providers Ollama exigent `ai@^7`. On teste donc la v7.

| Vérification | Résultat |
|---|---|
| Client MCP stdio (`@ai-sdk/mcp`) → serveur SDK v2 | ✅ 84 ms, 2 outils découverts |
| Le modèle enchaîne `list_files` → `move_file` | ✅ (modèle simulé `MockLanguageModelV4`) |
| `needsApproval: true` sur `move_file` : arrêt **avant** exécution | ✅ `tool-approval-request`, rien n'est exécuté côté serveur |
| Réponse `tool-approval-response` (approuvé) → l'outil MCP s'exécute | ✅ le serveur déplace le fichier (`list_files` le confirme ensuite) |
| **Avec un vrai modèle Ollama** | ⏳ quand Ollama sera installé : `bun t5-aisdk-ollama-mcp.ts qwen3:4b` |

Pièges de la v7 : les messages `system` sont refusés dans `messages` (il faut l'option `instructions`), et le résultat d'un outil exécuté après approbation n'apparaît pas dans `steps` du tour suivant.

## T6 — JSONata (expressions des pipelines)

`t6-jsonata.ts` évalue les expressions `${…}` de [feature/02](../feature/02-pipelines-factory.md) sur un contexte de run réaliste. Détails : `result-t6.json`.

| Expression (ligne de feature/02) | Résultat |
|---|---|
| `params.sources`, `item`, `params.notion_db` | ✅ |
| `$count(digest.output) > 0`, `$count(digest.output.points) <= 5`, `… > 0` | ✅ |
| `$flatten(collect.output)` (l.29) | ❌ **T1006 : `$flatten` n'existe pas en JSONata** → `collect.output.*` ✅, ou fonction enregistrée par le moteur |
| `collect.output[link in $not(previous.output.links)]` (l.118) | ⚠️ **renvoie `undefined` sans erreur** → `collect.output.*[$not(link in $$.previous.output.links)]` ✅ |
| Performance (expression compilée) | **~25 µs** par évaluation |

**Verdict : GO.** JSONata convient. Deux conséquences : corriger ces deux expressions dans la doc, et faire échouer toute étape dont une expression renvoie `undefined` (ADR-004).

## T7 — SDK MCP TypeScript v2 (2026-07-28, MRTR)

`t7-server.ts` expose `move_file`, qui renvoie `inputRequired({ confirm: elicit(…) })` tant qu'il n'a pas de réponse. `t7-mcp-v2-mrtr.ts` teste trois modes de négociation. Détails : `result-t7.json`.

| Vérification | `auto` / `pin 2026-07-28` | `legacy` (2025-11-25) |
|---|---|---|
| Version négociée | **2026-07-28** | 2025-11-25 |
| Mode manuel : le client reçoit `input_required` brut | ✅ clé `confirm`, message « Déplacer a.txt vers b.txt ? » | — (traduit en élicitation) |
| Mode auto : réponse « oui » → relance avec `inputResponses` → exécuté | ✅ ~80 ms | ✅ ~10 ms |
| Réponse « non » → refus propre | ✅ | ✅ |

**Verdict : GO.** Pièges : côté serveur, il faut **`serveStdio(factory)`** (avec `server.connect(new StdioServerTransport())`, le serveur reste en 2025). Côté client, il faut **`versionNegotiation: { mode: 'auto' }`**, car le mode par défaut est `legacy`. Bonne nouvelle : le même handler `inputRequired` sert les deux révisions, le SDK le traduisant en élicitation classique pour les clients 2025.

---

## W1 — Perchoir Tauri sous Windows (01/10/2026, partie automatique)

Tauri 2.12.1 / tao 0.37.1, Rust 1.98.1, MSVC 14.44, WebView2 154. Compilé depuis `C:\dev\owlcy` (`build.ps1`) : **3 min 53 s** la première fois, **sans aucune erreur de compilation**. `owlcy-perch.exe` : 6,1 Mo.

**Bug trouvé et corrigé** : au premier lancement, la fenêtre était **invisible**, et `WS_EX_NOACTIVATE` et `WS_EX_TOOLWINDOW` avaient disparu (seul `NonRudeHWND` restait). Cause : tao recalcule et **réécrit tous les styles étendus** à chaque changement d'état, dont `set_ignore_cursor_events` appelé par le hit-test. Les styles posés à la main en Win32 sont donc effacés, et le `ShowWindow` manuel est annulé, puisque pour tao la fenêtre n'est « pas visible ». Correctif dans `main.rs` :
- `.focusable(false)` : tao pose lui-même `WS_EX_NOACTIVATE` et le conserve ;
- `win.show()` plutôt que `ShowWindow` : tao fait un `SW_SHOWNOACTIVATE`, puisque `focused(false)` ;
- `WS_EX_TOOLWINDOW` réappliqué après chaque bascule du hit-test, car tao n'a pas d'indicateur pour ce style.

**Leçon pour le Sprint 2** : tout style Win32 posé à la main sur une fenêtre tao doit être réappliqué après chaque appel qui modifie l'état de la fenêtre.

| # | Contrôle automatique (`autocheck3.ps1`) | Résultat |
|---|---|---|
| 1.1 | Fenêtre 260×300 en bas à droite (1636,716), fond transparent, sans bordure | ✅ (capture `w1-capture-idle.png`) |
| 1.2 | Le perchoir n'est jamais au premier plan : après le lancement, après un clic sur la chouette | ✅ (vérif. manuelle avec Notepad à faire) |
| 1.4 | Clic sur la chouette → bulle Autoriser / Refuser + émote « ask » | ✅ (capture `w1-capture-bulle.png`) |
| 1.7 | État des notifications Windows avec le perchoir affiché | ✅ `5 = ACCEPTS_NOTIFICATIONS` |
| 1.9 | `WS_EX_TOOLWINDOW` présent (pas d'Alt+Tab) | ✅ style présent (vérif. manuelle à faire) |
| — | Animation | 61 fps |
| — | Processus | `owlcy-perch.exe` + 6 `msedgewebview2.exe` |

Restent les vérifications à la main : 1.2 avec Notepad, 1.3, 1.5, 1.6, 1.8 à 1.12 et 1.14, ainsi que W2 (1.13) et 1.15.

## W3 — Intégrations WSL via `wsl.exe` (01/10/2026)

| Cas | Démarrage | RTT p50 / p95 |
|---|---|---|
| Python natif Windows | 130 ms | 0,15 / 0,27 ms |
| Python dans WSL via `wsl.exe` | **318 ms** | **0,43 / 1,64 ms** |

| 1000 écritures + 1000 lectures | Durée |
|---|---|
| `~` dans WSL | 144 ms |
| `/mnt/c` depuis WSL | **16 518 ms (115× plus lent)** |

**Verdict : GO** (p95 < 5 ms, démarrage < 1,5 s). Réserve : le démarrage a été mesuré avec la VM WSL déjà lancée ; un vrai démarrage à froid de la VM prend plusieurs secondes. Règle qui en découle : une intégration `target: wsl` ne doit pas manipuler de nombreux fichiers dans `/mnt/c`.

## W5 — Windows Credential Manager (01/10/2026)

`keyring` 25.7.0 → backend `WinVaultKeyring`. Écriture en 5,2 ms, entrée visible dans `cmdkey` (`LegacyGeneric:target=owlcy-test`), lecture OK, suppression OK sans reste. **Verdict : GO.** Note : `test_keyring.py` plante en cp1252 quand sa sortie est redirigée. `run-w5.ps1` force l'UTF-8.

## W4 — Modèles locaux et appels d'outils (01/10/2026)

Ollama 0.35.0, 6 modèles téléchargés. **Banc arrêté volontairement après `qwen3:4b`** : sur ce GPU, il aurait fallu plus de 3 h pour les 6 modèles. On prend le résultat tel quel. Détails : `poc/windows/w4-ollama-tools/results-2026-10-01-partiel.json` et les sorties `partiel-*.txt`.

| `qwen3:4b` | Avec réflexion | `think: false` |
|---|---|---|
| simple | 6/6 ✅ | 6/6 ✅ |
| choix | 6/6 ✅ | 6/6 ✅ |
| parallèle | 3/3 ✅ | non atteint |
| **chaîné (3 outils)** | **0/1 : timeout 300 s** | non atteint |
| Durée par essai | ~1,7 min | ~1,5 min |

**Pourquoi c'est si lent :**
- Une fois chargé (contexte 4096), `qwen3:4b` occupe 3,5 Go et **ne tient pas dans les 4 Go de VRAM** : Ollama en met 36 % sur le CPU. Résultat : **~7,7 tokens/s**, avec le GPU quasi au repos (12 %, 210 MHz, P4, 12,6 W), sur secteur.
- `qwen3:4b` (version hybride) **ignore `think: false`** : le raisonnement passe dans `content`, soit 585 tokens pour un simple appel `weather`. La variante `qwen3:4b-instruct` n'a pas été testée.

**Verdict :**
- **Étapes `llm:` étroites** (classer, choisir un outil, extraire) : la **justesse** est bonne en local (100 % sur simple et choix). En revanche, ~1,5 min par appel exclut tout usage interactif. Ça reste acceptable pour une pipeline planifiée la nuit.
- **Mode agent (chaîné)** : **NO-GO en local** sur cette machine. Le mode agent passe par un **modèle cloud par défaut**, et le local reste une option.
- Non mesurés : `qwen3.5:4b`, `granite4:3b`, `ministral-3:3b`, `gemma4:e4b`, `qwen3:8b`, ainsi que le scénario « refus d'injection ». À relancer sur une machine avec ≥ 8 Go de VRAM, ou avec `qwen3:4b-instruct` et `num_ctx` 2048, si le local redevient un enjeu.
