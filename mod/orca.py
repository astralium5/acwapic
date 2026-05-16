# Starts the main Sober client and enters the game, and the site.
# Oh and does output magic, cant forget that

from mod import wmtool, config
from mod.logger import *
import subprocess, signal

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

def register(keyword):

    def decorator(func):
        registry[keyword] = func

        return func

    return decorator

def start():
    process = subprocess.Popen(
        # the backslash is extremely important (actually)
        ["flatpak", "run", "org.vinegarhq.Sober", f"roblox://placeId={cfg_gameid}\\&launchData={cfg_gamedomain}"],
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

                if not started_state:
                    if cfg_start_identifier in trimmed_line:
                        # We've started processing the logs
                        started_state = True
                    else:
                        continue

                if any(value in trimmed_line for value in cfg_ignorevalues):
                    # String contains a substring in ignore list
                    continue

                # trimmed trimmed line (detect a ".rbx]: " pattern)
                if ".rbx]: " in trimmed_line:
                    trimmed_line = trimmed_line.split(".rbx]: ")[1]

                log_site(trimmed_line)

                # keyword register magic
                for keyword, func in registry.items():
                    if trimmed_line.startswith(f"{keyword} "):
                        payload = trimmed_line[len(keyword) + 1::]

                        func(payload)
                        break

            pass
    except KeyboardInterrupt:
        log_sys("Processing stopped - Keyboard interrupt inside terminal")
        process.send_signal(signal.SIGTERM)
        return