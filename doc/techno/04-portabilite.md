# Portabilité macOS / Linux — état des lieux

Révision du 01/10/2026. **Aucune décision ne change** : Windows reste la seule cible jusqu'à la v0.4 ([ADR-003](../decisions/ADR-003-windows-natif-wsl.md)). Ce document dit ce qu'un portage coûterait, et pose une règle de conception peu chère pour ne pas se fermer la porte. Question liée : [Q27](../decisions/questions-ouvertes.md).

Niveaux de preuve : 🟢 mesuré ici · 🔵 mesuré ailleurs (issue, doc officielle, benchmark) · 🟡 déclaratif (blog, une seule source) · ⚪ à mesurer.

## 1. Constat

Le multi-OS n'est aujourd'hui qu'une **intention** (« on veut du multi-OS (Windows d'abord) », [`idee/01-inspiration-coucou.md`](../idee/01-inspiration-coucou.md)). Toute la conception du shell est écrite en Win32. La séparation shell Rust mince / moteur TS ([ADR-001](../decisions/ADR-001-moteur-ts-sidecar.md)) isole bien ce qui dépend de l'OS, mais elle n'a pas été pensée pour la portabilité.

## 2. Ce qui est déjà portable

| Brique | Pourquoi | Preuve |
|---|---|---|
| Moteur TS | Dépendances en JS pur (`ai`, `@ai-sdk/mcp`, `@modelcontextprotocol/*`, `jsonata`, `zod`), aucun chemin Windows en dur dans `poc/cloud/` | 🟢 T5-T7 exécutés sous Linux (WSL et machine cloud) |
| Binaire du moteur | `bun build --compile` cible `darwin-arm64/x64` et `linux-x64/arm64` ; compilation croisée depuis Linux possible | 🔵 [doc Bun](https://bun.com/docs/bundler/executables) |
| IPC shell ↔ moteur | JSON-RPC sur stdio, sans socket ni port | 🟢 T4 |
| Intégrations | MCP stdio | 🟢 T1 |
| Fichiers de config | YAML / Markdown dans `~/.owlcy/` (`%APPDATA%\Owlcy` sous Windows), voir [`feature/03`](../feature/03-personnalisation.md) | — |
| Chouette | SVG procédural dans la WebView | 🟢 T3 |

## 3. Ce qui est propre à Windows

- **Le Perchoir** : `WS_EX_NOACTIVATE`, `NonRudeHWND`, `WS_EX_TOOLWINDOW`, le contournement de tao qui réécrit les styles ([`03-resultats-tests.md`](03-resultats-tests.md), W1). Le code du spike est déjà isolé sous `#[cfg(windows)]` (`poc/windows/w1-perchoir-tauri/src-tauri/src/main.rs`). Rien ne se transpose.
- **Les secrets** : [`architecture/02`](../architecture/02-securite.md) dit « uniquement dans le Windows Credential Manager ». W5 a testé le `keyring` **Python**, pas la crate Rust.
- **`target: wsl`** ([`architecture/01`](../architecture/01-systeme-extension.md)) : sans objet ailleurs, une intégration y est simplement native.
- **Le packaging** : installeur NSIS, CI prévue sur `windows-latest` seulement, build depuis `C:\dev\owlcy`.
- **La sandbox future** : AppContainer (Q16).

## 4. Fonctions de plateforme par OS

« Linux X11 » couvre aussi XWayland (`GDK_BACKEND=x11`).

| Fonction de plateforme | Windows | macOS | Linux X11 | Linux Wayland (KDE, wlroots) | Linux Wayland (GNOME) |
|---|---|---|---|---|---|
| Perchoir non activable | ✅ W1 🟢 | NSPanel `nonactivatingPanel` via [`tauri-nspanel`](https://github.com/ahkohd/tauri-nspanel) 🔵 ; régression possible sous macOS 27 ([#123](https://github.com/ahkohd/tauri-nspanel/issues/123)) ⚪ | Hints X11 ⚪ | Non documenté ⚪ | Non documenté ⚪ |
| Toujours au-dessus, y compris plein écran | ✅ W1 🟢 | Niveau `NSStatusWindowLevel` + `fullScreenAuxiliary` / `canJoinAllSpaces` 🔵 | ✅ 🔵 | layer-shell uniquement 🔵 | ❌ ignoré sans erreur ([tauri#14913](https://github.com/tauri-apps/tauri/issues/14913)) 🔵 |
| Position choisie par l'app | ✅ | ✅ | ✅ | layer-shell uniquement 🔵 | ❌ ignorée sans erreur 🔵 |
| Absent de la barre des tâches / Alt+Tab | ✅ W1 🟢 | `ActivationPolicy::Accessory` (un `set_focus()` peut faire revenir l'icône du Dock) 🟡 | ✅ ⚪ | ❌ ignoré 🔵 | ❌ ignoré 🔵 |
| Transparence | ✅ | `macOSPrivateApi` → **refus du Mac App Store**, Developer ID uniquement 🔵 | Compositeur requis ; plantages et artefacts avec NVIDIA ([tauri#14924](https://github.com/tauri-apps/tauri/issues/14924)) 🔵 | idem 🔵 | idem 🔵 |
| Click-through (`setIgnoreCursorEvents`) | ✅ | ✅ 🔵 | ✅ ⚪ | Plantage si appelé trop tôt 🟡 | idem 🟡 |
| Curseur sur tout l'écran | ✅ | ✅ sans permission 🟡 | ✅ | ❌ (0,0) hors de la fenêtre 🔵 | ❌ 🔵 |
| Fenêtre active | ✅ | App au premier plan : ✅ sans permission. Titre : permission **Enregistrement de l'écran** 🔵 | ✅ | Script KWin / kdotool 🔵 | Extension GNOME Shell 🔵 |
| Hotkeys globales | ✅ | ✅ (permission Accessibilité selon un blog) 🟡 | ✅ | Portail `GlobalShortcuts` (KDE oui, wlroots non) 🔵 | Portail sur GNOME 48+, avec des bizarreries 🔵 |
| Tray | ✅ | ✅ | ✅ | Bugs d'enregistrement sur KDE 6 🔵 | Extension AppIndicator requise 🔵 |
| Démarrage auto | Registre | LaunchAgent / SMAppService (alerte « activité en arrière-plan ») 🔵 | `~/.config/autostart` | idem | idem |
| Secrets (crate `keyring`) | Credential Manager | Keychain ; un binaire non signé peut redemander l'accès à chaque mise à jour 🟡 | Secret Service (bloque sans démon ou trousseau verrouillé) ou keyutils (perdu au redémarrage) 🔵 | idem | idem |

Sources Linux détaillées : [global-hotkey#28](https://github.com/tauri-apps/global-hotkey/issues/28), [doc Tauri graphique Linux](https://v2.tauri.app/develop/debug/linux-graphics/), [tray-icon](https://github.com/tauri-apps/tray-icon), [Shijima-Qt](https://github.com/pixelomer/Shijima-Qt).

## 5. Packaging

| | macOS | Linux |
|---|---|---|
| Formats | `.dmg` / `.app` universel (`universal-apple-darwin`), sidecar compilé pour aarch64 **et** x86_64 | deb, rpm, AppImage, Flatpak (dépend de `libwebkit2gtk-4.1`, base Ubuntu 22.04 / Debian 12) |
| Signature | Apple Developer Program (99 $/an), notarisation obligatoire hors App Store 🔵 | — |
| Pièges connus | Sidecar Bun signé avec le hardened runtime : il faut `com.apple.security.cs.allow-jit`, sinon plantage au lancement ([bun](https://bun.com/docs/bundler/executables)) 🔵. Notarisation qui échoue avec `externalBin` ([tauri#11992](https://github.com/tauri-apps/tauri/issues/11992)) 🟡. Bun 1.4.0 tué par macOS 27 à cause d'une signature invalide, corrigé ensuite ([bun#39764](https://github.com/oven-sh/bun/issues/39764)) 🔵 | Flatpak : le contournement XWayland exige `--socket=x11`, ce qui affaiblit le bac à sable 🟡 |
| Machine de build | Mac ou runner macOS (signature) | Linux |

## 6. Mémoire

Benchmark [Elanis](https://github.com/Elanis/web-to-desktop-framework-comparison) (release, processus principal + enfants) 🔵 :

| OS | Tauri | Electron |
|---|---|---|
| Windows x64 | ≈ 317 Mo | ≈ 278 Mo |
| macOS arm64 | ≈ 95 Mo | ≈ 369 Mo |
| Linux x64 | ≈ 94 Mo | ≈ 586 Mo |

L'avantage mémoire de Tauri est réel sur macOS et Linux, pas sur Windows (Q22, W2).

## 7. Lecture par OS

- **macOS : faisable.** Le Perchoir devient un NSPanel. Le compagnon natif existe déjà (Coucou, en Swift) et des desktop pets Tauri tournent sur macOS ([deskpet](https://github.com/Scyyyy4/deskpet), [tutoriel CrabNebula](https://crabnebula.dev/blog/building-a-desktop-pet-with-tauri/)). Coûts : compte Developer ID, signature du sidecar, pas d'App Store, permission « Enregistrement de l'écran » si on veut le titre de la fenêtre active.
- **Linux : difficile, par niveaux.** On vise **X11 / XWayland d'abord**, où tout fonctionne. On ne promet pas Wayland natif. Sur KDE et wlroots, il faudrait layer-shell, les portails et un script KWin ; sur GNOME, XWayland plus une extension optionnelle. Signal d'alerte : Shijima-Qt, un desktop pet Linux, a été abandonné par son auteur sur ces problèmes.

## 8. Règle de conception (dès le Sprint 1)

Coût quasi nul maintenant, et évite une réécriture du shell plus tard. Ces règles sont dans les critères d'acceptation de US-012, US-020, US-021, US-024, US-030, US-013 et US-071 :

1. **Fonctions de plateforme optionnelles.** Le curseur global, la fenêtre active, les hotkeys globales, le tray, la position de fenêtre et le « toujours au-dessus » sont des fonctions de plateforme. Au démarrage, le shell déclare à l'UI et au moteur celles qui sont disponibles. Rien ne suppose qu'elles le sont. Exemple, US-021 : sans curseur global, les yeux suivent le curseur seulement au survol du Perchoir.
2. **Le code du Perchoir passe par une interface par plateforme** (et par type de session sous Linux), au lieu d'être dispersé dans `main.rs`.
3. **Aucun chemin Windows en dur dans le moteur** : le shell fournit les répertoires (`~/.owlcy`, `%APPDATA%\Owlcy`).

## 9. Coût d'un portage (après la v0.4)

Par OS : refaire W1 (Perchoir) et W2 (RAM) en spike, puis environ un sprint de shell et de packaging, et une CI en matrice. Points ⚪ à vérifier en premier sur un Mac réel : `tauri-nspanel` sous macOS 27, la signature du sidecar Bun et la notarisation avec `externalBin`.
