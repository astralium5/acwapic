# Do window manager stuff
import os, platform

window_manager = None
os_flavor = platform.system()

match os_flavor:
    case "Windows":
        import pywinctl
        window_manager = pywinctl
    case "Linux":
        from ewmh import EWMH
        window_manager = EWMH()

# Check the current OS.
def checkos():
    return os_flavor

# Check the window manager currently running.
def checkwm():
    match os_flavor:
        case "Windows":
            return 1 # NO I AM NOT DEALING WITH THIS STUPID CRAP
        case "Linux":
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
    match os_flavor:
        case "Windows":
            while True:
                # In windows the window that appears may not always be in focus immediately
                windows = window_manager.getWindowsWithTitle(name)
                if windows:
                    window = windows[0]
                    window.activate()
                    return window
        case "Linux":
            while True:
                active_win = window_manager.getActiveWindow()
                if active_win == None:
                    continue
                active_name = window_manager.getWmName(active_win)

                if active_name == name:
                    return active_win

# Setup a window.
def setup_window(window, px: int, py: int, sx: int, sy: int):
    match os_flavor:
        case "Windows":
            # window is a.. window
            if window.isMaximized:
                window.restore()
            window.moveTo(px, py)
            window.resizeTo(sx, sy)
        case "Linux":
            # window is an integer
            window_manager.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
            window_manager.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
            window_manager.setWmState(window, 0, '_NET_WM_STATE_FULLSCREEN')
            window_manager.setMoveResizeWindow(window, 0, px, py, sx, sy)
            window_manager.display.flush()