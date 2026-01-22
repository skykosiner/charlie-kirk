import pyautogui
import time

pyautogui.FAILSAFE = False

while True:
    pyautogui.move(100, 0, duration=0.5)
    pyautogui.move(0, 100, duration=0.5)
    pyautogui.move(-100, 0, duration=0.5)
    pyautogui.move(0, -100, duration=0.5)
    time.sleep(3)
