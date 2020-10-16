
import maya.cmds as cmds
import maya.mel
import maya.OpenMaya as om

from keychain.api.drags import abstract_drag
from keychain.api.utils import curves



class DrawCurveContext(abstract_drag.AbstractContextDragger):
    NAME = "DrawContext"
    def __init__(self, name=None, *args, **kwargs):
        name = name or DrawContext.NAME
        super(DrawContext, self).__init__(name=name, enable_drag=True,*args, **kwargs)
        self.curve = None
    
    # def _finalize(self):
    #     pass

    def _release(self):
        name = "TEST_crv"
        self.curve = curves.create_curve_from_positions(name, self.points_list)
        # self._exit_tool()
