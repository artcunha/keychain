from PySide2 import QtCore, QtGui, QtWidgets

class DragLine(QtWidgets.QLineEdit):
    """
    Custom 'spinBox' to mimic the middle-mouse scrollable behaviour of maya's channelBox.
    Source: https://stackoverflow.com/a/55685048
    """

    INT = "int"
    DOUBLE = "double"

    def __init__(self, type="int", default=0, minimum=None, maximum=None, parent=None, **kwargs):
        super(DragLine, self).__init__(parent)

        self.setToolTip(
            "Hold and drag middle mouse button to adjust the value\n"
            "(Hold CTRL or SHIFT change rate)"
        )

        if type == DragLine.INT:
            self.setValidator(QtGui.QIntValidator(parent=self))
        else:
            self.setValidator(QtGui.QDoubleValidator(parent=self))

        self.type = type
        self.minimum = minimum
        self.maximum = maximum
        self.steps = 1
        self.value_at_press = None
        self.pos_at_press = None

        self.setValue(default)

    def wheelEvent(self, event):
        super(DragLine, self).wheelEvent(event)

        steps_mult = self.get_steps_multiplier(event)

        if event.delta() > 0:
            self.setValue(self.value() + self.steps * steps_mult)
        else:
            self.setValue(self.value() - self.steps * steps_mult)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.MiddleButton:
            self.value_at_press = self.value()
            self.pos_at_press = event.pos()
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        else:
            super(DragLine, self).mousePressEvent(event)
            self.selectAll()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.value_at_press = None
            self.pos_at_press = None
            self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            return

        super(DragLine, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() != QtCore.Qt.MiddleButton:
            return

        if self.pos_at_press is None:
            return

        steps_mult = self.get_steps_multiplier(event)

        delta = event.pos().x() - self.pos_at_press.x()
        delta /= 6  # Make movement less sensitive.
        delta *= self.steps * steps_mult

        value = self.value_at_press + delta
        self.setValue(value)

        super(DragLine, self).mouseMoveEvent(event)

    def get_steps_multiplier(self, event):
        steps_mult = 1

        if event.modifiers() == QtCore.Qt.CTRL:
            steps_mult = 10
        elif event.modifiers() == QtCore.Qt.SHIFT:
            steps_mult = 0.1

        return steps_mult

    def set_steps(self, steps):
        if self.type == DragLine.INT:
            self.steps = max(steps, 1)
        else:
            self.steps = steps

    def value(self):
        if self.type == DragLine.INT:
            return int(self.text())
        else:
            return float(self.text())

    def setValue(self, value):
        if self.minimum:
            value = max(value, self.minimum)

        if self.maximum:
            value = min(value, self.maximum)

        if self.type == DragLine.INT:
            self.setText(str(int(value)))
        else:
            self.setText(str(float(value)))


class DragSpinBox(QtWidgets.QWidget):

    def __init__(self, label, tooltip="", label_width=None, type="int", default=0, minimum=None, maximum=None,  parent=None, **kwargs):
        super(DragSpinBox, self).__init__(parent)

        self.setToolTip(tooltip)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.line = DragLine(type="int", default=0, minimum=None, maximum=None,  parent=None, **kwargs)

        label = QtWidgets.QLabel(label)
        label.setAlignment(QtCore.Qt.AlignRight)
        if label_width is not None:
            label.setFixedWidth(label_width)

        layout.addWidget(label)
        layout.addWidget(self.line)
