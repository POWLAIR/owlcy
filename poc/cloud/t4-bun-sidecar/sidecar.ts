// Sidecar minimal : JSON-RPC ligne par ligne sur stdio (forme d'un moteur Owlcy)
const decoder = new TextDecoder();
let buf = "";
for await (const chunk of Bun.stdin.stream()) {
  buf += decoder.decode(chunk);
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, i); buf = buf.slice(i + 1);
    if (!line.trim()) continue;
    const req = JSON.parse(line);
    const res = { jsonrpc: "2.0", id: req.id, result: req.method === "ping" ? "pong" : { echo: req.params } };
    process.stdout.write(JSON.stringify(res) + "\n");
  }
}
