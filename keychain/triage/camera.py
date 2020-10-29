#
#
#
#
# To Install:
#
# 1-Copy to your scripts directory.
# 2-In either a python script editor tab or a shelf button, use the following text (with no indented space) to launch the UI.
#
# import rsCameraUI
# reload(rsCameraUI)
# rsCameraUI.rsCameraUIBuild()def plumberReadLic():
#
# See Help menu for details on use
#
#
#


def rsCameraUIBuild(): 
 import maya.cmds as cmds
 import maya.mel as mel

 if cmds.window("rsCameraUI", q=True, ex=True):
	cmds.deleteUI("rsCameraUI", window=True)
 
 cmds.window("rsCameraUI", sizeable=False, mb=1)
 cmds.menu("rsCameraUIDispMenuSet", label='Display', tearOff=False )
 rsm1=cmds.menuItem( label='Film Gate', checkBox=0, en=False )
 rsm2=cmds.menuItem( label='Resolution Gate', checkBox=0, en=0  )
 rsm3=cmds.menuItem( label='Field Chart', checkBox=0, en=0  )
 rsm4=cmds.menuItem( label='Safe Action', checkBox=0, en=0  )
 rsm5=cmds.menuItem( label='Safe Title', checkBox=0, en=0  )
 rsm6=cmds.menuItem( label='View Window', checkBox=0, en=0  )
 cmds.menu("rsCameraUIHelpMenuSet", label='Help', tearOff=False )
 cmds.menuItem( label='Instructions', c='rsCameraUI.rsCameraUIHelp()')
 cmds.menuItem( label='Copyright 2009 - Rob Skiena')

 rsCamUIMainColumn = cmds.columnLayout(columnAttach=('both', 10), adj=True)

 cmds.columnLayout(columnAttach=('both', 1), adj=True ) 

 cmds.separator(style="none", h=10)
 cOpt=cmds.optionMenu( label='Camera' )
 cmds.menuItem( label='--Unlink Camera--' )
 tempAllCams=cmds.ls(cameras=True)
 for tempCam in tempAllCams:
 	if cmds.getAttr(tempCam+".orthographic") == 0:
		tempShape = tempCam
		tempTrans = (mel.eval('listTransforms "' + tempCam +'";'))
 		cmds.menuItem(label=tempTrans[0])

 cmds.optionMenu(cOpt,e=1, cc=('import maya.cmds as cmds; rsCameraUI.rsCameraUIFill((cmds.optionMenu("'+cOpt+'",q=1,v=1)), "' + rsm1 + '","' +rsm2 + '","' +rsm3 + '","' + rsm4 + '","' +rsm5 +'","' +rsm6 +'","' + rsCamUIMainColumn +'")'))
 cmds.setParent("..")
 cmds.separator(style="none", h=10)
 cmds.showWindow("rsCameraUI")
 cmds.window("rsCameraUI",e=1,wh=[235,305])






def rsCameraUIShowWindow(rsm6, camT,rsCamUIMainColumn):

 import maya.cmds as cmds

 tempTrial = cmds.about(v=True)
 if len(tempTrial)<4:
	tempTrial = tempTrial+"____"
 tempTrialer = tempTrial[0:4]
 cmds.setParent(rsCamUIMainColumn)
 tempX = cmds.window("rsCameraUI",q=1,h=True)
 tempY = cmds.menuItem(rsm6, q=1,checkBox=1)
 if tempY==1:
	if tempTrialer=="2010" or tempTrialer=="2009":
	 	cmds.window("rsCameraUI",e=1,h=(tempX + 228))
		cmds.paneLayout("rsCameraUIplay", w=206,h=188)
	else:
	 	cmds.window("rsCameraUI",e=1,h=(tempX + 208))
		cmds.paneLayout("rsCameraUIplay", w=206,h=166)
	shotCamera = cmds.modelPanel(mbv=0,camera=camT)
	cmds.modelEditor(shotCamera, edit=True, grid=False, da="smoothShaded")
	cmds.modelEditor(shotCamera, edit=True, allObjects=False)
	cmds.modelEditor(shotCamera, edit=True, nurbsSurfaces =True)
	cmds.modelEditor(shotCamera, edit=True, polymeshes=True)
	cmds.modelEditor(shotCamera, edit=True, subdivSurfaces=True)
	if tempTrialer=="2010" or tempTrialer=="2009":
        	cmds.setParent("..")
        	cmds.setParent("..")
        cmds.setParent("..")
        cmds.setParent("..")
        cmds.setParent("..")
	myTimeCtrl = cmds.timePort( 'myTimePort', w=100, h=20 )


 else:
	if tempTrialer=="2010" or tempTrialer=="2009":
	 	cmds.window("rsCameraUI",e=1,h=(tempX - 228))
	else:
	 	cmds.window("rsCameraUI",e=1,h=(tempX - 208))
 	cmds.deleteUI("rsCameraUIplay", layout=True)









def rsCameraUIFill(camTrans,rsm1,rsm2,rsm3,rsm4,rsm5,rsm6,rsCamUIMainColumn):


 import maya.cmds as cmds
 
 cmds.setParent(rsCamUIMainColumn)

 cmds.window("rsCameraUI",e=1,wh=[235,305])

 if camTrans=='--Unlink Camera--':
  	if cmds.control('rsCameraReplaceColumn', query=True, exists=True):
 		cmds.deleteUI('rsCameraReplaceColumn',layout=True)
		return
 	

 camShape= cmds.listRelatives(camTrans, shapes=True)

 cmds.menuItem(rsm1, e=1, checkBox=cmds.getAttr(camShape[0] + ".displayFilmGate"), en=True)
 cmds.menuItem(rsm2, e=1, checkBox=cmds.getAttr(camShape[0] + ".displayResolution"), en=True)
 cmds.menuItem(rsm3, e=1, checkBox=cmds.getAttr(camShape[0] + ".displayFieldChart"), en=True)
 cmds.menuItem(rsm4, e=1, checkBox=cmds.getAttr(camShape[0] + ".displaySafeAction"), en=True)
 cmds.menuItem(rsm5, e=1, checkBox=cmds.getAttr(camShape[0] + ".displaySafeTitle"), en=True)
 cmds.menuItem(rsm6, e=1, checkBox=cmds.getAttr(camShape[0] + ".displaySafeTitle"), en=True)

 cmds.menuItem(rsm1, e=1, c=('import maya.cmds as cmds;cmds.setAttr("' + camShape[0] + '.displayFilmGate", cmds.menuItem("' + rsm1 + '", q=1,checkBox=1))'))
 cmds.menuItem(rsm2, e=1, c=('import maya.cmds as cmds;cmds.setAttr("' + camShape[0] + '.displayResolution", cmds.menuItem("' + rsm2 + '", q=1,checkBox=1))'))
 cmds.menuItem(rsm3, e=1, c=('import maya.cmds as cmds;cmds.setAttr("' + camShape[0] + '.displayFieldChart", cmds.menuItem("' + rsm3 + '", q=1,checkBox=1))'))
 cmds.menuItem(rsm4, e=1, c=('import maya.cmds as cmds;cmds.setAttr("' + camShape[0] + '.displaySafeAction", cmds.menuItem("' + rsm4 + '", q=1,checkBox=1))'))
 cmds.menuItem(rsm5, e=1, c=('import maya.cmds as cmds;cmds.setAttr("' + camShape[0] + '.displaySafeTitle", cmds.menuItem("' + rsm5 + '", q=1,checkBox=1))'))
 cmds.menuItem(rsm6, e=1, c=('import maya.cmds as cmds; rsCameraUI.rsCameraUIShowWindow("' + rsm6 + '","' + camShape[0] + '","' + rsCamUIMainColumn +'")'))
  
 if cmds.control('rsCameraReplaceColumn', query=True, exists=True):
	cmds.deleteUI('rsCameraReplaceColumn',layout=True)
 cmds.columnLayout('rsCameraReplaceColumn', columnAttach=('both', 1), adj=True ) 
 cmds.separator(style="double", h=20)
##
##### TRANSLATE
##
# cmds.text(fn="boldLabelFont",l="TRANSLATE")
 tempEC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x+116));'
 tempCC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x-116));'
# cmds.frameLayout(li=50, fn='boldLabelFont', l='TRANSLATE', la='center',bv=False,bs='etchedOut',ec='cmds.window("rsCameraUI",e=1,h=706)', cc='cmds.window("rsCameraUI",e=1,h=620)', cl=1, cll=1,)
 cmds.frameLayout(li=50, fn='boldLabelFont', l='TRANSLATE', la='center',bv=False,bs='etchedOut',ec=tempEC, cc=tempCC, cl=1, cll=1,)
 cmds.columnLayout(cat=['both', 1], adj=1)
 cmds.separator(style="none", h=5)

# cmds.separator(style="none", h=10)
 cmds.rowLayout( w=220, numberOfColumns=5, columnWidth5=(15,23,110,23,15),  adj=3, columnAttach5=['both','both','both','both','both'], cl5=["center","center","center","center","center"])
 tXSubSmall = cmds.button(l="<")
 tXSubBig = cmds.button(l="<<")
 tXKey = cmds.button(l="Key X ")
 tXAddBig = cmds.button(l=">>")
 tXAddSmall = cmds.button(l=">")
 cmds.setParent("..")
 cmds.rowLayout( w=220, numberOfColumns=5, columnWidth5=(15,23,110,23,15),  adj=3, columnAttach5=['both','both','both','both','both'], cl5=["center","center","center","center","center"])
 tYSubSmall = cmds.button(l="<")
 tYSubBig = cmds.button(l="<<")
 tYKey = cmds.button(l="Key Y ")
 tYAddBig = cmds.button(l=">>")
 tYAddSmall = cmds.button(l=">")
 cmds.setParent("..")
 cmds.rowLayout( w=220, numberOfColumns=5, columnWidth5=(15,23,110,23,15),  adj=3, columnAttach5=['both','both','both','both','both'], cl5=["center","center","center","center","center"])
 tZSubSmall = cmds.button(l="<")
 tZSubBig = cmds.button(l="<<")
 tZKey = cmds.button(l="Key Z ")
 tZAddBig = cmds.button(l=">>")
 tZAddSmall = cmds.button(l=">")
 cmds.setParent("..")
 tAttFld = cmds.attrFieldGrp(nf=3, l=" ", adj=1, cw4=[60,60,60,60], at=(camTrans+".translate"))
 tKey = cmds.button(l="Key Translations")
 cmds.setParent("..")
 cmds.setParent("..")
##
##### ROTATE
##
 cmds.separator(style="double", h=20)
 tempEC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x+142));'
 tempCC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x-142));'
 cmds.frameLayout(li=61, fn='boldLabelFont', l='ROTATE', la='center',bv=False,bs='etchedOut',ec=tempEC, cc=tempCC, cl=1, cll=1,)
 cmds.columnLayout(cat=['both', 1], adj=1)
 cmds.separator(style="none", h=10)
 tempRadButGrp = cmds.radioButtonGrp( label='Mode:', labelArray2=['Rotate', 'Pan/Lift/Tilt'], numberOfRadioButtons=2, cw3=[48,65, 100], select=1 )
 cmds.separator(style="none", h=5)
 cmds.rowLayout( w=220, numberOfColumns=5, columnWidth5=(15,23,110,23,15),  adj=3, columnAttach5=['both','both','both','both','both'], cl5=["center","center","center","center","center"])
 rXSubSmall = cmds.button(l="<")
 rXSubBig = cmds.button(l="<<")
 rXKey = cmds.button(l="Key X ")
 rXAddBig = cmds.button(l=">>")
 rXAddSmall = cmds.button(l=">")
 cmds.setParent("..")
 cmds.rowLayout( w=220, numberOfColumns=5, columnWidth5=(15,23,110,23,15),  adj=3, columnAttach5=['both','both','both','both','both'], cl5=["center","center","center","center","center"])
 rYSubSmall = cmds.button(l="<")
 rYSubBig = cmds.button(l="<<")
 rYKey = cmds.button(l="Key Y ")
 rYAddBig = cmds.button(l=">>")
 rYAddSmall = cmds.button(l=">")
 cmds.setParent("..")
 cmds.rowLayout( w=220, numberOfColumns=5, columnWidth5=(15,23,110,23,15),  adj=3, columnAttach5=['both','both','both','both','both'], cl5=["center","center","center","center","center"])
 rZSubSmall = cmds.button(l="<")
 rZSubBig = cmds.button(l="<<")
 rZKey = cmds.button(l="Key Z ")
 rZAddBig = cmds.button(l=">>")
 rZAddSmall = cmds.button(l=">")
 cmds.setParent("..")
 rAttFld = cmds.attrFieldGrp(nf=3, l=" ", adj=1, cw4=[60,60,60,60], at=(camTrans+".rotate"),precision=2)
 rKey = cmds.button(l="Key Rotations")
 cmds.setParent("..")
 cmds.setParent("..")
##
##### CAMERA
##
 tempEC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x+150));'
 tempCC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x-150));'
 cmds.separator(style="double", h=20)
 cmds.frameLayout(li=60, fn='boldLabelFont', l='CAMERA', la='center',bv=False,bs='etchedOut',ec=tempEC, cc=tempCC, cl=1, cll=1,)
 cmds.columnLayout(cat=['both', 1], adj=1)
 cmds.separator(style="none", h=10)
 pOpt=cmds.optionMenu( label='Primes',)
 cmds.menuItem( label='-Choose-' )
 cmds.menuItem( label='15mm' )
 cmds.menuItem( label='20mm' )
 cmds.menuItem( label='28mm' )
 cmds.menuItem( label='35mm' )
 cmds.menuItem( label='45mm' )
 cmds.menuItem( label='50mm' )
 cmds.menuItem( label='60mm' )
 cmds.menuItem( label='75mm' )
 cmds.menuItem( label='80mm' )
 cmds.menuItem( label='90mm' )
 cmds.menuItem( label='105mm' )
 cmds.menuItem( label='120mm' )
 cmds.menuItem( label='150mm' )
 cmds.menuItem( label='210mm' )
 cmds.menuItem( label='300mm' )
 cmds.menuItem( label='500mm' )
 cmds.menuItem( label='1000mm' )

 cmds.separator(style="none", h=3)
 lSldr=cmds.attrFieldSliderGrp(l="Lens: ", smn=15, smx=120.0, fmn=2.5, fmx=3500, adj=3, cw4=[34,42,40,10], pre=1, at=(camShape[0]+".focalLength"), hmb=True, cc='print "Boob"')

 cmds.separator(style="none", h=3)
 cmds.rowLayout( w=220, numberOfColumns=5, columnWidth5=(15,23,110,23,15),  adj=3, columnAttach5=['both','both','both','both','both'], cl5=["center","center","center","center","center"])
 fSubSmall = cmds.button(l="<")
 fSubBig = cmds.button(l="<<")
 fKey = cmds.button(l="Key Focal Length ")
 fAddBig = cmds.button(l=">>")
 fAddSmall = cmds.button(l=">")
 cmds.setParent("..")

 ncpAttFld = cmds.attrControlGrp( attribute=camShape[0]+'.nearClipPlane', hmb=True)
 fcpAttFld = cmds.attrControlGrp( attribute=camShape[0]+'.farClipPlane', hmb=True)
 oAttFld = cmds.attrControlGrp( attribute=camShape[0]+'.overscan', hmb=True)
 cmds.setParent("..")
 cmds.setParent("..")
 cmds.separator(style="none", h=5)
 cmds.separator(style="double", h=5)
##
##### SETTINGS
##
 tempEC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x+88));'
 tempCC = 'import maya.cmds as cmds; x=cmds.window("rsCameraUI",q=1,h=1);cmds.window("rsCameraUI",e=1,h=(x-88));'
 cmds.separator(style="none", h=5)
 cmds.frameLayout(li=55, fn='boldLabelFont', l='SETTINGS', la='center',bv=False,bs='etchedOut',ec=tempEC, cc=tempCC, cl=1, cll=1)
 cmds.columnLayout(cat=['both', 1], adj=1)
 cmds.separator(style="none", h=5)
 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["center","center","center"])
 cmds.separator(style="none", h=5)
 cmds.text(l="Small Step")
 cmds.text(l="Large Step")
 cmds.setParent("..")

 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["right","center","center"])
 cmds.text(l="Translate")
 tStepS=cmds.floatField(v=1)
 tStepL=cmds.floatField(v=20)
 cmds.setParent("..")

 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["right","center","center"])
 cmds.text(l="Rotate")
 rStepS=cmds.floatField(v=.25)
 rStepL=cmds.floatField(v=5)
 cmds.setParent("..")

 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["right","center","center"])
 cmds.text(l="Lens")
 fStepS=cmds.floatField(v=1)
 fStepL=cmds.floatField(v=5.0)
 cmds.setParent("..")
 cmds.setParent("..")
 cmds.setParent("..")

 cmds.separator(style="none", h=10)
 cmds.separator(style="double", h=5)
 cameSelBut = cmds.button(l="SELECT CAMERA", c='cmds.select(["' + camShape[0]+ '","' + camTrans +'"])')

 tempCom = 'import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '", attribute="translateX");cmds.setKeyframe("' + camTrans + '", attribute="translateY");cmds.setKeyframe("' + camTrans + '", attribute="translateZ");cmds.setKeyframe("' + camTrans + '", attribute="rotateX");cmds.setKeyframe("' + camTrans + '", attribute="rotateY");cmds.setKeyframe("' + camTrans + '", attribute="rotateZ");cmds.setKeyframe("' + camShape[0] + '", attribute="focalLength");'

 cameKeyBut = cmds.button(l="Keyframe CAMERA", c=tempCom)
 cmds.separator(style="double", h=5)

 cmds.separator(style="none", h=5)

 cmds.button(tXSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateX",(cmds.getAttr("' + camTrans + '.translateX") - tempFact))'))
 cmds.button(tXSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateX",(cmds.getAttr("' + camTrans + '.translateX") - tempFact))'))
 cmds.button(tXKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="translateX")'))
 cmds.button(tXAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateX",(cmds.getAttr("' + camTrans + '.translateX") + tempFact))'))
 cmds.button(tXAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateX",(cmds.getAttr("' + camTrans + '.translateX") + tempFact))'))
 cmds.button(tYSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateY",(cmds.getAttr("' + camTrans + '.translateY") - tempFact))'))
 cmds.button(tYSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateY",(cmds.getAttr("' + camTrans + '.translateY") - tempFact))'))
 cmds.button(tYKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="translateY")'))
 cmds.button(tYAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateY",(cmds.getAttr("' + camTrans + '.translateY") + tempFact))'))
 cmds.button(tYAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateY",(cmds.getAttr("' + camTrans + '.translateY") + tempFact))'))
 cmds.button(tZSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateZ",(cmds.getAttr("' + camTrans + '.translateZ") - tempFact))'))
 cmds.button(tZSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateZ",(cmds.getAttr("' + camTrans + '.translateZ") - tempFact))'))
 cmds.button(tZKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="translateZ")'))
 cmds.button(tZAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateZ",(cmds.getAttr("' + camTrans + '.translateZ") + tempFact))'))
 cmds.button(tZAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + tStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.translateZ",(cmds.getAttr("' + camTrans + '.translateZ") + tempFact))'))
 cmds.button(tKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="translate")'))

 cmds.button(rXSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") - tempFact))'))
 cmds.button(rXSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") - tempFact))'))
 cmds.button(rXKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotateX")'))
 cmds.button(rXAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") + tempFact))'))
 cmds.button(rXAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") + tempFact))'))
 cmds.button(rYSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") - tempFact))'))
 cmds.button(rYSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") - tempFact))'))
 cmds.button(rYKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotateY")'))
 cmds.button(rYAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") + tempFact))'))
 cmds.button(rYAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") + tempFact))'))
 cmds.button(rZSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") - tempFact))'))
 cmds.button(rZSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") - tempFact))'))
 cmds.button(rZKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotateZ")'))
 cmds.button(rZAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") + tempFact))'))
 cmds.button(rZAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") + tempFact))'))
 cmds.button(rKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotate")'))

 cmds.button(fSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + fStepS+ '",q=1,v=True); cmds.setAttr("' + camShape[0]+ '.focalLength",(cmds.getAttr("' + camShape[0]+ '.focalLength") - tempFact))'))
 cmds.button(fSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + fStepL+ '",q=1,v=True); cmds.setAttr("' + camShape[0]+ '.focalLength",(cmds.getAttr("' + camShape[0]+ '.focalLength") - tempFact))'))
 cmds.button(fKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotateZ")'))
 cmds.button(fAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + fStepL+ '",q=1,v=True); cmds.setAttr("' + camShape[0]+ '.focalLength",(cmds.getAttr("' + camShape[0]+ '.focalLength") + tempFact))'))
 cmds.button(fAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + fStepS+ '",q=1,v=True); cmds.setAttr("' + camShape[0]+ '.focalLength",(cmds.getAttr("' + camShape[0]+ '.focalLength") + tempFact))'))
 cmds.button(fKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camShape[0] + '" ,at="focalLength")'))

 cmds.optionMenu(pOpt, e=1, cc='rsCameraUI.rsCameraUIOpt("' + pOpt + '","' + camShape[0]+'")')
 tempRadC = 'import maya.cmds as cmds;rsCameraUI.rsCameraRadButC("'+ rStepS + '","' +  rStepL + '","' + tempRadButGrp + '","' + str(camTrans) +'","' + str(rXSubSmall) +'","' + str(rXSubBig) + '","' +str(rXKey) +'","' + str(rXAddBig) +'","' + str(rXAddSmall) +'","' + str(rYSubSmall) +'","' + str(rYSubBig) +'","' + str(rYKey) +'","' + str(rYAddBig) +'","' + str(rYAddSmall) +'","' + str(rZSubSmall) +'","' + str(rZSubBig) +'","' + str(rZKey) +'","' + str(rZAddBig) +'","' + str(rZAddSmall) +'")'
 cmds.radioButtonGrp(tempRadButGrp,e=1,cc=tempRadC)






def rsCameraRadButC(rStepS,rStepL,tempRadButGrp,camTrans,rXSubSmall,rXSubBig,rXKey,rXAddBig,rXAddSmall,rYSubSmall,rYSubBig,rYKey,rYAddBig,rYAddSmall,rZSubSmall,rZSubBig,rZKey,rZAddBig,rZAddSmall):

 import maya.cmds as cmds
 
 tempMode = cmds.radioButtonGrp(tempRadButGrp,q=1,select=1)

 if tempMode == 1:
 	cmds.button(rXSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") - tempFact))'))
 	cmds.button(rXSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") - tempFact))'))
 	cmds.button(rXKey, e=1,l="Key X", c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotateX")'))
 	cmds.button(rXAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") + tempFact))'))
 	cmds.button(rXAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateX",(cmds.getAttr("' + camTrans + '.rotateX") + tempFact))'))
 	cmds.button(rYSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") - tempFact))'))
 	cmds.button(rYSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") - tempFact))'))
 	cmds.button(rYKey, e=1, l="Key Y",c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotateY")'))
 	cmds.button(rYAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") + tempFact))'))
 	cmds.button(rYAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateY",(cmds.getAttr("' + camTrans + '.rotateY") + tempFact))'))
 	cmds.button(rZSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") - tempFact))'))
 	cmds.button(rZSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") - tempFact))'))
 	cmds.button(rZKey, e=1, l="Key Z", c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotateZ")'))
 	cmds.button(rZAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") + tempFact))'))
 	cmds.button(rZAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.setAttr("' + camTrans + '.rotateZ",(cmds.getAttr("' + camTrans + '.rotateZ") + tempFact))'))
 	cmds.button(rZKey, e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotate")'))

 if tempMode == 2:
 	cmds.button(rXSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True); cmds.rotate((tempFact*-1), 0, 0,"'+  camTrans + '",r=True, os=True)'))
 	cmds.button(rXSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True);cmds.rotate((tempFact*-1), 0, 0,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rXKey,l='LIFT - Key All', e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotate")'))
 	cmds.button(rXAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True);cmds.rotate(tempFact, 0, 0,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rXAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True);cmds.rotate(tempFact, 0, 0,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rYSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True);cmds.rotate(0, (tempFact*-1), 0,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rYSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True);cmds.rotate(0, (tempFact*-1), 0,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rYKey,l='PAN - Key All', e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotate")'))
 	cmds.button(rYAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True);cmds.rotate(0, tempFact, 0,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rYAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True);cmds.rotate(0, tempFact, 0,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rZSubSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True);cmds.rotate(0, 0, (tempFact*-1),"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rZSubBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True); cmds.rotate(0, 0, (tempFact*-1),"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rZKey,l='TILT - Key All', e=1, c=('import maya.cmds as cmds; cmds.setKeyframe("' + camTrans + '" ,at="rotate")'))
 	cmds.button(rZAddBig, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepL+ '",q=1,v=True);cmds.rotate(0, 0, tempFact,"'+  camTrans + '", r=True, os=True)'))
 	cmds.button(rZAddSmall, e=1, c=('import maya.cmds as cmds; tempFact=cmds.floatField("' + rStepS+ '",q=1,v=True);cmds.rotate(0, 0, tempFact,"'+  camTrans + '", r=True, os=True)'))


#cmds.rotate(tempFact, 0, 0, r=True, os=True)
#cmds.rotate(0, 0, tempFact, r=True, os=True)
#cmds.rotate(0, tempFact, 0, r=True, os=True)







def rsCameraUIOpt(pOpt,camShape):
 import maya.cmds as cmds
 
 if cmds.optionMenu(pOpt, q=1, v=1) != '-Choose-':
	temp = cmds.optionMenu(pOpt, q=1, v=1)
	temp=int(temp.replace("mm",""))
	cmds.setAttr(camShape + '.focalLength', temp)
	cmds.optionMenu(pOpt, e=1, v='-Choose-')

def rsCameraUIHelp():
 import maya.cmds as cmds
 
 if cmds.window("rsCameraUIHelp",q=1,exists=1)==True:
 	cmds.deleteUI("rsCameraUIHelp",window=1) 
 cmds.window("rsCameraUIHelp", wh=[351, 965],sizeable=False, title="rsCameraUI Help");
 cmds.columnLayout(cat=['both', 10],adj= 1, cal='left')
 cmds.separator(h=10, style='none')
 cmds.text(fn="boldLabelFont", l="CAMERA")
 cmds.separator(h=10, style='none')
 cmds.text(l="From the Camera Option Menu, choose the perspective camera\nin your current Maya scene you want to control.\n")
 cmds.text(l="If you have more than one camera in your scene, you may switch\nat any time from the Camera Option Menu\n")
 cmds.text(l="Note: RSControlUI only works with single node cameras.\n\n")
 cmds.text(fn="boldLabelFont", l="DISPLAY MENU")
 cmds.separator(h=10, style='none')
 cmds.text(l= "Sets display options for the camera to help with shot composition.\n\nThe 'Show Window' check box creates a thumbnail sized viewport\nof the camera being controlled. Click within the UI viewport\nto make it the active viewport for updating.\n\n")
 cmds.text(fn="boldLabelFont", l="CONTROL BUTTONS")
 cmds.separator(h=10, style='none')
 cmds.rowLayout(nc=2,cw2=[60, 250],ct2=['both', 'both'])
 cmds.columnLayout(w=20)
 cmds.button(l="<")
 cmds.setParent('..')
 cmds.text(l="Increment down by Small Step (see SETTINGS)")
 cmds.setParent('..')
 cmds.rowLayout(nc=2,cw2=[60, 250],ct2=['both', 'both'])
 cmds.columnLayout(w=30)
 cmds.button(l="<<")
 cmds.setParent('..')
 cmds.text(l="Increment down by Large Step (see SETTINGS)")
 cmds.setParent('..')
 cmds.rowLayout(nc=2,cw2=[60, 250],ct2=['both', 'both'])
 cmds.columnLayout(w=50)
 cmds.button(l="Key",w=48)
 cmds.setParent('..')
 cmds.text(l="Set keyframe on attribute at current frame")
 cmds.setParent('..')
 cmds.rowLayout(nc=2,cw2=[60, 250],ct2=['both', 'both'])
 cmds.columnLayout(w=30)
 cmds.button(l=">>")
 cmds.setParent('..')
 cmds.text(l="Increment up by Large Step (see SETTINGS)")
 cmds.setParent('..')
 cmds.rowLayout(nc=2,cw2=[60, 250],ct2=['both', 'both'])
 cmds.columnLayout(w=20)
 cmds.button(l=">")
 cmds.setParent('..')
 cmds.text(l="Increment up by Small Step (see SETTINGS)")
 cmds.setParent('..')
 cmds.text(l="\n")
 cmds.text(fn="boldLabelFont", l="ROTATION MODE")
 cmds.separator(h=10, style='none')
 cmds.radioButtonGrp( label='Mode:', labelArray2=['Rotate', 'Pan/Lift/Tilt'], numberOfRadioButtons=2, cw3=[48,65, 100], select=1 )
 cmds.separator(h=10, style='none')
 cmds.text(l= "The 'Rotate' option rotates the camera along the local axis. With\n'Pan/Lift/Tilt' selected, the buttons perform a pan, lift or tilt the\ncamera according to the current framing.\n\n")
 cmds.text(fn="boldLabelFont", l="ATTRIBUTE FIELDS")
 cmds.separator(h=10, style='none')
 cmds.attrFieldGrp(nf=3, l=" ", cw4=[60,60,60,60])
 cmds.text(l="These show the current settting for an attribute. Upon any change\nto an attribute these fields will update. Changes may also be directly\ninput here.\n")
 cmds.setParent('..')
 cmds.text(fn="boldLabelFont", l="\nSETTINGS")
 cmds.separator(h=10, style='none')
 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["center","center","center"])
 cmds.separator(style="none", h=5)
 cmds.text(l="Small Step")
 cmds.text(l="Large Step")
 cmds.setParent("..")
 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["right","center","center"])
 cmds.text(l="Translate")
 cmds.floatField(v=1)
 cmds.floatField(v=20)
 cmds.setParent("..")
 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["right","center","center"])
 cmds.text(l="Rotate")
 cmds.floatField(v=.25)
 cmds.floatField(v=5)
 cmds.setParent("..")
 cmds.rowLayout(numberOfColumns=3, columnWidth3=(50,65,55), w=200, co3=[0,5,0], columnAttach3=['both','both','both'], cl3=["right","center","center"])
 cmds.text(l="Lens")
 cmds.floatField(v=1)
 cmds.floatField(v=5.0)
 cmds.setParent("..")
 cmds.setParent("..")
 cmds.setParent("..")
 cmds.text(l="\nThese fields set the Small and Large increment amount used by the\nspecified CONTROL BUTTONS.\n\n")
 cmds.setParent('..')
 cmds.text(fn="boldLabelFont", l="\nCAMERA BUTTONS")
 cmds.separator(h=10, style='none')
 cmds.rowLayout(nc=2,cw2=[110, 250],ct2=['both', 'both'])
 cmds.columnLayout(w=100)
 cmds.button(l="SELECT CAMERA")
 cmds.setParent('..')
 cmds.text(l="Selects the Transform and Shape nodes\nfor the camera")
 cmds.setParent('..')
 cmds.separator(style="none", h=5)
 cmds.rowLayout(nc=2,cw2=[110, 250],ct2=['both', 'both'])
 cmds.columnLayout(w=100)
 cmds.button(l="Keyframe CAMERA")
 cmds.setParent('..')
 cmds.text(l="Keyframes the Translations, Rotations and\nFocal Length for the camera")
 cmds.setParent('..')
 cmds.setParent('..')
 cmds.showWindow("rsCameraUIHelp")
 cmds.window("rsCameraUIHelp", e=1, wh=[351, 965])
 
 
 