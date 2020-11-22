
from PySide2 import QtCore


class BoolSignal(QtCore.QObject):
    value_changed_signal = QtCore.Signal(bool)

class IntSignal(QtCore.QObject):
    value_changed_signal = QtCore.Signal(int)

class FloatSignal(QtCore.QObject):
    value_changed_signal = QtCore.Signal(float)

class StrSignal(QtCore.QObject):
    value_changed_signal = QtCore.Signal(str)
