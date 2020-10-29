import os
import shutil
import maya.OpenMaya as om
import maya.OpenMayaUI as omUi
import maya.OpenMayaAnim as omAnim

FOLDER = "/home/acunha/Desktop/playblast_test"
FILENAME = "playblast"
STEP = 2

# RESOLUTION = (1280, 720)

def get_frames(start, end, step=1):
    frames = []
    while start < end:
        frames.append(start)
        start += step
    return frames


def fill_stepped_img_sequence(input_image_seq, start_frame, end_frame):
    """ Fill out the 'in-between' frames in padded/stepped image sequences

    Args:
        input_image_seq (fileseq.FileSequence): Stepped image seq to work on.
        start_frame: The start frame of the image sequence.
        end_frame: The frame at which the function should stop
    """
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

def playblastViewport(outputDir=FOLDER,
                      filename=FILENAME,
                      fileFormat='iff',
                      step=STEP,
):
    """    
    Args:
        outputDir (str): The path to the directory to write the images to.
        
        filename (str): The base name of the image. The frame number will be 
            appended at the end of the filename.
        
        fileFormat (str): The format that the image should be saved in. Valid 
            formats are:  als, bmp, cin, gif, jpg, rla, sgi, tga, tif. 
            "iff" is the default, and is the fastest format to save into since 
            it doesn't need any internal conversion.
    """
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    # Time unit
    origTime = omAnim.MAnimControl.currentTime()
    startTime = omAnim.MAnimControl.minTime()
    endTime = omAnim.MAnimControl.maxTime()
    omAnim.MAnimControl.setCurrentTime(startTime)

    view = omUi.M3dView.active3dView()
    
    if view.getRendererName() == omUi.M3dView.kViewport2Renderer:
        vp2Enabled = True
    else:
        vp2Enabled = False

    # Frame unit
    startFrame = int(startTime.asUnits(om.MTime.kFilm))
    endFrame = int(endTime.asUnits(om.MTime.kFilm))
    totalFrames = endFrame - startFrame

    stepped_frames = get_frames(startFrame, endFrame, step=step)
    print stepped_frames

    for frameNum in xrange(startFrame, endFrame):
        # Skipping viewport refresh
        if frameNum in stepped_frames:
            view.scheduleRefresh()

        image = om.MImage()
        if vp2Enabled:
            image.create(view.portWidth(), view.portHeight(), 4, om.MImage.kFloat)
            view.readColorBuffer(image)
            image.convertPixelFormat(om.MImage.kByte)
        else:
            view.readColorBuffer(image)
        image.writeToFile(outputDir + '/{0}.{1}.{2}'.format(filename,
                                                            str(frameNum).zfill(3),
                                                            fileFormat),
                          fileFormat)
        omAnim.MAnimControl.setCurrentTime(om.MTime(frameNum, om.MTime.kFilm))
    omAnim.MAnimControl.setCurrentTime(origTime)
    
playblastViewport()


# seq = fileseq.findSequencesOnDisk(img_dir)[0]
# start_frame = seq.frameSet().start()


# def run_playblast():
	# start = cmds.playbackOptions(q=True,min=True)
	# end  = cmds.playbackOptions(q=True,max=True)

	# cmds.playblast(
	# 	filename=FILEPATH,
	# 	format=FORMAT,
	# 	frame=all_frames, 
	# 	viewer=False,
	# 	sequenceTime=False,
	# 	clearCache=True,
	# 	showOrnaments=False,
	# 	fp=4,
	# 	offScreen=True,
	# 	quality=100,
	# 	forceOverwrite=True,
	# 	startTime=start,
	# 	endTime=end,
	# 	width = RESOLUTION[0],
	# 	height = RESOLUTION[1],
	# 	rawFrameNumbers=True,
	# )
# run_playblast()


