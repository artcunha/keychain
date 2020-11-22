from PySide2 import QtCore, QtWidgets

from keychain.ui import constants

class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, settings, parent=None):
        super(SettingsMenu, self).__init__(parent)
        self.settings = settings
        # self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        self.build_ui()
    
    def build_ui(self):
        
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        for sting, attrs in self.settings.items():
            widget = constants.MAPPING[attrs.get("type")]
            attr_widget = widget(**attrs)
            main_layout.addWidget(attr_widget)

            # Connect signal
            if hasattr(widget, "value_signal"):
                widget.value_signal.value_changed_signal.connect(lambda value : self._on_value_changed(sting, value))
        
    def _on_value_changed(self, item, value):
        self.settings.as_dict()[item] = value
