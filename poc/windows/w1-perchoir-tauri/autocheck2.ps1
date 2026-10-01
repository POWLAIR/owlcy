Add-Type -TypeDefinition @'
using System; using System.Text; using System.Collections.Generic; using System.Runtime.InteropServices;
public static class Win {
  delegate bool CB(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(CB cb, IntPtr l);
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll", EntryPoint="GetWindowLongPtrW")] static extern IntPtr GWL(IntPtr h, int i);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetWindowTextW(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetClassNameW(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern IntPtr GetPropW(IntPtr h, string n);
  struct RECT { public int L, T, R, B; }
  public static List<string> List(uint pid) {
    var res = new List<string>(); var fg = GetForegroundWindow();
    EnumWindows((h, l) => { uint p; GetWindowThreadProcessId(h, out p); if (p != pid) return true;
      var t = new StringBuilder(256); GetWindowTextW(h, t, 256); var c = new StringBuilder(256); GetClassNameW(h, c, 256);
      long ex = GWL(h, -20).ToInt64(); RECT r; GetWindowRect(h, out r);
      res.Add(String.Format("visible={0} title='{1}' class='{2}' rect={3},{4}->{5},{6} NOACTIVATE={7} TOOLWINDOW={8} TOPMOST={9} LAYERED={10} NonRude={11} foreground={12}",
        IsWindowVisible(h), t, c, r.L, r.T, r.R, r.B, (ex & 0x08000000)!=0, (ex & 0x80)!=0, (ex & 0x8)!=0, (ex & 0x80000)!=0, GetPropW(h,"NonRudeHWND")!=IntPtr.Zero, h==fg));
      return true; }, IntPtr.Zero);
    return res; } }
'@
if ($MyInvocation.InvocationName -ne ".") { $procId = [uint32](Get-Process owlcy-perch | Select -First 1).Id; [Win]::List($procId) }
