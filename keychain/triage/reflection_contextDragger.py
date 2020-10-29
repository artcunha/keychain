# ----------------------------------------------------------------------
# placeReflection.py
#
# Copyright (c) 2018 Ingo Clemens, brave rabbit
# www.braverabbit.com
# ----------------------------------------------------------------------

VERSION = {"version": [1, 2, 7], "date": "2018-12-14"}

# ----------------------------------------------------------------------
# Description:
#
# This tool creates a standard dragger context which places the selected
# object at a reflected position based on the view vector and the
# surface normal of a mesh at the cursor position.
# Though any object can be placed this way it's main usage is to easily
# place a light so that the main light reflection occurs at the point
# of the cursor.
#
# The tool has two modes:
# Place Mode: The default dragger context mode. LMB click and drag to
#             place the selected object based on the surface the cursor
#             is dragged over.
# Move Mode: Press and hold Shift or Ctrl while dragging. This moves
#            the object towards/away from the reflection point. Ctrl
#            gives a finer control whereas Shift performs the moving
#            in a faster fashion.
#
# ----------------------------------------------------------------------
# Usage:
#
# When properly installed the Maya Modify menu has a new menu item named
# Place Reflection. It also allows to open a standard option box to set
# the preferences for the tool.
#
# Standalone Usage:
# When using the script without the supplementary scripts the tool can
# be activated using the following commands with the current selection:
#
# # import the module and create the context
# from placeReflection import placeReflectionTool
# placeReflectionTool.create()
#
# ----------------------------------------------------------------------
# Preferences:
#
# The tool has the following preference settings:
#   axis: Defines the axis which is aimed at the point of reflection.
#           Values:
#               0: x axis
#               1: y axis
#               2: z axis (default)
#   invert: True, if the axis should point away from the reflection
#           point. Default is True.
#   rotate: True, if the rotation of the placing obeject should be
#           affected. Default is True.
#   speed: The speed when moving the object towards/away from the
#          reflection point in move mode.
#          Defaults are:
#               0: Slow: 0.001
#               1: Fast: 0.01
#   translate: True, if the translation of the placing object should be
#              affected. Default is True.
#
# When setting these values for the existing context they get stored
# with the Maya preferences:
# placeReflectionTool.setInvert(True)
# placeReflectionTool.setSpeed(0, 0.001) # slow: 0.001
#
# To read the current settings use:
# placeReflectionTool.invert()
# placeReflectionTool.speed(0) # slow
#
# ----------------------------------------------------------------------
# Changelog:
#
#   1.2.7 - 2018-12-14
#         - Fixed that the in-view message displayed the modifier-keys
#           in the wrong order.
#         - Fixed some code typos.
#
#   1.2.6 - 2018-10-29
#         - Fixed that the menu items are not correctly added in Maya
#           2016.
#
#   1.2.5 - 2018-10-23
#         - Updated the icon to SVG.
#
#   1.2.4 - 2018-10-14
#         - Added a preference for the in-view message.
#
#   1.2.3 - 2018-10-09
#         - Added an in-view message when the tool is active.
#
#   1.2.2 - 2018-10-07
#         - In case the menu item cannot be added to the modify menu a
#           new menu gets created after the last.
#         - Fixed an incompatibility when calling the tool from another
#           module.
#         - Adjustments to the option box.
#         - Added the quick zoom tool.
#
#   1.2.1 - 2018-10-05
#         - Reversed the speed modifiers shift and ctrl to be more
#           inline with the default Maya navigation (channel box).
#         - Having no placing object selected is now only a warning.
#         - Added a method to read the version.
#
#   1.2.0 - 2018-10-04
#         - Added the option to define the axis which should aim towards
#           the point of reflection.
#         - Added the options to either affect just the translation or
#           the rotation of the placing object.
#         - Added a standard Maya option dialog for setting tool
#           preferences.
#         - Added a menu item in the default Maya modify menu.
#
#   1.1.0 - 2018-10-03
#         - Added a second speed mode which is accesible by pressing the
#           control key (shift: slow, ctrl: fast)
#         - Changed the optionVar names to reflect the new speed
#           settings.
#         - The executing _place() method now directly receives the
#           modifier key instead of just a boolean to turn move mode on
#           or off.
#         - Fixed a stutter during the placing when the placing object
#           moved under the cursor and gets picked as the object to drag
#           on.
#
#   1.0.0 - 2018-10-02
#         - Initial version.
#
# ----------------------------------------------------------------------

from maya.api import OpenMaya as om2
from maya.api import OpenMayaUI as om2UI
from maya import OpenMaya as om
from maya import cmds, mel

import math

import logging

logger = logging.getLogger(__name__)

CONTEXT_NAME = "brPlaceReflectionContext"

AFFECT_TRANSLATION = "brPlaceReflectionAffectTranslation"
AFFECT_ROTATION = "brPlaceReflectionAffectRotation"
INVERT_AXIS = "brPlaceReflectionInvertAxis"
MESSAGE_TYPE = "brPlaceReflectionMessageType"
ORIENT_AXIS = "brPlaceReflectionAxis"
SPEED_SLOW = "brPlaceReflectionSpeedSlow"
SPEED_FAST = "brPlaceReflectionSpeedFast"

SPEED_SLOW_VALUE = 0.001
SPEED_FAST_VALUE = 0.01

VIEW_MESSAGE = ("<hl>Drag</hl> to place.  |  "
                "<hl>Shift drag</hl> to move fast.  |  "
                "<hl>Ctrl drag</hl> to move slow.")


class PlaceReflection():

    def __init__(self):
        self._view = om2UI.M3dView()
        self._dag = None
        self._meshDag = None

        # Switch to make sure that values are present when using the
        # move mode.
        self._isSet = False

        # the world point of reflection on the surface
        self._reflPoint = None
        # The distance of the object from the surface.
        # This is used to store the distance during placing as well as
        # moving because the move mode needs a static base value to
        # calculate the new distance from.
        self._dist = 0.0
        # The distance of the object from the surface after moving.
        # This is used to be able to remember the last moved position
        # in case the move mode is performed with a new press and drag
        # operation after the placement. If this value is not stored the
        # new drag would always start from the self._dist position and
        # not from the last known self._moveDist position.
        self._moveDist = 0.0
        # the reflection vector
        self._reflVector = None

        # create the preference settings if they don't exist
        self._setOptionVars()

        self._axis = 2
        self._invert = True
        self._translate = True
        self._rotate = True
        self._speedSlow = 0.001
        self._speedFast = 0.01
        self._viewType = 2


    # ------------------------------------------------------------------
    # context creating and deleting
    # ------------------------------------------------------------------

    def create(self):
        """Create the dragger context and set it to be the active tool.
        """
        helpString = ("Press and drag over surface to place the selection. "
                      "Hold ctrl (slow) or shift (fast) to move.")
        if not cmds.draggerContext(CONTEXT_NAME, exists=True):
            cmds.draggerContext(CONTEXT_NAME,
                                pressCommand=self._press,
                                dragCommand=self._drag,
                                releaseCommand=self._release,
                                initialize=self._initialize,
                                finalize=self._finalize,
                                space="screen",
                                stepsCount=1,
                                undoMode="step",
                                cursor="crossHair",
                                helpString=helpString,
                                image1="placeReflection.svg")
            logger.info("Created {}".format(CONTEXT_NAME))
        cmds.setToolTo(CONTEXT_NAME)

    def delete(self):
        """Delete the dragger context.
        """
        tool = mel.eval("global string $gSelect; setToolTo $gSelect;")
        cmds.deleteUI(CONTEXT_NAME)
        logger.info("Deleted {}".format(CONTEXT_NAME))


    def _message(self, msg):
        """Display the given message as a status in-view message.

        :param msg: The message string to display.
        :type msg: str
        """
        if not self._viewType:
            return
        cmd = "inViewMessage"
        if self._viewType == 1:
            cmd += " -assistMessage \"{}\"".format(msg)
        elif self._viewType == 2:
            cmd += " -statusMessage \"{}\"".format(msg)
        cmd += " -position \"topCenter\""
        mel.eval(cmd)


    def _deleteMessage(self):
        """Delete the in view message.
        """
        if self._viewType:
            cmds.inViewMessage(clear="topCenter")


    def _version(self, long=True):
        """Return the tool version.

        :param long: True, if the version number and date should get
                     returned.
        :type long: bool

        :return: The version string.
        :rtype: str
        """
        version = ".".join([str(i) for i in VERSION["version"]])
        if not long:
            return version
        version = "{} {}".format(version, VERSION["date"])
        return version


    # ------------------------------------------------------------------
    # context commands
    # ------------------------------------------------------------------

    def _press(self):
        """Method to be executed when the mouse button is pressed.

        Get the current view and object to place.
        """
        self._view = om2UI.M3dView().active3dView()
        # get the MDagPath of the object to place
        self._dag = self._asDagPath()
        if self._dag is None:
            return
        # Set the distance to the last move distance so that the move
        # doesn't start from the original distance but the last modified
        # position.
        self._dist = self._moveDist


    def _drag(self):
        """Method to be executed when the mouse is dragged.

        Get the drag point and perform the placing.
        """
        # do nothing if there is no object selected to be placed
        if self._dag is None:
            return

        # get the drag points from the context and perform the placing
        anchorPoint = cmds.draggerContext(CONTEXT_NAME, query=True, anchorPoint=True)
        dragPoint = cmds.draggerContext(CONTEXT_NAME, query=True, dragPoint=True)
        modifier = cmds.draggerContext(CONTEXT_NAME, query=True, modifier=True)
        
        self.x, self.y, self.z = self.dragPoint


    def _release(self):
        """Method to be executed when the mouse button is released.

        Clear the view and object to place.
        """
        self._view = om2UI.M3dView()
        self._dag = None
        self._meshDag = None


    def _initialize(self):
        """Method to be executed when the tool is entered.
        """
        self._message(VIEW_MESSAGE)


    def _finalize(self):
        """Method to be executed when the tool is exited.

        Mark the context as unused.
        """
        self._moveDist = 0.0
        self._isSet = False
        self._deleteMessage()
        logger.info("Reset {}".format(CONTEXT_NAME))


    def _getMesh(self, xPos, yPos):
        """Return the MDagPath of the object at the cursor position.
        The current selection is left untouched.

        To get the object at the cursor MGlobal.selectFromScreen is used.
        But since this is not available in the new API it's performed
        using the old API and then converted using the full path name.

        :param xPos: The screen-based x position of the cursor.
        :type xPos: int
        :param yPos: The screen-based y position of the cursor.
        :type yPos: int

        :return: The MDagPath of the object at the cursor position.
        :rtype: om2.MDagPath
        """
        sel = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(sel)

        om.MGlobal.selectFromScreen(xPos, yPos, om.MGlobal.kReplaceList,
                                    om.MGlobal.kSurfaceSelectMethod)
        fromScreen = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(fromScreen)

        om.MGlobal.setActiveSelectionList(sel, om.MGlobal.kReplaceList)

        if fromScreen.length():
            dagPath = om.MDagPath()
            fromScreen.getDagPath(0, dagPath)

            # Prevent the case where the object to be placed (for
            # example a light) passes the camera view at the cursor
            # position. The light would get picked as the object under
            # the cursor and the method would return None causing the
            # placing to stutter.
            # Therefore the selected object's name gets checked against
            # the name of the placing object.
            # Important:
            # This needs to happen on a string level because the two
            # APIs are getting mixed here. dagPath is OpenMaya and
            # self._dag is OpenMaya.api.
            # The check is:
            # If the object under the cursor is the same as the placing
            # object and the mesh the context is dragging on is defined
            # it's safe to return the last known mesh name as the mesh
            # to perform the dragging on.
            if dagPath.fullPathName() == self._dag.fullPathName() and self._meshDag is not None:
                return self._meshDag

            dagPath.extendToShape()
            name = dagPath.fullPathName()

            if not dagPath.hasFn(om.MFn.kMesh):
                return

            # converting to maya.api
            return self._asDagPath(name)


    def _closestIntersection(self, dagPath, worldPt, worldVector):
        """Return the closest intersection data for the given mesh with
        the given point and vector.

        :param dagPath: The MDagPath of the mesh object.
        :type dagPath: om2.MDagPath
        :param worldPt: The world point of the ray to test for
                        intersection with.
        :type worldPt: om2.MPoint
        :param worldVector: The MVector of the intersection ray.
        :type worldVector: om2.MVector

        :return: The tuple with the intersection data:
                 hitPoint: The intersection point.
                 hitRayParam: The ray length to the intersection.
                 hitFace: The face index of the intersection.
                 hitTriangle: The relative index of the trangle.
                 hitBary1: First barycentric coordinate.
                 hitBary2: Second barycentric coordinate.
        :rtype: tuple(om2.MFloatPoint, float, int, int, float, float)
        """
        meshFn = om2.MFnMesh(dagPath)

        accelParams = om2.MMeshIsectAccelParams()
        accelParams = meshFn.autoUniformGridParams()

        return meshFn.closestIntersection(om2.MFloatPoint(worldPt),
                                          om2.MFloatVector(worldVector),
                                          om2.MSpace.kWorld,
                                          100000, # maxParam
                                          True)


    def _reflectionVector(self, viewVector, faceNormal):
        """Return the reflection vector based on the given view vector
        and normal at the reflection point.

        :param viewVector: The MVector of the reflection source ray.
        :type viewVector: om2.MVector
        :param faceNormal: The MVector of the normal at the reflection
                           point.
        :type faceNormal: om2.MVector

        :return: The MVector of the reflection.
        :rtype: om2.MVector
        """
        doublePerp = 2.0 * viewVector * faceNormal
        return viewVector - (doublePerp * faceNormal)
