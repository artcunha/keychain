from keychain.ui.widgets import lib

MAPPING = {
    "int" : lib.dragSpinBox.DragSpinBox,
    "double" : lib.dragSpinBox.DragSpinBox,
    "bool" : lib.checkBox,
    "str" : lib.lineEdit.LineEdit,
    "list" : lib.comboBox,

    "file" : lib.fileLine.FileLine,
}
