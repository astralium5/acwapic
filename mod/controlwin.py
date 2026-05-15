# Window manager for most stuff including clicking for API returns
from mod import checkwm, exceptions
import keyboard

window_manager = checkwm.checkwm()
if window_manager != 1:
    # We're not on X11!!!!!!!!!
    raise exceptions.X11RequiredError

