from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt


class SidebarButton(QPushButton):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
        self.setToolTip(text)
        self.setCursor(Qt.PointingHandCursor)
