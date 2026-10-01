"""W3 — Latence d'un serveur stdio lancé dans WSL via wsl.exe, vu depuis Windows.

À lancer côté WINDOWS (PowerShell), Python standard uniquement :
    python wsl_stdio_bench.py
Le script lance `wsl.exe -e python3 -u -c <serveur echo>` et mesure :
  - le démarrage à froid jusqu'à la première réponse
  - la latence aller-retour (p50 / p95) sur 2000 messages JSON-RPC
  - la même chose avec un serveur Python natif Windows (référence)
  - l'accès à un fichier Windows depuis WSL (/mnt/c) vs fichier Linux
"""
import json, statistics, subprocess, sys, time

ECHO = r"""
import sys, json
for line in sys.stdin:
    req = json.loads(line)
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": req.get("params")}) + "\n")
    sys.stdout.flush()
"""


def bench(cmd, label, n=2000):
    t = time.perf_counter()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    p.stdin.write(json.dumps({"id": 0, "params": "ping"}) + "\n"); p.stdin.flush(); p.stdout.readline()
    cold = (time.perf_counter() - t) * 1000
    lat = []
    for i in range(n):
        t = time.perf_counter()
        p.stdin.write(json.dumps({"id": i, "params": {"i": i, "pad": "x" * 200}}) + "\n"); p.stdin.flush()
        p.stdout.readline(); lat.append((time.perf_counter() - t) * 1000)
    p.stdin.close(); p.wait()
    return {"cas": label, "demarrage_froid_ms": round(cold, 1), "rtt_p50_ms": round(statistics.median(lat), 3),
            "rtt_p95_ms": round(sorted(lat)[int(n * .95)], 3)}


def fs_bench():
    script = ("import os,time;"
              "d1=os.path.expanduser('~/owlcy_fs_test');d2='/mnt/c/Users/Public/owlcy_fs_test';"
              "r={}\n"
              "for d in (d1,d2):\n"
              " os.makedirs(d,exist_ok=True);t=time.time()\n"
              " for i in range(1000): open(f'{d}/f{i}.txt','w').write('x'*100)\n"
              " for i in range(1000): open(f'{d}/f{i}.txt').read()\n"
              " r[d]=round((time.time()-t)*1000)\n"
              "print(r)")
    out = subprocess.run(["wsl.exe", "-e", "python3", "-c", script], capture_output=True, text=True)
    return out.stdout.strip() or out.stderr.strip()


if __name__ == "__main__":
    res = [bench([sys.executable, "-u", "-c", ECHO], "Python natif Windows"),
           bench(["wsl.exe", "-e", "python3", "-u", "-c", ECHO], "Python dans WSL via wsl.exe")]
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print("1000 écritures + 1000 lectures (ms) [Linux ~ vs /mnt/c] :", fs_bench())
