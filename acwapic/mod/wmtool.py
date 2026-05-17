# Do window manager stuff
from acwapic.mod import config
from ewmh import EWMH
import os, platform

ewmh = EWMH()

# Check the current OS.
def checkos():
    return platform.system()

# Check the window manager currently running.
def checkwm():
    session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    
    if session_type == 'wayland' or wayland_display:
        return 2
    elif session_type == 'x11' or os.environ.get('DISPLAY'):
        return 1
    else:
        return 0

# Yield until a window of a certain name appears.
def await_window(name: str) -> int:
    while True:
        active_win = ewmh.getActiveWindow()
        if active_win == None:
            continue
        active_name = ewmh.getWmName(active_win).decode("utf-8")

        if active_name == name:
            return active_win
    pass

# Setup a window.
def setup_window(id: int, px: int, py: int, sx: int, sy: int):
    ewmh.setWmState(id, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
    ewmh.setWmState(id, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
    ewmh.setWmState(id, 0, '_NET_WM_STATE_FULLSCREEN')
    ewmh.setMoveResizeWindow(id, 0, px, py, sx, sy)
    ewmh.display.flush()