# Reads the config.yaml.
import yaml, shutil, sys
from .logger import *
from pathlib import Path

config = {}

user_dir = Path.cwd()
external_config = user_dir / "config.yaml"

if external_config.exists():
    # External config file exists
    with external_config.open() as f:
        config = yaml.safe_load(f)
        log_sys(f"Config file path: {str(external_config)}")
else:
    # Clone internal config file into external
    fallback_file = Path(__file__).parent.parent.resolve() / "config.fallback.yaml"
    if fallback_file.exists():
        shutil.copy(fallback_file, external_config)
        log_warn("No config file found! A fallback config file has been created, and an early exit will be executed. Please read the config.yaml file and make any modifications you need.")
        sys.exit(1)
    else:
        log_error("Could not find fallback config file.")
        sys.exit(2)


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