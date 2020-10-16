import maya.OpenMaya as om
import maya.OpenMayaUI as OpenMayaUI

def drawText(*args):
    view = OpenMayaUI.M3dView.active3dView()

    view.beginGL()
    view.drawText('test text 2', om.MPoint(5, 5, 0.0, 1.0))
    view.endGL()

panel = cmds.getPanel(withFocus=True)
callBack = OpenMayaUI.MUiMessage.add3dViewPostRenderMsgCallback(panel, drawText)

view = OpenMayaUI.M3dView.active3dView()
view.refresh(True, True)


# Remove
OpenMayaUI.MUiMessage.removeCallback(callBack)
view = OpenMayaUI.M3dView.active3dView()
view.refresh(True, True)


import maya.cmds as cmds
def tabB(hkpressed):
	if( hkpressed == 1 ):
		pann = cmds.getPanel( wf=1 )
		if "modelPanel" in pann:
			cmds.modelEditor( pann, e=1, nc=1 )
			cmds.modelEditor( pann, e=1, ikHandles=1 )
			cmds.modelEditor( pann, e=1, xray=1 )
			if(cmds.ls(type='HIKCharacterNode')):
				cmds.modelEditor( pann, e=1, joints=1 )
		global oldObjL
		oldObjL = []
		visO = cmds.ls( tr=1, o=1, v=1 )
		for v in visO:
			shObj = cmds.listRelatives( v, s=1 )
			exType = cmds.ls( shObj, st=1 )
			if( exType ):
				if (cmds.getAttr( v+".overrideEnabled", se=1 ) == 1 and exType[1]=='mesh' ):
					cmds.setAttr( v+".overrideEnabled", 1 )
					cmds.setAttr( v+".overrideDisplayType", 2 )
					oldObjL.append(v)

	elif( hkpressed == 0 ):
		global oldObjL
		pann = cmds.getPanel( wf=1 )
		if "modelPanel" in pann:
			cmds.modelEditor( pann, e=1, nc=0 )
			cmds.modelEditor( pann, e=1, ikHandles=0 )
			cmds.modelEditor( pann, e=1, xray=0 )
			if(cmds.ls(type='HIKCharacterNode')):
				cmds.modelEditor( pann, e=1, joints=0 )
		for o in oldObjL:
			cmds.setAttr( o+".overrideEnabled", 0 )
			cmds.setAttr( o+".overrideDisplayType", 0 )
