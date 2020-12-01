from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel,  QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal
from .spinbox import QSteppedSpinBox


class QCustomSlider(QWidget):

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None, title='', min_=1, max_=99, step_=1, value_=None, spinbox=False, checkbox=False, label=False):
        QWidget.__init__(self, parent)

        if value_ is None:
            value_ = min_

        self.layout = QHBoxLayout()

        self.title_label = QLabel(title, self)
        self.layout.addWidget(self.title_label)

        self.slider = QSteppedSlider(Qt.Horizontal, self)
        self.slider.setRange(min_, max_)
        self.slider.setSingleStep(step_)
        self.slider.setValue(value_)
        self.slider.onValueChanged.connect(self.onValueChanged)
        self.layout.addWidget(self.slider)

        if spinbox:
            self.spinbox = QSteppedSpinBox(self)
            self.spinbox.setRange(min_, max_)
            self.spinbox.setSingleStep(step_)
            self.spinbox.setValue(value_)
            self.spinbox.onValueChanged.connect(self.onValueChanged)
            self.layout.addWidget(self.spinbox)
        else:
            self.spinbox = None

        if label:
            self.value_label = QLabel(str(value_), self)
            self.layout.addWidget(self.value_label)
        else:
            self.value_label = None

        if checkbox:
            self.checkbox = QCheckBox(self)
            self.checkbox.stateChanged.connect(self.checkboxChanged)
            self.layout.addWidget(self.checkbox)
        else:
            self.checkbox = None

        self.setLayout(self.layout)

    def value(self):
        return self.slider.value()

    def onValueChanged(self, i):
        self.slider.blockSignals(True)
        self.slider.setValue(i)
        self.slider.blockSignals(False)
        if self.spinbox:
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(i)
            self.spinbox.blockSignals(False)
        if self.value_label:
            self.value_label.setText(str(i))
        if self.checkbox:
            if self.checkbox.isChecked == Qt.Checked:
                self.valueChanged.emit(i)
        else:
            self.valueChanged.emit(i)

    def checkboxChanged(self):
        self.onValueChanged(self.slider.value())


class QSteppedSlider(QSlider):

    onValueChanged = pyqtSignal(int)

    def __init__(self, orient=Qt.Horizontal, parent=None):
        QSlider.__init__(self, orient, parent)
        self.valueChanged.connect(self.sliderValueChanged)
        self._min = 0
        self._max = 99
        self._step = 1

    def setValue(self, v):
        index = round((v - self._min) / self._step)
        return super(QSlider, self).setValue(index)

    def sliderValueChanged(self, i):
        self.onValueChanged.emit(i*self._step + self._min)

    def setRange(self, min_, max_):
        self._min = min_
        self._max = max_
        self.rangeAdjusted()

    def setSingleStep(self, step):
        self._step = step
        self.rangeAdjusted()

    def rangeAdjusted(self):
        N = (self._max - self._min) // self._step
        self.setMaximum(N)


class BackwardsRangeException(BaseException):
    def __init__(self, min_, max_):
        self.message = f"min_ value {min_} is greater than max_ value {max_}"
        super().__init__(self.message)