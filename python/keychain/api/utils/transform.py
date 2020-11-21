import maya.cmds as cmds
import maya.OpenMaya as om 

from keychain.api.utils import matrix as matrix_utils

def get_xform_relation(driver, target):
    # get parent
    rotOrder = cmds.getAttr("{}.rotateOrder".format(target))
    
    # get driver matrix
    driverInverseMatrix = matrix_utils.get_matrix_from_xform(
        driver,
        start,
        "worldInverseMatrix"
    )

    # get start matrix
    anchorMatrix = matrix_utils.get_matrix_from_xform(
        target,
        start,
        "worldMatrix"
    )
            
    # key frame attributes
    for i in range(start, end):
        # get driver and transform matrices
        driverMatrix = matrix_utils.get_matrix_from_xform(
            driver,
            i,
            "worldMatrix"
        )

        inverseMatrix = matrix_utils.get_matrix_from_xform(
            target, 
            i, 
            "parentInverseMatrix"
        )

        # get driver matrix difference
        differenceMatrix = driverInverseMatrix * driverMatrix

        # get local matrix
        localMatrix = differenceMatrix * anchorMatrix * inverseMatrix
                
        # extract transform values from matrix
        rotPivot = cmds.getAttr("{}.rotatePivot".format(target))[0]   
        transformValues = matrix_utils.decomposeMatrix(
            localMatrix, 
            rotOrder, 
            rotPivot,
        )
        