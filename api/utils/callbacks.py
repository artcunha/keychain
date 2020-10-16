import maya.cmds as cmds
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.OpenMayaUI as omui
import pymel.core as pm
from pose_sketch.utils import decorators
from pose_sketch import constants
from pose_sketch.utils import curves, transforms



def on_curve_created():

    if om2.MGlobal.getActiveSelectionList().isEmpty():
        return

    transform = om2.MGlobal.getActiveSelectionList().getDagPath(0)

    shape = om2.MDagPath(transform).extendToShape()
    if not shape.hasFn(om2.MFn.kNurbsCurve):
        return

    if cmds.objExists(constants.SKETCH_CURVE):
        cmds.delete(constants.SKETCH_CURVE)

    dag_mod = om2.MDagModifier()
    dag_mod.renameNode(transform, constants.SKETCH_CURVE)
    dag_mod.doIt()

    # TODO: Smooth slider
    cmds.smoothCurve("{}.cv[*]".format(constants.SKETCH_CURVE), s=100)

    # curve_locators = cmds.listRelatives(constants.LOCATORS_GROUP)

    curves.connect_curves(constants.SKETCH_CURVE, constants.INPUT_CURVE, curve_locators)

    transforms.match_control_rotation(sorted(curve_locators), sorted(controls))

    transforms.group_nodes(constants.SKETCH_CURVE)


def create_script_job(event, job, parent):
    return cmds.scriptJob(event=(event, job), parent=parent)
