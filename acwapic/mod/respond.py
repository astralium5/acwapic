# Handles responses
from . import config
from time import sleep
import pyperclip, keyboard, pyautogui

cfg_delays = config.get("window.delay-bewtween-inputs") / 1000

cfg_mx = config.get("window.input-x")
cfg_my = config.get("window.input-y")

def send(val: str):
    pyperclip.copy(val)
    pyautogui.click(cfg_mx, cfg_my)
    sleep(cfg_delays)
    keyboard.send("ctrl+v")
    sleep(cfg_delays)
    keyboard.send("enter")
    sleep(cfg_delays)

def antiidle():
    # press escape twice
    keyboard.send("esc")
    sleep(cfg_delays)
    keyboard.send("esc")
    sleep(cfg_delays)