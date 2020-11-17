from PySide2.QtWidgets import QApplication
from unittest import TestCase
from qtwidgets import data_dir, QImageViewer
import os
import sys
import cv2

class TestQImageViewer(TestCase):

    def test_with_sample_image(self):
        file = os.path.join(data_dir, "maxresdefault.jpg")
        im = cv2.imread(file)

        app = QApplication(sys.argv)

        viewer = QImageViewer()
        viewer.setImage(im)

        viewer.show()
        sys.exit(app.exec_())