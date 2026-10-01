"""T1 — Client MCP : N serveurs stdio en parallèle, latence, mémoire, elicitation."""
import asyncio, json, os, statistics, sys, time
from contextlib import AsyncExitStack

import psutil
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

HERE = os.path.dirname(os.path.abspath(__file__))
N_SERVERS = int(os.environ.get("N", "10"))
N_CALLS = 200


async def on_elicit(ctx, params: types.ElicitRequestParams):
    # Simule la bulle de validation : l'utilisateur clique « Autoriser »
    return types.ElicitResult(action="accept", content={"approve": True})


async def main():
    results = {}
    async with AsyncExitStack() as stack:
        t0 = time.perf_counter()

        async def start():
            params = StdioServerParameters(command=sys.executable, args=[os.path.join(HERE, "server.py")])
            r, w = await stack.enter_async_context(stdio_client(params))
            s = await stack.enter_async_context(ClientSession(r, w, elicitation_callback=on_elicit))
            init = await s.initialize()
            tools = await s.list_tools()
            return s, init, tools

        sessions = []
        for _ in range(N_SERVERS):  # démarrage séquentiel (enter_async_context non concurrent)
            sessions.append(await start())
        results["startup_total_s"] = round(time.perf_counter() - t0, 3)
        results["startup_per_server_ms"] = round(results["startup_total_s"] / N_SERVERS * 1000, 1)
        results["protocol_version"] = sessions[0][1].protocolVersion
        results["tools"] = [t.name for t in sessions[0][2].tools]

        # Mémoire des processus enfants (serveurs)
        me = psutil.Process()
        kids = me.children(recursive=True)
        rss = [k.memory_info().rss / 1e6 for k in kids]
        results["servers_rss_mb_each_median"] = round(statistics.median(rss), 1)
        results["servers_rss_mb_total"] = round(sum(rss), 1)

        # Latence d'appel d'outil
        s = sessions[0][0]
        lat = []
        for i in range(N_CALLS):
            t = time.perf_counter()
            await s.call_tool("echo", {"text": f"ping {i}"})
            lat.append((time.perf_counter() - t) * 1000)
        results["echo_latency_ms_p50"] = round(statistics.median(lat), 2)
        results["echo_latency_ms_p95"] = round(sorted(lat)[int(0.95 * N_CALLS)], 2)

        # Charge utile plus grosse
        t = time.perf_counter()
        r = await s.call_tool("fetch_items", {"n": 500})
        results["fetch_500_items_ms"] = round((time.perf_counter() - t) * 1000, 1)
        results["fetch_structured_ok"] = r.structuredContent is not None

        # Appels concurrents sur tous les serveurs
        t = time.perf_counter()
        await asyncio.gather(*[x[0].call_tool("echo", {"text": "x"}) for x in sessions])
        results["parallel_call_all_servers_ms"] = round((time.perf_counter() - t) * 1000, 1)

        # Human-in-the-loop via elicitation
        t = time.perf_counter()
        r = await s.call_tool("move_file", {"src": "a.pdf", "dst": "Docs/"})
        results["elicitation_result"] = r.content[0].text
        results["elicitation_roundtrip_ms"] = round((time.perf_counter() - t) * 1000, 1)

    print(json.dumps(results, indent=2, ensure_ascii=False))


asyncio.run(main())
