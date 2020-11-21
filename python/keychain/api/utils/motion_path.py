
import maya.cmds as cmds
from keychain.api.utils import keys as keys_utils


def create_path_animation(node, curve, frame_range, follow=True, step=1):
    path_node = "{}_temp_path".format(node)
    locator_name = "{}_temp_loc".format(node)
    plugs = []

    if cmds.objExists(path_node):
        cmds.delete(path_node)

    if cmds.objExists(locator_name):
        cmds.delete(locator_name)

    locator = cmds.duplicate(node, name=locator_name, returnRootsOnly=True)[0]

    start_frame, end_frame = frame_range
    cmds.pathAnimation(locator, curve=curve, name=path_node, startTimeU=start_frame, endTimeU=end_frame, worldUpType="object", upAxis="y", follow=follow, followAxis="x")
    
    # Bake anim
    # depend_node = maya_api_utils.get_dependency_node(locator)
    # plugs += [
    #     depend_node.findPlug(attr) for attr in constants.ATTRIBUTES_TO_BAKE
    # ]
    # keys_utils.bake_animation(plugs, frame_range=frame_range, step=step)
    # keys_utils.copy_keys(source=locator, target=node)

    cmds.delete(path_node)
    cmds.delete(locator)