
from os import name
from keychain.core import config, exceptions

class Settings(object):

    def __init__(self, settings):
        self.__dict__ = settings

    def items(self):
        return self.__dict__.items()
    
    def as_dict(self):
        return self.__dict__
        
def get_settings(name):
    config_dict = config.get_config(name)
    if not config_dict or not config_dict.get("settings"):
        return
    return Settings(config_dict["settings"])


