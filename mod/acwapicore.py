# "Astral's CatWeb API Core"
# Handles the interal definitions.``
from mod import exceptions, wmtool, orca

os_value = wmtool.checkos()

if os_value != "Linux":
    raise exceptions.LinuxRequiredError

orca.start()

print("tbd bro this module dont work while we make the internals :sob:")