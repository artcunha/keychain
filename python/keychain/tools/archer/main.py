import maya.cmds as cmds
from maya.api import OpenMaya as om2

from keychain.ui import maya_qt
from keychain.tools.archer import constants, api


class Controller(object):

    def __init__(self):

        self.curve_draw_context = api.DrawCurveContext(
            name="Archer_drawing_context",
            step=3,
        )

    def run(self):
        selection = om2.MGlobal.getActiveSelectionList()
        if selection.length() < 1:
            om2.MGlobal.displayWarning("Please select at least one control.")
            return

        self.nodes = selection.getSelectionStrings()
        self.curve_draw_context.nodes = self.nodes

        self.curve_draw_context.create()


def launch():
    controler = Controller()
    return controler.run()
