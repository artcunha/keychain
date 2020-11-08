from PySide2 import QtCore, QtWidgets
class CheckBox(QtWidgets.QCheckBox):

    def __init__(self,label, tooltip="", parent=None, **kwargs):
        super(CheckBox, self).__init__(label, parent=parent)

        self.setToolTip(tooltip)