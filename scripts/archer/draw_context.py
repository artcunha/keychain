
import maya.cmds as cmds
import maya.mel
import maya.OpenMaya as om

import math

from keychain.api.drags import abstract_drag
from keychain.api.utils import curves
from keychain.api.utils import maya_api as maya_api_utils
from keychain.api import timeline

from keychain.scripts.archer import constants, api

class DrawCurveContext(abstract_drag.AbstractContextDragger):

    INIT_MESSAGE = "Drawing mode active"

    def __init__(self, nodes=None, frame_range=None, step=3, name=None, orient_follow=True, *args, **kwargs):
        super(DrawCurveContext, self).__init__(name=name, enable_drag=True, *args, **kwargs)
        self.curve = None
        self.nodes = nodes
        self.timeline = timeline.Timeline()
        self.orient_follow = orient_follow
        self.step = step
    
    # def _finalize(self):
    #     pass

    def _release(self):

        self.frame_range = self.timeline.get_timeslider_range()
        # In timeslider is not selected, use the full frame range        
        self.stepped_frames = self.timeline.get_stepped_frames(self.frame_range, step=self.step)
        steps = len(self.stepped_frames)

        self.delete_curve(curve=constants.SKETCH_CURVE)
        self.curve = curves.create_curve_from_positions(constants.SKETCH_CURVE, self.points_list)
        
        # No need to recalculate if only using one frame. Also may cause problems if the curve is too small
        if not steps == 1:
            cmds.smoothCurve("{}.cv[*]".format(self.curve), s=100)

        dag = maya_api_utils.get_dag_path(self.curve)
        dag.extendToShape()
        # TODO: Remove self
        self.fn_curve = om.MFnNurbsCurve(dag)
        # TODO: Smooth slider
        # TODO: Blend slider
        
        ## Apply positions along frames

        for node in self.nodes:
            point_list = api.get_points_along_curve(self.fn_curve, samples=steps)
            for i, point in enumerate(point_list):
                cmds.setKeyframe(node, attribute="translateX", value=point.x, time=self.stepped_frames[i])
                cmds.setKeyframe(node, attribute="translateY", value=point.y, time=self.stepped_frames[i])
                cmds.setKeyframe(node, attribute="translateZ", value=point.z, time=self.stepped_frames[i])

            if self.orient_follow:
                rotate_order = cmds.getAttr("{}.rotateOrder".format(node))
                rotation_list = api.get_orient_along_curve(self.fn_curve, samples=steps, rotate_order=rotate_order)
                for i, rotation in enumerate(rotation_list):
                    cmds.setKeyframe(node, attribute="rotateX", value=math.degrees(rotation.x), time=self.stepped_frames[i])
                    cmds.setKeyframe(node, attribute="rotateY", value=math.degrees(rotation.y), time=self.stepped_frames[i])
                    cmds.setKeyframe(node, attribute="rotateZ", value=math.degrees(rotation.z), time=self.stepped_frames[i])
                
        self.delete_curve()
        # Go to the last frame
        self.timeline.current_frame = self.stepped_frames[-1]

        cmds.select(self.nodes)
        

    def delete_curve(self, curve=None):
        curve = curve or self.curve
        if curve and cmds.objExists(curve): 
            cmds.delete(self.curve)
