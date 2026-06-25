# Starts the main Sober client and enters the game, and the site.
# Oh and does output magic, cant forget that

from .logger import *
from .respond import *
from . import config, wmtool, perm
import subprocess, signal, time

cfg_fpname = config.get("launch.flatpak-name")
cfg_gameid = config.get("launch.place-id")
cfg_domains = config.get("launch.domains")
cfg_startingdomain = config.get("launch.starting-domain")

cfg_identifier = config.get("detection.rbx-identifier")

cfg_start_identifier = config.get("detection.start-processing-call")

cfg_ignorevalues = config.get("detection.ignore-values")

cfg_window_position_x = config.get("window.position-x")
cfg_window_position_y = config.get("window.position-y")
cfg_window_size_x = config.get("window.size-x")
cfg_window_size_y = config.get("window.size-y")

registry = {}

domainmap = {}

# Register a trigger.
def register(keyword):
    def decorator(func):
        registry[keyword] = func

        return func
    
    return decorator

# Functions to pre-run before actual start.
def pre():
    log_sys(f"Starting flatpak update for {cfg_fpname}...")

    p_update = subprocess.Popen(
        ["flatpak", "update", cfg_fpname, "-y"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    if p_update.stdout:
        for line in p_update.stdout:
            cleaned_line = line.strip()
            if cleaned_line:  # Skip empty lines
                log_sys(cleaned_line)

    return_code = p_update.wait()

    if return_code == 0:
        log_sys("Flatpak update completed successfully.")
    else:
        log_error(f"Flatpak update failed with exit code {return_code}")


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
        ["flatpak", "run", cfg_fpname, f"roblox://placeId={cfg_gameid}\\&launchData=confirmloading.acwapic.rbx"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
        )

    started_state = False

    log_sys("Awaiting for the player window")

    process_window = wmtool.await_window("Sober")

    wmtool.setup_window(process_window, cfg_window_position_x, cfg_window_position_y, cfg_window_size_x, cfg_window_size_y)

    # Tab setup does not start until the game fully loads and opens the confirmation site

    log_sys("Will start processing data")

    try:
        last_action = time.time()

        for line in process.stdout:
            line = line.strip()

            current_time = time.time()
            if current_time - last_action >= 600:
                last_action = current_time
                log_sys("Last action >600s, sending anti-idle key")
                antiidle()

            if cfg_identifier in line:
                # We got an output line!
                index = line.find(cfg_identifier)
                index += len(cfg_identifier)
                trimmed_line = line[index::]
                is_from_site = False
                which_site = ""
                tab_switch_goal = 0

                if not started_state:
                    if cfg_start_identifier in trimmed_line:
                        # We've started processing the logs
                        # Setup tabs here
                        domainmap = list(setuptabs(cfg_domains).values())
                        started_state = True
                    else:
                        continue

                # trimmed trimmed line (detect a "{SITENAME}]: " pattern)
                for domain in cfg_domains:
                    if f"{domain}]: " in trimmed_line:
                        # Find the index of the FIRST occourence of it
                        index = trimmed_line.find(f"{domain}]: ")
                        index += 3 + len(domain)
                        trimmed_line = trimmed_line[index::]
                        is_from_site = True
                        which_site = domain
                        tab_switch_goal = domainmap.index(domain) + 1
                        break

                if is_from_site:
                    log_site(trimmed_line, which_site)
                    
                # keyword register magic
                for keyword, func in registry.items():
                    if trimmed_line.startswith(f"{keyword} "):
                        payload = trimmed_line[len(keyword) + 1::]

                        # The part where the function runs
                        func_result = func(payload)
                        if (func_result != None) and can_respond:
                            func_result = str(func_result)
                            switchtab(tab_switch_goal)
                            send(func_result)
                            last_action = current_time
                        break
                
                if any(value in trimmed_line for value in cfg_ignorevalues) or is_from_site:
                    # String contains a substring in ignore list
                    continue
                else:
                    log_rbx(trimmed_line)

            pass
    except KeyboardInterrupt:
        log_sys("Processing stopped - Keyboard interrupt inside terminal")
        process.send_signal(signal.SIGTERM)
        return