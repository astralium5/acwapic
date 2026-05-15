# Reads the config.yaml.
import yaml

with open("config.yaml", "r") as f:
    global config
    config = yaml.safe_load(f)

def get(path, default=None):
    keys = path.split(".")
    current = config
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
            
    return current