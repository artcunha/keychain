import fnmatch
import glob
import json
import logging
import os

from keychain.core import exceptions

LOGGER = logging.getLogger(__name__)


def get_config_file(name):

    configs_dirs = os.environ["KC_CONFIG"]

    if not configs_dirs:
        LOGGER.error("No configs path set to KC_CONFIG")
        raise exceptions.ConfigError 
    
    for folder in configs_dirs.split(os.pathsep):
        for root, dirs, files in os.walk(folder):
            for basename in files:
                if fnmatch.fnmatch(basename, "{}.json".format(name)):
                    return os.path.join(root, basename)
                    
                
def get_config(name):
    filepath = get_config_file(name)
    if not filepath:
        LOGGER.error("No configs file found for {} in {}".format(name, os.environ["KC_configS"]))
        raise exceptions.ConfigError 

    with open(filepath, "r") as file_read:
        config = json.load(file_read)

    return config
        

def save_config(filepath, configs):
    with open(filepath, "w") as file_for_write:
        json.dump(configs, file_for_write, indent=4)
        
