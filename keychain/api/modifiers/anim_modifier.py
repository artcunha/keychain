import enum
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

from keychain.api.modifiers import abstract
from keychain.api import anim_curve 


class AnimModifier(abstract.AbstractModifier):

    @classmethod
    def from_selected_ctrls(cls, controls=None):
        source = {}
        controls = controls or cmds.ls(selection=True)
        # TODO: Custom exception nothing selected
        if not controls:
            return
        for control in controls:
            source.update(anim_curve.get_node_anim_data(control))
        
        return cls(source=source)


    def __init__(self, source=None, weight=1.000):
        super(AnimModifier, self).__init__(source, weight)

    def run(self):
        pass
    
    def update(self):
        # TODO : Try to use as much cached data as posisble
        pass
    
    def duplicate(self):
        pass