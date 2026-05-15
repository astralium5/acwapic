# Starts the main Sober client and enters the game, and the site.
# Oh and does output magic, cant forget that

from mod import controlwin, config
import subprocess, re

cfg_gameid = config.get("launch.place-id")
cfg_gamedomain = config.get("launch.goto-domain")

process = subprocess.Popen(
    # the backslash is extremely important (actually)
    ["flatpak", "run", "org.vinegarhq.Sober", f"roblox://placeId={cfg_gameid}\\&launchData={cfg_gamedomain}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
    )

for line in process.stdout:
    line = line.strip()

    print(line)
    pass