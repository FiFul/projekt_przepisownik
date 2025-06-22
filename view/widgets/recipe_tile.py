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
        self.setFixedSize(250, 200)

        image_path = recipe["image_path"]
        if image_path and os.path.exists(image_path):
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setFixedHeight(int(0.75 * self.height()))
            image_label.setScaledContents(True)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            pixmap = QPixmap(image_path).scaled(self.width(), int(0.8 * self.height()), Qt.KeepAspectRatioByExpanding)
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)
        title_label = QLabel(recipe['name'])
        title_label.setWordWrap(True)
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.recipe)