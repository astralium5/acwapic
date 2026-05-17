# Logger utilities. Has nothing to do with the actual functionality of the main utility.

def _c(color):
    if color == 0:
        return f"\033[49m\033[38;5;15m"
    else:
        return f"\033[48;5;{color}m\033[38;5;0m"

def log_site(msg):
    print(f"{_c(119)} SITE {_c(0)} {msg}")

def log_sys(msg):
    print(f"{_c(219)} SYS {_c(0)} {msg}")

def log_user(msg):
    print(f"{_c(221)} USER {_c(0)} {msg}")

def log_cw(msg):
    print(f"{_c(117)} CATWEB {_c(0)} {msg}")