"""
Utility methods for Qt inside maya
"""
import contextlib
from PySide2 import QtCore, QtWidgets
import shiboken2
import functools
import maya.cmds as cmds
import maya.OpenMayaUI as omui


def maya_window():
    """Get the main Maya window as a QtWidgets.QMainWindow instance

    Returns:
        [QtWidgets.QMainWindow]: instance of the top level Maya windows
    """

    mwindow = omui.MQtUtil.mainWindow()
    if mwindow is not None:
        return shiboken2.wrapInstance(long(mwindow), QtWidgets.QWidget)

def ensure_only_widget(name):
    """
    Ensure all existing widgets with the same name are destroyed before the new one is craeted.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if cmds.window(name, exists=True):
                cmds.deleteUI(name)

            wsname = name + "WorkspaceControl"
            if cmds.workspaceControl(wsname, ex=True):
                if cmds.workspaceControlState(wsname, ex=True):
                    cmds.workspaceControlState(wsname, remove=True)
                cmds.deleteUI(wsname)
            return func(*args, **kwargs)
        return wrapper

    return decorator


class MayaWidget(QtWidgets.QWidget):
    def keyPressEvent(self, event):
        """Maya's main window will catch shift and control keys, so accept
        them here to avoid it taking focus"""
        if event.key() in (QtCore.Qt.Key_Shift, QtCore.Qt.Key_Control):
            event.accept()
        else:
            event.ignore()

    @classmethod
    def launch_dialog(cls):
        widget = cls(parent=maya_window())
        widget.show()
        return widget
