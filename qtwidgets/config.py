from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
import PyQt6.QtCore as QtCore
from PyQt6.QtCore import pyqtSlot
from qtwidgets import QImageViewer, QCustomSlider, SelectAreaWidget

import sys


__all__ = [
    "ConfigGui",
    "SelectShapeGui",
    "get_monitor_size"
]


def get_monitor_size():
    """Get details about the monitor size"""
    app = QApplication([])
    screen = app.primaryScreen()
    screen_resolution = screen.geometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    return width, height


class ConfigGui:
    
    def __init__(self, img, func, param_dict=None) -> None:
        """ConfigGui

        Takes an image and applies a image processing function to it.
        It then displays that image processed via the arguments in param_dict.
        Each param is assigned a slider which can be used to adjust the params.
        This is called by most functions if you set config=True.
        Enter or quite closes the window.

        Parameters
        ----------
        img : np.ndarray
            an image to be processed. Can be updated via setter Instance.img0 = new_image
        func : a function for processing the images self._im0 = func(img)
        param_dict : dictionary with all the keyword args for func.
        """
        self.im=img
        self._im0 = img.copy()
        if param_dict is None:
            self.param_dict = None
        else:
            self.param_dict = {k:check_init_param_val(v) for k,v in param_dict.items()}
        self.func = func
        self.init_ui()
        self.window.show()
        self.app.exec()
    
    def init_ui(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.image_viewer = QImageViewer()
        self.image_viewer.setImage(self.im)
        self.image_viewer.keyPressed.connect(self.close_gui)
        layout = QVBoxLayout()
        layout.addWidget(self.image_viewer)
       
        if self.param_dict is not None:
            self.live_update_checkbox = QCheckBox('Live Update', parent=self.window)
            layout.addWidget(self.live_update_checkbox)
            self.add_sliders(layout)
            self.live_update_checkbox.stateChanged.connect(self._update_sliders)
            
        self.window.setLayout(layout)
        
    
    def add_sliders(self, layout):
        self.sliders = {}

        for key in sorted(self.param_dict.keys()):
            val, bottom, top, step = self.param_dict[key]
            slider = QCustomSlider(
                parent=self.window, value_=val, title=key, min_=bottom, max_=top,
                step_=step, spinbox=True)
            slider.valueChanged.connect(self._update_sliders)
            layout.addWidget(slider)
            self.sliders[key] = slider

    
    def _update_sliders(self, val):
        print('_update')
        if self.live_update_checkbox.isChecked():
            # Update reduced_dict with current values
            self.reduced_dict = {k: self.sliders[k].value() for k in self.param_dict.keys()}
            # Update the image
            result = self.func(self._im0, **self.reduced_dict)
            # Display the result
            self.image_viewer.setImage(result)

    def _update_img(self):
        """Update the image. Takes original image and applies the function
        to it. The dict comprehension takes the first value from the list of values
        with each key which corresponds to the value and passes new dictionary with key and 
        just this value to function."""

        if self.param_dict is None:
            self.im = self.func(self._im0)
        else:
            self.im = self.func(self._im0,**{k:v[0] for k,v in self.param_dict.items()})
        self.image_viewer.setImage(self.im)
    
    @property
    def img0(self):
        return self._im0
    
    @img0.setter
    def img0(self, img):
        """Update the initial image with setter method"""
        self._im0=img
        self._update_img()
    
    def close_gui(self, event):
        if (event.type() == QtCore.QEvent.Type.KeyPress):
            if event.key() == QtCore.Qt.Key.Key_Space:
                if self.param_dict is not None:
                    self.reduced_dict = {k:v[0] for k,v in self.param_dict.items()}
                    print(self.reduced_dict)
                self.window.close()


class SelectShapeGui:
    def __init__(self, img, shape='rect', handle_rad=5) -> None:
        """SelectShapeGui

        Takes an image and applies a image processing function to it.
        It then displays that image processed via the arguments in param_dict.
        Each param is assigned a slider which can be used to adjust the params.
        This is called by most functions if you set config=True.
        Enter or quit closes the window.

        Parameters
        ----------
        img : np.ndarray
            an image to be processed. Can be updated via setter Instance.img0 = new_image
        shape : 'rect', 'ellipse', 'circle' or 'polygon'
        handle_rad : int - This is the size of the handles that allow the user to drag the shape around
        """
        self.im=img
        self.shape=shape
        self.handle_rad=handle_rad
        self.init_ui()
    
    def init_ui(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.image_viewer = QImageViewer()
        self.image_viewer.setImage(self.im)
        self.image_viewer.keyPressed.connect(self.close_gui)
        self.vbox = QVBoxLayout()
        self.select_area=SelectAreaWidget(self.shape, self.image_viewer, handle_rad=self.handle_rad)
        self.image_viewer.scene.addWidget(self.select_area)
        self.vbox.addWidget(self.image_viewer)
        self.window.setLayout(self.vbox)
        self.window.show()
        
        self.app.exec_()
        
    
    def close_gui(self, event):
        if (event.type() == QtCore.QEvent.Type.KeyPress):
            self.pts=self.select_area.points
            if event.key() == QtCore.Qt.Key.Key_Space:
                self.window.close()



def check_init_param_val(param_list: list[int]):
    """Some OpenCV functions require certain parameters to be odd or even. This is a convenience function to check and adjust the parameters."""
    if param_list[3]%2==0:
        #If the increment value is 2 implies only odd values allowed
        if param_list[0]%2==0:
            #If initial value is even make it odd
            param_list[0] += 1
    return param_list
