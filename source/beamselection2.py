"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: May, 2017

beamselection2.py

This file provides a class representing the User selection region within
a LEED or LEEM image.

Adapted from https://stackoverflow.com/users/2593236/pbreach
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class ResizeableRect(QtWidgets.QGraphicsRectItem):
    """Provide moveable, resizeable, and selectable rect item for beam selection."""

    def __init__(self, position, rect=QtCore.QRectF(0, 0, 100, 50), parent=None):
        """Init base graphics item, setup geometry, set resizing handle."""
        super(QtWidgets.QGraphicsItem, self).__init__(rect, parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setPos(position)

        self.resizer = Resizer(parent=self)
        resizerWidth = self.resizer.rect.width() / 2
        resizerOffset = QtCore.QPointF(resizerWidth, resizerWidth)
        self.resizer.setPos(self.rect().bottomRight() - resizerOffset)
        self.resizer.resizeSignal.connect(self.resize)

        def paint(self, painter, option, widget=None):
            """Draw to screen."""
            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.black)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.transparent)
            painter.drawRect(self.rect())

        @QtCore.pyqtSlot(QtCore.QPointF)
        def resize(self, change):
            self.setRect(self.rect().adjusted(0, 0, change.x(), change.y()))
            self.prepareGeometryChange()
            self.update()


class Resizer(QtWidgets.QGraphicsItem):
    """Handle resizing of arbitrary QGraphicsItems."""

    resizeSignal = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, rect=QtCore.QRectF(0, 0, 10, 10), parent=None):
        super(Resizer, self).__init__(parent)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.rect = rect

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            pen = QtGui.QPen()
            pen.setStyle(QtCore.Qt.DotLine)
            painter.setPen(pen)
        painter.drawEllipse(self.rect)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            if self.isSelected():
                self.resizeSignal.emit(value - self.pos())
        return value

###
# Testing
###


def test():
    import sys
    app = QtWidgets.QApplication(sys.argv)

    view = QtWidgets.QGraphicsView()
    scene = QtWidgets.QGraphicsScene()
    scene.setSceneRect(0, 0, 500, 1000)
    view.setScene(scene)

    box = ResizeableRect(QtCore.QPointF(50, 50))
    scene.addItem(box)

    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
