"""T2 — Hôte MCP Apps minimal : client MCP (Python) + page hôte Chromium + iframe sandboxée.
Protocole volontairement simplifié (ui/initialize, tools/call, ui/notifications/tool-result) :
l'AppBridge officiel (@modelcontextprotocol/ext-apps) n'a pas pu être installé (registre npm bloqué)."""
import asyncio, json, os, sys, pathlib, time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent

HOST = """<!doctype html><html><body style="font-family:sans-serif;background:#1E1B2E;color:#eee">
<p>Hôte Owlcy (dashboard)</p><div id="slot"></div>
<script>
window.probe = null;
function mount(html, initialResult){
  const f = document.createElement("iframe");
  f.setAttribute("sandbox", "allow-scripts");        // pas allow-same-origin → origine opaque
  f.style = "width:420px;height:260px;border:0;border-radius:12px;background:#FAF7FF";
  f.srcdoc = html;
  document.getElementById("slot").appendChild(f);
  addEventListener("message", async e => {
    if (e.source !== f.contentWindow) return;          // n'accepter que cette vue
    const m = e.data;
    if (m.method === "ui/initialize") {
      f.contentWindow.postMessage({jsonrpc:"2.0", id:m.id, result:{hostContext:{theme:"dark", locale:"fr-FR", platform:"desktop"}}}, "*");
      f.contentWindow.postMessage({jsonrpc:"2.0", method:"ui/notifications/tool-result", params:initialResult}, "*");
    } else if (m.method === "tools/call") {
      const r = await window.mcpCallTool(m.params.name, m.params.arguments);   // → client MCP Python
      f.contentWindow.postMessage({jsonrpc:"2.0", id:m.id, result:r}, "*");
    } else if (m.method === "test/probe") { window.probe = m.params; }
  });
}
</script></body></html>"""


async def main():
    res = {}
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")])
    async with stdio_client(params) as (r, w), ClientSession(r, w) as s:
        await s.initialize()
        tools = (await s.list_tools()).tools
        tool = next(t for t in tools if t.name == "digest")
        ui_uri = (tool.meta or {}).get("ui", {}).get("resourceUri")
        res["tool_meta_ui_resourceUri"] = ui_uri
        rsc = await s.read_resource(ui_uri)
        html = rsc.contents[0].text
        res["resource_mime"] = rsc.contents[0].mimeType
        first = await s.call_tool("digest", {"n": 3})

        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page(viewport={"width": 520, "height": 340})

            async def call_tool(name, args):
                t = time.perf_counter()
                out = await s.call_tool(name, args)
                res.setdefault("tools_call_ms", []).append(round((time.perf_counter() - t) * 1000, 1))
                return {"structuredContent": out.structuredContent}

            await page.expose_function("mcpCallTool", call_tool)
            await page.set_content(HOST)
            await page.evaluate("([h, r]) => mount(h, r)", [html, {"structuredContent": first.structuredContent}])
            await page.wait_for_function("window.probe !== null", timeout=10000)
            res["sandbox_probe"] = await page.evaluate("window.probe")
            frame = page.frames[1]
            res["items_after_initial_result"] = await frame.locator("li").count()
            await frame.click("#more")
            await frame.wait_for_function("document.querySelectorAll('li').length === 5")
            res["items_after_button_tools_call"] = await frame.locator("li").count()
            await page.screenshot(path=str(HERE / "capture-card.png"))
            res["chromium"] = b.version
            await b.close()
    (HERE / "result.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))

asyncio.run(main())
