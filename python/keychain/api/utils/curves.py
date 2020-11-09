
import math
import maya.cmds as cmds
import maya.mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.OpenMayaUI as omui

from keychain.api.utils import matrix as matrix_utils

def create_curve_from_positions(name, positions_list):
    # Calculate curve degrees
    if len(positions_list) <= 3:
        degree = 1
    else:
        degree = 3

    return cmds.curve(name=name, degree=degree, point=positions_list, ws=True)


def get_cvs_number(curve):
    """
    Get the number of CVs of a curve.
    :param curve:
    :return: number of cvs
    :rtype: int
    """
    return cmds.getAttr("{0}.cp".format(curve), s=1)


def get_point_at_length(fn_curve, length=0.0):
    parameter = fn_curve.findParamFromLength(length)
    point = om.MPoint()
    fn_curve.getPointAtParam(parameter, point)
    return point


def get_points_along_curve(fn_curve, samples=2):
    points = []
    for i in xrange(samples):
        percent = float(i)/(samples-1) if not samples == 1 else 0
        point = get_point_at_length(fn_curve, length=fn_curve.length()*percent)
        points.append(point)
    return points


def get_orient_along_curve(fn_curve, samples=2, temp_normal=None, rotate_order=om.MEulerRotation.kXYZ):
    
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
        
        temp_normal = temp_normal or om.MVector([0,1,0])

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
            x=(tangent.x,tangent.y,tangent.z),
            y=(binormal.x,binormal.y,binormal.z),
            z=(normal.x,normal.y,normal.z),
        )

        transform = om.MTransformationMatrix(matrix)
        rotate = transform.eulerRotation().reorder(rotate_order)

        rotation_list.append(rotate)
    return rotation_list
                

def jc_closestPointOnCurve(location, curveObject):
    import maya.OpenMaya as om
    import maya.cmds as mc

    # input curve
    # input point
    # output param
    # output point

            
    curve = curveObject
            
            # put curve into the MObject
    tempList = om.MSelectionList()
    tempList.add(curve)
    curveObj = om.MObject()
    tempList.getDependNode(0, curveObj)  # puts the 0 index of tempList's depend node into curveObj
            
            # get the dagpath of the object
    dagpath = om.MDagPath()
    tempList.getDagPath(0, dagpath)
            
            # define the curve object as type MFnNurbsCurve
    curveMF = om.MFnNurbsCurve(dagpath)
            
            # what's the input point (in world)
    point = om.MPoint( location[0], location[1], location[2])
            
            # define the parameter as a double * (pointer)
    prm = om.MScriptUtil()
    pointer = prm.asDoublePtr()
    om.MScriptUtil.setDouble (pointer, 0.0)
            
    # set tolerance
    tolerance = .00000001
            
    # set the object space
    space = om.MSpace.kObject
            
    # result will be the worldspace point
    result = om.MPoint()
    result = curveMF.closestPoint (point, pointer,  0.0, space)
            
    position = [(result.x), (result.y), (result.z)]
    curvePoint = om.MPoint ((result.x), (result.y), (result.z))
            
    # creates a locator at the position
    mc.spaceLocator (p=(position[0], position[1], position[2]))
            
    parameter = om.MScriptUtil.getDouble (pointer)
            
    # just return - parameter, then world space coord.
    return [parameter, (result.x), (result.y), (result.z)]


def create_locators_on_curve(curve, count, destructive=False):
    """
    Overview:
        Create a Locator on the selected NurbsCurve.
    argument:
        count (int): Number of locators to create.
        connect (bool): Connect the locator to the curve.
    Return count:
        string []: The name of the created locator.
    """

    # Store the selected NurbsCurve to MFn
    mfn_curve = om.MFnNurbsCurve(transforms.get_dag_path(curve))

    # Get the number of CVs
    cvs = mfn_curve.length()

    locList = []
    for i in range(int(count)):
        param = mfn_curve.findParamFromLength(cvs / (count - 1) * i)
        # Declare world space
        space = om2.MSpace.kTransform

        # Get CV position, tangent and normal information
        position = om.MPoint()
        mfn_curve.getPointAtParam(param, position, space)
        tangent = mfn_curve.tangent(param, space)

        # Normal adjust values
        if i == 0:
            normal = mfn_curve.normal(param + 0.0001, space)
        elif (i + 1) == count:
            normal = mfn_curve.normal(param - 0.0001, space)
        else:
            normal = mfn_curve.normal(param, space)
        # Calculate the outer product of tangent and normal
        binormal = tangent ^ normal

        # Convert vector information to matrix
        worldMatrix = [
            tangent.x,
            tangent.y,
            tangent.z,
            1,
            normal.x,
            normal.y,
            normal.z,
            1,
            binormal.x,
            binormal.y,
            binormal.z,
            1,
            position.x,
            position.y,
            position.z,
            1,
        ]

        # Create a locator, substituting the position rotation information
        locator = cmds.spaceLocator()[0]
        cmds.xform(locator, matrix=worldMatrix)
        locList.append(locator)

        if not destructive:

            # Create point on curve node setup
            poci = cmds.createNode("pointOnCurveInfo")
            vecX = cmds.createNode("vectorProduct")
            vecZ = cmds.createNode("vectorProduct")
            mat = cmds.createNode("fourByFourMatrix")
            dec = cmds.createNode("decomposeMatrix")

            # Set
            # Set to cross-product
            cmds.setAttr("{}.operation".format(vecX), 2)
            cmds.setAttr("{}.operation".format(vecZ), 2)
            cmds.setAttr(poci + ".parameter", param)
            cmds.setAttr(vecX + ".input1Y", 1)
            cmds.setAttr(
                cmds.listRelatives(locator, s=True)[0] + ".localScale", 1, 1, 1
            )

            # Connect
            cmds.connectAttr(
                mfn_curve.fullPathName() + ".worldSpace[0]", poci + ".inputCurve"
            )
            cmds.connectAttr(poci + ".tangent", vecX + ".input2")
            cmds.connectAttr(vecX + ".output", vecZ + ".input2")
            cmds.connectAttr(poci + ".tangent", vecZ + ".input1")

            cmds.connectAttr(poci + ".tangentX", mat + ".in00")
            cmds.connectAttr(poci + ".tangentY", mat + ".in01")
            cmds.connectAttr(poci + ".tangentZ", mat + ".in02")
            cmds.connectAttr(vecZ + ".outputX", mat + ".in10")
            cmds.connectAttr(vecZ + ".outputY", mat + ".in11")
            cmds.connectAttr(vecZ + ".outputZ", mat + ".in12")
            cmds.connectAttr(vecX + ".outputX", mat + ".in20")
            cmds.connectAttr(vecX + ".outputY", mat + ".in21")
            cmds.connectAttr(vecX + ".outputZ", mat + ".in22")
            cmds.connectAttr(poci + ".positionX", mat + ".in30")
            cmds.connectAttr(poci + ".positionY", mat + ".in31")
            cmds.connectAttr(poci + ".positionZ", mat + ".in32")

            cmds.connectAttr(mat + ".output", dec + ".inputMatrix")
            cmds.connectAttr(dec + ".outputTranslate", locator + ".t")
            cmds.connectAttr(dec + ".outputRotate", locator + ".r")

    return locList
