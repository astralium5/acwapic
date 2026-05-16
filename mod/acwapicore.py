# "Astral's CatWeb API Core"
# Handles the interal definitions.``
from mod import exceptions, wmtool, orca
from mod.logger import *

register = orca.register
print = log_user

os_value = wmtool.checkos()

if os_value != "Linux":
    raise exceptions.LinuxRequiredError

def run():
    log_sys("Starting main orca process")
    orca.start()