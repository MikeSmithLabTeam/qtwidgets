from .data import data_dir
from .images import QImageViewer
from .sliders import QCustomSlider

import PySide2
import os

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path