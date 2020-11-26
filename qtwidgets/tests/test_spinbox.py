from unittest import TestCase
from PyQt5.QtWidgets import QApplication
from qtwidgets import QSteppedSpinBox
import sys



class TestSteppedSpinbox(TestCase):

    def test(self):
        qpp = QApplication(sys.argv)
        w = QSteppedSpinBox(None)
        w.setRange(5, 99)
        w.setSingleStep(5)
        w.newValueChanged.connect(print)
        w.show()
        qpp.exec_()