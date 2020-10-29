import fnmatch
import glob
import json
import logging
import os

LOGGER = logging.getLogger(__name__)


def append_to_path():
    pass


def get_setting_file(setting):

    settings = None
    settings_file = None
    settings_dirs = os.environ["KC_SETTINGS"]

    if not settings_dirs:
        LOGGER.error("No settings path set to KC_SETTINGS")
        return 

    # for folder in settings_dirs.split(os.pathsep):
    for root, dirnames, filenames in os.walk(settings_dirs):
        for json_file in fnmatch.filter(filenames, "{}.json".format(setting)):
            settings_file = json_file
            
    return settings_file

def get_settings(setting):
    settings_file = get_setting_file(setting)
    if not settings_file:
        LOGGER.error("No settings file found for {} in {}".format(setting, os.environ["KC_SETTINGS"]))
        return 

    with open(settings_file, "r") as file_read:
        settings = json.load(file_read)

    return settings
        

def save_settings(settings_file):
    with open(settings_file, "w") as file_for_write:
        json.dump(self.settings, file_for_write, indent=4)
        
