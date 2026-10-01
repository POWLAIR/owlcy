# Architecture — vue d'ensemble

> **Révision v2 (30/09/2026)** après benchmark : Tauri 2 + moteur TS en sidecar, MCP partout, IPC local uniquement. Justifications : [`techno/01-benchmark-stack.md`](../techno/01-benchmark-stack.md).

## Schéma

```
┌──────────────────────────── Owlcy (Windows natif) ─────────────────────────────┐
│                                                                                 │
│  UI (WebView2, React)              Shell Tauri (Rust, fin)                      │
│  ┌──────────────────────┐          ┌──────────────────────────────┐             │
│  │ Perchoir (overlay)   │◀────────▶│ Fenêtres, click-through      │             │
│  │ Bulles / validations │  events  │ Hotkeys globales, tray       │             │
│  │ Dashboard / Runs     │          │ Coffre secrets (keyring)     │             │
│  │ Éditeurs (xyflow)    │          │ Fenêtre active, curseur      │             │
│  └──────────────────────┘          │ Supervision du sidecar       │             │
│                                    └──────────────┬───────────────┘             │
│                                    stdio JSON-RPC (le shell lance le moteur)          │
│                                    ┌──────────────▼───────────────┐             │
│                                    │ Moteur (sidecar TypeScript)  │             │
│                                    │ Event Bus · Registry         │             │
│                                    │ Pipeline Engine (JSONata)    │             │
│                                    │ Agent Runtime (AI SDK 7)     │             │
│                                    │ Trigger Manager              │             │
│                                    │ Permission Guard · SQLite    │             │
│                                    └──────────────┬───────────────┘             │
└───────────────────────────────────────────────────┼─────────────────────────────┘
                      MCP (stdio)                    │                 HTTP
        ┌──────────────────────┬─────────────────────┼──────────────┐
        ▼                      ▼                     ▼              ▼
 Intégrations Windows   Intégrations WSL      Ollama (local)   Claude / autres
 (1 processus chacune)  (via wsl.exe)
        ▲
 Hooks Claude Code ──HTTP 127.0.0.1 + token──▶ Moteur
```

## Répartition des responsabilités

| Couche | Techno | Pourquoi |
|---|---|---|
| **Shell** | Rust / Tauri 2 | Ce qui touche l'OS : fenêtres transparentes, click-through (hit-test ~60 fps + `setIgnoreCursorEvents`), hotkeys, secrets, fenêtre active. Mince et stable. Ces fonctions de plateforme sont **optionnelles** : le shell déclare celles qui sont disponibles ([`techno/04`](../techno/04-portabilite.md) §8). |
| **Moteur** | TypeScript (sidecar compilé en binaire unique) | Là où on itère : pipelines, agents, triggers. SDK MCP Tier 1 + AI SDK 7. Même langage que l'UI. |
| **UI** | React + xyflow + SVG | Mascotte, bulles, dashboard, éditeurs. |
| **Outils internes** | TypeScript, dans le moteur | `owl.say`, `fs.*`, `llm.*`, `http.fetch` : sans processus séparé (un processus MCP ≈ 50 Mo, test T1). |
| **Intégrations** | N'importe quel langage via MCP | Tierces ou isolées : 1 processus chacune, **démarrées à la demande et arrêtées après inactivité (obligatoire)**. |

## Principes

1. **Zéro coût au repos** : l'animation s'arrête quand la chouette est cachée ; les intégrations sont arrêtées après N minutes d'inactivité ; aucun polling sans abonné (principe Coucou).
2. **Tout est événement** : `run.started`, `step.started`, `step.done`, `permission.requested`, `run.failed`… La chouette n'est qu'un abonné du bus.
3. **Aucun port réseau** par défaut ; seul l'endpoint des hooks écoute sur `127.0.0.1` avec un token.
4. **Non bloquant pour les outils observés** : si Owlcy ne répond pas, le hook sort immédiatement.
5. **Le moteur peut tourner sans UI** (CLI `owlcy run veille-du-matin`), ce qui est utile pour les tests et le mode nuit.

## Flux type : fichier glissé sur la chouette

1. UI → `drop { path, mime }`.
2. Registry → pipelines dont le trigger `drop` accepte ce type.
3. Bulle : « Je peux : résumer / ranger / traduire ».
4. Run → événements → la chouette vole de perchoir en perchoir.
5. Outil `fs.write` → Permission Guard → **MRTR `input_required`** → bulle de validation.
6. Fin → `owl.say` + entrée dans l'historique.

## Perchoir : règles issues de la veille (v4)

- **Petite fenêtre dimensionnée au contenu**, jamais plein écran : une fenêtre transparente plein écran est détectée comme appli plein écran (Focus Assist activé, barre des tâches bloquée — carnac #12, tauri #7328).
- `WS_EX_NOACTIVATE` + `ShowWindow(SW_SHOWNOACTIVATE)` : `focusable(false)` seul ne suffit pas (tao PR #1358, ouverte le 30/09/2026).
- Propriété `NonRudeHWND`, décalage des bords, « topmost » réaffirmé seulement sur événement.
- Click-through : hit-test à ~60 Hz côté Rust sur les zones envoyées par le front (`set_ignore_cursor_events`).
- Tout cela est implémenté dans le spike W1 (`poc/windows/w1-perchoir-tauri`) : à valider avant le Sprint 2.

## Canal shell ↔ moteur

Le shell lance le moteur (sidecar) et lui parle en **JSON-RPC sur stdio** : aucun port, aucun pipe nommé à sécuriser, et le moteur meurt avec l'application. Un pipe nommé ne sera ajouté que si un autre client doit piloter le moteur (CLI séparée…).
