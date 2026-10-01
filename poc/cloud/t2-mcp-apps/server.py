"""Serveur MCP exposant un outil + une ressource UI (ui://) façon MCP Apps."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("veille-ui")

CARD = """<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src data:">
<style>body{font-family:sans-serif;margin:8px}li{margin:2px 0}button{margin-top:6px}</style></head><body>
<h3>Digest de veille</h3><ul id="list"><li>…</li></ul><button id="more">Charger 5 de plus</button>
<pre id="probe"></pre>
<script>
let id = 0; const pending = {};
function rpc(method, params){ return new Promise(r => { const i = ++id; pending[i] = r; parent.postMessage({jsonrpc:"2.0", id:i, method, params}, "*"); }); }
addEventListener("message", e => {
  const m = e.data;
  if (m.id && pending[m.id]) { pending[m.id](m.result); delete pending[m.id]; }
  if (m.method === "ui/notifications/tool-result") render(m.params.structuredContent.result);
});
function render(items){ document.getElementById("list").innerHTML = items.map(x => `<li>${x.title}</li>`).join(""); }
document.getElementById("more").onclick = async () => { const r = await rpc("tools/call", {name:"digest", arguments:{n:5}}); render(r.structuredContent.result); };
(async () => {
  const init = await rpc("ui/initialize", {appInfo:{name:"veille-card"}});
  const probe = {};
  try { probe.parentDom = !!parent.document.body; } catch (e) { probe.parentDom = "bloqué"; }
  try { await fetch("https://example.org"); probe.fetch = "autorisé"; } catch (e) { probe.fetch = "bloqué"; }
  try { localStorage.setItem("x","1"); probe.localStorage = "autorisé"; } catch (e) { probe.localStorage = "bloqué"; }
  probe.theme = init.hostContext.theme;
  document.getElementById("probe").textContent = JSON.stringify(probe);
  parent.postMessage({jsonrpc:"2.0", method:"test/probe", params: probe}, "*");
})();
</script></body></html>"""


@mcp.resource("ui://veille/digest", mime_type="text/html;profile=mcp-app")
def digest_card() -> str:
    return CARD


@mcp.tool(meta={"ui": {"resourceUri": "ui://veille/digest"}})
def digest(n: int = 3) -> list[dict]:
    """Renvoie les n derniers articles de veille."""
    return [{"title": f"Article de veille n°{i+1}"} for i in range(n)]


if __name__ == "__main__":
    mcp.run()
