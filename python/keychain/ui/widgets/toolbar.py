import importlib
from PySide2 import QtCore, QtWidgets, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from keychain.core import config as config_api
from keychain.core import settings as settings_api
from keychain.ui import maya_qt
from keychain.ui import icons as icons_utils
from keychain.ui.widgets import settings_menu

NAME = "Keychain Toolbar"
TOOL_PATH = "keychain.tools.{tool}.main"
class Toolbar(MayaQWidgetDockableMixin,QtWidgets.QWidget):
    def __init__(self, parent=maya_qt.get_maya_window()):
        super(Toolbar, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(4)
        self.setLayout(layout)
        
        self.setWindowTitle(NAME)
        self.setObjectName(NAME)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Tool)
        
        kc_config = config_api.get_config("keychain")
        self.tools_list = kc_config.get("UI").get("tools")
        
        self.tools_settings ={}
        self.tools_icons = {}
        for tool in self.tools_list:
            config_dict = config_api.get_config(tool)
            if not config_dict or not config_dict.get("settings"):
                continue

            self.tools_settings[tool] = settings_api.Settings(config_dict.get("settings"))
            self.tools_icons[tool] = config_dict.get("icon")
            # Create the ToolButton for each tool
            self.add_tool(tool)

        
    def add_tool(self, tool):
        button = QtWidgets.QToolButton(parent=self)
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.layout().addWidget(button)
        print button.geometry()


        # Connect command slot
        button.clicked.connect(getattr(importlib.import_module(TOOL_PATH.format(tool=tool)), "launch"))

        # Aesthetics
        button.setFixedSize(60,60)
        button.setText(tool)
        # Icon
        path_to_icon = icons_utils.get_icon(self.tools_icons.get(tool))
        if path_to_icon:
            icon = QtGui.QIcon(path_to_icon)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(40,40))
    
        # Set right click settings widget
        tool_sting = self.tools_settings.get(tool)

        if not tool_sting:
            return
        menu = settings_menu.SettingsMenu(tool_sting, parent=button)
        button.customContextMenuRequested.connect(lambda point: self._on_context_menu(menu))

    def _on_context_menu(self, menu):
        # Qt will only have the geometry information once the widget is visible
        # This means we have to separate this into a separate method
        menu.move(menu.parent().mapToGlobal(QtCore.QPoint(40, 0))) 
        menu.show()

@maya_qt.ensure_single_widget(NAME)
def launch():
    toolbar = Toolbar()
    toolbar.show(dockable=True, floating=False, area="top")

