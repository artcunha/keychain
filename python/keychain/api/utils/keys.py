
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.cmds as cmds 

import math
import itertools
from keychain.api import timeline

def get_step_range(start_frame, end_frame, step=1):
    """
    Args:
        start_frame (int/float): Start value
        end_frame (int/float): End value
        step (int/float): Step increment
    """
    return int(math.floor((end_frame - start_frame) / step)) + 1

def bake_animation(plugs, frame_range=None, step=1):
    """Bake the animation to all nodes based on the passed list of plugs.

    Args:
        plugs (list): List of maya.om.MPlug Plugs to bake the animation to.
    
    Keyword Args:
        frame_range (float, float): Time range in which the keys are to be created.
        step (float): Time step for each sample.
    """

    frame_range = frame_range or timeline.Timeline.frame_range()
    start_frame, end_frame = frame_range
    step_range = get_step_range(start_frame, end_frame, step=step)

    times = om.MTimeArray(step_range, om.MTime())
    plugValues = [om.MDoubleArray(step_range, 0) for i in range(len(plugs))]
    plugsAndValues = zip(plugs, plugValues)
    for i in range(step_range):
        time = om.MTime(start_frame + i * step, om.MTime.kFilm)
        times.set(time, i)

        context = om.MDGContext(time)
        for plug, values in plugsAndValues:
            values.set(plug.asDouble(context), i)

    dg = om.MDGModifier()
    for plug in plugs:
        sources = om.MPlugArray()
        plug.connectedTo(sources, True, False)
        for i in range(sources.length()):
            dg.disconnect(sources[i], plug)

    dg.doIt()
    for plug, values in itertools.izip(plugs, plugValues):
        curve = oma.MFnAnimCurve()
        curve.create(plug, dg)
        curve.addKeys(times, values)

    dg.doIt()


def copy_keys(source=None, target=None, offset=0, rotateOrder=True):
    if not cmds.keyframe(source, q=True):
        om.MGlobal.displayInfo("Source: {} has no animation".format(source))
        return

    if not isinstance(target, (list, tuple)):
        target = [target]
    # TODO: animLayer check
    # if layer:
    #     cmds.select(target)
    #     cmds.animLayer(layer, edit=True, addSelectedObjects=True)

    #     #we want to make sure rotation values are within 360 degrees, so we don't get flipping when blending layers.
    #     utl.minimizeRotationCurves(source)
    #     for each in target:
    #         utl.minimizeRotationCurves(each)

    if rotateOrder:
        for each in target:
            try:
                if cmds.getAttr(each + ".rotateOrder", keyable=True):
                    cmds.setAttr(
                        each + ".rotateOrder", cmds.getAttr(source + ".rotateOrder")
                    )
            except:
                pass

    cmds.copyKey(source)
    # if layer:
    #     cmds.animLayer(layer, edit=True, selected=True)
    for each in target:
        cmds.pasteKey(each, option="insert", timeOffset=offset)


def apply_euler_filter(transform):
    """
    Apply an euler filter on the curves connected to the 
    transforms' rotation.
    Args:
        transform(str): Path to transform
    """
    # Get rotation anim curves 
    rotationCurves = []
    for channel in ("x","y","z"): 
        node = "{}.rotate{}".format(transform, channel)
        
        # Get animCurve
        rotationCurves.extend(
            cmds.listConnections(
                node, 
                type="animCurve",
                destination=False
            ) or []
        )
        
    # Apply euler filter
    if rotationCurves:
        cmds.filterCurve(*rotationCurves, filter="euler")
