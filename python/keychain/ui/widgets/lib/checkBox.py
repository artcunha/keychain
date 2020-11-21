from PySide2 import QtCore, QtWidgets

class CheckBox(QtWidgets.QCheckBox):

    value_changed_signal = QtCore.Signal()

    def __init__(self,label=None, tooltip="", parent=None, **kwargs):
        super(CheckBox, self).__init__(label, parent=parent)

        self.setToolTip(tooltip)

        self.stateChanged.connect(self.value_changed_signal.emit)
