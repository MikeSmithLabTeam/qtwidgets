from qtwidgets import QCustomSlider, QSteppedSlider
from PyQt5.QtWidgets import QApplication
from unittest import TestCase
import os
import sys

class TestSlider2(TestCase):

    def test(self):
        qpp = QApplication(sys.argv)
        w = QSteppedSlider()
        w.setRange(5, 55)
        w.setSingleStep(10)
        w.setValue(25)
        w.onValueChanged.connect(print)
        w.show()
        qpp.exec_()

class TestCustomSlider(TestCase):

    def test_slider(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(title='hello', label=True, min_=4, max_=20, step_=4)
        w.valueChanged.connect(print)
        w.show()

        sys.exit(app.exec_())

    def test_slider_step_size(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(title='hello', spinbox=True, step_=2)
        w.show()

        sys.exit(app.exec_())

    def test_odd_slider(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(title='hello', spinbox=True, odd=True)
        w.show()

        sys.exit(app.exec_())

    def test_odd_slider_with_different_range(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(title='hello', spinbox=True, min_=15, max_=31, step_=3)
        w.valueChanged.connect(print)
        w.show()
        app.exec_()

    def test_odd_slider_with_label(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(spinbox=True, label=True, odd=True)
        w.show()
        sys.exit(app.exec_())

    def test_odd_slider_with_checkbox(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(label=True, checkbox=True)
        w.show()
        sys.exit(app.exec_())

    def test_return_func(self):
        app = QApplication(sys.argv)
        def printprint(val):
            print(val, val)
        w = QCustomSlider(return_func=printprint, checkbox=True)
        w.show()
        sys.exit(app.exec_())
