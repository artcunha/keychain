from PySide2 import QtCore, QtWidgets

from keychain.ui import constants

class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, settings, parent=None):
        super(SettingsMenu, self).__init__(parent)
        self.settings = settings
        # self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        self.build_ui(settings)
    
    def build_ui(self, settings):
        
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        for sting, attrs in settings.items():
            widget = constants.MAPPING[attrs.get("type")]
            attr_widget = widget(sting, **attrs)
            main_layout.addWidget(attr_widget)
    