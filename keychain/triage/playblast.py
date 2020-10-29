import os
import shutil
import fileseq
import maya.OpenMaya as om
import maya.OpenMayaUI as omUi
import maya.OpenMayaAnim as omAnim
FOLDER = "/home/acunha/Desktop/playblast_test"
FILENAME = "playblast"
STEP = 2

RESOLUTION = (1280, 720)

def get_frames(start, end, step=1):
    frames = []
    while start < end:
        frames.append(start)
        start += step
    return frames


def fill_stepped_img_sequence(folder, start_frame, end_frame):
    """ Fill out the 'in-between' frames in padded/stepped image sequences
    """
    try:
        seq = fileseq.findSequencesOnDisk(folder)[0]
    except IndexError:
        print("No sequence found on directory: {}".format(folder))
        return
    for frame in range(start_frame, end_frame + 1):
        frame_path = input_image_seq.frame(frame)
        if not os.path.exists(frame_path):
            if os.path.exists(input_image_seq.frame(frame - 1)):
                shutil.copy(input_image_seq.frame(frame - 1), frame_path)
            else:
                raise IOError(
                    "{} does not exist on disk!".format(
                        input_image_seq.frame(frame - 1)
                    )
                )

def run_playblast(folder, name, step=1):
	start_frame = cmds.playbackOptions(q=True,min=True)
	end_frame = cmds.playbackOptions(q=True,max=True)
    # stepped_frames = get_frames(start_frame, end_frame, step=step)
    path = os.path.join(folder, name)
    cmds.playblast(
		filename=path,
		format=FORMAT,
		frame=all_frames, 
		viewer=False,
		sequenceTime=False,
		clearCache=True,
		showOrnaments=False,
		fp=4,
		offScreen=True,
		quality=100,
		forceOverwrite=True,
		startTime=start_frame,
		endTime=end_frame,
		width = RESOLUTION[0],
		height = RESOLUTION[1],
		rawFrameNumbers=True,
	)
    fill_stepped_img_sequence(folder, start_frame, end_frame)
run_playblast()


