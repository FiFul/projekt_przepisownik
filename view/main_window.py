from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget

from view.calendar_list_view import CalendarListView
from view.recipe_detail_view import RecipeDetailView
from view.recipe_form import RecipeForm
from view.recipe_list_view import RecipeListView
from view.stats_view import StatsView


class MainWindow(QMainWindow):
    def __init__(self, recipe_controller, calendar_controller):
        super().__init__()
        self.setWindowTitle("Przepisownik")

        self.recipe_controller = recipe_controller
        self.calendar_controller = calendar_controller

        # Główne widgety
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Lewy panel (menu)
        self.menu = QVBoxLayout()
        self.btn_recipes = QPushButton("Przepisy")
        self.btn_calendar = QPushButton("Kalendarz")
        self.btn_stats = QPushButton("Statystyki")
        self.btn_exit = QPushButton("Zamknij")

        self.btn_recipes.clicked.connect(self.show_recipes)
        self.btn_calendar.clicked.connect(self.show_calendar)
        self.btn_stats.clicked.connect(self.show_stats)
        self.btn_exit.clicked.connect(self.close)

        for btn in [self.btn_recipes, self.btn_calendar, self.btn_stats, self.btn_exit]:
            self.menu.addWidget(btn)
        self.menu.addStretch()

        # Prawy panel (dynamiczne widoki)
        self.stack = QStackedWidget()
        self.recipe_list_view = RecipeListView(recipe_controller, self.calendar_controller)
        self.calendar_list_view = CalendarListView(recipe_controller, calendar_controller)
        self.stats_view = StatsView(recipe_controller, calendar_controller)

        self.stack.addWidget(self.recipe_list_view)   # index 0
        self.stack.addWidget(self.calendar_list_view)      # index 1
        self.stack.addWidget(self.stats_view)         # index 2

        # Połączenie layoutów
        menu_widget = QWidget()
        menu_widget.setLayout(self.menu)
        menu_widget.setFixedWidth(160)

        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)

        self.show_recipes()

    def show_recipes(self):
        self.recipe_list_view.display_recipes(self.recipe_controller.db.recipes)
        self.stack.setCurrentWidget(self.recipe_list_view)

    def show_calendar(self):
        self.calendar_list_view.display_recipes()
        self.stack.setCurrentWidget(self.calendar_list_view)

    def show_stats(self):
        self.stats_view.update()
        self.stack.setCurrentWidget(self.stats_view)

    def show_recipe_detail(self, recipe):
        detail_view = RecipeDetailView(recipe, self.recipe_controller, self.calendar_controller, self.show_recipes, self.show_edit_recipe)
        self.stack.addWidget(detail_view)
        self.stack.setCurrentWidget(detail_view)

    def show_edit_recipe(self, recipe=None):
        form = RecipeForm(recipe, self.recipe_controller, self.show_recipes)
        self.stack.addWidget(form)
        self.stack.setCurrentWidget(form)

    def show_add_recipe(self):
        self.show_edit_recipe(None)

