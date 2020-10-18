import maya.cmds as cmds
import maya.mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.OpenMayaUI as omui

def create_curve_from_positions(name, positions_list):
    # Calculate curve degrees
    if len(positions_list) <= 3:
        degree = 1
    else:
        degree = 3

    return cmds.curve(name=name, degree=degree, point=positions_list, ws=True)


def create_curve(name, controls):
    cv_positions = [
        cmds.xform(transform, q=True, t=True, ws=True) for transform in controls
    ]
    curve = cmds.curve(degree=1, point=cv_positions, name=name)

    # Rename shapes
    for shape in cmds.listRelatives(curve, s=True, f=True) or []:
        shape = cmds.rename(shape, "{}Shape".format(name))

    return curve



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


def rebuild_curve(curve, spans):
    cmds.rebuildCurve(curve, rebuildType=0, degree=1, spans=spans)
    return curve

def get_cvs_number(curve):
    """
    Get the number of CVs of a curve.
    :param curve:
    :return: number of cvs
    :rtype: int
    """
    return cmds.getAttr("{0}.cp".format(curve), s=1)


def split_curve_to_parameter(curve, num):
    """
    Get a list of parameters evenly spaced along a curve, based on the
    length of the curve. Ranges are normalizes to be between 0-1.
    :param str curve:
    :param int num:
    :return: parameters
    :rtype: list
    """
    mfn_curve = om.MFnNurbsCurve(transforms.get_dag_path(curve))
    increment = 1.0 / (num - 1)

    # get parameters
    parameters = []
    for i in range(num):
        parameter = mfn_curve.findParamFromLength(mfn_curve.length() * increment * i)
        parameters.append(parameter)

    # # normalize
    # factor = parameters[-1]
    # parameters = [p / factor for p in parameters]

    if cmds.getAttr("{0}.form".format(curve)) == 2:
        parameters.insert(0, parameters[-1])
        parameters.pop(-1)

    return parameters


def snap_to(target, obj, rot=True, trans=True):
    """
    TODO: make it apply to points and verts, etc
    """
    if trans:
        pos = cmds.xform(target, q=True, ws=True, rp=True)
        cmds.xform(obj, ws=True, t=pos)
    if rot:
        rot = cmds.xform(target, q=True, ws=True, ro=True)
        cmds.xform(obj, ws=True, ro=rot)


def align_to_curve(crv=None, obj=None, param=None, destructive=True):
    """
    places the obj on the curve aligned to . . .
    Args:
        obj (string): object to align
        crv: (string): curve TRANSFORM to align to
        param (float): parameter along curve to position and orient to
        *args:
    Returns:
        void
    """
    # TODO - check on non-orig geo, check the matrix plugin is loaded
    if not obj and crv and param:
        cmds.warning("Didnt' get all the correct params! (obj, crv, param)")
        return ()

    if not transforms.type_check(crv, "nurbsCurve"):
        cmds.warning("Crv param wasn't a curve!")
        return ()

    crvShp = cmds.listRelatives(crv, s=True)[0]
    tempObj = cmds.group(empty=True, name="tempCrvNull")

    poci = cmds.shadingNode("pointOnCurveInfo", asUtility=True, name="tempPOCI")
    cmds.connectAttr("{0}.worldSpace[0]".format(crvShp), "{0}.inputCurve".format(poci))
    cmds.setAttr("{0}.parameter".format(poci), param)
    cmds.connectAttr("{0}.position".format(poci), "{0}.translate".format(tempObj))
    sideVal = cmds.getAttr("{0}.normalizedNormal".format(poci))[0]
    side = om.MVector(sideVal[0], sideVal[1], sideVal[2])
    frontVal = cmds.getAttr("{0}.normalizedTangent".format(poci))[0]
    front = om.MVector(frontVal[0], frontVal[1], frontVal[2])

    up = side ^ front

    matrix = cmds.shadingNode("fourByFourMatrix", asUtility=True, name="temp4x4")
    decomp = cmds.shadingNode("decomposeMatrix", asUtility=True, name="tempDM")
    yrow = [side[0], side[1], side[2], 0]
    xrow = [front[0], front[1], front[2], 0]
    zrow = [up[0], up[1], up[2], 0]

    for col in range(3):
        cmds.setAttr("{0}.in0{1}".format(matrix, col), xrow[col])
        cmds.setAttr("{0}.in1{1}".format(matrix, col), yrow[col])
        cmds.setAttr("{0}.in2{1}".format(matrix, col), zrow[col])

    cmds.setAttr("{0}.in33".format(matrix), 1)

    cmds.connectAttr("{0}.output".format(matrix), "{0}.inputMatrix".format(decomp))
    cmds.connectAttr("{0}.outputRotate".format(decomp), "{0}.rotate".format(tempObj))

    snap_to(tempObj, obj)

    if destructive:
        pass

    # cmds.delete(tempObj, poci, decomp, matrix)


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
