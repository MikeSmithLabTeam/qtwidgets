"""This is a boilerplate code snippet for a PyQt5 application.
You can use it to try out a widget etc."""


import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtCore import pyqtSlot

from qtwidgets.sliders import QCustomSliderDecimal
from qtwidgets.spinbox import QSteppedSpinBoxDecimal
from qtwidgets.textbox import QCustomTextBox


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #self.slider = QCustomSliderDecimal(min_=2, max_=10, step_=0.1,value_=5,label=True, spinbox=False)
        self.spinbox = QSteppedSpinBoxDecimal(value_=5, decimals=2,range=(0.01, 6.0, 0.01))
        #self.textbox = QCustomTextBox(title='test', value_='test', checkbox = True)
        #self.setCentralWidget(self.slider)
        #self.slider.valueChanged.connect(self.change)
        self.setCentralWidget(self.spinbox)
        self.spinbox.valueChanged.connect(self.change)
        #self.setCentralWidget(self.textbox)
        #self.textbox.returnPressed.connect(self.change_str)
        
    @pyqtSlot(float)
    def change(self, value):
        print(value)
    
    @pyqtSlot(str)
    def change_str(self, value):
        print(value)



if __name__ == '__main__':

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
