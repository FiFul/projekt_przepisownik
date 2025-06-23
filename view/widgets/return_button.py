from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

class ReturnButton(QPushButton):
    def __init__(self, close_view_connection):
        super().__init__()
        size = 50
        self.setIcon(QIcon(f"assets/icons/icon_arrow_back.png"))
        self.setIconSize(QSize(size, size))
        self.setToolTip("Powrót")
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(close_view_connection)
        self.setFixedSize(QSize(size, size))
        self.setStyleSheet("QPushButton {background: transparent;}")