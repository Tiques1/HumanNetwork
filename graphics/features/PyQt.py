import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QGraphicsItem
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF


class RectangleItem(QGraphicsItem):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.setFlags(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return self.rect.adjusted(-2, -2, 2, 2)

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(self.rect)


class GraphicsEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Графический редактор')

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 800, 600)

        self.add_rectangle_button = QPushButton('Добавить прямоугольник', self)
        self.add_rectangle_button.clicked.connect(self.add_rectangle)
        self.add_rectangle_button.setGeometry(10, 10, 180, 30)

    def add_rectangle(self):
        rect = QRectF(0, 0, 100, 50)
        rectangle_item = RectangleItem(rect)
        self.scene.addItem(rectangle_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = GraphicsEditor()
    editor.show()
    sys.exit(app.exec_())
