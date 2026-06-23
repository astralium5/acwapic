# Handles responses
from . import config, logger
from time import sleep
import pyperclip, keyboard, pyautogui

cfg_delays = config.get("window.delay-bewtween-inputs") / 1000
cfg_setup_delays = 0.350

cfg_mx = config.get("window.input-x")
cfg_my = config.get("window.input-y")

def setuptabs(domains):
    # make sure we're not focused on the beginning input field
    pyautogui.click(cfg_mx, cfg_my)
    sleep(cfg_setup_delays)

    # send Ctrl+W 2x to close current tab + the other tab
    keyboard.send("ctrl+w")
    sleep(cfg_setup_delays)
    keyboard.send("ctrl+w")
    sleep(cfg_setup_delays)

    # open tabs
    tabs_open = 0
    tabs = {}
    for domain in domains:
        if tabs_open >= 9:
            logger.log_warn("Only 9 tabs can be open at a time.")
            break
        if tabs_open != 0:
            keyboard.send("ctrl+t")
            sleep(cfg_setup_delays)
        pyperclip.copy(domain)
        keyboard.send("ctrl+v")
        sleep(cfg_setup_delays)
        keyboard.send("enter")
        sleep(cfg_setup_delays)
        tabs_open += 1
        tabs[tabs_open] = domain
    
    return tabs

def switchtab(index):
    print(index)
    if index > 0 and index < 10:
        keyboard.send(f"ctrl+{index}")
        sleep(cfg_delays)

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