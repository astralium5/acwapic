# Handles responses
from . import config, logger
from time import sleep
import pyperclip, keyboard, pyautogui

cfg_delays = config.get("window.delay-bewtween-inputs") / 1000
cfg_setup_delays = 0.350

cfg_mx = config.get("window.input-x")
cfg_my = config.get("window.input-y")

tabs_open = 0
tabs = {}
current_tab = 0

def setuptabs(domains):
    global tabs_open, tabs, current_tab

    # make sure we're not focused on the beginning input field
    pyautogui.click(cfg_mx, cfg_my)
    sleep(cfg_setup_delays)

    # send Ctrl+W 2x to close current tab + the other tab
    keyboard.send("ctrl+w")
    sleep(cfg_setup_delays)
    keyboard.send("ctrl+w")
    sleep(cfg_setup_delays)

    # open tabs
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
    
    current_tab = tabs_open
    
    return tabs

def switchtab(index):
    global current_tab

    if index > 0 and index <= tabs_open and index != current_tab:
        keyboard.send(f"ctrl+{index}")
        current_tab = index
        sleep(cfg_delays)

def send(val: str):
    pyperclip.copy(val)
    pyautogui.click(cfg_mx, cfg_my)
    sleep(cfg_delays)
    keyboard.send("ctrl+v")
    sleep(cfg_delays)
    keyboard.send("enter")
    sleep(cfg_delays)

def send_tab(tab: int, val: str):
    global current_tab

    if tab > 0 and tab <= tabs_open and tab != current_tab:
        switchtab(tab)

    send(val)

def antiidle():
    # press escape twice
    keyboard.send("esc")
    sleep(cfg_delays)
    keyboard.send("esc")
    sleep(cfg_delays)