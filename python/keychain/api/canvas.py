import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

from keychain.api import group
from keychain.api.utils import distance

class Canvas(object):
    
    NAME = "CANVAS_Drawing_Plane" 

    def __init__(self, name=None, controls=None):
        
        super(Canvas, self).__init__()
        self.name = name or Canvas.NAME
        self.controls = controls or []

        group_name = self.name + "_grp"
        # Create ALL group
        self.all_group = group.Group(group_name)
        self.drawing_plane = None


    def create():
        # TODO: Bit convoluted
        self.reset_canvas()
        
    @property
    def camera(self):
        return self.get_active_camera()

    @property
    def _active_view(self):
        return omui.M3dView.active3dView()

    @property
    def center_of_interest(self):
        return distance.get_average_center(self.controls)

    @property
    def control_count(self):
        return len(self.controls)

    ### FUNCTIONS

    def get_active_camera(self):
        dag_path = om.MDagPath()
        self._active_view.getCamera(dag_path)
        return om.MFnDagNode(dag_path.transform()).name()

    def reset_canvas(self):
        self.delete_custom_nodes()
        self._create_drawing_plane(self.camera)

    def _create_drawing_plane(self, camera=None, position=None):

        camera = camera or self.camera

        self.drawing_plane = cmds.plane(
            name=self.name,
            length=self._active_view.portHeight(),
            width=self._active_view.portWidth(),
        )
        if position:
            cmds.xform(self.drawing_plane, ws=True, t=position)
        cmds.connectAttr(
            "{}.rotate".format(camera), "{}.rotate".format(self.drawing_plane)
        )
        cmds.hide(self.drawing_plane)
        cmds.makeLive(self.drawing_plane)
        self.all_group.group_nodes(self.drawing_plane)
        return self.drawing_plane

    def delete_custom_nodes(self):
        if self.all_group.children:
            cmds.delete(self.all_group.children)
