import os

def get_icon(name):
    icon_dirs = os.environ.get("KC_ICONS").split(os.pathsep)
    # Get icons from maya's icon path
    icon_dirs.extend(os.environ.get("XBMLANGPATH").split(os.pathsep))
    if not icon_dirs:
        return
    # TODO A bit verbose...
    for dir in icon_dirs:
        for root, __, files in os.walk(dir):
            for basename in files:
                if basename == name:
                    return os.path.join(root, basename)

