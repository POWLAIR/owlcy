# Système d'extension — « ajouter une capacité en 5 minutes »

> **Révision v2 (30/09/2026)** : on abandonne le format de manifeste 100 % maison au profit de **MCP + MCP Apps + Agent Skills**, avec un fin fichier `owlcy.yaml` en complément. Justification : [`techno/02-standards-agents.md`](../techno/02-standards-agents.md).

## Les 3 règles d'or

1. **Un dossier = une extension.** Déposé dans `integrations/`, `skills/`, `pipelines/`, `owls/` ou `skins/`, il est détecté, validé (JSON Schema) et rechargé à chaud.
2. **Pas de format propriétaire quand un standard existe.**
3. **Rien ne s'active sans que tu aies vu ses permissions.**

## A. Intégration (serveur MCP)

### Cas 1 : réutiliser un serveur MCP existant (0 ligne de code)

```yaml
# integrations/notion/owlcy.yaml
id: notion
mcp:
  command: npx
  args: ["-y", "@notionhq/notion-mcp-server"]
  env: { NOTION_TOKEN: secret-ref:notion }
target: windows            # windows | wsl
permissions: [network, secrets:notion]
ui:
  icon: notion
  pill: "${pages_today} pages"
```

### Cas 2 : écrire sa propre intégration (Python, SDK MCP officiel)

```python
# integrations/rss/server.py
from mcp.server.fastmcp import FastMCP
import feedparser

mcp = FastMCP("rss")

@mcp.tool()
def fetch(url: str, since_hours: int = 24) -> list[dict]:
    """Récupère les entrées d'un flux RSS/Atom."""
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link, "summary": e.get("summary", "")}
            for e in feed.entries]

if __name__ == "__main__":
    mcp.run()   # stdio
```

```yaml
# integrations/rss/owlcy.yaml
id: rss
mcp: { command: uv, args: ["run", "server.py"] }
permissions: [network]
trust: untrusted-output        # le contenu renvoyé vient du web → marqué non fiable
```

- Isolation Python : **uv** (un environnement par intégration).
- SDK officiels de niveau 1 : TypeScript, Python, Go, C#. Un script PHP ou bash peut aussi être enveloppé.
- **Intégration WSL** : `target: wsl` → Owlcy lance `wsl.exe -e uv run server.py` ; MCP en stdio traverse sans souci.

### Carte UI (MCP Apps)

L'outil déclare `_meta.ui.resourceUri: ui://rss/digest` → Owlcy affiche le HTML dans une iframe sandboxée, dans le dashboard ou dans une bulle. La même carte fonctionne dans Claude Desktop.

## B. Skill (`SKILL.md`, standard Agent Skills)

```markdown
---
name: veille-techno
description: Faire une veille techno de qualité à partir d'articles bruts — filtrer, dédupliquer, résumer en 5 points avec sources. À utiliser pour tout digest de veille.
---
# Veille techno
1. Écarter les articles promotionnels ou sans source primaire.
2. Regrouper les doublons (même annonce, plusieurs sites).
…
```

Utilisée par les Owls en mode agent et par les étapes `agent:` des pipelines. Tes skills Claude existantes (montées de version Symfony, etc.) se déposent telles quelles.

## C. Owl, Pipeline, Skin

Du **YAML pur**, sans code : voir [`feature/01-owls.md`](../feature/01-owls.md), [`feature/02-pipelines-factory.md`](../feature/02-pipelines-factory.md) et [`design/01-systeme-mascottes.md`](../design/01-systeme-mascottes.md).

## D. Points d'extension avancés (core)

| Point | Mécanisme |
|---|---|
| Provider LLM | Adaptateur AI SDK (Ollama, Anthropic, OpenAI… déjà fournis) |
| Trigger | Module TS du moteur (`triggers/*.ts`) |
| Hook externe | Endpoint local + adaptateur (Claude Code en premier, via handler `http`) |
| Emote / son | Dans le skin |

## E. Auto-extension (la Forgeronne)

1. Tu décris : « une intégration qui liste mes MR GitLab ouvertes ».
2. Elle cherche d'abord **un serveur MCP existant** ; sinon, elle génère `server.py` + `owlcy.yaml` + un test.
3. Scan statique + exécution **dry-run** avec permissions minimales.
4. Diff + résultat du test présentés dans le dashboard → **validation humaine** → activation.

Aides pour que l'IA produise du bon travail : JSON Schemas publiés, gabarits d'exemple, un `CLAUDE.md` / `AGENTS.md` à la racine du repo Owlcy.

## F. Paquets partageables

`package.yaml` (nom, version, auteur, contenu, **permissions demandées**, signature). Installation : scan → écran de permissions → validation. Pas de registre public avant d'avoir la signature et le scan (leçon ClawHub).
