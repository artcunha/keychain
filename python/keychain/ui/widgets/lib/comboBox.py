from PySide2 import QtCore, QtWidgets
from keychain.ui.widgets import signals


class ComboBox(QtWidgets.QCheckBox):

    value_signal = signals.IntSignal()
    
    def __init__(self,items, tooltip="", parent=None, **kwargs):
        super(ComboBox, self).__init__(items, parent=parent)

        self.setToolTip(tooltip)

        self.currentIndexChanged.connect(self.value_signal.value_changed_signal.emit)
