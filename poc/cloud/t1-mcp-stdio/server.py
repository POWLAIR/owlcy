"""Serveur MCP minimal (FastMCP, SDK Python officiel) pour le test T1."""
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel

mcp = FastMCP("owlcy-test")


@mcp.tool()
def echo(text: str) -> str:
    """Renvoie le texte (mesure de latence aller-retour)."""
    return text


@mcp.tool()
def fetch_items(n: int = 20) -> list[dict]:
    """Simule une intégration type RSS : renvoie n éléments."""
    return [{"title": f"Article {i}", "link": f"https://ex.org/{i}"} for i in range(n)]


class Confirm(BaseModel):
    approve: bool


@mcp.tool()
async def move_file(src: str, dst: str, ctx: Context) -> str:
    """Action sensible : demande une validation humaine via elicitation."""
    res = await ctx.elicit(message=f"Déplacer {src} vers {dst} ?", schema=Confirm)
    if res.action == "accept" and res.data.approve:
        return "moved"
    return "refused"


if __name__ == "__main__":
    mcp.run()  # stdio
