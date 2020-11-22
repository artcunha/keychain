from PySide2 import QtCore, QtWidgets
from keychain.ui.widgets import signals

class CheckBox(QtWidgets.QCheckBox):

    value_signal = signals.BoolSignal()

    def __init__(self,label=None, tooltip="", parent=None, **kwargs):
        super(CheckBox, self).__init__(label, parent=parent)

        self.setToolTip(tooltip)

        self.stateChanged.connect(self.value_signal.value_changed_signal.emit)
