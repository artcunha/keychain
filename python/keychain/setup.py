import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def set_env():
    #### KEYCHAIN ENV:
    os.environ["KC_CONFIG"] = os.path.join(ROOT, "config")
    os.environ["KC_TOOLS"] = os.path.join(ROOT, "tools")
    # os.environ["KC_SETTINGS"] = os.pathsep + os.path.join(ROOT, "settings")
    # os.environ["KC_TOOLS"] = os.pathsep + os.path.join(ROOT, "tools")


    #### MAYA ENV:
    # Append to script path
    # os.environ["MAYA_SCRIPT_PATH"].append()

    # Append icons to maya icon path
    if sys.platform.startswith("linux"):
        os.environ["XBMLANGPATH"] += os.pathsep + os.path.join(ROOT, "resources", "icons", "%B")
    else:
        os.environ["XBMLANGPATH"] += os.pathsep + os.path.join(ROOT, "resources", "icons")

