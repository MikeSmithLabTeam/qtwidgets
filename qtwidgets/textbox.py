from PyQt6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QCheckBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from .spinbox import QSteppedSpinBox


class QCustomTextBox(QWidget):
    """This textbox is a custom widget that allows the user to input text.
    It has a title, a textbox and a checkbox.
    The checkbox is used to enable or disable the textbox.
    The textbox is used to input text.
    The title is used to describe the textbox.
    When the user presses enter, the text is emitted via the returnPressed signal.
    """
    returnPressed = pyqtSignal(str)

    def __init__(self,
                 parent: QWidget = None,
                 title: str = '',
                 value_: str = None,
                 checkbox: bool =False
                 ):
        QWidget.__init__(self, parent)

        self.title = title
        self.text=value_
        self.layout = QHBoxLayout()

        self.title_label = QLabel(title, self)
        self.layout.addWidget(self.title_label)

        self.textbox = QLineEdit(str(value_))
        self.textbox.returnPressed.connect(self.onValueChanged)
        self.layout.addWidget(self.textbox)

        if checkbox:
            self.checkbox = QCheckBox(self)
            self.checkbox.setEnabled(True)
            self.checkbox.setChecked(True)
            self.checkbox.stateChanged.connect(self.checkboxChanged)
            self.layout.addWidget(self.checkbox)

        else:
            self.checkbox = None

        self.setLayout(self.layout)

    def value(self):
        return self.textbox.text()

    def onValueChanged(self) -> None:
        self.text = self.value()
        if self.checkbox:
            #If there is a checkbox and it is checked then return value when enter pressed
            if self.checkbox.isChecked():
                self.returnPressed.emit(self.text)
        else:
            #If no checkbox return value when enter pressed
            self.returnPressed.emit(self.text)

    def checkboxChanged(self) -> None:
        checkstate = self.checkbox.isChecked()
        if checkstate:
            self.textbox.setEnabled(True)
            self.text = self.value()
            #self.returnPressed.emit(self.text)
        else:
            self.textbox.setEnabled(False)
