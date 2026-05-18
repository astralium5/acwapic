# Logger utilities. Has nothing to do with the actual functionality of the main utility.
import inspect
from pathlib import Path

def _c(color):
    if color == 0:
        return f"\033[49m\033[38;5;15m"
    else:
        return f"\033[48;5;{color}m\033[38;5;0m"
    
def _t(color):
    # ditto but with text color instead
    if color == 0:
        return f"\033[39m"
    else:
        return f"\033[38;5;{color}m"
    
def _l(t):
    print(f"{t}{_c(0)}{_t(0)}")

def _get_caller_name():
    try:
        caller_frame = inspect.stack()[2]
        
        filename = Path(caller_frame.filename).stem
        
        return f"{_c(16)}{_t(0)} {filename.upper()} {_c(0)} "
    except Exception:
        return ""

def log_site(msg):
    _l(f"{_c(119)} SITE {_c(0)} {_t(119)}{msg}")

def log_sys(msg):
    _l(f"{_c(219)} SYS {_c(0)}{_get_caller_name()}{_t(219)}{msg}")

def log_user(msg):
    _l(f"{_c(221)} USER {_c(0)} {_t(221)}{msg}")

def log_rbx(msg):
    _l(f"{_c(117)} RBX {_c(0)} {_t(117)}{msg}")

def log_warn(msg):
    _l(f"{_c(220)} WARN {_c(0)}{_get_caller_name()}{_t(220)}{msg}")

def log_error(msg):
    _l(f"{_c(210)} ERROR {_c(0)}{_get_caller_name()}{_t(210)}{msg}")