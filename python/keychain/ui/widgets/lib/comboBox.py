from PySide2 import QtCore, QtWidgets


class ComboBox(QtWidgets.QCheckBox):

    value_changed_signal = QtCore.Signal()
    
    def __init__(self,items, tooltip="", parent=None, **kwargs):
        super(ComboBox, self).__init__(items, parent=parent)

        self.setToolTip(tooltip)

        self.currentIndexChanged.connect(self.value_changed_signal.emit)
