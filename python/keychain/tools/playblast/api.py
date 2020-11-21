
import maya.cmds as cmds
import maya.OpenMaya as om

import math

from keychain.api.drags import abstract_drag
from keychain.api.utils import curves, camera
from keychain.api.utils import maya_api as maya_api_utils
from keychain.api import timeline

from keychain.tools.archer import constants

import os
import re
import shutil
import glob
import subprocess
import sys

import maya.mel
import maya.cmds as cmds

from step_playblast import constants

def encode_image_sequence(image_seq_path, output_path, framerate=24, crf=21, preset="ultrafast", audio_path=None, audio_offset=None):

    ffmpeg_cmd = constants.FFMPEG_PATH
    ffmpeg_cmd += ' -y '
    ffmpeg_cmd += ' -framerate {0}'.format(framerate)
    ffmpeg_cmd += ' -i {0}'.format(image_seq_path)
    if audio_path:
        if audio_offset:
            ffmpeg_cmd += ' -itsoffset {0}'.format(audio_offset)

        ffmpeg_cmd += ' -i {0}'.format(audio_path)

    ffmpeg_cmd += ' -c:v libx264 -crf {0} -preset {1}'.format(crf, preset)
    if audio_path:
        ffmpeg_cmd += ' -c:a aac -filter_complex "[1:0] apad" -shortest'

    ffmpeg_cmd += ' {0}'.format(output_path)

    print(ffmpeg_cmd)
    subprocess.call(ffmpeg_cmd)

def get_frames(start, end, step=1):
    frames = []
    while start < end:
        frames.append(start)
        start += step
    return frames

def get_audio_from_scene():
    playback_slider = maya.mel.eval('$tmpVar=$gPlayBackSlider')
    audio = cmds.timeControl(playback_slider, q=True, sound=True)
    if audio:
        return (audio, cmds.getAttr("{}.filename".format(audio)))

def get_audio_offset(audio=None):
    if audio:
        offset = cmds.getAttr("{}.offset".format(audio))
        offset = offset/constants.FRAMES_PER_SECOND
        return offset

def ls_frames_from_path(filepath):
    return glob.glob(filepath.replace("####", "*"))

def parse_frame_number(filepath):
    # Should change this to regex
    search = os.path.splitext(filepath).split(".")
    if search and search[1]:
        return search[1]

def get_file_from_frame(filepath, frame):
    return filepath.replace("####", str(format(frame, "04")))

def fill_stepped_img_sequence(filepath, frame_range):
    """ 
    Copy over previous frame to fill in the sequence
    """
    start_frame, end_frame = frame_range
    frame_range = range(start_frame, end_frame + 1)
    for index, frame in enumerate(frame_range):
        frame_path = get_file_from_frame(filepath, frame)

        if not os.path.exists(frame_path):
            if index > 0:
                previous_frame = frame_range[index - 1]
                last_frame_path = get_file_from_frame(filepath, previous_frame)
                    
                if os.path.exists(last_frame_path):
                    shutil.copy(last_frame_path, frame_path)
                else:
                    raise IOError(
                        "{} does not exist on disk!".format(
                            last_frame_path
                        )
                    )


def clear_img_sequence(filepath, frame_range):
    start_frame, end_frame = frame_range
    for index, frame in enumerate(range(start_frame, end_frame + 1)):
        frame_path = get_file_from_frame(filepath, frame)
        if os.path.exists(frame_path):
            os.remove(frame_path)

def run_playblast(path, step=1, resolution=constants.RESOLUTION):
    start_frame = cmds.playbackOptions(q=True,min=True)
    end_frame = cmds.playbackOptions(q=True,max=True)

    current_frame = cmds.currentTime(query=True)

    stepped_frames = get_frames(start_frame, end_frame, step=step)
    
    # Audio
    audio = None
    audio_path = None
    audio_offset = None
    scene_audio = get_audio_from_scene()
    if scene_audio:
        audio, audio_path = scene_audio
        audio_offset = get_audio_offset(audio)

    # Set to png format
    current_image_format = cmds.getAttr(constants.RENDER_IMAGE_ATTR)
    cmds.setAttr(constants.RENDER_IMAGE_ATTR, constants.IMAGE_FORMAT)

    sequence_path = cmds.playblast(
        filename=path,
        format=constants.FORMAT,
        frame=stepped_frames, 
        viewer=False,
        sequenceTime=False,
        clearCache=True,
        showOrnaments=False,
        fp=4,
        offScreen=True,
        quality=100,
        percent=100,
        forceOverwrite=True,
        startTime=start_frame,
        endTime=end_frame,
        width = resolution[0],
        height = resolution[1],
        rawFrameNumbers=True,
    )
    # Return back to previous state
    cmds.setAttr(constants.RENDER_IMAGE_ATTR, current_image_format)
    current_frame = cmds.currentTime(current_frame)

    # Fille the stepped frames
    fill_stepped_img_sequence(sequence_path, (int(start_frame), int(end_frame)))
    print(sequence_path) 
    ffmpeg_seq_path = sequence_path.replace("####", "%04d")
    output_path = "{}.mp4".format(path)

    encode_image_sequence(ffmpeg_seq_path, output_path, audio_path=audio_path, audio_offset=audio_offset)

    # Delete temp img files
    clear_img_sequence(sequence_path, (int(start_frame), int(end_frame)))

    # Open video file
    os.system(output_path)
