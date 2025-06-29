from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class MyListWidget(QListWidget):   
    """
    This widget implements the draggable list to control
    which methods are run and in which order.

    method_list : list of strings of desired methods in list. In particletracker method_list should be `list(param_dict[title][title + '_method'])`
    dynamic :  boolean to determine if elements are draggable or not.

    """
    listChanged = pyqtSignal(tuple)

    def __init__(self, method_list: list[str], title: str = '',dynamic: bool = True, dynamic_label='----Inactive----',*args, **kwargs):
        self.dynamic=dynamic
        self.meta='mylistwidget'
        self.widget='draggable_list'
        self.title=title
        self.method_list = method_list
        if self.dynamic:
            self.method_list.append(dynamic_label)
        super(MyListWidget, self).__init__(*args, **kwargs)
        self.item_index = 0

        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setMovement(QListView.Movement.Snap)
        font=QFont()
        font.setPointSize(12)
        self.setFont(font)
        if self.dynamic:
            self.setDragEnabled(True)
            self.setDropIndicatorShown(True)
            self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
            self.setDefaultDropAction(Qt.DropAction.MoveAction)
            self.setAcceptDrops(True)
        else:
            self.setDragEnabled(False)
        
        # Add the items to the list
        self.add_draggable_list_methods()
   
    def get_new_method_list(self):
        #Query the MyListWidget for the current list of methods
        new_method_list = []
        for index in range(self.count()):
            method = self.item(index).text()
            new_method_list.append(method)
        self.method_list=new_method_list
        return new_method_list

    def add_item(self, key, update=False):
        #If static list replace the list with new item else if dynamic add the method to end of list
        if not self.dynamic:
            self.clear()
        self.addItem(key)
        if update:
            self.get_new_method_list()      

    def add_draggable_list_methods(self):
        #update the list with the new methods
        self.clear()
        for item in self.method_list:
            self.add_item(item)  
        self.get_new_method_list()    
        
    def mousePressEvent(self, event):
        pos = self.mapFromGlobal(QCursor.pos())
        row = self.indexAt(pos).row()
        #If right click on item remove it from list
        if event.button() == Qt.MouseButton.RightButton:
            items = self.findItems('----Inactive----', Qt.MatchFlag.MatchExactly)
            if self.dynamic:
                if row != self.row(items[0]):
                    self.takeItem(row)
                    self.send_signal()
        #else register mouse button clicked
        else:
            super().mousePressEvent(event)

    def dropEvent(self, event):
        '''
        The logic in this method is complicated by the behaviour of
        drag and drop in PyQT5. Whilst the visible list updates correctly
        returning the list of methods ends up with 2 entries for the
        selected method at the former and new locations. 
        We compare the list before and after implementing the drop event
        and correct it to remove the duplicate. Finally we return
        just the active events via the signal.
        '''
        widget = self.currentItem()
        active_method = widget.text()
        old_method_list = self.get_new_method_list()
        old_item_index = old_method_list.index(active_method)
        super().dropEvent(event)
        widget = self.currentItem()
        new_method_list = self.get_new_method_list()
        new_item_indices = [i for i in range(len(new_method_list)) if new_method_list[i] == active_method]

        # Behaviour of drop event has changed in a recent update so that it doesn't create the copy
        # Only remove the copy if its actually there
        if len(new_method_list) > len(old_method_list):
            if old_item_index in new_item_indices:
                #Move method down in list
                new_method_list.pop(old_item_index)
            else:
                #Move method up in list
                new_method_list.pop(old_item_index+1)
        self.method_list = new_method_list
        #update the list
        
        self.add_draggable_list_methods()
        self.send_signal()

    def send_signal(self):
        #Emit the signal with the active methods
        self.get_new_method_list()
        if self.dynamic:
            active_method_list = self.method_list[:self.method_list.index('----Inactive----')]
        else:
            active_method_list = self.method_list     
        self.listChanged.emit(tuple(active_method_list))
        

