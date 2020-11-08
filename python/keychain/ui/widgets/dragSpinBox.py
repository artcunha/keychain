from PySide2 import QtCore, QtGui, QtWidgets

class DragSpinBox(QtWidgets.QLineEdit):
    """
    Custom 'spinBox' to mimic the middle-mouse scrollable behaviour of maya's channelBox.
    Source: https://stackoverflow.com/a/55685048
    """

    INT = "int"
    DOUBLE = "double"

    def __init__(self, type="int", default=0, minimum=None, maximum=None, parent=None):
        super(DragSpinBox, self).__init__(parent)

        self.setToolTip(
            "Hold and drag middle mouse button to adjust the value\n"
            "(Hold CTRL or SHIFT change rate)"
        )

        if type == DragSpinBox.INT:
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
        super(DragSpinBox, self).wheelEvent(event)

        steps_mult = self.getStepsMultiplier(event)

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
            super(DragSpinBox, self).mousePressEvent(event)
            self.selectAll()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.value_at_press = None
            self.pos_at_press = None
            self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            return

        super(DragSpinBox, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() != QtCore.Qt.MiddleButton:
            return

        if self.pos_at_press is None:
            return

        steps_mult = self.getStepsMultiplier(event)

        delta = event.pos().x() - self.pos_at_press.x()
        delta /= 6  # Make movement less sensitive.
        delta *= self.steps * steps_mult

        value = self.value_at_press + delta
        self.setValue(value)

        super(DragSpinBox, self).mouseMoveEvent(event)

    def getStepsMultiplier(self, event):
        steps_mult = 1

        if event.modifiers() == QtCore.Qt.CTRL:
            steps_mult = 10
        elif event.modifiers() == QtCore.Qt.SHIFT:
            steps_mult = 0.1

        return steps_mult

    def setSteps(self, steps):
        if self.type == DragSpinBox.INT:
            self.steps = max(steps, 1)
        else:
            self.steps = steps

    def value(self):
        if self.type == DragSpinBox.INT:
            return int(self.text())
        else:
            return float(self.text())

    def setValue(self, value):
        if self.minimum:
            value = max(value, self.minimum)

        if self.maximum:
            value = min(value, self.maximum)

        if self.type == DragSpinBox.INT:
            self.setText(str(int(value)))
        else:
            self.setText(str(float(value)))

class Test(QtWidgets.QWidget):
    """
    Test widget.
    """
    
    def __init__(self, parent=None):
        super(MyTool, self).__init__(parent)

        self.setWindowTitle("Custom spinboxes")

        int_spinbox = DragSpinBox(DragSpinBox.INT, parent=self)
        int_spinbox.setMinimum(-50)
        int_spinbox.setMaximum(100)

        float_spinbox = DragSpinBox(DragSpinBox.DOUBLE, parent=self)
        float_spinbox.setSteps(0.1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(int_spinbox)
        main_layout.addWidget(float_spinbox)
        self.setLayout(main_layout)

tool_instance = TestDragSpinBox()
tool_instance.resize(300, 150)
tool_instance.show()