from keychain.ui.widgets.lib import dragSpinBox, checkBox, lineEdit, comboBox, fileLine, label

MAPPING = {
    "int" : dragSpinBox.DragSpinBox,
    "double" : dragSpinBox.DragSpinBox,
    "bool" : checkBox.CheckBox,
    "str" : lineEdit.LineEdit,
    "list" : comboBox.ComboBox,

    "label" : label.Label,
    "file" : fileLine.FileLine,
    "folder" : fileLine.FolderLine,
}
