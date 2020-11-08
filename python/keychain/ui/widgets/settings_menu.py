from PySide2 import QtCore, QtWidgets

from keychain.ui import constants

class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, settings, parent=None):
        super(SettingsMenu, self).__init__(parent)
        self.settings = settings
        self.build_ui(settings)
    
    def build_ui(self, settings):
        
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        for stings in settings:
            widget = constants.MAPPING.GET(stings.type, None)
            widget(**stings.as_dict())
            main_layout.addWidget(widget)
    