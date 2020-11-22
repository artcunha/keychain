from PySide2 import QtCore, QtWidgets
from keychain.ui.widgets import signals

class LineEdit(QtWidgets.QWidget):
    value_signal = signals.StrSignal()

    def __init__(self, label, default_text="", tooltip="", label_width=None, parent=None, **kwargs):
        super(LineEdit, self).__init__(parent)

        self.setToolTip(tooltip)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.line = QtWidgets.QLineEdit(default_text)
        self.line.textChanged.connect(self.value_signal.value_changed_signal.emit)

        label = QtWidgets.QLabel(label)
        # label.setAlignment(QtCore.Qt.AlignRight)
        if label_width is not None:
            label.setFixedWidth(label_width)

        layout.addWidget(label)
        layout.addWidget(self.line)
