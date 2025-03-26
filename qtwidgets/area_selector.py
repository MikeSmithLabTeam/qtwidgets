from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import numpy as np


class SelectAreaWidget(QWidget):
    """This gui is a widget that allows the user to select an area on the image.
    
        shape: 'rect', 'ellipse', 'circle' or 'polygon'
        viewer: QImageViewer object
        points: list of tuples with the coordinates of the shape
        colour: QColor object
        handle_rad: int - This is the size of the handles that allow the user to drag the shape around

        The SelectAreaWidget connects to a signal from the viewer's keyPressEvent that can be used to close the window and return the points.
    """
    def __init__(self, shape=None, viewer=None, points=None, colour=QColor(250, 10, 10, 80), handle_rad=5):
        self.viewer = viewer
        self.viewer.keyPressed.connect(self.keyPressEvent)
        geometry = self.viewer.geometry
  
        self.shape=shape 
        self.handle_rad = handle_rad      
        self.points = points # Store coords        
        self.handles = [] # Contains the QEllipse used to drag shapes around
        self.adjustable = (points is not None)

        #self.display_point_list = []
        self.colour=colour
        super().__init__()
        self.setGeometry(geometry)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.transparent)
        self.setPalette(p)

        self.parse_points(points)
        if points is not None:
            self.draw_shape()
            self.update()

    def parse_points(self, points):
        self.qpoints=[]
        if points is not None: 
            for point in points:
                self.qpoints.append(QPoint(point[0],point[1]))

    def paintEvent(self, event):
        self.draw_shape()

    def draw_shape(self):
        if len(self.qpoints) > 0:
            self.handles = []
            if self.shape=='rect':
                self.rectangle(self.qpoints)
            elif self.shape == 'ellipse':
                self.ellipse(self.qpoints)
            elif self.shape == 'circle':
                self.circle(self.qpoints)       
            elif self.shape == 'polygon':
                self.polygon(self.qpoints)

    def rectangle(self, qpoints):
        qp = QPainter(self)
        br = QBrush(self.colour)
        qp.setBrush(br)
        qp.drawRect(QRect(qpoints[0], qpoints[1]))   
        handles = [QPoint(qpoints[0].x(),qpoints[0].y()),
                   QPoint(qpoints[1].x(),qpoints[1].y())]
        self.add_handles(qp, handles)
        self.qpoints = qpoints 
        self.points = [(qpoints[0].x(),qpoints[0].y()),(qpoints[1].x(),qpoints[1].y())]

    def ellipse(self, qpoints):
        qp = QPainter(self)
        br = QBrush(self.colour)
        qp.setBrush(br)
        qp.drawEllipse(QRect(qpoints[0], qpoints[1]))  
        handles = [QPoint(qpoints[0].x(),qpoints[0].y()),
                   QPoint(qpoints[1].x(),qpoints[1].y())]
        self.add_handles(qp, handles)
        self.qpoints=qpoints
        self.points = [(qpoints[0].x(),qpoints[0].y()),(qpoints[1].x(),qpoints[1].y())]
        
    def circle(self, qpoints):
        qp = QPainter(self)
        br = QBrush(self.colour)
        qp.setBrush(br)
        dx = qpoints[1].x() - qpoints[0].x()
        dy = qpoints[1].y() - qpoints[0].y()
        rad = ((dx)**2 + (dy)**2)**0.5
        qp.drawEllipse(qpoints[0], rad, rad)
        self.qpoints=qpoints
        handles = self.qpoints
        self.add_handles(qp, handles)
        self.points = [(qpoints[0].x(),qpoints[0].y()),(qpoints[1].x(),qpoints[1].y())]

    def polygon(self, qpoints):
        qp = QPainter(self)
        br = QBrush(self.colour)
        qp.setBrush(br)
        polygon = QPolygon(qpoints)
        qp.drawPolygon(polygon) 
        self.add_handles(qp, qpoints)  
        self.points=[]   
        for qpoint in qpoints:
            self.points.append((qpoint.x(),qpoint.y()))
        

    def add_handles(self, qp, handles, colour=QColor(Qt.GlobalColor.lightGray)):
        br2=QBrush(colour)
        qp.setBrush(br2)
        if len(handles)>0:
            for qpoint in handles:
                qp.drawEllipse(qpoint, self.handle_rad, self.handle_rad)
                self.handles.append(qpoint)

    def which_handle(self):
        val = None
        for index, handle in enumerate(self.qpoints):
            distance2 = ((handle.x() - self.end.x())**2 + (handle.y() - self.end.y())**2)
            if distance2 <= (self.handle_rad**2):#If they click within the handle
                val=index
        return val

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.adjustable = True
            print(self.points)
    
    def mousePressEvent(self, event):
        self.begin = event.position().toPoint()
        self.end = event.position().toPoint()
        
        if (self.shape == 'polygon') &  (self.adjustable == False):
            self.qpoints.append(self.begin)
        elif self.adjustable:
            #This enables updating the position of handle and shape
            self.handle_index = self.which_handle()  
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.position().toPoint()
        if self.adjustable: 
            if self.handle_index is not None:               
                self.points[self.handle_index] = (self.end.x(),self.end.y())
                self.qpoints[self.handle_index] = self.end
        else:
            if self.shape != 'polygon':
                self.points = [(self.begin.x(),self.begin.y()),(self.end.x(),self.end.y())]
                self.qpoints = [self.begin, self.end]
        self.update()
        
    def mouseReleaseEvent(self, event):
        if self.shape != 'polygon':
            self.adjustable = True
            
        

    
