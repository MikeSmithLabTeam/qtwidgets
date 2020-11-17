from PySide2.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel, QSpinBox, QCheckBox
from PySide2.QtCore import Qt
from .spinbox import QOddSpinBox

class QCustomSlider(QWidget):

    def __init__(self, parent=None, title='', min_=1, max_=99, spinbox=False, checkbox=False, odd=False):
        QWidget.__init__(self, parent)

        if min_ > max_:
            raise BackwardsRangeException(min_, max_)


        self.odd = odd

        self.layout = QHBoxLayout()

        self.label = QLabel(title)
        self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_, max_)
        self.layout.addWidget(self.slider)

        if spinbox:
            if odd:
                self.spinbox = QOddSpinBox(self)
            else:
                self.spinbox = QSpinBox(self)
            self.spinbox.valueChanged.connect(self.spinboxChanged)
            self.spinbox.setRange(min_, max_)
            self.layout.addWidget(self.spinbox)
        else:
            self.spinbox = None

        if checkbox:
            self.checkbox = QCheckBox()
            self.layout.addWidget(self.checkbox)

        self.slider.valueChanged.connect(self.sliderChanged)

        self.setLayout(self.layout)

    def sliderChanged(self, val):
        if self.odd:
            if even(val):
                val -= 1
        self.slider.setValue(val)
        if self.spinbox is not None:
            self.spinbox.setValue(val)

    def spinboxChanged(self, val):
        self.slider.setValue(val)
        self.spinbox.setValue(val)

    def spinboxTextChanged(self, val):
        print(val)


class BackwardsRangeException(BaseException):
    def __init__(self, min_, max_):
        self.message = f"min_ value {min_} is greater than max_ value {max_}"
        super().__init__(self.message)


def odd(a):
    return a%2 == 1

def even(a):
    return a%2 == 0