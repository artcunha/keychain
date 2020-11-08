import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def set_key_env(root):
    #### KEYCHAIN ENV:
    # Config Path:
    config_path = os.path.join(root, "config")
    try:
        os.environ["KC_CONFIG"] += "".join((os.pathsep, config_path))
    except KeyError:
        os.environ["KC_CONFIG"] = config_path

    # Tools Path:
    tools_path = os.path.join(root, "tools")
    try:
        os.environ["KC_TOOLS"] += "".join((os.pathsep, tools_path))
    except KeyError:
        os.environ["KC_TOOLS"] = tools_path

def set_maya_env(root):
    #### MAYA ENV:
    # Append python to script path
    os.environ["MAYA_SCRIPT_PATH"] += "".join((os.pathsep, os.path.join(root, "python")))
    
    # Append icons to maya icon path
    if sys.platform.startswith("linux"):
        os.environ["XBMLANGPATH"] += "".join((os.pathsep, os.path.join(root, "resources", "icons", "%B")))
    else:
        os.environ["XBMLANGPATH"] += "".join((os.pathsep, os.path.join(root, "resources", "icons")))


def set_env():
    set_key_env(ROOT)
    # TODO find a better way to check this
    if "maya" in os.path.basename(sys.executable):
        set_maya_env(ROOT)
