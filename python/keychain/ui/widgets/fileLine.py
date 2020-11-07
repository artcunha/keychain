
from PySide2 import QtCore, QtWidgets

class FileLine(QtWidgets.QWidget):
    valueSet = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(FileLine, self).__init__(parent)

        self.text = QtWidgets.QLineEdit()
        self.text.returnPressed.connect(self.apply)
        self.button = QtWidgets.QPushButton('B')
        self.button.setFixedSize(21, 21)
        self.button.released.connect(self.browse)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self._value = self.value()

    def browse(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, 'select')
        self.text.setText(dialog[0])
        self.apply()

    def apply(self):
        self.valueSet.emit(self.text.text())

    def value(self):
        value = self.text.text()
        return value if value != '' else None

    def set_value(self, value):
        self.text.setText(value)
