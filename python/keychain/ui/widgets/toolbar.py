import importlib
from PySide2 import QtCore, QtWidgets, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from keychain import config
from keychain.api import settings as settings_api
from keychain.ui import maya_qt
from keychain.ui.widgets import settings_menu


TOOL_PATH = "keychain.tools.{tool}.main"
class Toolbar(MayaQWidgetDockableMixin,QtWidgets.QWidget):
    def __init__(self, parent=maya_qt.get_maya_window()):
        super(Toolbar, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        
        self.setWindowTitle("Keychain Toolbar")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Tool)
        
        kc_settings = settings_api.get_settings("keychain")
        self.tools_list = kc_settings.get("UI").get("tools")
        self.tools_list = ["archer","tracer"]

        self.tools_settings = settings_api.get_tools_settings(self.tools_list)
        # Create the ToolButton for each tool
        [self.add_tool(tool) for tool in self.tools_list]

        
    def add_tool(self, tool):
        icon = QtGui.QIcon(":/{}.png".format(tool))
        button = QtWidgets.QToolButton()
        # Set right click menu
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(lambda point: self.on_context_menu(point, tool))
        # Aesthetics
        button.setFixedSize(60,60)
        button.setIcon(icon)
        button.setText(tool)
        button.setIconSize(QtCore.QSize(20,20))
        
        # Connect slot
        button.clicked.connect(getattr(importlib.import_module(TOOL_PATH.format(tool=tool)), "launch"))
        # button.setDefaultAction(getattr(importlib.import_module(TOOL_PATH.format(tool=tool)), "launch"))

        self.layout().addWidget(button)
    
    def on_context_menu(self, point, tool):
        # Show settings context menu
        settings = self.tools_settings.get(tool, None)
        if not settings:
            return
        menu = settings_menu.SettingsMenu(settings, parent=self)
        menu.exec_(self.button.mapToGlobal(point))    


def launch():
    toolbar = Toolbar()
    toolbar.show(dockable=True, floating=False, area="bottom")
