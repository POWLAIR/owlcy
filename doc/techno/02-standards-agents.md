# Standards à adopter : MCP, MCP Apps, Agent Skills

Conclusion de la veille : **ne pas inventer de format propriétaire** pour les capacités du bot. Trois standards couvrent 90 % du besoin.

## 1. MCP — Model Context Protocol (la couche « connexion »)

- **Spec actuelle : 2026-07-28** (GA). Grands changements :
  - **Protocole sans état** : plus de handshake `initialize`, chaque requête décrit sa version et ses capacités dans `_meta`. Beaucoup plus simple pour un hôte qui gère **plein de petits serveurs locaux**, ce qui est exactement le cas d'Owlcy.
  - **MRTR (requêtes multi-allers-retours)** : un outil peut répondre `input_required` pour demander une confirmation en cours d'appel → c'est notre **bulle de validation**, en natif.
  - Extension **Tasks** (`tasks/get`, `tasks/update`, `subscriptions/listen`) → tâches longues avec progression → animation de la chouette.
  - `ttlMs` / `cacheScope` sur les listes d'outils → cache côté hôte.
  - **Dépréciés** (12 mois de transition) : Roots, Sampling, Logging, transport HTTP+SSE, Dynamic Client Registration.
- **SDK officiels de niveau 1 (Tier 1)** : TypeScript, Python, Go, C#. **Rust en bêta** → argument pour un moteur en TypeScript.

➜ **Pour Owlcy** : toute capacité d'action (API, fichiers, shell) = un serveur MCP. L'écosystème MCP existant (Notion, GitHub, système de fichiers…) devient disponible sans rien coder.

## 2. MCP Apps (la couche « UI des plugins »)

- Extension officielle (SEP-1865, spec 2026-01-26) : un outil déclare `_meta.ui.resourceUri` → l'hôte charge une ressource `ui://` (HTML/JS) dans une **iframe sandboxée** ; la communication passe par JSON-RPC via `postMessage`, et elle est auditable.
- Supporté par Claude (web/desktop), ChatGPT, Goose et VS Code.

➜ **Pour Owlcy** : remplace notre idée de `card.html` maison. Les « cartes » des intégrations (façon Coucou) = des MCP Apps. Bonus : une carte écrite pour Owlcy marche aussi dans Claude Desktop, et inversement.

## 3. Agent Skills — `SKILL.md` (la couche « savoir-faire »)

- Standard ouvert (agentskills.io), **plus de 40 plateformes** (Claude, ChatGPT/Codex, Copilot, Cursor, VS Code…).
- Un dossier avec `SKILL.md` (frontmatter `name` ≤ 64 caractères, `description` ≤ 1024 caractères) + `scripts/`, `references/`, `assets/` optionnels.
- **Divulgation progressive** : ≈100 tokens par skill en permanence, le corps n'est chargé que si la description correspond → on peut installer des dizaines de skills sans exploser le contexte.
- Complémentaire de MCP : **MCP = accès**, **Skill = procédure / jugement**.
- ⚠️ Qualité : une étude de 2026 trouve des « skill smells » dans plus de 99 % de 238 skills réelles, et un audit Snyk trouve des failles dans 36 % des skills communautaires.

➜ **Pour Owlcy** : les Owls en mode agent chargent des `SKILL.md`. Tes skills Claude existantes (montées de version Symfony…) deviendraient réutilisables telles quelles.

## 4. Hooks Claude Code (pour l'Owl « Mécano »)

- 27+ événements (`PreToolUse`, `PostToolUse`, `PermissionRequest`, `Notification`, `Stop`, `SubagentStart`…).
- 5 types de handler, dont **`http`** : Claude Code peut POSTer directement vers un endpoint local d'Owlcy, sans script intermédiaire.
- `PermissionRequest` peut renvoyer `allow` / `deny`, et même modifier l'entrée → validation depuis la chouette, comme Coucou.
- À garder du modèle Coucou : **si Owlcy ne répond pas → sortie immédiate**, Claude Code n'est jamais bloqué.

## Conséquence sur le vocabulaire Owlcy

Le mot « skill » avait chez nous le sens d'« action atomique ». Pour éviter la collision avec le standard :

| Ancien terme Owlcy | Nouveau terme | Implémentation |
|---|---|---|
| Skill (action) | **Outil** (*tool*), regroupés en **Intégrations** | Serveur MCP |
| — | **Skill** | `SKILL.md` (standard) |
| Carte UI de skill | **Carte** | MCP App (`ui://`) |

Détail dans [`feature/00-concepts.md`](../feature/00-concepts.md) et [`architecture/01-systeme-extension.md`](../architecture/01-systeme-extension.md).

## Sources

- [Spec MCP 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) · [Feuille de route MCP](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)
- [MCP Apps — spec](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx) · [WorkOS](https://workos.com/blog/2026-01-27-mcp-apps) · [SEP-1865](https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp)
- [Agent Skills — format et adoption](https://atlan.com/know/ai-agent/ai-agent-skills/what-are-agent-skills/) · [Rapport écosystème 2026](https://agentman.ai/blog/agent-skills-ecosystem-report-2026)
- [Hooks Claude Code — référence 2026](https://thepromptshelf.dev/blog/claude-code-hooks-complete-reference-2026/) · [Référence des événements](https://cc.bruniaux.com/guide/hooks-events-reference/)
