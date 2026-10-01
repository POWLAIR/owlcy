// T5 — AI SDK 7 + provider Ollama + outils MCP (stdio) + needsApproval
// Usage : bun t5-aisdk-ollama-mcp.ts [modèle]   (défaut qwen3:4b, Ollama sur OLLAMA_HOST ou localhost:11434)
//         bun t5-aisdk-ollama-mcp.ts --mock     (valide la chaîne sans Ollama)
import { generateText, stepCountIs, type ModelMessage } from "ai";
import { createMCPClient } from "@ai-sdk/mcp";
import { Experimental_StdioMCPTransport as StdioMCPTransport } from "@ai-sdk/mcp/mcp-stdio";
import { createOllama } from "ai-sdk-ollama";
import { MockLanguageModelV4 } from "ai/test";

const arg = process.argv[2] ?? "qwen3:4b";
const mock = arg === "--mock";
const out: Record<string, unknown> = { model: mock ? "mock" : arg };

function mockModel() {
  let turn = 0;
  const usage = { inputTokens: { total: 1, noCache: 1, cacheRead: 0, cacheWrite: 0 }, outputTokens: { total: 1, text: 1, reasoning: 0 } };
  return new MockLanguageModelV4({
    doGenerate: async () => {
      turn++;
      if (turn === 1) return { content: [{ type: "tool-call", toolCallId: "c1", toolName: "list_files", input: "{}" }], finishReason: { unified: "tool-calls", raw: "tool_calls" }, usage, warnings: [] } as any;
      if (turn === 2) return { content: [{ type: "tool-call", toolCallId: "c2", toolName: "move_file", input: JSON.stringify({ file: "notes.txt", folder: "archive" }) }], finishReason: { unified: "tool-calls", raw: "tool_calls" }, usage, warnings: [] } as any;
      return { content: [{ type: "text", text: "C'est fait : notes.txt est dans archive/." }], finishReason: { unified: "stop", raw: "stop" }, usage, warnings: [] } as any;
    },
  });
}

const t0 = performance.now();
const mcp = await createMCPClient({ transport: new StdioMCPTransport(process.env.T5_SERVER_EXE ? { command: process.env.T5_SERVER_EXE, args: [], stderr: "inherit" } : { command: "bun", args: ["t5-server.ts"], stderr: "inherit" }) });
const mcpTools = await mcp.tools();
out.mcp_connect_ms = +(performance.now() - t0).toFixed(1);
out.mcp_tools = Object.keys(mcpTools);
const tools = { ...mcpTools, move_file: { ...mcpTools.move_file, needsApproval: true } };

const model = mock ? mockModel() : createOllama({ baseURL: process.env.OLLAMA_HOST ?? "http://localhost:11434" })(arg);
const instructions = "Tu es une chouette assistante. Utilise les outils. Réponds en français, brièvement.";
const messages: ModelMessage[] = [
  { role: "user", content: "Regarde les fichiers puis range notes.txt dans le dossier archive." },
];

// Tour 1 : le modèle doit lister puis demander move_file → l'exécution doit s'arrêter sur une demande d'approbation
const t1 = performance.now();
const r1 = await generateText({ model, instructions, tools, messages, stopWhen: stepCountIs(5) });
out.turn1_ms = +(performance.now() - t1).toFixed(0);
out.turn1_tool_calls = r1.steps.flatMap((s) => s.toolCalls.map((c) => ({ tool: c.toolName, input: c.input })));
const approvals = r1.content.filter((p) => p.type === "tool-approval-request") as any[];
out.approval_requested = approvals.map((a) => ({ tool: a.toolCall.toolName, input: a.toolCall.input }));
out.move_executed_before_approval = r1.steps.some((s) => s.toolResults.some((t) => t.toolName === "move_file"));

// Tour 2 : l'utilisateur approuve (≈ bouton « Autoriser » de la bulle) → l'outil MCP s'exécute
if (approvals.length) {
  messages.push(...r1.response.messages, { role: "tool", content: approvals.map((a) => ({ type: "tool-approval-response" as const, approvalId: a.approvalId, approved: true })) });
  const t2 = performance.now();
  const r2 = await generateText({ model, instructions, tools, messages, stopWhen: stepCountIs(5) });
  out.turn2_ms = +(performance.now() - t2).toFixed(0);
  out.final_text = r2.text;
  out.usage = r2.totalUsage;
}
// Preuve côté serveur : l'état après coup (notes.txt ne doit plus être listé)
const after: any = await (mcpTools.list_files as any).execute({}, { toolCallId: "check", messages: [] });
out.files_after = JSON.parse(after.content[0].text);
out.moved = !out.files_after.includes("notes.txt");
await mcp.close();
out.verdict = approvals.length > 0 && !out.move_executed_before_approval && out.moved ? "GO" : "À ANALYSER";
console.log(JSON.stringify(out, null, 2));
