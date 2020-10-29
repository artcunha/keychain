class Test(QtWidgets.QWidget):
    """
    Test widget.
    """
    
    def __init__(self, parent=None):
        super(MyTool, self).__init__(parent)

        self.setWindowTitle("Custom spinboxes")

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(int_spinbox)
        main_layout.addWidget(self.float_spinbox)
        self.setLayout(self.main_layout)


test = Test()
test.resize(300, 150)
test.show()