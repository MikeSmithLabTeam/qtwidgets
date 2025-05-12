from PyQt6.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel, QCheckBox, QToolButton, QInputDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from .spinbox import QSteppedSpinBox, QSteppedSpinBoxDecimal


class QCustomSlider(QWidget):
    """This slider has a slider, spinbox, checkbox and label. It can be used to adjust values in a GUI.
    You can set the limits, step size, initial value and whether the spinbox, checkbox and label are displayed.
    It emits a signal when the value is changed."""
    valueChanged = pyqtSignal(int)
    rangeChanged = pyqtSignal(tuple)

    def __init__(self,
                 parent: QWidget = None,
                 title: str = '',
                 value_: int = 100,
                 min_: int = 1,
                 max_: int = 99,
                 step_: int = 1,
                 spinbox: bool = True,
                 checkbox: bool = True,
                 settings: bool = True,
                 label: bool = True):
        QWidget.__init__(self, parent)

        self.title = title

        self.layout = QHBoxLayout()
        self.title_label = QLabel(title, self)
        self.layout.addWidget(self.title_label)
        self.add_slider(min_, max_, step_, value_, settings=settings)
        self.add_spinbox(min_, max_, step_, value_, show=spinbox)
        self.add_label(value_, show=label)
        self.add_checkbox(show=checkbox)
        self.changeSettings(min_, max_, step_, value_)
        self.setLayout(self.layout)

    def add_slider(self, min_, max_, step_, value_, settings=True):
        if settings:
            self.settings_button = QToolButton(self)
            self.settings_button.clicked.connect(lambda x=None: self.changeSettings())
            self.settings_button.setText('⚙')
            self.layout.addWidget(self.settings_button)

        self.slider = QSteppedSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(min_, max_, step_)
        self.slider.setValue(value_)
        self.slider.sliderReleased.connect(lambda slider_val=self.slider.value: self.onValueChanged(slider_val))
        self.layout.addWidget(self.slider)

    def add_spinbox(self, min_, max_, step_, value_, show=True):
        if show:
            self.spinbox = QSteppedSpinBox(self)
            self.spinbox.editingFinished.connect(lambda spinbox_val=self.spinbox.value: self.onValueChanged(spinbox_val))
            self.layout.addWidget(self.spinbox)
        else:
            self.spinbox=None

    def add_label(self, value_, show=True):
        if show:
            self.value_label = QLabel(str(value_), self)
            self.layout.addWidget(self.value_label)
        else:
            self.value_label = None

    def add_checkbox(self, show=True):
        if show:
            self.checkbox = QCheckBox(self)
            self.checkbox.stateChanged.connect(self.checkboxChanged)
            self.layout.addWidget(self.checkbox)
            self.checkbox.setEnabled(True)
            self.checkbox.setChecked(True)
        else:
            self.checkbox = None

    def _changeDialogs(self, min_, max_, step_):
        if min_ is None:
            min_, ok = QInputDialog.getInt(self, 'Enter new min:', 'min: ', self.slider._min)
        if max_ is None:
            max_, ok = QInputDialog.getInt(self, 'Enter new max:', 'max: ',self.slider._max)
        if step_ is None:
            step_, ok = QInputDialog.getInt(self, 'Enter new step:', 'step: ',self.slider._step)
        return (min_, max_, step_)

    def changeSettings(self, min_=None, max_=None, step_=None, value_=None):
        min_, max_, step_ = self._changeDialogs(min_, max_, step_)
        old_value = self.value()
        self.slider.setRange(min_, max_, step_)
        
        if value_ is None:
            value = self.value()
        else:
            value = value_

        if value > max_:
            value = max_
        elif value < min_:
            value = min_

        self.slider.setValue(value)

        if self.spinbox:
            self.spinbox.setRange(min_, max_)
            self.spinbox.setSingleStep(step_)
            self.spinbox.setValue(value)

        if self.value_label:
            self.value_label.setText(str(value))

        self.rangeChanged.emit((min_,max_,step_))
        if value < old_value:
            self.valueChanged.emit(value)

    def value(self):
        return self.slider.value()

    def onValueChanged(self, get_value) -> None:
        i=get_value()
        self.slider.blockSignals(True)
        self.slider.setValue(i)
        self.slider.blockSignals(False)
        
        if self.spinbox:
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(i)
            self.spinbox.blockSignals(False)
        if self.value_label:
            self.value_label.setText(str(i))
        
        self.valueChanged.emit(int(i))

    def checkboxChanged(self) -> None:
        checkstate = self.checkbox.isChecked()
        if checkstate:
            self.slider.setEnabled(True)
            self.spinbox.setEnabled(True)
            self.onValueChanged(self.slider.value)
        else:
            self.slider.setEnabled(False)
            self.spinbox.setEnabled(False)

class QSteppedSlider(QSlider):
    onValueChanged = pyqtSignal(int)

    def __init__(self,
                 orient: Qt.Orientation = Qt.Orientation.Horizontal,
                 parent: QWidget = None):
        QSlider.__init__(self, orient, parent)
        self.valueChanged.connect(self.sliderValueChanged)
        self._min = 0
        self._max = 99
        self._step = 1

    def setValue(self, v: int) -> None:
        index = round((v - self._min) / self._step)
        return super(QSlider, self).setValue(index)

    def sliderValueChanged(self, i: int) -> None:
        self.onValueChanged.emit(i * self._step + self._min)

    def value(self) -> int:
        return super().value()*self._step + self._min

    def setRange(self, min_: int, max_: int, step_: int) -> None:
        self._min = min_
        self._max = max_
        self._step = step_
        self.rangeAdjusted()

    def rangeAdjusted(self):
        N = int((self._max - self._min) // self._step)
        self.setMaximum(N)

class QCustomSliderDecimal(QWidget):
    """
    QCustomSliderDecimal creates a slider, spinbox, checkbox label combo that can handle
    floating point numbers.

    inputs
    ------
    parent  :   parent widget.
    title   :   title for widget
    min_    :   initial minimum value
    max_    :   initial maximum value
    step_   :   step for slider
    value_  :   initial value
    spinbox :   boolean value that determines whether spinbox is added
    checkbox :   boolean value that determines whether checkbox is added
    label   :    boolean value that determines whether label is added
    settings :  boolean value that determines whether settings button is displayed
    decimals:   numerical integer >=0 which determines how many decimal places to use.

    """

    valueChanged = pyqtSignal(float)
    rangeChanged =  pyqtSignal(tuple)

    def __init__(self,
                 parent: QWidget = None,
                 title: str = '',
                 min_: float = 1.0,
                 max_: float = 99.0,
                 step_: float = 0.1,
                 value_: float = None,
                 spinbox: bool = False,
                 checkbox: bool = False,
                 label: bool = False,
                 settings: bool = True,
                 decimals=None):


        self.title = title
        self.decimals = decimals

        if decimals is None:
            self.num_figs = self.detect_decimals(step_)
        else:
            self.num_figs=decimals

        QWidget.__init__(self, parent)

        if value_ is None:
            value_ = min_

        self.layout = QHBoxLayout()
        self.title_label = QLabel(title, self)
        self.layout.addWidget(self.title_label)
        self.add_slider(min_, max_, step_, value_, settings=settings)
        self.add_spinbox(min_, max_, step_, value_, show=spinbox)
        self.add_label(value_, show=label)
        self.add_checkbox(show=checkbox)
        self.changeSettings(min_, max_, step_, value_, decimals)
        self.setLayout(self.layout)

    def detect_decimals(self, step_):
        #auto calculate number of decimal places based on value
        _=str(round(step_, 5))
        if '.' in _:
            return len(_[_.index('.'):])-1
        else:
            return 0

    def add_slider(self, min_, max_, step_, value_, settings=None):
        if settings:
            self.settings_button = QToolButton(self)
            self.settings_button.clicked.connect(lambda x=None: self.changeSettings())
            self.settings_button.setText('⚙')
            self.layout.addWidget(self.settings_button)

        self.slider = QSteppedSliderDecimal(Qt.Orientation.Horizontal, self)
        self.slider.setRange(min_, max_, step_)
        self.slider.setValue(value_)
        self.slider.sliderReleased.connect(lambda slider_val=self.slider.value: self.onValueChanged(slider_val))
        self.layout.addWidget(self.slider)

    def add_spinbox(self, min_, max_, step_, value_, show=True):
        if show:
            self.spinbox = QSteppedSpinBoxDecimal(self, value_=value_, decimals=self.num_figs, range=(min_, max_, step_))
            self.spinbox.editingFinished.connect(lambda spinbox_val=self.spinbox.value: self.onValueChanged(spinbox_val))
            self.layout.addWidget(self.spinbox)
        else:
            self.spinbox=None

    def add_label(self, value_, show=True):
        if show:
            self.value_label = QLabel(str(value_), self)
            self.update_label(value_)
            self.layout.addWidget(self.value_label)
        else:
            self.value_label = None

    def update_label(self, value_):
        value_ = str(round(value_,self.num_figs))
        if '.' in value_:
            missing_zeros = self.num_figs + 1 - len(value_[value_.index('.'):])
        else:
            missing_zeros = self.num_figs
            if self.num_figs > 0:
                value_ = value_ + '.'
        value_ = value_ + '0'*missing_zeros
        self.value_label.setText(value_)

    def add_checkbox(self, show=True):
        if show:
            self.checkbox = QCheckBox(self)
            self.checkbox.stateChanged.connect(self.checkboxChanged)
            self.layout.addWidget(self.checkbox)
            self.checkbox.setEnabled(True)
            self.checkbox.setChecked(True)
        else:
            self.checkbox = None

    def _changeDialogs(self, min_, max_, step_, decimals):
        if self.decimals is None:
            display_decimals = 3
        else:
            display_decimals = self.decimals
        if min_ is None:
            min_, ok = QInputDialog.getDouble(self, 'Enter new min:', 'min: ', self.slider._min, decimals=display_decimals)
        if max_ is None:
            max_, ok = QInputDialog.getDouble(self, 'Enter new max:', 'max: ',self.slider._max, decimals=display_decimals)
        if step_ is None:
            step_, ok = QInputDialog.getDouble(self, 'Enter new step:', 'step: ',self.slider._step, decimals=display_decimals)
        return (min_, max_, step_)

    def changeSettings(self, min_=None, max_=None, step_=None, value_=None, decimals=None):
        min_, max_, step_ = self._changeDialogs(min_, max_, step_, decimals)
        if decimals is None:
            self.num_figs=self.detect_decimals(step_)
        else:
            self.num_figs = decimals

        if value_ is None:
            value = self.value()
        else:
            value = value_
        self.slider.setRange(min_, max_, step_)

        if value > max_:
            value = max_
        elif value < min_:
            value = min_

        value = round(value, self.num_figs)
        self.slider.setValue(value)

        if self.spinbox:
            self.spinbox.setDecimals(self.num_figs)
            self.spinbox.setRange(min_, max_)
            self.spinbox.setSingleStep(step_)
            self.spinbox.setValue(value)

        if self.value_label:
            self.update_label(value)

        self.rangeChanged.emit((min_,max_,step_))

    def value(self):
        return self.slider.value()

    def onValueChanged(self, get_value) -> None:
        i=get_value()
        self.slider.blockSignals(True)
        self.slider.setValue(i)
        self.slider.blockSignals(False)
        if self.spinbox:
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(i)
            self.spinbox.blockSignals(False)
        if self.value_label:
            self.update_label(i)
        if self.checkbox:
            if self.checkbox.isChecked() == Qt.CheckState.Checked:
                self.valueChanged.emit(i)
        else:
            self.valueChanged.emit(i)

    def checkboxChanged(self) -> None:
        checkstate = self.checkbox.isChecked()
        if checkstate:
            self.slider.setEnabled(True)
            self.spinbox.setEnabled(True)
            self.onValueChanged(self.slider.value)
        else:
            self.slider.setEnabled(False)
            self.spinbox.setEnabled(False)


class QSteppedSliderDecimal(QSlider):
    onValueChanged = pyqtSignal(float)

    def __init__(self,
                 orient: Qt.Orientation = Qt.Orientation.Horizontal,
                 parent: QWidget = None):
        QSlider.__init__(self, orient, parent)
        self.valueChanged.connect(self.sliderValueChanged)
        self._min = 0.0
        self._max = 99.0
        self._step = 1.0

    def setValue(self, v: float) -> None:
        index = round((v - self._min) / self._step)
        return super(QSlider, self).setValue(index)

    def sliderValueChanged(self, i: float) -> None:
        self.onValueChanged.emit(i * self._step + self._min)

    def value(self) -> float:
        return super(QSteppedSliderDecimal, self).value()*self._step + self._min

    def setRange(self, min_: int, max_: int, step_: int) -> None:
        self._min = min_
        self._max = max_
        self._step = step_
        self.rangeAdjusted()

    def rangeAdjusted(self):
        N = int((self._max - self._min) // self._step)
        self.setMaximum(N)

