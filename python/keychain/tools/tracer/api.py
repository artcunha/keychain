
import maya.cmds as cmds
import maya.mel
import maya.OpenMaya as om

import math

from keychain.api.drags import abstract_drag
from keychain.api.utils import camera, curves
from keychain.api.utils import maya_api as maya_api_utils
from keychain.api import timeline

from keychain.tools.tracer import constants

class PoseDrawContext(abstract_drag.AbstractContextDragger):

    INIT_MESSAGE = "Draw a curve to pose your selection"

    def __init__(self, nodes=None, name=None, translate_follow=False, orient_follow=True, *args, **kwargs):
        super(PoseDrawContext, self).__init__(name=name, enable_drag=True, *args, **kwargs)
        self.curve = None
        self.nodes = nodes
        self.timeline = timeline.Timeline()
        self.translate_follow = translate_follow
        self.orient_follow = orient_follow
    
    # def _finalize(self):
    #     pass

    def _release(self):

        # In timeslider is not selected, use the full frame range        

        self.delete_curve(curve=constants.SKETCH_CURVE)
        self.curve = curves.create_curve_from_positions(constants.SKETCH_CURVE, self.points_list)
        
        # No need to recalculate if only using one frame. Also may cause problems if the curve is too small
        steps = len(self.nodes)
        if not steps == 1:
            cmds.smoothCurve("{}.cv[*]".format(self.curve), s=100)
            cmds.smoothCurve("{}.cv[*]".format(self.curve), s=100)
            cmds.smoothCurve("{}.cv[*]".format(self.curve), s=100)

        dag = maya_api_utils.get_dag_path(self.curve)
        dag.extendToShape()
        # TODO: Remove self
        self.fn_curve = om.MFnNurbsCurve(dag)
        # TODO: Smooth slider
        # TODO: Blend slider
        
        # debug
        locs = cmds.ls("locator*")
        if locs:
            try:
                cmds.delete(locs)
            except:
                pass
        locs = []
        ## Apply positions along frames
        # if self.translate_follow:
        point_list = curves.get_points_along_curve(self.fn_curve, samples=steps)
        for i, point in enumerate(point_list):
            if self.translate_follow:
                cmds.xform(self.nodes[i], translation=(point.x, point.y, point.z))

            # Debug
            locs.append(cmds.spaceLocator())
            cmds.xform(locs[i], translation=(point.x, point.y, point.z))
            cmds.toggle(locs[i], localAxis=True)

        if self.orient_follow:
            # TODO: Sample rotateOrder per node
            rotate_order = cmds.getAttr("{}.rotateOrder".format(self.nodes[0]))

            camera_aim = self._get_camera_vector(self.fn_curve)
            rotation_list = curves.get_orient_along_curve(self.fn_curve, samples=steps, temp_normal=camera_aim, rotate_order=rotate_order)
            for i, rotation in enumerate(rotation_list):
                rotation_degrees = [math.degrees(axis) for axis in (rotation.x, rotation.y, rotation.z)]
                # cmds.xform(self.nodes[i], rotation=rotation_degrees)

                # Debug
                cmds.xform(locs[i], rotation=rotation_degrees)

                cmds.setAttr("{}.localScaleX".format(locs[i][0]), 0.1)
                cmds.setAttr("{}.localScaleY".format(locs[i][0]), 0.1)
                cmds.setAttr("{}.localScaleZ".format(locs[i][0]), 0.1)
                
                # Testy
                cmds.xform(self.nodes[i], rotation=[0,0,0])
                cmds.parent(locs[i], self.nodes[i])
                loc_rot = cmds.xform(locs[i], q=True, rotation=True, os=True)
                cmds.parent(locs[i], world=True)
                cmds.xform(self.nodes[i], rotation=loc_rot)
                cmds.delete(locs[i])


                # loc_mat = om2.MMatrix(cmds.xform(locs[i], q=True,ws=True, matrix=True))

                # inverse_mat = om2.MMatrix(cmds.xform(self.nodes[i], q=True,ws=True, matrix=True)).inverse()

                # final_mat = om2.MTransformationMatrix(loc_mat*inverse_mat)
                # rotation = final_mat.rotation()

                # rotation_degrees = [math.degrees(axis) for axis in (rotation.x, rotation.y, rotation.z)]
                # cmds.xform(self.nodes[i], rotation=rotation_degrees)



                # 
                
        self.delete_curve()
        # Go to the last frame
        cmds.select(self.nodes)
        

    def _get_camera_vector(fn_curve):
        ## Get camera vector
        cam_matrix = camera.get_active_camera().inclusiveMatrix()
        # Get position data from the matrix
        cam_point = om.MPoint(cam_matrix(3,0), cam_matrix(3,1), cam_matrix(3,2),)
        ## Get camera vector
        crv_point = om.MPoint()
        fn_curve.getPointAtParam(0.0, crv_point)
        return om.MVector(crv_point-cam_point).normal()
        
    def delete_curve(self, curve=None):
        curve = curve or self.curve
        if curve and cmds.objExists(curve): 
            cmds.delete(self.curve)
