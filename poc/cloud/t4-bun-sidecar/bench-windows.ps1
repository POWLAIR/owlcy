# Banc T4 sous Windows : démarrage -> 1re réponse, RTT sur 2000 échos, mémoire privée
$exe = Join-Path $PSScriptRoot 'owlcy-engine.exe'
$psi = New-Object System.Diagnostics.ProcessStartInfo $exe
$psi.UseShellExecute = $false; $psi.RedirectStandardInput = $true; $psi.RedirectStandardOutput = $true
$sw = [Diagnostics.Stopwatch]::StartNew()
$p = [Diagnostics.Process]::Start($psi)
$p.StandardInput.WriteLine('{"jsonrpc":"2.0","id":0,"method":"ping"}'); $p.StandardInput.Flush()
[void]$p.StandardOutput.ReadLine(); $first = $sw.Elapsed.TotalMilliseconds
$lat = New-Object System.Collections.Generic.List[double]
for ($i = 1; $i -le 2000; $i++) {
  $t = [Diagnostics.Stopwatch]::StartNew()
  $p.StandardInput.WriteLine("{`"jsonrpc`":`"2.0`",`"id`":$i,`"method`":`"echo`",`"params`":{`"i`":$i}}"); $p.StandardInput.Flush()
  [void]$p.StandardOutput.ReadLine(); $lat.Add($t.Elapsed.TotalMilliseconds)
}
$p.Refresh(); $priv = $p.PrivateMemorySize64 / 1MB; $ws = $p.WorkingSet64 / 1MB
$p.StandardInput.Close(); $p.WaitForExit(3000) | Out-Null
$s = $lat | Sort-Object
[pscustomobject]@{
  runtime = 'bun compiled (windows-x64)'; cold_start_to_first_reply_ms = [math]::Round($first, 1)
  private_mb = [math]::Round($priv, 1); working_set_mb = [math]::Round($ws, 1)
  rtt_ms_p50 = [math]::Round($s[1000], 3); rtt_ms_p95 = [math]::Round($s[1900], 3)
  exe_mb = [math]::Round((Get-Item $exe).Length / 1MB, 1)
} | ConvertTo-Json
