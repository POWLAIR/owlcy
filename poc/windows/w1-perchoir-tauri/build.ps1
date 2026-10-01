$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
Set-Location $PSScriptRoot
"rustc: " + (rustc --version); "cargo: " + (cargo --version); "node: " + (node -v)
if (-not (Test-Path src-tauri\icons\icon.ico)) { npx --yes @tauri-apps/cli@2 icon owl-icon.png -o src-tauri/icons 2>&1 | Select-Object -Last 3 }
Set-Location src-tauri
$sw = [Diagnostics.Stopwatch]::StartNew()
cargo build --release 2>&1 | ForEach-Object { "$_" } | Select-String -Pattern "^(error|warning: unused|\s+-->|\s+\|)|Finished|error\[" | Select-Object -First 80
"duree_s=" + [math]::Round($sw.Elapsed.TotalSeconds)
"exit=$LASTEXITCODE"
