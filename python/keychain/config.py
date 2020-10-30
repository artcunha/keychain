import fnmatch
import glob
import json
import logging
import os

LOGGER = logging.getLogger(__name__)


def append_to_path():
    pass


def get_setting_file(setting):

    filepath = None
    settings_dirs = os.environ["KC_SETTINGS"]

    if not settings_dirs:
        LOGGER.error("No settings path set to KC_SETTINGS")
        return 
    
    # TODO Nested configs
    # for folder in settings_dirs.split(os.pathsep):
    for root, dirnames, filenames in os.walk(settings_dirs):
        for json_file in fnmatch.filter(filenames, "{}.json".format(setting)):
            filepath = json_file
            
    return filepath

def get_settings(setting):
    filepath = get_setting_file(setting)
    if not filepath:
        LOGGER.error("No settings file found for {} in {}".format(setting, os.environ["KC_SETTINGS"]))
        return 

    with open(filepath, "r") as file_read:
        settings = json.load(file_read)

    return settings
        

def save_settings(filepath, settings):
    with open(filepath, "w") as file_for_write:
        json.dump(settings, file_for_write, indent=4)
        
