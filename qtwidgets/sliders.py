from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel, QSpinBox, QCheckBox
from PyQt5.QtCore import Qt
from .spinbox import QOddSpinBox

class QCustomSlider(QWidget):

    def __init__(self, parent=None, title='', min_=1, max_=99, value_=None, spinbox=False, checkbox=False, odd=False, label=False, return_func=None):
        QWidget.__init__(self, parent)

        if min_ > max_:
            raise BackwardsRangeException(min_, max_)

        if value_ is None:
            value_ = min_

        self.return_func = return_func


        self.odd = odd

        self.layout = QHBoxLayout()

        self.label = QLabel(title)
        self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_, max_)
        self.slider.setValue(value_)
        self.layout.addWidget(self.slider)

        if spinbox:
            if odd:
                self.spinbox = QOddSpinBox(self)
            else:
                self.spinbox = QSpinBox(self)

            self.spinbox.setRange(min_, max_)
            self.spinbox.setValue(self.slider.value())
            self.layout.addWidget(self.spinbox)
        else:
            self.spinbox = None

        if label:
            self.value_label = QLabel(str(self.slider.value()))
            self.layout.addWidget(self.value_label)
        else:
            self.value_label = None

        if checkbox:
            self.checkbox = QCheckBox()
            self.layout.addWidget(self.checkbox)
        else:
            self.checkbox = None

        if self.spinbox is not None:
            self.spinbox.valueChanged.connect(self.valueChanged)
        self.slider.valueChanged.connect(self.valueChanged)

        self.setLayout(self.layout)

    def valueChanged(self, val):
        if self.odd:
            if even(val):
                val -= 1
        self.slider.setValue(val)
        if self.spinbox is not None:
            self.spinbox.setValue(val)
        if self.value_label is not None:
            self.value_label.setText(str(val))

        if self.return_func is not None:
            if self.checkbox is None:
                self.return_func(val)
            else:
                if self.checkbox.isChecked():
                    self.return_func(val)

    def value(self):
        return self.slider.value()

    def spinboxChanged(self, val):
        self.slider.setValue(val)
        self.spinbox.setValue(val)


class BackwardsRangeException(BaseException):
    def __init__(self, min_, max_):
        self.message = f"min_ value {min_} is greater than max_ value {max_}"
        super().__init__(self.message)


def odd(a):
    return a%2 == 1

def even(a):
    return a%2 == 0