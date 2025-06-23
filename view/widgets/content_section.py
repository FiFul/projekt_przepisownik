from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout


class ContentSection(QVBoxLayout):
    def __init__(self, header, body, spacing=10):
        super().__init__()
        self.header = header
        self.body = body
        self.setSpacing(spacing)
        self.setAlignment(Qt.AlignTop)

        self.addWidget(self.header)
        self.addWidget(self.body)

