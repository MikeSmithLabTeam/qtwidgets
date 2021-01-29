from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from .spinbox import QSteppedSpinBox


class QCustomTextBox(QWidget):
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
            self.checkbox.stateChanged.connect(self.checkboxChanged)
            self.layout.addWidget(self.checkbox)
            self.checkbox.setEnabled(True)
            self.checkbox.setChecked(True)
        else:
            self.checkbox = None

        self.setLayout(self.layout)

    def value(self):
        return self.textbox.text()

    def onValueChanged(self) -> None:
        self.text = self.value()
        if self.checkbox:
            if self.checkbox.isChecked == Qt.Checked:
                self.returnPressed.emit(self.text)
        else:
            self.returnPressed.emit(self.text)

    def checkboxChanged(self) -> None:
        checkstate = self.checkbox.isChecked()
        if checkstate:
            self.slider.setEnabled(True)
            self.spinbox.setEnabled(True)
            self.returnPressed.emit(self.value)
        else:
            self.slider.setEnabled(False)
            self.spinbox.setEnabled(False)
