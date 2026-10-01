# Laboratoire de tests — Owlcy

Objectif : **ne rien développer tant que les points techniques risqués ne sont pas prouvés.**
Chaque test produit un résultat chiffré et une décision go / no-go. Synthèse des résultats : [`../doc/techno/03-resultats-tests.md`](../doc/techno/03-resultats-tests.md).

```
poc/
├── cloud/     tests déjà exécutés (Linux + Chromium 141) — résultats dans chaque result.json
│   ├── t1-mcp-stdio/      10 serveurs MCP stdio, latence, mémoire, validation humaine (elicitation)
│   ├── t2-mcp-apps/       carte UI MCP dans une iframe sandboxée, pilotée par un vrai serveur MCP
│   ├── t3-chouette-svg/   chouette SVG procédurale : coût CPU animée / en pause + captures
│   └── t4-bun-sidecar/    moteur TS compilé en binaire unique : taille, démarrage, mémoire
└── windows/   kit à lancer sur TON PC (impossible à tester depuis le cloud)
    ├── w1-perchoir-tauri/ LE test critique : overlay Tauri sous Windows
    ├── w2-memoire/        mesure mémoire réelle (processus + enfants WebView2) + état Focus Assist
    ├── w3-wsl-stdio/      latence d'un serveur stdio dans WSL via wsl.exe + accès /mnt/c
    ├── w4-ollama-tools/   fiabilité des appels d'outils de tes modèles locaux sur ta RTX 500 Ada (4 Go)
    └── w5-secrets/        Windows Credential Manager via keyring
```

## Kit Windows — mode d'emploi

Prérequis : Python 3.10+, [Rust](https://rustup.rs) (toolchain MSVC), Node 20+, Ollama. Tout se lance depuis PowerShell, **côté Windows** (pas dans WSL, sauf mention contraire).

**Installation** (dans un PowerShell Windows classique, pas le terminal WSL de l'éditeur, car la fenêtre UAC peut s'ouvrir derrière) :

```powershell
winget install -e --id Python.Python.3.12
winget install -e --id Rustlang.Rustup
winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override "--quiet --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
winget install -e --id OpenJS.NodeJS.LTS
winget install -e --id Ollama.Ollama
```

Désactiver ensuite l'alias `python.exe` du Store (Paramètres → Applications → Paramètres avancés → Alias d'exécution), puis **redémarrer l'éditeur** pour qu'il récupère le nouveau PATH.

**Copier le kit dans un dossier Windows.** Ne jamais compiler depuis `\wsl$\…` : `cargo` et MSVC y sont lents et se trompent de répertoire courant.

```powershell
robocopy \\wsl$\Ubuntu\home\paul\solo-project\owlcy\poc\windows C:\dev\owlcy\windows /E
```

### W1 — Perchoir Tauri (critique, ~1 h)

```powershell
cd C:\dev\owlcy\windows\w1-perchoir-tauri
npm create tauri-app@latest -- --help   # juste pour vérifier que npm/Node marchent
npx @tauri-apps/cli@latest icon owl-icon.png -o src-tauri/icons
cd src-tauri
cargo run --release
# 1.15 : cargo install tauri-cli --version "^2" ; cargo tauri build
```

> Le code n'a pas pu être compilé pendant la conception (crates.io bloqué) : s'il y a des erreurs de compilation, les corriger fait partie du test. Noter chaque correction dans les résultats.

| # | Vérification | Attendu | Résultat |
|---|---|---|---|
| 1.1 | La chouette apparaît en bas à droite, fond transparent, pas de bordure | ✅ | |
| 1.2 | Taper dans un éditeur (Notepad) puis cliquer la chouette : **le focus reste dans Notepad** | ✅ | |
| 1.3 | Cliquer **à côté** de la chouette (zone transparente de la fenêtre) : le clic atteint la fenêtre dessous | ✅ | |
| 1.4 | Clic sur la chouette → bulle ; Autoriser / Refuser fonctionnent, emote change | ✅ | |
| 1.5 | Les yeux suivent le curseur **partout sur l'écran** | ✅ | |
| 1.6 | Barre des tâches en masquage auto : elle se révèle toujours normalement | ✅ | |
| 1.7 | `.\mesure-memoire.ps1 -Nom owlcy-perch` → état notifications = `ACCEPTS_NOTIFICATIONS` (pas « plein écran détecté ») | ✅ | |
| 1.8 | Vidéo YouTube en plein écran (F11) puis un jeu en plein écran : la chouette reste visible au-dessus ? (noter le comportement, pas bloquant) | à noter | |
| 1.9 | Alt+Tab : la chouette n'apparaît pas dans la liste | ✅ | |
| 1.10 | Écran secondaire / mise à l'échelle 125-150 % : position et hit-test corrects | ✅ | |
| 1.11 | Tray → « Labo : carte MCP Apps » : la carte affiche `parentDom: bloqué`, `localStorage: bloqué` | ✅ | |
| 1.12 | Refaire 1.11 avec une CSP stricte dans `tauri.conf.json` (`"csp": "default-src 'self'; script-src 'self'"`) : noter si le script de la carte est bloqué | à noter (décide du besoin d'un proxy sandbox comme l'AppBridge officiel) | |
| 1.13 | RAM et CPU au repos (W2, 60 s) | < 150 Mo privés, < 1 % CPU | |
| 1.14 | Réduire la chouette (fermer la bulle, ne plus bouger la souris) : CPU animé vs pause | noter | |
| 1.15 | Taille de l'installeur NSIS (`cargo tauri build`) | noter | |

### W2 — Mémoire réelle

```powershell
wsl --shutdown        # sinon la VM WSL fausse le relevé (et coupe les sessions WSL ouvertes)
cd C:\dev\owlcy\windows\w2-memoire
.\mesure-memoire.ps1 -Nom owlcy-perch -Secondes 60
```
Mesure la somme **processus principal + tous les `msedgewebview2.exe` enfants** (c'est là que les chiffres publics divergent : 14 Mo vs 317 Mo selon ce qu'on compte). Comparer si possible avec une appli Electron ouverte (ex. `-Nom Code` ou `-Nom Discord`).

### W3 — WSL via stdio

```powershell
cd C:\dev\owlcy\windows\w3-wsl-stdio
python wsl_stdio_bench.py
```
Critère : RTT p95 via `wsl.exe` < 5 ms et démarrage à froid < 1,5 s → les intégrations `target: wsl` sont viables.

### W4 — Modèles locaux et appels d'outils

```powershell
ollama pull qwen3:4b; ollama pull qwen3.5:4b; ollama pull granite4:3b; ollama pull ministral-3:3b; ollama pull gemma4:e4b; ollama pull qwen3:8b
cd C:\dev\owlcy\windows\w4-ollama-tools
python bench_ollama_tools.py qwen3:4b qwen3.5:4b granite4:3b ministral-3:3b gemma4:e4b qwen3:8b
```
GPU réel : **RTX 500 Ada Laptop, 4 Go de VRAM** (et non 8 Go). Les modèles 3-4B tiennent entièrement sur le GPU. `gemma4:e4b` et `qwen3:8b` débordent en partie sur le CPU : noter les tokens/s (`ollama ps` montre la répartition GPU/CPU). Tags vérifiés sur ollama.com le 01/10/2026.

7 scénarios × 3 répétitions : simple, choix, parallèle, **chaîné (3 outils)**, **refus d'injection**. Critère : ≥ 90 % sur simple/choix pour le modèle retenu en étapes `llm:` ; le score « chaîné » décide si le mode agent peut être local.

### W5 — Coffre de secrets

```powershell
python -m pip install keyring
cd C:\dev\owlcy\windows\w5-secrets; python test_keyring.py
```

## Rendre les résultats

Remplir la colonne « Résultat » ci-dessus, déposer les `results-*.json` dans chaque dossier, puis mettre à jour [`doc/techno/03-resultats-tests.md`](../doc/techno/03-resultats-tests.md) et fermer les issues du Sprint 0 correspondantes.
