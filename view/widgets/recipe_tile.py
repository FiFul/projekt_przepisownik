from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame


class RecipeTile(QFrame):
    clicked = pyqtSignal(dict)

    def __init__(self, recipe):
        super().__init__()
        layout = QVBoxLayout()
        self.recipe = recipe
        self.setLayout(layout)
        self.setFixedSize(200, 200)
        name_label = QLabel(recipe['name'])
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.recipe)