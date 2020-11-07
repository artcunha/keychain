import fnmatch
import glob
import json
import logging
import os

LOGGER = logging.getLogger(__name__)


def append_to_path():
    pass


def get_config_file(config):

    filepath = None
    configs_dirs = os.environ["KC_CONFIG"]

    if not configs_dirs:
        LOGGER.error("No configs path set to KC_CONFIG")
        return 
    
    # TODO Nested configs
    # for folder in configs_dirs.split(os.pathsep):
    for root, dirnames, filenames in os.walk(configs_dirs):
        for json_file in fnmatch.filter(filenames, "{}.json".format(config)):
            filepath = json_file
            
    return filepath

def get_config(config):
    filepath = get_config_file(config)
    if not filepath:
        LOGGER.error("No configs file found for {} in {}".format(config, os.environ["KC_configS"]))
        return 

    with open(filepath, "r") as file_read:
        configs = json.load(file_read)

    return config
        

def save_config(filepath, configs):
    with open(filepath, "w") as file_for_write:
        json.dump(configs, file_for_write, indent=4)
        
