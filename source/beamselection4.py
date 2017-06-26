"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: May, 2017

beamselection4.py

This file provides a class representing the User selection region within
a LEED or LEEM image.

Adapted from https://stackoverflow.com/users/979203/onlyjus
"""

import copy
from PyQt5 import QtCore, QtGui, QtWidgets


class ResizableRect(QtWidgets.QGraphicsRectItem):
    """Provide moveable, resizeable, and selectable rect item for beam selection."""

    def __init__(self, rect, parent=None, scene=None):
        super(QtWidgets.QGraphicsItem, self).__init__(rect, parent)
        self._rect = rect
        self._scene = scene
        if not self._scene:
            print("Warning: ResizableRect instantiated with no reference to QGraphicsScene!")
        self.mouseOver = False
        self.resizeHandlesize = 4.0  # corner box size
        self.mousePressPos = None
        self.mouseMovePos = None
        self.mouseIsPressed = False

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

        self.updateResizeHandles()

    def hoverEnterEvent(self, event):
        """Prepare to resize rect."""
        self.updateResizeHandles()
        self.mouseOver = True
        self.prepareGeometryChange()

    def hoverLeaveEvent(self, event):
        """Drop resize focus."""
        self.mouseOver = False
        self.prepareGeometryChange()

    def hoverMoveEvent(self, event):
        """Set mouse cursor for resize."""
        if self.topLeft.contains(event.scenePos()) or self.bottomRight.contains(event.scenePos()):
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif self.topRight.contains(event.scenePos()) or self.bottomLeft.contains(event.scenePos()):
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        else:
            self.setCursor(QtCore.Qt.SizeAllCursor)

        super(QtWidgets.QGraphicsRectItem, self).hoverMoveEvent(event)

    def mousePressEvent(self, event):
        """On mousePress, identify region of Rect that was pressed."""
        self.mousePressPos = event.scenePos()
        self.mouseIsPressed = True
        self.pressedRect = copy.deepcopy(self._rect)

        # Get active area

        # Top left corner
        if self.topLeft.contains(event.scenePos()):
            self.mousePressArea = 'topleft'
        # top right corner
        elif self.topRight.contains(event.scenePos()):
            self.mousePressArea = 'topright'
        #  bottom left corner
        elif self.bottomLeft.contains(event.scenePos()):
            self.mousePressArea = 'bottomleft'
        # bottom right corner
        elif self.bottomRight.contains(event.scenePos()):
            self.mousePressArea = 'bottomright'
        # entire rectangle
        else:
            self.mousePressArea = None

        super(QtWidgets.QGraphicsRectItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        self.mouseIsPressed = False
        self.updateResizeHandles()
        self.prepareGeometryChange()
        super(QtWidgets.QGraphicsRectItem, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse movement."""
        self.mouseMovePos = event.scenePos()
        if self.mouseIsPressed:
            # Move top left corner
            if self.mousePressArea == 'topleft':
                self._rect.setTopLeft(self.pressedRect.topLeft()-(self.mousePressPos-self.mouseMovePos))
            # Move top right corner
            elif self.mousePressArea == 'topright':
                self._rect.setTopRight(self.pressedRect.topRight()-(self.mousePressPos-self.mouseMovePos))
            # Move bottom left corner
            elif self.mousePressArea == 'bottomleft':
                self._rect.setBottomLeft(self.pressedRect.bottomLeft()-(self.mousePressPos-self.mouseMovePos))
            # Move bottom right corner
            elif self.mousePressArea == 'bottomright':
                self._rect.setBottomRight(self.pressedRect.bottomRight()-(self.mousePressPos-self.mouseMovePos))
            # Move entire rectangle, don't resize
            else:
                self._rect.moveCenter(self.pressedRect.center()-(self.mousePressPos-self.mouseMovePos))

            self.updateResizeHandles()
            self.prepareGeometryChange()
        super(QtWidgets.QGraphicsRectItem, self).mousePressEvent(event)

    def boundingRect(self):
        return self._boundingRect

    def updateResizeHandles(self):
        """Update bounding rect and the corner resize handles."""
        self.offset = self.resizeHandlesize * (self._scene.graphicsView.mapToScene(1, 0) -
                                               self._scene.graphicsView.mapToScene(0, 1)).x()
        self._boundingRect = self._rect.adjusted(-1*self.offset, self.offset, self.offset, -1*self.offset)
        # Note: this draws correctly on a view with an inverted y axes. i.e. QGraphicsView.scale(1,-1)
        self.topLeft = QtCore.QRectF(self._boundingRect.topLeft().x(),
                                     self._boundingRect.topLeft().y() - 2*self.offset,
                                     2*self.offset, 2*self.offset)
        self.topRight = QtCore.QRectF(self._boundingRect.topRight().x() - 2*self.offset,
                                      self._boundingRect.topRight().y() - 2*self.offset,
                                      2*self.offset, 2*self.offset)
        self.bottomLeft = QtCore.QRectF(self._boundingRect.bottomLeft().x(),
                                        self._boundingRect.bottomLeft().y(),
                                        2*self.offset, 2*self.offset)
        self.bottomRight = QtCore.QRectF(self._boundingRect.bottomRight().x() - 2*self.offset,
                                         self._boundingRect.bottomRight().y(),
                                         2*self.offset, 2*self.offset)

    def paint(self, painter, option, widget):
        """Override paint() to implement resizing."""
        # show boundingRect for debug purposes
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
        painter.drawRect(self._boundingRect)

        # Paint rectangle
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine))  # TODO: set to proper color
        painter.drawRect(self._rect)

        # When mouse is hovering -> draw dorner handles for resizing
        if self.mouseOver:
            if self.isSelected():
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
            painter.drawRect(self.topLeft)
            painter.drawRect(self.topRight)
            painter.drawRect(self.bottomLeft)
            painter.drawRect(self.bottomRight)


class graphicsScene(QtWidgets.QGraphicsScene):
    """Shim to provide access to scene/view."""

    def __init__(self, parent=None):
        super(QtWidgets.QGraphicsScene, self).__init__(parent)

    def setGraphicsView(self, view):
        self.graphicsView = view


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    scene = graphicsScene()
    scene.setSceneRect(0, 0, 640, 480)
    view = QtWidgets.QGraphicsView()
    view.setScene(scene)
    view.scale(1, -1)
    view.setRenderHint(QtGui.QPainter.Antialiasing)
    view.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
    view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    view.setUpdatesEnabled(True)
    view.setMouseTracking(True)
    # view.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
    view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    scene.setGraphicsView(view)

    box = ResizableRect(QtCore.QRectF(50, 50, 50, 50), parent=None, scene=scene)
    scene.addItem(box)

    mw.setCentralWidget(view)
    mw.show()
    sys.exit(app.exec_())
