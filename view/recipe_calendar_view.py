from PyQt5.QtGui import QTextCharFormat, QFont, QColor
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDateEdit, QPushButton, QTextEdit, QMessageBox, QWidget, QHBoxLayout
from PyQt5.QtCore import QDate, Qt
from datetime import date

from controller.calendar_controller import CalendarController
from view.widgets.calendar_popup import CalendarPopup
from view.widgets.content_section import ContentSection
from view.widgets.return_button import ReturnButton
from view.widgets.sidebar_button import SidebarButton


class RecipeCalendarView(QWidget):
    def __init__(self, main_window, parent_widget, recipe_name):
        super().__init__(parent_widget)
        self.main_window = main_window
        self.parent_widget = parent_widget
        self.recipe_name = recipe_name
        self.setWindowTitle(f"Kalendarz gotowania - {self.recipe_name}")

        layout = QVBoxLayout()
        layout.setSpacing(50)

        self.return_button = ReturnButton(self.close_view)
        layout.addWidget(self.return_button)

        title_label = QLabel(f"Kalendarz gotowania przepisu:\n{recipe_name}")
        title_label.setStyleSheet("QLabel { background: transparent; font-family: 'Verdana'; font-weight: bold; font-size: 32px;}")
        layout.addWidget(title_label)

        button_layout = QHBoxLayout()

        add_record_button = SidebarButton("Dodaj gotowanie do historii")
        add_record_button.clicked.connect(self.add_record)
        button_layout.addWidget(add_record_button)

        clear_button = SidebarButton("Wyczyść historię gotowania")
        clear_button.clicked.connect(self.clear_cook_history)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)
        self.history_label = QLabel("Historia gotowania")
        self.history_label.setStyleSheet("QLabel { background: transparent; font-family: 'Verdana'; font-weight: bold; font-size: 32px;}")
        self.history_box = QTextEdit()
        self.history_box.setFixedWidth(300)
        self.history_box.setFixedHeight(500)
        self.history_box.setStyleSheet("QTextEdit {font-family: 'Verdana'; font-size: 20px;}")
        self.history_box.setReadOnly(True)

        layout.addLayout(ContentSection(self.history_label, self.history_box))
        layout.addStretch()
        self.setLayout(layout)
        self.update_history()

    def add_record(self):
        dialog = CalendarPopup(self)
        if dialog.exec_():
            qdate = dialog.selected_date
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