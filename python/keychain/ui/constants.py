from keychain.ui.widgets.lib import dragSpinBox, checkBox, lineEdit, comboBox, fileLine

MAPPING = {
    "int" : dragSpinBox.DragSpinBox,
    "double" : dragSpinBox.DragSpinBox,
    "bool" : checkBox,
    "str" : lineEdit.LineEdit,
    "list" : comboBox,

    "file" : fileLine.FileLine,
}
