. (Join-Path $PSScriptRoot 'autocheck2.ps1') | Out-Null
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type -TypeDefinition @'
using System; using System.Runtime.InteropServices;
public static class In {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  public static uint FgPid() { uint p; GetWindowThreadProcessId(GetForegroundWindow(), out p); return p; }
  public static void Click(int x, int y) { SetCursorPos(x, y); System.Threading.Thread.Sleep(300); mouse_event(2,0,0,0,IntPtr.Zero); mouse_event(4,0,0,0,IntPtr.Zero); }
}
'@
function Snap($name) { $b = New-Object Drawing.Bitmap 300, 340; $g = [Drawing.Graphics]::FromImage($b); $g.CopyFromScreen(1616, 696, 0, 0, $b.Size); $b.Save((Join-Path $PSScriptRoot $name)); $g.Dispose(); $b.Dispose() }
$np = Start-Process notepad -PassThru; Start-Sleep 2
$npPid = (Get-Process notepad | Sort-Object StartTime | Select -Last 1).Id
[void][In]::SetForegroundWindow((Get-Process -Id $npPid).MainWindowHandle); Start-Sleep 1
"avant lancement : fg_pid=$([In]::FgPid()) notepad=$npPid"
Start-Process (Join-Path $PSScriptRoot 'src-tauri\target\release\owlcy-perch.exe'); Start-Sleep 6
"apres lancement : fg_est_notepad=$([In]::FgPid() -eq $npPid)  (1.2a : le lancement ne vole pas le focus)"
$perch = [uint32](Get-Process owlcy-perch | Select -First 1).Id
[Win]::List($perch) | ? { $_ -match "Tauri Window" }
Snap "w1-capture-idle.png"
# clic au centre de la chouette : fenêtre 1636,716 (260x300), svg left 60 bottom 6, 140x154
[In]::Click(1636 + 60 + 70, 716 + 300 - 6 - 77); Start-Sleep 1
"apres clic chouette : fg_est_notepad=$([In]::FgPid() -eq $npPid)  (1.2b : cliquer la chouette ne vole pas le focus)"
Snap "w1-capture-bulle.png"
[Win]::List($perch) | ? { $_ -match "Tauri Window" }
# clic dans la zone transparente (haut gauche de la fenêtre, hors bulle fermée/ouverte ?) -> doit atteindre ce qui est dessous
[In]::Click(1636 + 250, 716 + 10); Start-Sleep 1
"apres clic zone transparente : fg_pid=$([In]::FgPid()) perch=$perch  (1.3 : ne doit PAS etre la chouette)"
$s = 0; Add-Type -Namespace W2 -Name S -MemberDefinition '[DllImport("shell32.dll")] public static extern int SHQueryUserNotificationState(out int s);'; [void][W2.S]::SHQueryUserNotificationState([ref]$s); "notification_state=$s (5 = OK)  (1.7)"
Stop-Process -Id $npPid
