
from PySide2 import QtCore, QtWidgets, QtGui

class FileLine(QtWidgets.QWidget):
    value_changed_signal = QtCore.Signal()

    def __init__(self, parent=None, **kwargs):
        super(FileLine, self).__init__(parent)

        self.text_line = QtWidgets.QLineEdit()
        self.text_line.returnPressed.connect(self.apply)
        label = QtWidgets.QLabel(kwargs.get("label"))
        
        button = QtWidgets.QPushButton('B')
        icon = QtGui.QIcon(":/folder-open.png")
        button.setIcon(icon)
        button.setFixedSize(21, 21)
        button.released.connect(self.browse)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(label)
        layout.addWidget(self.text_line)
        layout.addWidget(button)

        self._value = self.value()

    def browse(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, 'select')
        self.text_line.setText(dialog[0])
        self.apply()

    def apply(self):
        self.value_changed_signal.emit(self.text_line.text())

    def value(self):
        value = self.text_line.text()
        return value if value != '' else None

    def set_value(self, value):
        self.text_line.setText(value)

class FolderLine(FileLine):
    value_changed_signal = QtCore.Signal(str)

    def __init__(self, parent=None, **kwargs):
        super(FolderLine, self).__init__(parent)

    def browse(self):
        browser = QtWidgets.QFileDialog()
        filepath = browser.getExistingDirectory()
        self.text_line.setText(filepath)

        self.apply()
