import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui


class Camera(object):
    @classmethod
    def get_active_camera(cls):
        view = omui.M3dView.active3dView()
        cam = om.MDagPath()
        view.getCamera(cam)
        return cls(om.MFnCamera(cam))

    @classmethod
    def from_name(cls, name):
        pass

    def __init__(self, mfn_cam):
        self.mfn_cam = mfn_cam
        pass
    
    @property
    def name(self):
        return self.mfn_cam.absoluteName()

    def duplicate_camera(self,camera=None, name="shotCam_#"):
        
        camera = camera or self.name

        duplicate = cmds.duplicate(camera, name=name+'_#')[0]
            
        for attr in ('translate', 'rotate'):
            cmds.setAttr(duplicate+'.'+attr, lock=0)
            for ax in ('X', 'Y', 'Z'):
                cmds.setAttr(duplicate+'.'+attr+ax, lock=0)
                
                
        if (cmds.listRelatives(duplicate, parent=True)):
            cmds.parent(duplicate, world=True)
        cmds.lookThru( duplicate )

        return duplicate
