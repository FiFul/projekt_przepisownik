from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication

from utils.style_manager import update_stylesheets


class HomepageView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Strona Główna")

        layout = QVBoxLayout()
        self.refresh_view()

    def refresh_view(self):
        update_stylesheets("home_section")