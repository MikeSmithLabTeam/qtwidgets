from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

from sliders import QCustomSlider





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_panel = QWidget()
        slider = QCustomSlider()
        layout=QVBoxLayout()
        layout.addWidget(slider)
        self.main_panel.setLayout(layout)
        self.setCentralWidget(self.main_panel)











if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    #Start event loop
    app.exec_()

