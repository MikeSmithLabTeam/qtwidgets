from PyQt5.QtWidgets import QSpinBox, QWidget
from PyQt5.QtCore import Qt, pyqtSignal


class QOddSpinBox(QSpinBox):
    """Spinbox that only accepts odd values"""

    def __init__(self, parent):
        QSpinBox.__init__(self, parent)
        self.setSingleStep(2)
        self.setKeyboardTracking(False)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return:
            txt = self.text()
            val = int(txt)
            if val % 2 == 1:
                self.setValue(val)
        else:
            QSpinBox.keyPressEvent(self, event)


# class QSteppedSpinBox(QWidget):
#
#     valueChanged = pyqtSignal(int)
#
#     def __init__(self, parent, min_, max_, step_):
#         QWidget.__init__(self, parent)
#         self.min_ = min_
#         self.max_ = max_
#         self.step_ = step_
#         self.spinbox = QSpinBox(self)
#         self.spinbox.setKeyboardTracking(False)
#         self.spinbox.valueChanged.connect(self.spinboxValueChanged)
#         N = self.getN()
#         self.spinbox.setRange(0, N)
#
#     def getN(self):
#         return (self.max_ - self.min_) // self.step_
#
#     def spinboxValueChanged(self, val):
#         val = self.step_ * val + self.min_
#         self.valueChanged.emit(val)


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
