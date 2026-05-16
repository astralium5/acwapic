# Do window manager stuff, it's that simple
# (+input magic)
from mod import config
from ewmh import EWMH
import os, platform

ewmh = EWMH()

# 2 = wayland
# 1 = x11 (the one we're using)
# 0 = other

def checkos():
    return platform.system()

def checkwm():
    
    session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    
    if session_type == 'wayland' or wayland_display:
        return 2
    elif session_type == 'x11' or os.environ.get('DISPLAY'):
        return 1
    else:
        return 0

def await_window(name: str) -> int:
    while True:
        active_win = ewmh.getActiveWindow()
        if active_win == None:
            continue
        active_name = ewmh.getWmName(active_win).decode("utf-8")

        if active_name == name:
            return active_win
    pass

def setup_window(id: int, px: int, py: int, sx: int, sy: int):
    ewmh.setWmState(id, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
    ewmh.setWmState(id, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
    ewmh.setWmState(id, 0, '_NET_WM_STATE_FULLSCREEN')
    ewmh.setMoveResizeWindow(id, 0, px, py, sx, sy)
    ewmh.display.flush()