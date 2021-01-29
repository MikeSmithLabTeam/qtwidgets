from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel, QCheckBox, QToolButton, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from .spinbox import QSteppedSpinBox


class QCustomSlider(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self,
                 parent: QWidget = None,
                 title: str = '',
                 min_: int = 1,
                 max_: int = 99,
                 step_: int = 1,
                 value_: int = None,
                 update: str = 'onValueChanged',
                 spinbox: bool = False,
                 checkbox: bool = False,
                 label: bool = False):
        QWidget.__init__(self, parent)

        self.title = title

        if value_ is None:
            value_ = min_

        self.layout = QHBoxLayout()

        self.title_label = QLabel(title, self)
        self.layout.addWidget(self.title_label)

        self.settings_button = QToolButton(self)
        self.settings_button.clicked.connect(lambda x=None: self.changeSettings())
        self.settings_button.setText('⚙')
        self.layout.addWidget(self.settings_button)

        self.slider = QSteppedSlider(Qt.Horizontal, self)
        self.slider.setRange(min_, max_)
        self.slider.setSingleStep(step_)
        self.slider.setValue(value_)
        if update == 'onValueChanged':
            self.slider.onValueChanged.connect(lambda slider_val=self.slider.value: self.onValueChanged(slider_val))
        elif update == 'sliderReleased':
            self.slider.sliderReleased.connect(lambda slider_val=self.slider.value: self.onValueChanged(slider_val))
        self.layout.addWidget(self.slider)

        if spinbox:
            self.spinbox = QSteppedSpinBox(self)
            self.spinbox.setRange(min_, max_)
            self.spinbox.setSingleStep(step_)
            self.spinbox.setValue(value_)
            self.spinbox.editingFinished.connect(lambda spinbox_val=self.spinbox.value: self.onValueChanged(spinbox_val))
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

    def changeSettings(self, min_=None, max_=None, step_=None):
        if min_ is None:
            min_, ok = QInputDialog.getInt(self, 'Enter new min:', 'min: ', self.slider._min)
        if max_ is None:
            max_, ok = QInputDialog.getInt(self, 'Enter new max:', 'max: ',self.slider._max)
        if step_ is None:
            step_, ok = QInputDialog.getInt(self, 'Enter new step:', 'step: ',self.slider._step)
        self.slider.setRange(min_, max_)
        self.slider.setSingleStep(step_)

        if self.slider.value > max_:
            self.slider.setValue(max_)
        elif self.slider.value < min_:
            self.slider.setValue(min_)

        if self.spinbox:
            self.spinbox.setRange(min_, max_)
            self.spinbox.setSingleStep(step_)
            self.spinbox.setValue(min_)

    def value(self):
        return self.slider.value()

    def onValueChanged(self, get_value) -> None:
        i=get_value()
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

    def checkboxChanged(self) -> None:
        self.onValueChanged(self.slider.value())


class QSteppedSlider(QSlider):
    onValueChanged = pyqtSignal(int)

    def __init__(self,
                 orient: Qt.Orientation = Qt.Horizontal,
                 parent: QWidget = None):
        QSlider.__init__(self, orient, parent)
        self.valueChanged.connect(self.sliderValueChanged)
        self._min = 0
        self._max = 99
        self._step = 1

    def setValue(self, v: int) -> None:
        index = round((v - self._min) / self._step)
        return super(QSlider, self).setValue(index)

    def sliderValueChanged(self, i: int) -> None:
        self.onValueChanged.emit(i * self._step + self._min)

    def value(self) -> int:
        return super(QSteppedSlider, self).value()*self._step + self._min

    def setRange(self, min_: int, max_: int) -> None:
        self._min = min_
        self._max = max_
        self.rangeAdjusted()

    def setSingleStep(self, step: int) -> None:
        self._step = step
        self.rangeAdjusted()

    def rangeAdjusted(self):
        N = (self._max - self._min) // self._step
        self.setMaximum(N)