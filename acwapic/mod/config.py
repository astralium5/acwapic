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

# Will override this session only
def override(path: str, value):
    keys = path.split(".")
    current = config
    
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value