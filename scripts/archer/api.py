import math

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omUI

from keychain.api.utils import maya_api as maya_api_utils
from keychain.api.utils import matrix as matrix_utils
from keychain.api.utils import keys as keys_utils


from keychain.scripts.archer import constants

def create_path_animation(node, curve, frame_range, follow=True, step=1):
    path_node = "{}_temp_path".format(node)
    locator_name = "{}_temp_loc".format(node)
    plugs = []

    if cmds.objExists(path_node):
        cmds.delete(path_node)

    if cmds.objExists(locator_name):
        cmds.delete(locator_name)

    locator = cmds.duplicate(node, name=locator_name, returnRootsOnly=True)[0]

    # Fix curve normals
    # curve = curve_on_surface(curve)

    # cmds.parent(locator, node)
    start_frame, end_frame = frame_range
    cmds.pathAnimation(locator, curve=curve, name=path_node, startTimeU=start_frame, endTimeU=end_frame, worldUpType="object", upAxis="y", follow=follow, followAxis="x")
    
    # cmds.bakeResults(locator, simulation=True, sparseAnimCurveBake=True, time=frame_range,sampleBy=step)
    depend_node = maya_api_utils.get_dependency_node(locator)
    plugs += [
        depend_node.findPlug(attr) for attr in constants.ATTRIBUTES_TO_BAKE
    ]
    keys_utils.bake_animation(plugs, frame_range=frame_range, step=step)
    keys_utils.copy_animation(source=locator, target=node)

    cmds.delete(path_node)
    cmds.delete(locator)


def get_point_at_length(fn_curve, length=0.0):
    parameter = fn_curve.findParamFromLength(length)
    point = om.MPoint()
    fn_curve.getPointAtParam(parameter, point)
    return point

def get_points_along_curve(fn_curve, samples=2):
    points = []
    for i in xrange(samples):
        percent = float(i)/(samples-1) if not samples == 1 else 0
        point = get_point_at_length(fn_curve.length() * percent)
        points.append(point)
    return points

def get_orient_along_curve(fn_curve, samples=2, rotate_order=om.MEulerRotation.kXYZ):
    
    rotation_list = [] 

    temp_normal = om.MVector(1,0,0).normal()
    normals_list = []
    tangents_list = []

    quaternion = om.MQuaternion()
    script_util = om.MScriptUtil()

    for i in xrange(samples):
        percent = float(i)/(samples-1) if not samples == 1 else 0
        parameter = fn_curve.findParamFromLength(fn_curve.length() * percent)

        tangent = fn_curve.tangent(parameter).normal()
        tangents_list.insert(i, tangent)
        
        # Parallel Transport to calculate better normals
        if i == 0:
            # Use the temp_normal to get one ortogonal vector to the tangent
            binormal = tangent ^ temp_normal
            # Get the third ortogonal vector to both tangent and binormal
            normal = tangent ^ binormal
            
        else:
            previous_tangent = tangents_list[i-1]
            previous_normal = normals_list[i-1]
            
            binormal = tangent ^ previous_tangent
            normal = previous_normal

            if not binormal.length() == 0:
                binormal.normalize()
                theta = math.acos(previous_tangent * tangent)
                
                mt = om.MTransformationMatrix()
                mt.setToRotationAxis(binormal, theta)
                
                rotation_mtx = mt.asRotateMatrix()
                normal *= rotation_mtx
                
        normals_list.insert(i, normal)
        
        binormal = normal ^ tangent
        binormal.normalize()
        
        matrix = matrix_utils.build_matrix(
            x=(normal.x,normal.y,normal.z),
            y=(tangent.x,tangent.y,tangent.z),
            z=(binormal.x,binormal.y,binormal.z),
        )

        transform = om.MTransformationMatrix(matrix)
        rotate = transform.eulerRotation().reorder(rotate_order)

        rotation_list.append(rotate)
    return rotation_list
                

def get_active_camera_matrix():
    view = omUI.M3dView.active3dView()
    cam = om.MDagPath()
    view.getCamera(cam)
    return cam.inclusiveMatrix()

def get_vector_from_matrix