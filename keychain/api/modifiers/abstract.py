import enum
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

class BlendModes(enum.IntEnum):
    # MUTE = 0
    ADD = 1
    OVERRIDE = 2

class AbstractModifier(object):

    def __init__(self, source=None, weight=1.000):
        self.source = source
        self.weight = weight
        self.blend_mode = blend
        self.mute = False
    
    def run(self):
        pass
    
    def update(self):
        # TODO : Try to use as much cached data as posisble
        pass
    
    def duplicate(self):
        pass