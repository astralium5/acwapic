# "Astral's CatWeb API Core"
from .mod import config, exceptions, orca, wmtool, respond
from .mod.logger import log_user, log_sys

version = "1.0.0"

register = orca.register
log = log_user
override = config.override

send_tab = respond.send_tab

os_value = wmtool.checkos()

if os_value != "Linux":
    raise exceptions.LinuxRequiredError

def run():
    log_sys("Running preload")
    orca.pre()
    log_sys("Starting main orca process")
    orca.start()

__all__ = [
    'register',
    'override',
    'log',
    'run',
    'exceptions',
    'version',
    'send_tab',
]