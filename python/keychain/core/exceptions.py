
class ConfigError(Exception):
    """Raise when no config is found"""
    pass

class NotInSceneError(Exception):
    """Raise when object doesn't exist"""
    pass

class SelectionError(Exception):
    """Raise when selection length doesn't match the number required"""
    pass
