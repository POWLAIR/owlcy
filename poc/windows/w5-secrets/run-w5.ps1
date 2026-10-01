$env:PYTHONIOENCODING = "utf-8"
$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
& $py -m pip install --quiet --disable-pip-version-check --no-warn-script-location keyring
$psi = New-Object Diagnostics.ProcessStartInfo $py, "-u test_keyring.py"
$psi.WorkingDirectory = $PSScriptRoot; $psi.UseShellExecute = $false
$psi.RedirectStandardInput = $true; $psi.RedirectStandardOutput = $true
$p = [Diagnostics.Process]::Start($psi)
"> " + $p.StandardOutput.ReadLine(); "> " + $p.StandardOutput.ReadLine()
Start-Sleep -Milliseconds 500
"--- cmdkey pendant le test :"; cmdkey /list | Select-String -Context 0,3 "owlcy-test"
$p.StandardInput.WriteLine(""); $p.WaitForExit(10000) | Out-Null
$p.StandardOutput.ReadToEnd() -split "`n" | % { "> $_" }
"exit=$($p.ExitCode)"
"--- cmdkey après le test :"; if (cmdkey /list | Select-String "owlcy-test") { "ENCORE PRÉSENTE" } else { "absente (OK)" }
