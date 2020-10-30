"""
Inspired by Michael Howard's (@hoorayfor3d) mash setup.
"""


import openMASH
import maya.api.OpenMaya as om

# initialise the MASH network data
md = openMASH.MASHData(thisNode)

# Need a reset frame and a delay amount
firstFrame = 1
frameDelay = 3

# Current frame
frame = md.getFrame()
# Number of points in the network
count = md.count()
# Get the first falloff node (applied to the Python node)
falloff = md.getFalloff(0)

# Re-initialize lists on the first frame
if frame == firstFrame:
    tmList = []

    for i in range(count):
        tmList.append([])

for i in range(count):
    curTM = md.getMatrix(i)
    tmList[i].append(curTM)

    # Don't access out of bounds values (when jumping around on the timeline)
    if len(tmList[i]) > frame - firstFrame:
        # Need MMatrix for blending
        curMMatrix = curTM.asMatrix()
        # Delay per point (point index plus the delay amount)
        # Avoid accessing negative indices in the list. Grab the first transform instead.
        prevMMatrix = tmList[i][max(frame - (i + frameDelay), 0)].asMatrix()
        blendMMatrix = (curMMatrix * (1.0 - falloff[i])) + (prevMMatrix * (falloff[i]))

        # Back to MTransformationMatrix for final
        finalTM = om.MTransformationMatrix(blendMMatrix)
        md.setMatrix(finalTM, i)

# tell MASH to write the network data
md.setData()