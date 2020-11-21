import math
import maya.OpenMaya as om
import maya.cmds as cmds

def build_matrix(translate=(0,0,0),x=(1,0,0),y=(0,1,0),z=(0,0,1)):
    '''
    Build a transformation matrix based on the input vectors
    @param translate: Translate values for the matrix
    @type translate: tuple/list
    @param x: x of the matrix
    @type x: tuple/list
    @param y: y of the matrix
    @type y: tuple/list
    @param z: z of the matrix
    @type z: tuple/list
    '''
    # Create transformation matrix from input vectors
    matrix = om.MMatrix()
    values = []
    om.MScriptUtil.setDoubleArray(matrix[0], 0, x[0])
    om.MScriptUtil.setDoubleArray(matrix[0], 1, x[1])
    om.MScriptUtil.setDoubleArray(matrix[0], 2, x[2])
    om.MScriptUtil.setDoubleArray(matrix[1], 0, y[0])
    om.MScriptUtil.setDoubleArray(matrix[1], 1, y[1])
    om.MScriptUtil.setDoubleArray(matrix[1], 2, y[2])
    om.MScriptUtil.setDoubleArray(matrix[2], 0, z[0])
    om.MScriptUtil.setDoubleArray(matrix[2], 1, z[1])
    om.MScriptUtil.setDoubleArray(matrix[2], 2, z[2])
    om.MScriptUtil.setDoubleArray(matrix[3], 0, translate[0])
    om.MScriptUtil.setDoubleArray(matrix[3], 1, translate[1])
    om.MScriptUtil.setDoubleArray(matrix[3], 2, translate[2])
    return matrix


def get_matrix_from_xform(transform, time=None, matrixType="worldMatrix"):
    """
    Get the matrix of the desired matrix type from the transform in a specific
    moment in time. If the transform doesn't exist an empty matrix will be 
    returned. If not time is specified, the current time will be used.
    
    :param str transform: Path to transform
    :param float/int time: Time value
    :param str matrixType: Matrix type to query
    :return: Matrix
    :rtype: om.MMatrix
    """
    if not transform:
        return om.MMatrix()
        
    time = time or cmds.currentTime(query=True)

    matrix = cmds.getAttr("{0}.{1}".format(transform, matrixType), time=time)
    return om.MMatrix(matrix)


def decompose_matrix(matrix, rotOrder, rotPivot):
    """
    Decompose a matrix into translation, rotation and scale values. A 
    rotation order has to be provided to make sure the euler values are 
    correct.
    
    :param om.MMatrix matrix:
    :param int rotOrder: Rotation order
    :param list rotPivot: Rotation pivot
    :return: Translate, rotate and scale values
    :rtype: list
    """
    matrixTransform = om.MTransformationMatrix(matrix)
    
    # set pivots
    matrixTransform.setRotatePivot(
        om.MPoint(rotPivot), 
        om.MSpace.kTransform, 
        True
    )
    
    # get rotation pivot translation
    posOffset =  matrixTransform.rotatePivotTranslation(
        om.MSpace.kTransform
    )
    
    # get pos values
    pos = matrixTransform.translation(om.MSpace.kTransform)
    pos += posOffset
    pos = [pos.x, pos.y, pos.z]
    
    # get rot values
    euler = matrixTransform.rotation()
    euler.reorderIt(rotOrder)
    rot = [math.degrees(angle) for angle in [euler.x, euler.y, euler.z]]
    
    # get scale values
    scale = matrixTransform.scale(om.MSpace.kTransform)
    
    return [pos, rot, scale]