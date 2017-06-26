import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Box(QGraphicsRectItem):

    def __init__(self, position, rect=QRectF(0, 0, 100, 50), parent=None):
        super().__init__(rect, parent)

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setPos(position)

        self.resizer = Resizer(parent=self)
        resizerWidth = self.resizer.rect.width() / 2
        resizerOffset = QPointF(resizerWidth, resizerWidth)
        self.resizer.setPos(self.rect().bottomRight() - resizerOffset)
        self.resizer.resizeSignal.connect(self.resize)

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.black)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        painter.drawRect(self.rect())

    @pyqtSlot(QPointF)
    def resize(self, change):
        self.setRect(self.rect().adjusted(0, 0, change.x(), change.y()))
        self.prepareGeometryChange()
        self.update()


class Resizer(QGraphicsObject):

    resizeSignal = pyqtSignal(QPointF)

    def __init__(self, rect=QRectF(0, 0, 10, 10), parent=None):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.rect = rect

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            pen = QPen()
            pen.setStyle(Qt.DotLine)
            painter.setPen(pen)
        painter.drawEllipse(self.rect)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if self.isSelected():
                self.resizeSignal.emit(value - self.pos())
        return value


if __name__ == "__main__":

    app = QApplication(sys.argv)

    view = QGraphicsView()
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 500, 1000)
    view.setScene(scene)

    box = Box(QPointF(50, 50))

    view.show()

    sys.exit(app.exec_())
