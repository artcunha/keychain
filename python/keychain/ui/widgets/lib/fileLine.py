
from PySide2 import QtCore, QtWidgets

class FileLine(QtWidgets.QWidget):
    value_set_signal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(FileLine, self).__init__(parent)

        self.text_line = QtWidgets.QLineEdit()
        self.text_line.returnPressed.connect(self.apply)
        button = QtWidgets.QPushButton('B')
        button.setFixedSize(21, 21)
        button.released.connect(self.browse)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.text_line)
        layout.addWidget(button)

        self._value = self.value()

    def browse(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, 'select')
        self.text_line.setText(dialog[0])
        self.apply()

    def apply(self):
        self.value_set_signal.emit(self.text_line.text())

    def value(self):
        value = self.text_line.text()
        return value if value != '' else None

    def set_value(self, value):
        self.text_line.setText(value)
