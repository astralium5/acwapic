# Handles permissions
import os

# Check if user is sudo/root.
def checksudo():
    if os.geteuid() != 0:
        return False
    else:
        return True

