import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtCore import pyqtSlot
import cv2
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from qtwidgets.images import QImageViewer
from qtwidgets.area_selector import SelectAreaWidget



class MainWindow(QMainWindow):
    """This file is a test for simple widgets
    
    Window should open displaying image.

    Test the following:
    Hold and drag right mouse button to zoom
    Hold and drag left mouse button to pan
    Double click right mouse button to restore to full image
    Click left mouse button prints coords to terminal
    Press key and ascii number printed to terminal

    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        image_path = os.path.join(os.path.dirname(__file__), 'maxresdefault.jpg')
        im = cv2.imread(image_path)
        
        def press_key(e):
            print(e.key())
        
        def print_coords(x,y):
            print(x,y)

        viewer = QImageViewer()
        viewer.setImage(im)
        viewer.keyPressed.connect(press_key)
        viewer.leftMouseButtonPressed.connect(print_coords)
        
        #Add the Widget to the QImageViewer. Enter
        area_selector = SelectAreaWidget(shape='rect', viewer=viewer, points=[(20,20),(200,200)], handle_rad=25)
        viewer.scene.addWidget(area_selector)
        
        self.setCentralWidget(viewer)
        self.resize(800,600)


if __name__ == '__main__':

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
