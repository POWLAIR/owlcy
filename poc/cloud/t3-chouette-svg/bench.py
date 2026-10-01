"""T3 — Coût CPU de la chouette SVG procédurale dans Chromium (moteur de WebView2)."""
import json, pathlib, time
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
URL = (HERE / "owl.html").as_uri()


def cpu_ms_per_s(cdp, page, seconds=5.0, move_mouse=False):
    m0 = {m["name"]: m["value"] for m in cdp.send("Performance.getMetrics")["metrics"]}
    t0 = time.time()
    while time.time() - t0 < seconds:
        if move_mouse:
            x = 100 + int((time.time() - t0) * 200) % 500
            page.mouse.move(x, 120)
        page.wait_for_timeout(50)
    m1 = {m["name"]: m["value"] for m in cdp.send("Performance.getMetrics")["metrics"]}
    dt = time.time() - t0
    return {
        "task_ms_per_s": round((m1["TaskDuration"] - m0["TaskDuration"]) * 1000 / dt, 2),
        "script_ms_per_s": round((m1["ScriptDuration"] - m0["ScriptDuration"]) * 1000 / dt, 2),
        "layout_ms_per_s": round((m1["LayoutDuration"] - m0["LayoutDuration"]) * 1000 / dt, 2),
        "recalc_style_ms_per_s": round((m1["RecalcStyleDuration"] - m0["RecalcStyleDuration"]) * 1000 / dt, 2),
        "js_heap_mb": round(m1["JSHeapUsedSize"] / 1e6, 2),
    }


with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 560, "height": 260})
    page.goto(URL)
    cdp = page.context.new_cdp_session(page)
    cdp.send("Performance.enable")
    page.wait_for_timeout(500)
    res = {
        "chromium_version": b.version,
        "3_chouettes_idle_60fps": cpu_ms_per_s(cdp, page),
        "3_chouettes_suivi_curseur": cpu_ms_per_s(cdp, page, move_mouse=True),
    }
    page.evaluate("owlcy.setEmote('owlcy','happy'); owlcy.setEmote('veilleuse','thinking'); owlcy.setEmote('mecano','dizzy')")
    res["3_chouettes_emotes_actives"] = cpu_ms_per_s(cdp, page)
    page.evaluate("owlcy.pause()")
    res["animation_en_pause"] = cpu_ms_per_s(cdp, page)
    # captures
    page.evaluate("owlcy.resume(); owlcy.setEmote('owlcy','idle'); owlcy.setEmote('veilleuse','idle'); owlcy.setEmote('mecano','idle')")
    page.wait_for_timeout(300)
    page.screenshot(path=str(HERE / "capture-idle.png"))
    page.evaluate("owlcy.setEmote('owlcy','happy'); owlcy.setEmote('veilleuse','thinking'); owlcy.setEmote('mecano','sleepy')")
    page.wait_for_timeout(400)
    page.screenshot(path=str(HERE / "capture-emotes.png"))
    b.close()

(HERE / "result.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
print(json.dumps(res, indent=2, ensure_ascii=False))
