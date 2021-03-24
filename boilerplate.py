import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from qtwidgets.sliders import QCustomSliderDecimal
from qtwidgets.spinbox import QSteppedSpinBoxDecimal


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.slider = QCustomSliderDecimal(min_=2, max_=10, step_=0.1,value_=5,label=True, spinbox=False)
        self.setCentralWidget(self.slider)
        #self.slider.valueChanged.connect(self.change)
        
    #@pyqtSlot(float)
    #def change(self, value):
    #    print(value)



if __name__ == '__main__':

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()