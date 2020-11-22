
import maya.cmds as cmds
import maya.OpenMaya as om

import math

from keychain.api.drags import abstract_drag
from keychain.api.utils import maya_api as maya_api_utils
from keychain.api.utils import keys as key_utils
from keychain.api.utils import matrix as matrix_utils

def pin_to_world(node, frame_range):

    pass




# ----------------------------------------------------------------------------


def getInTangent(animCurve, time):
    """
    Query the in tangent type of the key frame closest but higher than the 
    parsed time. 
    
    :param str animCurve: Animation curve to query
    :param int time:
    :return: In tangent type
    :rtype: str
    """
    times = cmds.keyframe(animCurve, query=True, timeChange=True) or []
    for t in times:
        if t <= time:
            continue
        
        tangent = cmds.keyTangent(
            animCurve, 
            time=(t,t), 
            query=True, 
            inTangentType=True
        )
        
        return tangent[0]

    return "auto"


def getOutTangent(animCurve, time):
    """
    Query the out tangent type of the key frame closest but lower than the 
    parsed time. 
    
    :param str animCurve: Animation curve to query
    :param int time:
    :return: Out tangent type
    :rtype: str
    """
    times = cmds.keyframe(animCurve, query=True, timeChange=True) or []
    for t in times:
        if t >= time:
            continue
        
        tangent = cmds.keyTangent(
            animCurve, 
            time=(t,t), 
            query=True, 
            outTangentType=True
        )
        
        return tangent[0]

    return "auto"


# ----------------------------------------------------------------------------



def anchorTransform(transform, driver, start, end):
    """
    Anchor a transform for the parsed time range, ideal to fix sliding feet. 
    Function will take into account the in and out tangents in case the 
    transform is already animated. 
    
    :param str transform: Path to transform
    :param str driver: Path to the driver transform
    :param int start: Start time value
    :param int end: End time value
    """ 
    # get parent
    rotOrder = cmds.getAttr("{}.rotateOrder".format(transform))
    
    # get driver matrix
    driverInverseMatrix = matrix_utils.get_matrix_from_xform(
        driver,
        start,
        "worldInverseMatrix"
    )

    # get start matrix
    anchorMatrix = matrix_utils.get_matrix_from_xform(
        transform,
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
            transform, 
            i, 
            "parentInverseMatrix"
        )


                
        # extract transform values from matrix
        rotPivot = cmds.getAttr("{}.rotatePivot".format(transform))[0]   
        transformValues = matrix_utils.decomposeMatrix(
            localMatrix, 
            rotOrder, 
            rotPivot,
        )
        
        for attr, value in zip(("translate","rotate","scale"), transformValues):
            for j, channel in enumerate(("X","Y","Z")):
                # variables
                node = "{}.{}{}".format(transform, attr, channel)
                tangents = {
                    "inTangentType": "linear",
                    "outTangentType": "linear"
                }
                                    
                # check if input connections are
                animInputs = cmds.listConnections(
                    node, 
                    type="animCurve",
                    destination=False
                )

                # adjust tangents
                if animInputs and i == end:
                    tangent = getOutTangent(
                        animInputs[0], 
                        end
                    )
                    
                    tangents["outTangentType"] = tangent
                        
                elif animInputs and i == start:
                    tangent = getInTangent(
                        animInputs[0], 
                        start
                    )
                    
                    tangents["inTangentType"] = tangent
                    
                # set key frame
                cmds.setKeyframe(
                    node, 
                    t=i, 
                    v=value[j],
                    **tangents
                )
    
    # apply euler filter
    key_utils.applyEulerFilter(transform)