import maya.cmds as cmds
import pymel.core as pm



def jc_getDist2Points(pointA, pointB):
	"""end jc_sketchPoseApply"""
	

	xDist=pointB[0] - pointA[0]
	# get distance between 2 points
	yDist=pointB[1] - pointA[1]
	zDist=pointB[2] - pointA[2]
	distance=float(cmds.mel.sqrt(xDist * xDist) + (yDist * yDist) + (zDist * zDist))
	return distance
	


def zooCSTUpVector_float(obj, vector):
	"""end jc_getDist2Points
	quired sketchPose utils...
	couple grabbed from zooCSTUtils - hamish rocks.
	---
	s function will return a string indicating the axis of an object, closest in orientation to a compare vector.
	---"""
	

	vec=str(zooCSTUpVector(obj, vector))
	temp=[]
	result=[]
	temp=vec.split(" ")
	for n in range(0,3):
		result[n]=float(float(temp[n]))
		
	return result
	


def zooCSTUpVector(obj, vector):
	"""------
	this function will return a string indicating the axis of an object, closest in orientation to a compare vector.
	------"""
	

	sel=cmds.ls(l=1, sl=1)
	transform=cmds.xform(obj, q=1, ws=1, m=1)
	objX=cmds.mel.pointMatrixMult([1., 0., 0.], transform)
	objY=cmds.mel.pointMatrixMult([0., 1., 0.], transform)
	objZ=cmds.mel.pointMatrixMult([0., 0., 1.], transform)
	dotX=float(cmds.mel.dotProduct(vector, objX, 1))
	dotY=float(cmds.mel.dotProduct(vector, objY, 1))
	dotZ=float(cmds.mel.dotProduct(vector, objZ, 1))
	dotList=[dotX, dotY, dotZ]
	highest=dotList[0]
	highestN=0
	for n in range(1,3):
		if abs(dotList[n])>abs(highest):
			highest=dotList[n]
			highestN=int(n)
			
		
	cmds.select(sel)
	if highestN == 0:
		if highest>0:
			return "1 0 0"
			
		
		else:
			return "-1 0 0"
			
		
	if highestN == 1:
		if highest>0:
			return "0 1 0"
			
		
		else:
			return "0 -1 0"
			
		
	if highestN == 2:
		if highest>0:
			return "0 0 1"
			
		
		else:
			return "0 0 -1"
			
		
	


def jc_getAimAxis(controlToAim, aimTarget):
	"""aim axis utils aren't working, lets write our own"""
	

	aimVector = []
	# create locator under each control, at their ws location
	locA=cmds.spaceLocator()
	locB=cmds.spaceLocator()
	locA_ws=cmds.xform(controlToAim, q=1, rp=1, ws=1)
	locB_ws=cmds.xform(aimTarget, q=1, rp=1, ws=1)
	cmds.xform(locA[0], ws=1, t=(locA_ws[0], locA_ws[1], locA_ws[2]))
	cmds.xform(locB[0], ws=1, t=(locB_ws[0], locB_ws[1], locB_ws[2]))
	cmds.parent(locA[0], controlToAim)
	cmds.parent(locB[0], aimTarget)
	# 0 out all
	cmds.makeIdentity(locA[0], apply=True, s=1, r=1, t=1, n=0)
	cmds.makeIdentity(locB[0], apply=True, s=1, r=1, t=1, n=0)
	# now move B to under A
	cmds.parent(locB[0], locA[0])
	# take 2nd locator, and calculate 
	stretchAxis = [""] * (3)
	t = [0.0] * (3)
	t=cmds.getAttr(locB[0] + ".t")
	if (abs(t[0])>abs(t[1])) and (abs(t[0])>abs(t[2])):
		if t[0]>0:
			aimVector=[1, 0, 0]
			# aim is X, find pos or neg
			
		
		elif t[0]<0:
			aimVector=[-1, 0, 0]
			
		stretchAxis=["sx", "sy", "sz"]
		
	
	elif (abs(t[1])>abs(t[0])) and (abs(t[1])>abs(t[2])):
		if t[1]>0:
			aimVector=[0, 1, 0]
			# aim is Y, find pos or neg
			
		
		elif t[1]<0:
			aimVector=[0, -1, 0]
			
		stretchAxis=["sx", "sy", "sz"]
		
	
	elif (abs(t[2])>abs(t[0])) and (abs(t[2])>abs(t[1])):
		if t[2]>0:
			aimVector=[0, 0, 1]
			# aim is Z, find pos or neg
			
		
		elif t[2]<0:
			aimVector=[0, 0, -1]
			
		stretchAxis=["sx", "sy", "sz"]
		
	cmds.delete(locA)
	return aimVector
	
	
	

def jc_sketchPoseApply(controlsList, curveSel, checkboxLayout, stretch):
	"""end jc_sketchPoseTool
	=======================================================
	-------------------------------------------------------
	=======================================================
	ly button, have curve selected..."""
	

	cvs=len(controlsList)
	cmds.select(curveSel)
	# dup curve to pull it off the plane
	duplicateCurve=cmds.duplicateCurve(curveSel[0], rn=0, ch=1, local=0)
	# rebuild curve to be smooth? (cvs uniform, # = number of objs selected?)
	newCurve=cmds.rebuildCurve(duplicateCurve[0], rt=0, ch=1, end=1, d=3, kr=0, s=(cvs - 1), kcp=0, kt=0, rpo=1, kep=1)
	cmds.DeleteHistory()
	# find the parent shape of the drawn curve, then find its parent and delete (this is just deleting the plane created in the tool proc, without passing the plane's name)
	parentShape=cmds.listRelatives(curveSel[0], p=1)
	cmds.delete(cmds.listRelatives(parentShape[0], p=1))
	#  get curve distance
	curveinfo=str(cmds.createNode('curveInfo'))
	# get curve shape node
	shape=cmds.listRelatives(newCurve[0], s=1)
	cmds.connectAttr((shape[0] + ".worldSpace[0]"), (curveinfo + ".inputCurve"))
	length=float(cmds.getAttr(curveinfo + ".arcLength"))
	# .06b addition - preserve ct spacing --------------------------
	# get distance between controls
	# ***** MAKE SURE YOU USE THE DOLIST, *NOT* the original, or full list.  also, take out the use of 'count'
	ctDistance = []
	ctDistance[0]=float(0)
	for n in range(1,len(doList)+1):
		if cmds.objExists(doList[n]):
			pointB=cmds.xform(doList[n], q=1, rp=1, ws=1)
			# get location of 2 controls
			pointA=cmds.xform(doList[n - 1], q=1, rp=1, ws=1)
			ctDistance[n]=float(jc_getDist2Points(pointB, pointA))
			
		
	ctTotalDist=float(0)
	# find total distance between ct's
	for n in range(0,len(doList)):
		ctTotalDist+=ctDistance[n]
		
	aimVectors = []
	# END .06b addition - preserve ct spacing -----------------------
	
	# for saving current locations in world (v.09)
	for n in range(1,len(doList)+1):
		if cmds.objExists(doList[n]):
			aim=jc_getAimAxis(doList[n - 1], doList[n])
			aimVectors[n - 1]=pm.datatypes.Vector([aim[0], aim[1], aim[2]])
			
		
		else:
			aim=jc_getAimAxis(doList[n - 1], doList[n - 2])
			aimVectors[n - 1]=pm.datatypes.Vector([aim[0], aim[1], aim[2]])
			
		
	locs = []
	# end else if
	# end for loop (vector $aimVectors[] contains all xyz's for aiming, per control
	# make locs in cv positions (can simplify this later - parent locs to target aim, zero out, parent to aiming ct and get highest abs value trans)
	for n in range(1,len(doList)+1):
		currLoc=cmds.spaceLocator(n=("control_loc_0" + str(n)))
		#if ($n > $count)
		#{
		# make a locator
		locs[n - 1]=currLoc[0]
		# add to the list of locators
		#  float $coord[] = `xform -q -os -t ($newCurve[0] + ".ep[" + ($n-1) + "]")`; // query position of each Edit Point on curve...
		# added $pos, $totalPos, and $newPos for determining distance preserving along curve
		# $pos = position along curve as if its distance were the same as the controls in total
		# $totalPos = sum of distances up to the current
		# $newPos = the new position along the curve, adjusted for preserving length of curve versus length of original controls
		pos = 0.0
		totalPos=float(0)
		# must add each distance between control to get proper 'along curve' distance
		if cmds.objExists(doList[n]):
			for i in range(int(n),1-1,-1):
				totalPos+=ctDistance[i - 1]
				# adding all distance up to the current
				
			pos=(totalPos / length)
			# find the ratio
			
		
		else:
			pos=float(1)
			# else, you're at the end, and it should be 1
			
		newPos = 0.0
		if pos != 1:
			newPos=(pos / ctTotalDist) * length
			# need to check for this to make sure the end control gets placed at 1.  alternatively could just clamp $newPos @ 1
			
		
		else:
			newPos=pos
			# if stretch is off, we need to find the ratio of controls length to curve length, 
			# and multiply that by the newPos ratio that we would normally use with stretching on
			
		if stretch == 0:
			newPos=(ctTotalDist / length) * newPos
			
		coord=cmds.pointOnCurve(newCurve[0], pr=newPos, p=1)
		# move locator into position of cvs
		cmds.move(coord[0], coord[1], coord[2], locs[n - 1], rpr=1, ws=1)
		# adding for depth control:
		# -------------------------
		# aim at camera
		aimLoc=cmds.aimConstraint(cam, locs[n - 1], upVector=(0, 0, 1), o=(0, 0, 0), worldUpType="vector", w=1, aimVector=(0, 1, 0), worldUpVector=(0, 1, 0))
		# get distance of control to camera (first get control's ws rp, get cam's ws rp, then make distance node)
		camPiv=cmds.xform(cam, q=1, rp=1, ws=1)
		controlPiv=cmds.xform(doList[n - 1], q=1, rp=1, ws=1)
		camDistNum=float(jc_getDist2Points(camPiv, controlPiv))
		# get distance of loc to camera
		locPiv=cmds.xform(locs[n - 1], q=1, rp=1, ws=1)
		locDistNum=float(jc_getDist2Points(camPiv, locPiv))
		# move local in Y the difference
		distanceDiff=camDistNum - locDistNum
		cmds.move(0, 
			(0 - distanceDiff), 
			0, locs[n - 1], r=1, os=1)
		# get position of loc again
		locPiv=cmds.xform(locs[n - 1], q=1, rp=1, ws=1)
		# -------------------------
		# copy to controllers
		if trans[n - 1] == 1:
			cmds.move(locPiv[0], locPiv[1], locPiv[2], doList[n - 1], rpr=1, ws=1)
			
		cmds.delete(aimLoc)
		#} // end if contains..
		
	aims = []
	# end for loop
	# do rotates
	vector=[0, 0, 0]
	for n in range(1,len(doList)+1):
		if cmds.objExists(doList[n]):
			cmds.parent(locs[n - 1], doList[n - 1])
			cmds.setAttr((locs[n - 1] + ".r"), 
				0, 0, 0)
			vector=aimVectors[n - 1]
			# aim vector now has upVector set to 0 0 0, hopefully will fix flipping
			aimName=cmds.aimConstraint(locs[n], locs[n - 1], upVector=(0, 0, 0), o=(0, 0, 0), worldUpType="vector", w=1, aimVector=(vector[0], vector[1], vector[2]), worldUpVector=(0, 1, 0))
			aims[n - 1]=aimName[0]
			if rot[n - 1] == 1:
				cmds.delete(cmds.aimConstraint(locs[n], doList[n - 1], upVector=(0, 0, 0), o=(0, 0, 0), worldUpType="vector", w=1, aimVector=(vector[0], vector[1], vector[2]), worldUpVector=(0, 1, 0)))
				
			
		if n == (len(doList)):
			cmds.parent(locs[n - 1], doList[n - 1])
			#float $nextCT[] = `xform -q -ws -t $list[$n-2]`;
			#float $aimVector[] = `zooCSTUpVector_float $list[$n-1] $nextCT`;
			# parent current locator in, 0 out 
			cmds.setAttr((locs[n - 1] + ".r"), 
				0, 0, 0)
			vector=aimVectors[n - 1]
			aimName=cmds.aimConstraint(locs[n - 2], locs[n - 1], upVector=(0, 0, 0), o=(0, 0, 0), worldUpType="vector", w=1, aimVector=((vector[0]), (vector[1]), (vector[2])), worldUpVector=(0, 1, 0))
			aims[n - 1]=aimName[0]
			if rot[n - 1] == 1:
				cmds.delete(cmds.aimConstraint(locs[n - 2], doList[n - 1], upVector=(0, 0, 0), o=(0, 0, 0), worldUpType="vector", w=1, aimVector=((vector[0]), (vector[1]), (vector[2])), worldUpVector=(0, 1, 0)))
				
			
		
	# end for rot
	for obj in locs:
		if cmds.objExists(obj):
			cmds.delete(obj)
			
		
	cmds.delete(newCurve[0])
	# end for delete locators
	# remove curve 
	cmds.setToolTo('selectSuperContext')
	
