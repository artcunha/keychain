
import maya.api.OpenMaya as om2
from keychain.tools.pinner import constants, api
from keychain.api.utils import contexts

from keychain.api import timeline as timeline_api


def launch(step=None):
    
    # Get selection
    selection = om2.MGlobal.getActiveSelectionList()
    if selection.length() < 1:
        om2.MGlobal.displayWarning("Please select at least one control.")
        return

    # Get time range
    timeline = timeline_api.Timeline()
    frame_range = timeline.get_selected_range()
    if step:
        stepped_frames = timeline.get_stepped_frames(frame_range, step=step)
        steps_length = len(stepped_frames)

    nodes = selection.getSelectionStrings()
    with contexts.chunk_undo():
        for node in nodes:
            api.pin_to_world(node, frame_range)
        
