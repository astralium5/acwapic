# Exception classes

class AcwapicError(Exception):
    """Base class for all engine exceptions."""
    pass

class X11RequiredError(AcwapicError):
    """Raised when the script is run on Wayland but requires X11 features."""
    def __init__(self, message="X11 protocol not detected. This utility requires an X11 session."):
        self.message = message
        super().__init__(self.message)

class LinuxRequiredError(AcwapicError):
    """Raised when the script is run on non-Linux systems."""
    def __init__(self, message="This utility is only supported on Linux."):
        self.message = message
        super().__init__(self.message) 

class SoberNotInstalledError(AcwapicError):
    """Raised when the Sober Flatpak cannot be found on the system."""
    def __init__(self, message="Sober (org.vinegarhq.Sober) is not installed via Flatpak."):
        self.message = message
        super().__init__(self.message)