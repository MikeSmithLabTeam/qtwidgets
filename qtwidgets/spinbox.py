from PySide2.QtWidgets import QSpinBox
from PySide2.QtGui import QKeyEvent
from PySide2.QtCore import Qt


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