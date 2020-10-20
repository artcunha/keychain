
import maya.OpenMayaUI as omui


def get_active_camera():
    view = omui.M3dView.active3dView()
    cam = om.MDagPath()
    view.getCamera(cam)
    return cam
