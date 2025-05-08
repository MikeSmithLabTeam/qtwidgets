"""This is a boilerplate code snippet for a PyQt6 application.
You can use it to try out compound but simple widgets"""


import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtCore import pyqtSlot

# Add parent directory to Python path
# Add the root project directory to Python path (two levels up from test file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)


from qtwidgets.sliders import QCustomSlider, QSteppedSlider, QSteppedSliderDecimal, QCustomSliderDecimal
from qtwidgets.spinbox import QSteppedSpinBoxDecimal
from qtwidgets.textbox import QCustomTextBox


class MainWindow(QMainWindow):
    """This file is a test for simple widgets
    
    Uncomment the appropriate widget and run the code to check it is working

    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #Widgets
        #integer slider
        self.slider = QCustomSlider(min_=0, max_=99, step_=1, spinbox=True, checkbox=True, label='test', settings=True)
        self.setCentralWidget(self.slider)
        self.slider.valueChanged.connect(self.change_int)

        #Decimal slider
        #self.float_slider = QCustomSliderDecimal(min_=2, #max_=10, step_=0.1,value_=5,label=True, spinbox=False)
        #self.setCentralWidget(self.float_slider)
        #self.float_slider.valueChanged.connect(self.change_float) 
        
        #Test spinbox        
        #self.spinbox = QSteppedSpinBoxDecimal(value_=5, #decimals=2,range=(0.01, 6.0, 0.01))
        #self.setCentralWidget(self.spinbox)
        #self.spinbox.valueChanged.connect(self.change_float)

        #Test textbox
        #self.textbox = QCustomTextBox(title='test', #value_='test', checkbox = True)
        #self.setCentralWidget(self.textbox)
        #self.textbox.returnPressed.connect(self.change_str)
        
    @pyqtSlot(float)
    def change_float(self, value):
        print(value)
    
    @pyqtSlot(int)
    def change_int(self, value):
        print(value)

    @pyqtSlot(str)
    def change_str(self, value):
        print(value)



if __name__ == '__main__':

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
