# Starts the main Sober client and enters the game, and the site.
# Oh and does output magic, cant forget that

from mod import controlwin, config
import subprocess, re

cfg_gameid = config.get("launch.place-id")
cfg_gamedomain = config.get("launch.goto-domain")

cfg_identifier = config.get("detection.rbx-identifier")
cfg_sliceindex = config.get("detection.slice-index")

cfg_start_identifier = config.get("detection.start-processing-call")

cfg_ignorevalues = config.get("detection.ignore-values")

print(cfg_ignorevalues)

process = subprocess.Popen(
    # the backslash is extremely important (actually)
    ["flatpak", "run", "org.vinegarhq.Sober", f"roblox://placeId={cfg_gameid}\\&launchData={cfg_gamedomain}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
    )

started_state = False

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

        print(trimmed_line)

    pass