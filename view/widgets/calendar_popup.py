from PyQt5.QtWidgets import QDialog, QCalendarWidget, QVBoxLayout


class CalendarPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wybierz datę")

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.return_date)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        self.setLayout(layout)

    def return_date(self, date):
        self.selected_date = date
        self.accept()