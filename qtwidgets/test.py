from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import sys

from area_selector import SelectAreaWidget
from images import QImageViewer




class MainWindow(QMainWindow):
    def __init__(self, img):
        super().__init__()
        self.main_panel = QWidget()
        self.viewer = QImageViewer()
        self.viewer.setImage(img)
        layout=QVBoxLayout()
        layout.addWidget(self.viewer)
        self.main_panel.setLayout(layout)
        self.setCentralWidget(self.main_panel)   
        selector = SelectAreaWidget(shape='polygon', viewer=self.viewer, points=[(359, 184), (1432, 253), (1673, 1097), (608, 1199)])
        
        self.viewer.scene.addWidget(selector)








if __name__ == '__main__':
    img = cv2.imread('C:\\Users\\ppzmis\\OneDrive - The University of Nottingham\\Pictures\\Camera Roll\\test.jpg')

    app = QApplication(sys.argv)
    window = MainWindow(img)
        
    window.show()
    #Start event loop
    app.exec_()
    
