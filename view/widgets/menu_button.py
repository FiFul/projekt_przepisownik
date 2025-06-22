from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize

class MenuButton(QPushButton):
    def __init__(self, icon_name, tool_tip):
        super().__init__()

        self.setIcon(QIcon(f"assets/icons/{icon_name}.png"))
        self.setToolTip(tool_tip)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(QSize(size, size))
        self.setIconSize(QSize(size, size))
        super().resizeEvent(event)
