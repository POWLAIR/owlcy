// Serveur MCP (SDK TS v2) : un outil qui demande une validation humaine via MRTR (input_required).
// serveStdio(factory) est nécessaire pour servir la révision 2026-07-28 en stdio ;
// la même factory sert aussi les clients 2025 (le SDK traduit input_required en élicitation classique).
import { McpServer, inputRequired, acceptedContent } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { z } from "zod";

serveStdio(() => {
  const server = new McpServer({ name: "owlcy-t7", version: "0.0.1" }, { capabilities: { tools: {} } });
  server.registerTool(
    "move_file",
    { description: "Déplace un fichier (demande confirmation)", inputSchema: z.object({ from: z.string(), to: z.string() }) },
    async ({ from, to }, ctx) => {
      console.error(`[srv] tools/call move_file, inputResponses=${JSON.stringify(ctx.mcpReq.inputResponses ?? null)}`);
      const ok = acceptedContent<{ confirm: boolean }>(ctx.mcpReq.inputResponses, "confirm");
      if (!ok) {
        return inputRequired({
          inputRequests: {
            confirm: inputRequired.elicit({
              message: `Déplacer ${from} vers ${to} ?`,
              requestedSchema: { type: "object", properties: { confirm: { type: "boolean" } }, required: ["confirm"] },
            }),
          },
        });
      }
      return { content: [{ type: "text", text: ok.confirm ? `déplacé : ${from} → ${to}` : "refusé par l'utilisateur" }] };
    },
  );
  return server;
});
