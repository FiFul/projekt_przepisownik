import os

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame


class RecipeTile(QFrame):
    clicked = pyqtSignal(dict)

    def __init__(self, recipe):
        super().__init__()
        layout = QVBoxLayout()
        self.recipe = recipe
        self.setLayout(layout)
        self.setFixedSize(200, 200)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(100)  # lub dopasuj dynamicznie

        image_path = recipe["image_path"]
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Brak zdjęcia")

        layout.addWidget(image_label)

        name_label = QLabel(recipe['name'])
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.recipe)