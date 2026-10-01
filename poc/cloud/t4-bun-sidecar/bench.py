import subprocess,time,json,psutil,statistics,sys
def bench(cmd,label):
    t=time.perf_counter()
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1)
    p.stdin.write(json.dumps({"jsonrpc":"2.0","id":0,"method":"ping"})+"\n");p.stdin.flush();p.stdout.readline()
    first=(time.perf_counter()-t)*1000
    lat=[]
    for i in range(2000):
        t=time.perf_counter();p.stdin.write(json.dumps({"jsonrpc":"2.0","id":i,"method":"echo","params":{"i":i}})+"\n");p.stdin.flush();p.stdout.readline();lat.append((time.perf_counter()-t)*1000)
    rss=psutil.Process(p.pid).memory_info().rss/1e6
    p.stdin.close();p.wait()
    return {"runtime":label,"cold_start_to_first_reply_ms":round(first,1),"rss_mb":round(rss,1),"rtt_ms_p50":round(statistics.median(lat),3),"rtt_ms_p95":round(sorted(lat)[1900],3)}
out=[bench(["./owlcy-engine"],"bun compiled"),bench(["node","sidecar.mjs"],"node 22 script"),bench(["bun","sidecar.ts"],"bun script")]
print(json.dumps(out,indent=2))
