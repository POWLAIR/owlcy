// T7 — SDK MCP TS v2 : le serveur renvoie input_required (MRTR, spec 2026-07-28), le client le gère
import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";

const params = { command: "bun", args: ["t7-server.ts"], stderr: "inherit" as const };
const neg = { versionNegotiation: { mode: (process.argv[2] === "pin" ? { pin: "2026-07-28" } : process.argv[2] ?? "auto") as any } };
const out: Record<string, unknown> = {};

// 1) Mode manuel : on doit voir le résultat input_required brut
{
  const c = new Client({ name: "t7-manual", version: "0" }, { ...neg, capabilities: { elicitation: { form: {} } }, inputRequired: { autoFulfill: false } });
  const t0 = performance.now();
  await c.connect(new StdioClientTransport(params));
  out.connect_ms = +(performance.now() - t0).toFixed(1);
  out.protocol_version = c.getNegotiatedProtocolVersion();
  const r: any = await c.callTool({ name: "move_file", arguments: { from: "a.txt", to: "b.txt" } }, { allowInputRequired: true } as any);
  out.manual_result_type = r.resultType ?? (r.inputRequests ? "input_required" : "complete");
  out.manual_input_request_keys = Object.keys(r.inputRequests ?? {});
  out.manual_message = r.inputRequests?.confirm?.params?.message;
  await c.close();
}

// 2) Mode auto : le client répond à l'élicitation (≈ bulle de la chouette) et relance l'appel
for (const answer of [true, false]) {
  const c = new Client({ name: "t7-auto", version: "0" }, { ...neg, capabilities: { elicitation: { form: {} } } });
  let asked = "";
  c.setRequestHandler("elicitation/create" as any, async (req: any) => {
    asked = req.params.message;
    return { action: "accept", content: { confirm: answer } };
  });
  await c.connect(new StdioClientTransport(params));
  const t0 = performance.now();
  const r: any = await c.callTool({ name: "move_file", arguments: { from: "a.txt", to: "b.txt" } });
  out[`auto_${answer ? "accept" : "refuse"}`] = { protocol_version: c.getNegotiatedProtocolVersion(), asked, text: r.content?.[0]?.text, roundtrip_ms: +(performance.now() - t0).toFixed(1) };
  await c.close();
}
console.log(JSON.stringify(out, null, 2));
