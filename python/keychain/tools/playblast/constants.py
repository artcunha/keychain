import os
TOOL_DIR =os.path.dirname(os.path.realpath(__file__))

RESOLUTION = (1280, 720)
FORMAT = "image"
IMAGE_FORMAT = 32 # PNG
RENDER_IMAGE_ATTR = "defaultRenderGlobals.imageFormat"
FFMPEG_PATH = "{}/bin/ffmpeg.exe".format(TOOL_DIR)

FRAMES_PER_SECOND = 24.0
WINDOW_NAME = "Step Playblast"
DEFAULT_NAME = "playblast"

JSON_SETTINGS = "{}/settings.json".format(TOOL_DIR)
