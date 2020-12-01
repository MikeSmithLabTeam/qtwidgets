from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import pyqtSignal


class QSteppedSpinBox(QSpinBox):
    onValueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        QSpinBox.__init__(self, parent)
        self.valueChanged.connect(self.sliderValueChanged)
        self.setKeyboardTracking(False)

    def sliderValueChanged(self, i):
        if (i - self.minimum()) % self.singleStep() == 0:
            self.onValueChanged.emit(i)
        else:
            v = (i - self.minimum()) // self.singleStep()
            v *= self.singleStep()
            v += self.minimum()
            self.setValue(v)
