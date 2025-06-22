from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()
