from PyQt5.QtWidgets import QSpinBox, QWidget, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal


class QSteppedSpinBox(QSpinBox):
    """
    Child of QSpinBox that limits the selectable values by changing the
    range and singleStep of the spinbox.

    The signal that requires a slot is 'onValueChanged'.

    The 'valueChanged' signal will return the wrong values.
    """
    onValueChanged = pyqtSignal(int)

    def __init__(self,
                 parent: QWidget = None
                 ):
        QSpinBox.__init__(self, parent)
        self.valueChanged.connect(self.sliderValueChanged)
        self.setKeyboardTracking(False)

    def sliderValueChanged(self, i: int) -> None:
        if (i - self.minimum()) % self.singleStep() == 0:
            self.onValueChanged.emit(i)
        else:
            v = (i - self.minimum()) // self.singleStep()
            v *= self.singleStep()
            v += self.minimum()
            self.setValue(v)

class QSteppedSpinBoxDecimal(QDoubleSpinBox):
    """
    Child of QSpinBox that limits the selectable values by changing the
    range and singleStep of the spinbox.

    The signal that requires a slot is 'onValueChanged'.

    The 'valueChanged' signal will return the wrong values.
    """
    onValueChanged = pyqtSignal(int)

    def __init__(self,
                 parent: QWidget = None,
                 ):
        QSpinBox.__init__(self, parent)
        self.valueChanged.connect(self.sliderValueChanged)
        self.setKeyboardTracking(False)

    def sliderValueChanged(self, i: float) -> None:
        if (i - self.minimum()) % self.singleStep() == 0:
            self.onValueChanged.emit(i)
        else:
            v = (i - self.minimum()) // self.singleStep()
            v *= self.singleStep()
            v += self.minimum()
            self.setValue(v)