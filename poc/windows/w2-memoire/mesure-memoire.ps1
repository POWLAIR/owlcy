# W2 — Mémoire RÉELLE d'une app Tauri/Electron : processus principal + TOUS ses enfants
# (msedgewebview2.exe : browser, GPU, renderer, utility…). C'est cette somme qui compte.
#
# Usage : .\mesure-memoire.ps1 -Nom owlcy-perch        (nom de l'exe sans .exe)
#         .\mesure-memoire.ps1 -Nom owlcy-perch -Secondes 60   (moyenne sur 60 s)
param(
  [Parameter(Mandatory=$true)][string]$Nom,
  [int]$Secondes = 30
)

function Get-Arbre([int]$ParentId) {
  $enfants = Get-CimInstance Win32_Process -Filter "ParentProcessId=$ParentId"
  foreach ($e in $enfants) { $e; Get-Arbre $e.ProcessId }
}

$racine = Get-Process -Name $Nom -ErrorAction Stop | Select-Object -First 1
$echantillons = @()
$cpu0 = @{}
for ($i = 0; $i -lt $Secondes; $i++) {
  $ids = @($racine.Id) + (Get-Arbre $racine.Id | ForEach-Object { $_.ProcessId })
  $procs = Get-Process -Id $ids -ErrorAction SilentlyContinue
  $echantillons += [pscustomobject]@{
    PrivateMB = [math]::Round(($procs | Measure-Object PrivateMemorySize64 -Sum).Sum / 1MB, 1)
    WorkingSetMB = [math]::Round(($procs | Measure-Object WorkingSet64 -Sum).Sum / 1MB, 1)
    NbProcessus = $procs.Count
    CpuS = ($procs | Measure-Object CPU -Sum).Sum
  }
  Start-Sleep -Seconds 1
}
$premier = $echantillons[0]; $dernier = $echantillons[-1]
$cpuPct = [math]::Round((($dernier.CpuS - $premier.CpuS) / $Secondes) * 100 / [Environment]::ProcessorCount, 2)

"Processus suivis : $($dernier.NbProcessus)"
Get-Process -Id $ids -ErrorAction SilentlyContinue | Sort-Object PrivateMemorySize64 -Descending |
  Format-Table Id, ProcessName, @{n='PrivateMB';e={[math]::Round($_.PrivateMemorySize64/1MB,1)}}, @{n='WorkingSetMB';e={[math]::Round($_.WorkingSet64/1MB,1)}}
"Mémoire privée totale (médiane) : $(($echantillons.PrivateMB | Sort-Object)[[int]($Secondes/2)]) MB"
"Working set total (médiane)     : $(($echantillons.WorkingSetMB | Sort-Object)[[int]($Secondes/2)]) MB"
"CPU moyen (tous cœurs)          : $cpuPct %"

# Etat « Focus Assist / plein écran détecté » vu par Windows (doit rester QUNS_ACCEPTS_NOTIFICATIONS = 5)
Add-Type -Namespace W -Name Shell -MemberDefinition '[DllImport("shell32.dll")] public static extern int SHQueryUserNotificationState(out int state);'
$s = 0; [void][W.Shell]::SHQueryUserNotificationState([ref]$s)
$etats = @{1='NOT_PRESENT';2='BUSY (plein écran détecté !)';3='RUNNING_D3D_FULL_SCREEN';4='PRESENTATION_MODE';5='ACCEPTS_NOTIFICATIONS (OK)';6='QUIET_TIME';7='APP'}
"Etat notifications Windows      : $s = $($etats[$s])"
