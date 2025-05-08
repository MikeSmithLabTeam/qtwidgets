import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtCore import pyqtSlot
import cv2
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from qtwidgets.draggable_list import MyListWidget



class MainWindow(QMainWindow):
    """This file is a test for simple widgets
    
    Window should open displaying image.

    Test the following:
    Check method_list is printed to the terminal and contains all items displayed in gui
    Drag and drop item to new position
    Right click on item to remove
    Try to remove --inactive--, you shouldn't be able to.
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        my_list = MyListWidget(['item1','item2'], title='Draggable List Widget', dynamic=True)
        
        self.setCentralWidget(my_list)
        my_list.add_item('test',update=True)
        print(my_list.get_new_method_list())
        
        



if __name__ == '__main__':

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
