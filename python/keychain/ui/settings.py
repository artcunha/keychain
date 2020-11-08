from PySide2 import QtCore, QtWidgets

from keychain.api import settings as settings_api
from keychain.ui import widgets

MAPPING = {
    "int" : widgets.dragSpinBox.DragSpinBox,
    "double" : widgets.dragSpinBox.DragSpinBox,
    "bool" : widgets.checkBox,
    "str" : widgets.lineEdit.LineEdit,
    "list" : widgets.comboBox,

    "file" : widgets.fileLine.FileLine,
}

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, settings, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.settings = settings
        self.build_ui(settings)
    
    def build_ui(self, settings):
        
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        for stings in settings:
            widget = MAPPING.GET(stings.type, None)
            widget(**stings.as_dict())
            main_layout.addWidget(widget)
    