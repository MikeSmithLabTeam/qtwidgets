from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from .spinbox import QSteppedSpinBox


class QCustomTextBox(QWidget):
    valueChanged = pyqtSignal(str)

    def __init__(self,
                 parent: QWidget = None,
                 title: str = '',
                 value_: str = None,
                 checkbox: bool =False
                 ):
        QWidget.__init__(self, parent)

        self.title = title

        self.layout = QHBoxLayout()

        self.title_label = QLabel(title, self)
        self.layout.addWidget(self.title_label)

        textbox = QLineEdit(str(value_))
        textbox.returnPressed.connect(lambda x=textbox.text: self.onValueChanged(x))
        self.layout.addWidget(textbox)

        if checkbox:
            self.checkbox = QCheckBox(self)
            self.checkbox.stateChanged.connect(self.checkboxChanged)
            self.layout.addWidget(self.checkbox)
        else:
            self.checkbox = None

        self.setLayout(self.layout)

    def value(self):
        return self.textbox.value()

    def onValueChanged(self, text_method) -> None:
        text = text_method()
        if self.checkbox:
            if self.checkbox.isChecked == Qt.Checked:
                self.valueChanged.emit(text)
        else:
            self.valueChanged.emit(text)

    def checkboxChanged(self) -> None:
        self.onValueChanged(self.slider.value())