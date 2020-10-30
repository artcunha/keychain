import maya.OpenMaya as om

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
