from ewmh import EWMH
from time import sleep

ewmh = EWMH()

sleep(1)

active = ewmh.getActiveWindow()

name = ewmh.getWmName(active).decode("utf-8")

print(f"focused on {name}")