import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from qtwidgets.sliders import QCustomSliderDecimal


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.slider = QCustomSliderDecimal(decimals=0, label=True, spinbox=True)
        self.setCentralWidget(self.slider)
        






if __name__ == '__main__':

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()