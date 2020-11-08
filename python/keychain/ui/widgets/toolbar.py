from PySide2 import QtCore, QtWidgets, QtGui
import importlib

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


TOOL_PATH = "keychain.tools.{tool}.main"
class Toolbar(MayaQWidgetDockableMixin,QtWidgets.QWidget):
    def __init__(self, parent=ui.maya_qt.get_maya_window()):
        super(Toolbar, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        
        self.setWindowTitle("Path Tool")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setLayout(layout)
        
        # settings = settings_api.get_settings("keychain")
        # self.tools_list = settings.get("UI").get("tools")
        self.tools_list = ["archer","tracer"]

        for tool in self.tools_list:
            icon = QtGui.QIcon(":/{}.png".format(tool))
            button = QtWidgets.QToolButton()
            button.setFixedSize(60,60)
            # button.setIcon(icon)
            button.setText(tool)
            button.setIconSize(QtCore.QSize(20,20))
            
            # button.clicked.connect(getattr(importlib.import_module(TOOL_PATH.format(tool=tool)), "launch"))
            button.setDefaultAction(getattr(importlib.import_module(TOOL_PATH.format(tool=tool)), "launch"))

            layout.addWidget(button)
            
def launch():
    toolbar = Toolbar()
    toolbar.show(dockable=True, floating=False, area='bottom')
