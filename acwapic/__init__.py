# "Astral's CatWeb API Core"
# Handles the interal definitions.
from acwapic.mod import config, exceptions, orca
from acwapic.mod import wmtool
from acwapic.mod.logger import *

register = orca.register
print = log_user
override = config.override

os_value = wmtool.checkos()

if os_value != "Linux":
    raise exceptions.LinuxRequiredError

def run():
    log_sys("Running preload")
    orca.pre()
    log_sys("Starting main orca process")
    orca.start()