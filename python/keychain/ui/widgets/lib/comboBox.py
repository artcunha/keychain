from PySide2 import QtCore, QtWidgets


class ComboBox(QtWidgets.QCheckBox):

    def __init__(self,items, tooltip="", parent=None, **kwargs):
        super(ComboBox, self).__init__(items, parent=parent)

        self.setToolTip(tooltip)