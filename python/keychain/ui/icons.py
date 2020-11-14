import os
import glob

def get_icon(name):
    icon_dirs = os.environ.get("KC_ICONS").split(os.pathsep)
    if not icon_dirs:
        return
    for dir in icon_dirs:
        for icon in glob.glob(os.path.join(dir, "{}.*".format(name))):
            return icon

