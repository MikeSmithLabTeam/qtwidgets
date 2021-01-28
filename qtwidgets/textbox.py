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
                 label: bool = False,
                 checkbox: bool =False
                 ):
        QWidget.__init__(self, parent)

        self.title = title

        self.layout = QHBoxLayout()

        self.title_label = QLabel(title, self)
        self.layout.addWidget(self.title_label)

        self.textbox = QLineEdit(str(value_))

        if label:
            self.value_label = QLabel(str(value_), self)
            self.layout.addWidget(self.value_label)
        else:
            self.value_label = None

        self.textbox.stateChanged.connect()

        if checkbox:
            self.checkbox = QCheckBox(self)
            self.checkbox.stateChanged.connect(self.checkboxChanged)
            self.layout.addWidget(self.checkbox)
        else:
            self.checkbox = None

        self.setLayout(self.layout)

    def value(self):
        return self.textbox.value()

    def onValueChanged(self, text: str) -> None:
        self.textbox.blockSignals(True)
        self.textbox.setValue(text)
        self.textbox.blockSignals(False)

        if self.checkbox:
            if self.checkbox.isChecked == Qt.Checked:
                self.valueChanged.emit(text)
        else:
            self.valueChanged.emit(text)

    def checkboxChanged(self) -> None:
        self.onValueChanged(self.slider.value())