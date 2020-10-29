import maya.OpenMaya as om
import maya.OpenMayaUI as omui


class Viewport(object):
	
	def __init__(self, view=None):
		self.view = view or omui.M3dView.active3dView()

	def drawText(text, view=None):
		view = view or self.view
		view.beginGL()
		view.drawText(text, om.MPoint(5, 5, 0.0, 1.0))
		view.endGL()

	# panel = cmds.getPanel(withFocus=True)
	# callBack = OpenMayaUI.MUiMessage.add3dViewPostRenderMsgCallback(panel, drawText)
	# view = OpenMayaUI.M3dView.active3dView()
	# view.refresh(True, True)

	# Remove
	# OpenMayaUI.MUiMessage.removeCallback(callBack)
	# view = OpenMayaUI.M3dView.active3dView()
	# view.refresh(True, True)
