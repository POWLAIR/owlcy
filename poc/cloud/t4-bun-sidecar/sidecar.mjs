import readline from "node:readline";
const rl = readline.createInterface({ input: process.stdin });
rl.on("line", (line) => { if (!line.trim()) return; const req = JSON.parse(line);
  process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id: req.id, result: req.method === "ping" ? "pong" : { echo: req.params } }) + "\n"); });
