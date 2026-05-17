# Handles permissions
import os, grp, pwd

# Check if user is sudo/root.
def checksudo():
    if os.geteuid() != 0:
        return False
    else:
        return True

def checkinput():
    try:
        username = pwd.getpwuid(os.getuid()).pw_name
        input_group = grp.getgrnam("input")
        user_current_gid = pwd.getpwuid(os.getuid()).pw_gid

        if username in input_group.gr_mem or user_current_gid == input_group.gr_gid:
            return True
        if input_group.gr_gid in os.getgroups():
            return True
            
        return False
        
    except KeyError:
        return False