import maya.api.OpenMaya as om2
import maya.cmds as cmds

from keychain.api import camera as camera_api

def launch():
    
    # Get selection
    selection = om2.MGlobal.getActiveSelectionList()
    if selection.length() < 1:
        om2.MGlobal.displayWarning("Please select at least one control.")
        return

    nodes = selection.getSelectionStrings()

    camera = camera_api.Camera.get_active_camera()
    follow_cam = camera.duplicate_camera(name="followCam_#")

    # TODO : Skip attributes setting
    cmds.parentConstraint(nodes, follow_cam, maintainOffset=True)
    

