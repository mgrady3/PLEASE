"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: May, 2017

beamselection.py

This file provides a class representing the User selection region within
a LEED or LEEM image.

Adapted from https://stackoverflow.com/users/3477005/daniele-pantaleone
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class BeamSelection(QtWidgets.QGraphicsRectItem):
    """Provide moveable, resizeable, and selectable rect item for beam selection."""

    # Setup standard resizing markers for corner/sides of rect
    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = 8.0
    handleSpace = -4.0

    handleCursors = {
        handleTopLeft: QtCore.Qt.SizeFDiagCursor,
        handleTopMiddle: QtCore.Qt.SizeVerCursor,
        handleTopRight: QtCore.Qt.SizeBDiagCursor,
        handleMiddleLeft: QtCore.Qt.SizeHorCursor,
        handleMiddleRight: QtCore.Qt.SizeHorCursor,
        handleBottomLeft: QtCore.Qt.SizeBDiagCursor,
        handleBottomMiddle: QtCore.Qt.SizeVerCursor,
        handleBottomRight: QtCore.Qt.SizeFDiagCursor,
    }

    def __init__(self, *args, **kwargs):
        super(BeamSelection, self).__init__(*args, **kwargs)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """Test if mousepos is at one of the resize handles and returns the resize handle below the given point."""
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """Executed when the mouse moves over the shape (NOT PRESSED)."""
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = QtCore.Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """Executed when the mouse leaves the shape (NOT PRESSED)."""
        self.setCursor(QtCore.Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """Executed when the mouse is pressed on the item."""
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """Executed when the mouse is being moved over the item while being pressed."""
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """Executed when the mouse is released from the item."""
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """Return the bounding rect of the shape (including the resize handles)."""
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """Update current resize handles according to the shape size and position."""
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QtCore.QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QtCore.QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QtCore.QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QtCore.QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QtCore.QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QtCore.QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """Perform shape interactive resize."""
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QtCore.QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:
            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:
            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:
            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            # print("MR")
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:
            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:
            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """Return the shape of this item as a QPainterPath in local coordinates."""
        path = QtGui.QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """Paint the node in the graphic view."""
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 100)))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1.0, QtCore.Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 255)))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 255),
                                  1.0,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))

        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)

###
# Testing
###


def test():
    """Test resizeable QGraphicsItem."""
    import sys
    app = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QGraphicsView()
    scene = QtWidgets.QGraphicsScene()
    scene.setSceneRect(0, 0, 640, 480)

    rectF = QtCore.QRectF(0, 0, 300, 150)
    pen = QtGui.QPen(QtGui.QColor(200, 0, 0), 1.0, QtCore.Qt.SolidLine)
    rectI = BeamSelection(rectF, parent=None)
    scene.addItem(rectI)

    view.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
    view.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
