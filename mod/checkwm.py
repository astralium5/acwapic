# Check window manager, it's that simple
import os

# 2 = wayland
# 1 = x11 (the one we're using)
# 0 = other

def checkwm():
    session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    
    if session_type == 'wayland' or wayland_display:
        return 2
    elif session_type == 'x11' or os.environ.get('DISPLAY'):
        return 1
    else:
        return 0

