from PySide2 import QtGui, QtCore, QtWidgets
from keychain.api import settings as settings_api


class Toolbar(QtWidgets.QWidget):
    layout = QtWidgets.QHBoxLayout()
    self.setLayout(layout)
    
    settings = settings_api.get_settings("keychain")
    self.tools_list = settings.get("UI").get("tools")

    for tool in self.tools_list:
        icon = QtGui.QIcon(":/{}.png".format(tool))
        button = QtWidgets.QToolButton()
        button.setFixedSize(24,24)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(20,20))
        cmd = "from keychain.tools import {0};{0}.launch()".format(tool)
        button.clicked.connect(cmd)

        layout.addWidget(button)

def launch():
    toolbar = Toolbar()
    toolbar.show()
