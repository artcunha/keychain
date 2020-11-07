from PySide2 import QtCore, QtWidgets

class LineEdit(QtWidgets.QWidget):

    def __init__(self,label, default_text="", tooltip="", label_width=None, parent=None):
        super(LineEdit, self).__init__(parent)

        self.setToolTip(tooltip)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.line = QtWidgets.QLineEdit(default_text)

        label = QtWidgets.QLabel(label)
        label.setAlignment(QtCore.Qt.AlignRight)
        if label_width is not None:
            label.setFixedWidth(label_width)

        layout.addWidget(label)
        layout.addWidget(self.line)
