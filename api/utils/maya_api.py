
import maya.OpenMaya as om
import maya.cmds as cmds

def get_dependency_node(name):
    """
    Args:
        name (str): Node name.
    
    Returns:
        om.MFnDependencyNode
    """
    try:
        selection_list = om.MSelectionList()
        selection_list.add(name)

        m_object = om.MObject()
        selection_list.getDependNode(0, m_object)

        dependency_node = om.MFnDependencyNode(m_object)
        return dependency_node

    except RuntimeError:
        om.MGlobal.displayError("No node matches name: {}".format(name))

def get_dag_path(node=None):
    """
    Convert a node into a OpenMaya.MObject.
    :param str node:
    :return: MDagPath of parsed node
    :rtype: OpenMaya.MDagPath
    """
    if not cmds.objExists(node):
        om2.MGlobal.displayWarning("Node -{}- not found".format(node))
        return

    # Clear selection and get object
    # om2.MGlobal.selectByName(node, om2.MGlobal.kReplaceList)
    selection = om.MSelectionList()
    selection.add(node)
    dag_path = om.MDagPath()
    selection.getDagPath(0, dag_path)

    return dag_path

def find_plug(target_dg_name, mplugs, depth=0, depth_limit=5):
    if depth > depth_limit:
        return
    depth += 1
    for mplug in mplugs:
        mdepnode, dg_name = get_mdependency_node_path(mplug.node())
        if dg_name == target_dg_name:
            return mplug
        affected_plugs = {}
        for p in mdepnode.getAffectedAttributes(mplug.attribute()):
            mp = om.MPlug(mplug.node(), p)
            affected_plugs[mp.partialName(useLongNames=True)] = mp
        if len(affected_plugs)!=1:
            try:
                attribute = MyAttribute(mplug.partialName(useLongNames=True))
            except NameError:  # not a valid or supported attribute
                continue
            plugs = affected_plugs[attribute.get_name(plug='out', index='')].destinations()
        else:
            plugs = mp.destinations()
        return find_plug(target_dg_name, plugs, depth, depth_limit)


def get_mdependency_node_path(mobject):
    mdepnode = om.MFnDagNode(mobject)
    try:
        node_dg_name = mdepnode.getPath().fullPathName()
    except RuntimeError:
        mdepnode = om.MFnDependencyNode(mobject)
        node_dg_name = mdepnode.name()
    return mdepnode, node_dg_name


# ------------------------------------------------------------------
# general functions
# ------------------------------------------------------------------

def _asDagPath(self, name=None):
    """Return the dagPath of the node with the given name.
    If the name is None the active selection list is used.

    :param name: The name of the node.
    :type name: str or None

    :return: The dagPath of the node.
    :rtype: om2.MDagPath or None
    """
    sel = om2.MSelectionList()
    if name is None:
        sel = om2.MGlobal.getActiveSelectionList()
    else:
        try:
            sel.add(name)
        except RuntimeError:
            msg = "The node with the name {} does not exist.".format(name)
            raise RuntimeError(msg)
    if sel.length():
        return sel.getDagPath(0)
    else:
        logger.warning("No object selected to place.")


def _worldMatrix(self, obj):
    """Return the world matrix of the given MObject.

    :param obj: The transform node MObject.
    :type obj: om2.MObject

    :return: The world matrix.
    :rtype: om2.MMatrix
    """
    mfn = om2.MFnDependencyNode(obj)
    matrixObject = mfn.findPlug("worldMatrix", False).elementByLogicalIndex(0).asMObject()
    return om2.MFnMatrixData(matrixObject).matrix()


def _translation(self, obj):
    """Return the world space translation of the given MObject.

    :param obj: The transform node MObject.
    :type obj: om2.MObject

    :return: The world space translation vector.
    :rtype: om2.MVector
    """
    mat = self._worldMatrix(obj)
    transMat = om2.MTransformationMatrix(mat)
    return transMat.translation(om2.MSpace.kWorld)


def _distance(self, point1, point2):
    """Return the distance between the two given points.

    :param point1: The first MPoint.
    :type point1: om2.MPoint
    :param point2: The second MPoint.
    :type point2: om2.MPoint

    :return: The distance between the points.
    :rtype: float
    """
    value = 0.0
    for i in range(3):
        value += math.pow(point1[i] - point2[i], 2)
    return math.sqrt(value)


def _quatFromVector(self, vector):
    """Return a quaternion rotation from the given vector.

    The y axis is used as the up vector.

    :param vector: The vector to build the quaternion from.
    :type vector: om2.MVector

    :return: The rotation quaternion.
    :rtype: om2.MQuaternion
    """
    cross1 = (vector^om2.MVector(0, 1, 0)).normalize()
    cross2 = (vector^cross1).normalize()

    # x axis
    if self._axis == 0:
        xRot = om2.MVector(-vector.x, -vector.y, -vector.z)
        yRot = om2.MVector(-cross2.x, -cross2.y, -cross2.z)
        zRot = cross1
        if self._invert:
            xRot = om2.MVector(-xRot.x, -xRot.y, -xRot.z)
    # y axis
    elif self._axis == 1:
        xRot = om2.MVector(-cross2.x, -cross2.y, -cross2.z)
        yRot = om2.MVector(-vector.x, -vector.y, -vector.z)
        zRot = cross1
        if self._invert:
            yRot = om2.MVector(-yRot.x, -yRot.y, -yRot.z)
    # z axis
    else:
        xRot = cross1
        yRot = om2.MVector(-cross2.x, -cross2.y, -cross2.z)
        zRot = vector
        if self._invert:
            xRot = om2.MVector(-xRot.x, -xRot.y, -xRot.z)
            zRot = om2.MVector(-zRot.x, -zRot.y, -zRot.z)

    mat = om2.MMatrix([xRot.x, xRot.y, xRot.z, 0,
                       yRot.x, yRot.y, yRot.z, 0,
                       zRot.x, zRot.y, zRot.z,
                       0, 0, 0, 0, 1])

    # return the rotation as quaternion
    transMat = om2.MTransformationMatrix(mat)
    return transMat.rotation(True)


def _valueList(self, mat):
    """Return the given MMatrix as a value list.

    :param matrix: The MMatrix to generate the list from.
    :type matrix: om2.MMatrix

    :return: The list of matrix values.
    :rtype: list(float)
    """
    values = []
    for i in range(4):
        for j in range(4):
            values.append(mat.getElement(i, j))
    return values
