# ADR-003 — Owlcy natif Windows, intégrations `target: wsl` via `wsl.exe`

- **Date** : 2026-10-01
- **Statut** : proposé (**en attente de W1 et W3**)
- **Questions liées** : Q7, Q22

## Contexte

L'utilisateur travaille sous Windows 11, avec une partie de ses outils dans WSL (Ubuntu, réseau en mode `mirrored`). Owlcy doit vivre sur le bureau Windows, avec un overlay, le tray et le Credential Manager, tout en pouvant réutiliser des outils Linux.

## Options envisagées

1. **Tout dans WSL** (WSLg pour l'interface) : impossible d'avoir un vrai overlay Windows (focus, click-through, barre des tâches), et pas de Credential Manager.
2. **Natif Windows**, avec certaines intégrations lancées dans WSL par `wsl.exe -e <commande>` sur stdio : l'overlay et les secrets sont natifs, les outils Linux restent accessibles.
3. Natif Windows sans WSL : plus simple, mais on perd les outils Linux.

## Décision

**Option 2**, sous réserve des tests Windows :

| Preuve | Critère GO | Résultat | Source |
|---|---|---|---|
| Overlay Tauri : focus jamais volé, click-through, pas de Focus Assist | 1.2, 1.3, 1.7 ✅ | ⏳ à faire | W1 |
| Mémoire totale au repos (processus + WebView2) | < 150 Mo privés, < 1 % CPU | ⏳ à faire | W2 |
| stdio via `wsl.exe` | RTT p95 < 5 ms, démarrage à froid < 1,5 s | ⏳ à faire | W3 |
| Secrets | Credential Manager via `keyring` | ⏳ à faire | W5 |
| Sidecar compilé pour Windows depuis WSL | démarre et répond | ✅ 24 ms, 75 Mo privés | T4 Windows |

## Conséquences

- Le build et les tests Windows se font **depuis un dossier Windows** (`C:\dev\owlcy`), jamais depuis `\\wsl$\…` : `cargo` et MSVC y sont lents et gèrent mal le répertoire courant.
- Une intégration déclare `target: windows | wsl`. Pour `wsl`, le moteur lance `wsl.exe -e …`, et l'intégration ne doit pas travailler sur de nombreux petits fichiers dans `/mnt/c` (lent, mesuré en W3).
- Mesurer la RAM après un `wsl --shutdown` : sinon, la VM WSL (jusqu'à 10 Go ici) fausse le relevé.
- **Repli** : si W3 est NO-GO, les intégrations Linux passent en HTTP local (streamable HTTP MCP, que le mode `mirrored` rend accessible sur `localhost`). Si W1 ou W2 est NO-GO, ouvrir un ADR Tauri vs Electron (Q22).
