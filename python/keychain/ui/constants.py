from keychain.ui.widgets.lib import dragSpinBox, checkBox, lineEdit, comboBox, fileLine

MAPPING = {
    "int" : dragSpinBox.DragSpinBox,
    "double" : dragSpinBox.DragSpinBox,
    "bool" : checkBox.CheckBox,
    "str" : lineEdit.LineEdit,
    "list" : comboBox.ComboBox,

    "file" : fileLine.FileLine,
}
