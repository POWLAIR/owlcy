// Spike W1 — Perchoir Owlcy sous Windows.
// Vérifie : petite fenêtre transparente toujours au-dessus, qui ne vole JAMAIS le focus,
// click-through hors de la chouette (hit-test), pas de détection « plein écran » par Windows,
// yeux qui suivent le curseur sur tout l'écran, icône de tray.
//
// ⚠️ Écrit sans pouvoir être compilé dans l'environnement de conception (crates.io bloqué) :
//    corriger les éventuelles erreurs de compilation fait partie du spike.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::Deserialize;
use std::sync::Mutex;
use std::time::Duration;
use tauri::menu::{Menu, MenuItem};
use tauri::tray::TrayIconBuilder;
use tauri::{Emitter, Manager, PhysicalPosition, State, WebviewUrl, WebviewWindow, WebviewWindowBuilder};

/// Zones cliquables (en pixels CSS, relatives à la fenêtre) envoyées par le front.
#[derive(Deserialize, Clone, Debug)]
struct Rect { x: f64, y: f64, w: f64, h: f64 }

struct HitRegions(Mutex<Vec<Rect>>);

#[tauri::command]
fn set_hit_regions(state: State<HitRegions>, regions: Vec<Rect>) {
    *state.0.lock().unwrap() = regions;
}

/// Styles Win32 que tao ne gère pas : WS_EX_TOOLWINDOW (pas d'Alt+Tab) et la propriété NonRudeHWND
/// (ne pas être traité comme une appli plein écran).
/// ⚠️ Constat W1 : tao recalcule et RÉÉCRIT tous les styles étendus à chaque changement d'état
/// (ex. set_ignore_cursor_events). WS_EX_NOACTIVATE passe donc par `focusable(false)` (géré par tao),
/// et WS_EX_TOOLWINDOW doit être réappliqué après chaque bascule du hit-test.
#[cfg(windows)]
fn apply_win32(win: &WebviewWindow) {
    use windows_sys::Win32::Foundation::HWND;
    use windows_sys::Win32::UI::WindowsAndMessaging::*;
    let Ok(h) = win.hwnd() else { return };
    let hwnd = h.0 as HWND;
    unsafe {
        let ex = GetWindowLongPtrW(hwnd, GWL_EXSTYLE);
        let want = ex | WS_EX_TOOLWINDOW as isize;
        if want != ex {
            SetWindowLongPtrW(hwnd, GWL_EXSTYLE, want);
        }
        let name: Vec<u16> = "NonRudeHWND\0".encode_utf16().collect();
        SetPropW(hwnd, name.as_ptr(), 1usize as _);
    }
}

#[cfg(not(windows))]
fn apply_win32(_win: &WebviewWindow) {}

fn main() {
    tauri::Builder::default()
        .manage(HitRegions(Mutex::new(vec![])))
        .invoke_handler(tauri::generate_handler![set_hit_regions])
        .setup(|app| {
            // 1. Petite fenêtre dimensionnée au contenu (JAMAIS plein écran : cf. carnac #12, tauri #7328)
            let win = WebviewWindowBuilder::new(app, "perch", WebviewUrl::App("index.html".into()))
                .title("Owlcy")
                .inner_size(260.0, 300.0)
                .decorations(false)
                .transparent(true)
                .always_on_top(true)
                .skip_taskbar(true)
                .resizable(false)
                .shadow(false)
                .focused(false)
                .focusable(false) // WS_EX_NOACTIVATE, conservé par tao
                .visible(false)
                .build()?;

            // 2. Position : coin bas-droit, au-dessus de la barre des tâches, décalé des bords
            if let Some(m) = win.primary_monitor()? {
                let s = m.size();
                let w = win.outer_size()?;
                let x = s.width as i32 - w.width as i32 - 24;
                let y = s.height as i32 - w.height as i32 - 64;
                win.set_position(PhysicalPosition::new(x, y))?;
            }
            win.show()?; // tao : SW_SHOWNOACTIVATE car focused(false)
            apply_win32(&win);

            // 3. Hit-test ~60 Hz : click-through partout sauf sur les zones déclarées par le front.
            //    Émet aussi la position du curseur (repère fenêtre) pour les yeux, à ~30 Hz.
            let w2 = win.clone();
            let handle = app.handle().clone();
            std::thread::spawn(move || {
                let mut ignoring: Option<bool> = None;
                let mut tick: u64 = 0;
                loop {
                    std::thread::sleep(Duration::from_millis(16));
                    tick += 1;
                    let (Ok(c), Ok(p), Ok(scale)) = (w2.cursor_position(), w2.outer_position(), w2.scale_factor()) else { continue };
                    let lx = (c.x - p.x as f64) / scale;
                    let ly = (c.y - p.y as f64) / scale;
                    let regions = handle.state::<HitRegions>().0.lock().unwrap().clone();
                    let inside = regions.iter().any(|r| lx >= r.x && lx <= r.x + r.w && ly >= r.y && ly <= r.y + r.h);
                    if ignoring != Some(!inside) {
                        let _ = w2.set_ignore_cursor_events(!inside);
                        apply_win32(&w2); // tao vient de réécrire les styles étendus
                        ignoring = Some(!inside);
                    }
                    if tick % 2 == 0 {
                        let _ = w2.emit("cursor", (lx, ly));
                    }
                }
            });

            // 4. Tray : quitter + ouvrir la page de labo (test MCP Apps dans WebView2)
            let quit = MenuItem::with_id(app, "quit", "Quitter", true, None::<&str>)?;
            let labo = MenuItem::with_id(app, "labo", "Labo : carte MCP Apps", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&labo, &quit])?;
            TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .tooltip("Owlcy — spike perchoir")
                .menu(&menu)
                .on_menu_event(|app, e| match e.id.as_ref() {
                    "quit" => app.exit(0),
                    "labo" => {
                        let _ = WebviewWindowBuilder::new(app, "labo", WebviewUrl::App("labo.html".into()))
                            .title("Owlcy — labo MCP Apps")
                            .inner_size(560.0, 420.0)
                            .build();
                    }
                    _ => {}
                })
                .build(app)?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("erreur au lancement du spike");
}
