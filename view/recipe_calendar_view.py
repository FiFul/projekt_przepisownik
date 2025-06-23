from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDateEdit, QPushButton, QTextEdit, QMessageBox, QWidget
from PyQt5.QtCore import QDate
from datetime import date

from controller.calendar_controller import CalendarController
from view.widgets.return_button import ReturnButton


class RecipeCalendarView(QWidget):
    def __init__(self, main_window, parent_widget, recipe_name):
        super().__init__(parent_widget)
        self.main_window = main_window
        self.parent_widget = parent_widget
        self.recipe_name = recipe_name
        self.setWindowTitle(f"Kalendarz gotowania - {self.recipe_name}")

        layout = QVBoxLayout()

        self.return_button = ReturnButton(self.close_view)
        layout.addWidget(self.return_button)

        title_label = QLabel(f"Kalendarz gotowania przepisu:\n{recipe_name}")
        title_label.setStyleSheet("QLabel { background: transparent; font-family: 'Verdana'; font-weight: bold; font-size: 32px;}")
        layout.addWidget(title_label)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        save_button = QPushButton("Zapisz gotowanie")
        save_button.clicked.connect(self.save_cook_date)
        layout.addWidget(save_button)

        clear_button = QPushButton("Wyczyść historię gotowania")
        clear_button.clicked.connect(self.clear_cook_history)
        layout.addWidget(clear_button)

        layout.addWidget(QLabel("Historia gotowania:"))
        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)
        layout.addWidget(self.history_box)

        self.setLayout(layout)
        self.update_history()

    def save_cook_date(self):
        qdate = self.date_edit.date()
        cook_date = date(qdate.year(), qdate.month(), qdate.day())
        CalendarController.instance().log_cook(self.recipe_name, cook_date)
        self.update_history()

    def clear_cook_history(self):
        confirm = QMessageBox.question(
            self,
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć całą historię gotowania dla przepisu „{self.recipe_name}”?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            CalendarController.instance().clear_history(self.recipe_name)
            self.update_history()

    def update_history(self):
        history = CalendarController.instance().get_history(self.recipe_name)
        self.history_box.clear()
        if history:
            for entry in history:
                self.history_box.append(f"{entry.cook_date}")
        else:
            self.history_box.setText("Brak historii gotowania.")

    def close_view(self):
        self.main_window.stack.setCurrentWidget(self.parent_widget)
        self.main_window.stack.currentWidget().refresh_view()
        self.close()