import sys
from math import floor, sqrt
from random import shuffle

from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import QWidget, QApplication, QPixmap, QGridLayout, QLabel


class ClickableImage(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, image_path):
        super(ClickableImage, self).__init__()
        self.pixmap = QPixmap(image_path)
        self.setPixmap(self.pixmap)
        self.setObjectName(image_path)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())


class ChooseImageGame(QWidget):
    def __init__(self, parent=None):
        super(ChooseImageGame, self).__init__(parent)
        self.main_layout = QGridLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.generate_image_tile_widget(
            ["../resources/1.jpg", "../resources/2.jpg", "../resources/3.jpg", "../resources/4.jpg"])

    def generate_image_tile_widget(self, images_path_list):
        if images_path_list is not None:
            image_count = len(images_path_list)
            rows = int(floor(sqrt(image_count)))
            columns = int(image_count / rows)
            shuffle(images_path_list)
            for n_image, image_path in enumerate(images_path_list):
                row = n_image % rows
                column = int(n_image / rows)
                label = ClickableImage(image_path)
                label.clicked.connect(self.handleLabelClicked)
                self.main_layout.addWidget(label, row, column)

    def handleLabelClicked(self, name):
        print('"%s" clicked' % name)


def main():
    app = QApplication([])
    game = ChooseImageGame()
    game.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
