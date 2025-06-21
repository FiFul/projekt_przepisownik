from PyQt5.QtWidgets import QWidget, QVBoxLayout


class HomepageView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Strona Główna")

        layout = QVBoxLayout()

    def refresh_view(self):
        pass