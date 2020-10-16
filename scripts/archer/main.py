import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from maya.api import OpenMaya as om2

from keychain.api import canvas, group, timeline
from keychain.api.utils import callbacks, curves, maya_qt

from keychain.scripts.archer import constants, api, draw_context, pose_draw_context
from keychain.scripts.archer.ui import widget

reload(callbacks)
reload(curves)
reload(maya_qt)
reload(widget)
reload(canvas)
reload(constants)
reload(api)
reload(draw_context)
reload(pose_draw_context)

class Controller(object):

    def __init__(self):

        self.widget = widget.SketchWidget(controller=self, parent=maya_qt.maya_main_window())

        # UI Signals
        self.widget.draw_signal.connect(self._on_draw_signal)
        self.widget.delete_signal.connect(self._on_delete_signal)
        self.widget.close_signal.connect(self._on_close_signal)
        

        # self.curve_draw_context = draw_context.DrawCurveContext(
        #     name="Archer_drawing_context",
        #     step=1,
        # )
        self.curve_draw_context = pose_draw_context.PoseDrawContext(
            name="Archer_drawing_context",
            step=1,
            translate_follow=False,
            orient_follow=True,
        )
        
        # self.all_group = group.Group(constants.ALL_GROUP)
        # self.canvas = canvas.Canvas("Canvas_test")
        # self.timeline = timeline.Timeline()
        # self.frame_range = self.timeline.get_timeslider_range() or self.timeline.frame_range

        # Register curve creation callback


    def _on_draw_signal(self):
        selection = om2.MGlobal.getActiveSelectionList()
        if selection.length() < 1:
            om2.MGlobal.displayWarning("Please select at least one control.")
            return

        self.nodes = selection.getSelectionStrings()
        # self.canvas.reset_canvas()
        self.curve_draw_context.nodes = self.nodes
        
        self.curve_draw_context.create()
        # self.sj_id = callbacks.create_script_job("DagObjectCreated", self._on_curve_created_callback, constants.WINDOW_NAME)

    def _on_delete_signal(self):
        # Explicitly cast to string as PyQt4 returns QString
        # cmds.scriptJob(kill=self.sj_id)
        # self.canvas.delete_custom_nodes()
        pass

    def _on_close_signal(self):
        # Explicitly cast to string as PyQt4 returns QString
        self.close()

    # @ensure_qapp
    def launch(self):
        self.widget.show()
        return self.widget

@maya_qt.ensure_unique_window(constants.WINDOW_NAME)
def launch():
    controler = Controller()
    return controler.launch()
