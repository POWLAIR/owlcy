// Serveur MCP minimal (SDK TS v2) pour T5 : deux outils fichiers simulés
import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { z } from "zod";

const files = new Set(["notes.txt", "todo.md", "photo.png"]);
serveStdio(() => {
  const s = new McpServer({ name: "owlcy-t5-fs", version: "0.0.1" }, { capabilities: { tools: {} } });
  s.registerTool("list_files", { description: "Liste les fichiers du dossier courant", inputSchema: z.object({}) },
    async () => ({ content: [{ type: "text", text: JSON.stringify([...files]) }] }));
  s.registerTool("move_file", { description: "Déplace un fichier dans un dossier", inputSchema: z.object({ file: z.string(), folder: z.string() }) },
    async ({ file, folder }) => {
      console.error(`[srv] move_file ${file} -> ${folder}`);
      if (!files.has(file)) return { isError: true, content: [{ type: "text", text: `introuvable : ${file}` }] };
      files.delete(file);
      return { content: [{ type: "text", text: `déplacé : ${file} → ${folder}/` }] };
    });
  return s;
});
