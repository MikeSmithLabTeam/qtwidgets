from PyQt6.QtWidgets import QSpinBox, QWidget, QDoubleSpinBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QValidator



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
    onValueChanged = pyqtSignal(float)

    def __init__(self,parent: QWidget | None = None, value_: float | None =None, decimals: int = 0, range: tuple[float, float, float] | None = None):
        QDoubleSpinBox.__init__(self, parent)
        self.valueChanged.connect(self.spinboxValueChanged)
        self.setKeyboardTracking(False)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.UpDownArrows)
        max_ = range[1]
        min_ =  range[0]
        step_ = range[2]
        self.blockSignals(True)
        self.setSingleStep(step_)  
        self.setRange(min_, max_)
        self.setValue(value_)
        self.blockSignals(False)
        self.setDecimals(decimals)

    def spinboxValueChanged(self, i: float) -> None:
        self.onValueChanged.emit(i)
        