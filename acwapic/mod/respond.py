# Handles responses
from acwapic.mod import config
from time import sleep
import pyperclip, keyboard, mouse

cfg_delays = config.get("window.delay-bewtween-inputs")

cfg_mx = config.get("window.input-x")
cfg_my = config.get("window.input-y")

def send(val: str):
    pyperclip.copy(val)
    mouse.move(x=cfg_mx, y=cfg_my)
    sleep(cfg_delays)
    mouse.click(button="left")
    sleep(cfg_delays)
    keyboard.send("ctrl+v")
    sleep(cfg_delays)
    keyboard.send("enter")
    sleep(cfg_delays)