from qtwidgets import QCustomSlider
from qtwidgets.sliders import BackwardsRangeException
from PyQt5.QtWidgets import QApplication
from unittest import TestCase
import os
import sys

class TestCustomSlider(TestCase):

    def test_slider(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(title='hello', spinbox=True)
        w.show()

        sys.exit(app.exec_())

    def test_odd_slider(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(title='hello', spinbox=True, odd=True)
        w.show()

        sys.exit(app.exec_())

    def test_odd_slider_with_different_range(self):
        app = QApplication(sys.argv)
        w = QCustomSlider(title='hello', spinbox=True, odd=True, min_=15, max_=19)
        w.show()

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
