# Starts the main Sober client and enters the game, and the site.
# Oh and does output magic, cant forget that

from .logger import *
from .respond import send
from . import config, wmtool, perm
import subprocess, signal

cfg_fpname = config.get("launch.flatpak-name")
cfg_gameid = config.get("launch.place-id")
cfg_gamedomain = config.get("launch.goto-domain")

cfg_identifier = config.get("detection.rbx-identifier")
cfg_sliceindex = config.get("detection.slice-index")

cfg_start_identifier = config.get("detection.start-processing-call")

cfg_ignorevalues = config.get("detection.ignore-values")

cfg_window_position_x = config.get("window.position-x")
cfg_window_position_y = config.get("window.position-y")
cfg_window_size_x = config.get("window.size-x")
cfg_window_size_y = config.get("window.size-y")

registry = {}

# Register a trigger.
def register(keyword):
    def decorator(func):
        registry[keyword] = func

        return func
    
    return decorator

# Functions to pre-run before actual start.
def pre():
    # Update package
    subprocess.run(
        ["flatpak", "update", cfg_fpname]
    )

# Start the main orca process.
def start():
    # Get permissions
    can_respond = False
    sudo_value = perm.checksudo()
    input_value = perm.checkinput()

    if not (sudo_value or input_value):
        log_warn("Missing input permissions. Responses won't send.")
    else:
        can_respond = True

    process = subprocess.Popen(
        # the backslash is extremely important (actually)
        ["flatpak", "run", cfg_fpname, f"roblox://placeId={cfg_gameid}\\&launchData={cfg_gamedomain}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
        )

    started_state = False

    log_sys("Awaiting for the player window")

    process_window = wmtool.await_window("Sober")

    wmtool.setup_window(process_window, cfg_window_position_x, cfg_window_position_y, cfg_window_size_x, cfg_window_size_y)

    log_sys("Will start processing data")

    try:
        for line in process.stdout:
            line = line.strip()

            if cfg_identifier in line:
                # We got an output line!
                trimmed_line = line[cfg_sliceindex::]
                is_from_site = False

                if not started_state:
                    if cfg_start_identifier in trimmed_line:
                        # We've started processing the logs
                        started_state = True
                    else:
                        continue

                if any(value in trimmed_line for value in cfg_ignorevalues):
                    # String contains a substring in ignore list
                    continue

                # trimmed trimmed line (detect a "]: " pattern)
                if "]: " in trimmed_line:
                    # Find the index of the FIRST occourence of it
                    index = trimmed_line.find("]: ")
                    index += 3
                    trimmed_line = trimmed_line[index::]
                    is_from_site = True

                if is_from_site:
                    log_site(trimmed_line)
                else:
                    log_cw(trimmed_line)

                # keyword register magic
                for keyword, func in registry.items():
                    if trimmed_line.startswith(f"{keyword} "):
                        payload = trimmed_line[len(keyword) + 1::]

                        # The part where the function runs
                        func_result = func(payload)
                        if (func_result != None) and can_respond:
                            func_result = str(func_result)
                            send(func_result)
                        break

            pass
    except KeyboardInterrupt:
        log_sys("Processing stopped - Keyboard interrupt inside terminal")
        process.send_signal(signal.SIGTERM)
        return