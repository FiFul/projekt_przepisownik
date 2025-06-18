from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from view.recipe_list_view import RecipeListView
from view.calendar_list_view import CalendarListView
from view.stats_view import StatsView

class MainWindow(QMainWindow):
    def __init__(self, recipe_controller, calendar_controller):
        super().__init__()
        self.setWindowTitle("Przepisownik")

        self.recipe_controller = recipe_controller
        self.calendar_controller = calendar_controller

        layout = QVBoxLayout()

        self.open_recipe_list_button = QPushButton("Przepisy")
        self.open_recipe_list_button.clicked.connect(self.open_recipe_list)
        layout.addWidget(self.open_recipe_list_button)

        calendar_button = QPushButton("Kalendarz gotowania")
        calendar_button.clicked.connect(self.open_calendar_list)
        layout.addWidget(calendar_button)

        self.stats_button = QPushButton("Statystyki")
        self.stats_button.clicked.connect(self.open_stats)
        layout.addWidget(self.stats_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_recipe_list(self):
        self.recipe_list_view = RecipeListView(self.recipe_controller, self.calendar_controller)
        self.recipe_list_view.show()

    def open_calendar_list(self):
        self.calendar_list_view = CalendarListView(self.recipe_controller, self.calendar_controller)
        self.calendar_list_view.show()

    def open_stats(self):
        self.stats_view = StatsView(self.recipe_controller, self.calendar_controller)
        self.stats_view.show()