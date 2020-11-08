import importlib
from PySide2 import QtCore, QtWidgets, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from keychain.core import config as config_api
from keychain.core import settings as settings_api
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
        
        kc_config = config_api.get_config("keychain")
        self.tools_list = kc_config.get("UI").get("tools")
        
        self.tools_settings = {tool : settings_api.get_settings(tool) for tool in self.tools_list}
        # Create the ToolButton for each tool
        [self.add_tool(tool) for tool in self.tools_list]

        
    def add_tool(self, tool):
        icon = QtGui.QIcon(":/{}.png".format(tool))
        button = QtWidgets.QToolButton()
        # Set right click menu
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(lambda point: self.on_context_menu(point, button))
        # Aesthetics
        button.setFixedSize(60,60)
        # button.setIcon(icon)
        button.setText(tool)
        button.setIconSize(QtCore.QSize(20,20))
        
        # Connect slot
        button.clicked.connect(getattr(importlib.import_module(TOOL_PATH.format(tool=tool)), "launch"))
        # button.setDefaultAction(getattr(importlib.import_module(TOOL_PATH.format(tool=tool)), "launch"))

        self.layout().addWidget(button)
    
    def on_context_menu(self, point, button):
        # Show settings context menu
        tool_sting = self.tools_settings.get(button.text())
        if not tool_sting:
            return
        menu = settings_menu.SettingsMenu(tool_sting, parent=self)
        # menu.exec_(self.button.mapToGlobal(point))    
        menu.move(button.mapToGlobal(point)) 
        menu.show()  


def launch():
    toolbar = Toolbar()
    toolbar.show(dockable=True, floating=False, area="top")

