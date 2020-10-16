# ACKNOWLEDGEMENTS:
# 	Josh Burton
#   Morgan Loomis
# 	http://forums.cgsociety.org/archive/index.php/t-983068.html
# 	http://forums.cgsociety.org/archive/index.php/t-1002257.html
# 	https://groups.google.com/forum/?fromgroups#!topic/python_inside_maya/n6aJq27fg0o%5B1-25%5D
#======================================================================================================================
import maya.cmds as cmds
import maya.mel
import maya.OpenMaya as om

class AbstractContextDragger(object):

    INIT_MESSAGE = "AbstractContextDragger active"

    def __init__(self, name='AbstractDraggerContext', enable_drag=True, *args,**kwargs):
        """
        Initializes a draggerContext object for use with other tools

        Arguments:
        undoMode --
        projection --
        plane --
        space --
        cursor
        drag -- Whether to enable drag mode
        """
        self.undoMode = kwargs.get('undoMode','step')
        self.projection = kwargs.get('projection',"objectViewPlane")
        self.plane = kwargs.get('plane',[1,0,0])
        self.space = kwargs.get('space','world')
        self.cursor = kwargs.get('cursor','crossHair')
        
        self.IMAGE = None
        # self.projection = "objectViewPlane"
        # self.cursor = 'crossHair'
        # self.space = "world"

        self.enable_drag= enable_drag

        self.name = name
        self.anchor_point = None
        self.modifier = None 
        self.button = None
        self.points_list = []


    def create(self,*args,**kwargs ):
        # Delete if it exists
        if cmds.draggerContext(self.name,query=True,exists=True):
            cmds.setToolTo('selectSuperContext')
            cmds.selectMode(object=True)
            cmds.deleteUI(self.name)

        cmds.draggerContext( 
            self.name,  
            image1 = self.IMAGE,
            undoMode = self.undoMode, 
            projection = self.projection, 
            space = self.space,
            initialize = self._initialize,
            pressCommand = self._press,
            releaseCommand = self._release,
            finalize = self._finalize,
            cursor=self.cursor,
            drawString="Test",
            *args,**kwargs 
        )

        if self.projection == 'plane': 
            cmds.draggerContext(self.name,e=True, plane=self.plane)
        if self.enable_drag: 
            cmds.draggerContext(self.name,e=True, dragCommand=self._drag)

        self.set_tool()

    def set_tool(self):
        cmds.setToolTo(self.name)
    
    def _initialize(self):
        """Method to be executed when the tool is entered.
        """
        self._message(self.INIT_MESSAGE)

    def _finalize(self):
        pass

    def _press(self):
        if cmds.draggerContext(self.name,query=True,exists=True):
            self._clear_info()
            self._clear_message()

        self.anchor_point = cmds.draggerContext(self.name, query=True, anchorPoint=True)
        self.modifier = cmds.draggerContext(self.name, query=True, modifier=True)
        self.button = cmds.draggerContext(self.name, query=True, button=True)

        self.points_list.append(self.anchor_point)
    
    def _release(self):
        pass

    def _drag(self):
        self.dragPoint = cmds.draggerContext(self.name, query=True, dragPoint=True)
        self.button = cmds.draggerContext( self.name, query=True, button=True)
        self.modifier = cmds.draggerContext( self.name, query=True, modifier=True)
        self.points_list.append(self.dragPoint)

    def _clear_info(self):
        self.anchor_point = None
        self.modifier = None 
        self.button = None
        self.points_list = []

    def _exit_tool(self):
        cmds.setToolTo('selectSuperContext')
        cmds.selectMode(object=True)

    def _message(self, msg, message_type="status"):
        """Display the given message as a status in-view message.

        :param msg: The message string to display.
        :type msg: str
        """
        cmd = "inViewMessage"
        if message_type == "assist":
            cmd += " -assistMessage \"{}\"".format(msg)
        elif message_type == "status":
            cmd += " -statusMessage \"{}\"".format(msg)
        cmd += " -position \"topCenter\""
        maya.mel.eval(cmd)

    def _clear_message(self):
        """Delete the in view message.
        """
        cmds.inViewMessage(clear="topCenter")