from qtwidgets import QCustomSlider
from qtwidgets.sliders import BackwardsRangeException
from PySide2.QtWidgets import QApplication
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

