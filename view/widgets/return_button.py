from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QGraphicsOpacityEffect


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
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(1.0)

    def enterEvent(self, event):
        self.effect.setOpacity(0.5)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.effect.setOpacity(1.0)
        super().leaveEvent(event)