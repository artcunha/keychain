from keychain.ui.widgets.lib import dragSpinBox, checkBox, lineEdit, comboBox, fileLine, label

MAPPING = {
    "int" : dragSpinBox.IntDragSpinBox,
    "double" : dragSpinBox.DoubleDragSpinBox,
    "bool" : checkBox.CheckBox,
    "str" : lineEdit.LineEdit,
    "list" : comboBox.ComboBox,

    "label" : label.Label,
    "file" : fileLine.FileLine,
    "folder" : fileLine.FolderLine,
}
