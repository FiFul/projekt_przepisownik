from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QSizePolicy

from model.database import Database
from view.calendar_dialog import CalendarDialog
from view.calendar_list_view import CalendarListView
from view.homepage_view import HomepageView
from view.recipe_detail_view import RecipeDetailView
from view.recipe_form import RecipeForm
from view.recipe_list_view import RecipeListView
from view.stats_view import StatsView
from view.widgets.menu_button import MenuButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Przepisownik")

        # Główne widgety
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Lewy panel (menu)
        self.menu = QVBoxLayout()

        self.btn_home = MenuButton("icon_home", "Strona Główna")

        self.btn_recipes = MenuButton("icon_recipe_list", "Lista Przepisów")
        self.btn_calendar = MenuButton("icon_calendar_list", "Kalendarz")
        self.btn_stats = MenuButton("icon_statistics", "Statystyki")
        self.btn_exit = MenuButton("icon_close", "Zamknij")

        self.btn_home.clicked.connect(self.show_homepage)
        self.btn_recipes.clicked.connect(self.show_recipes)
        self.btn_calendar.clicked.connect(self.show_calendar)
        self.btn_stats.clicked.connect(self.show_stats)
        self.btn_exit.clicked.connect(self.close)

        for btn in [self.btn_home, self.btn_recipes, self.btn_calendar, self.btn_stats]:
            self.menu.addWidget(btn)
        self.menu.addStretch()
        self.menu.addWidget(self.btn_exit)

        # Prawy panel (dynamiczne widoki)
        self.stack = QStackedWidget()
        self.homepage_view = HomepageView(self)
        self.recipe_list_view = RecipeListView(self)
        self.calendar_list_view = CalendarListView(self)
        self.stats_view = StatsView()

        self.stack.addWidget(self.homepage_view)
        self.stack.addWidget(self.recipe_list_view)
        self.stack.addWidget(self.calendar_list_view)
        self.stack.addWidget(self.stats_view)

        # Połączenie layoutów
        menu_widget = QWidget()
        menu_widget.setLayout(self.menu)
        menu_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)

        self.show_homepage()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showNormal()

    def show_homepage(self):
        self.homepage_view.refresh_view()
        self.stack.setCurrentWidget(self.homepage_view)

    def show_recipes(self):
        self.recipe_list_view.refresh_view()
        self.stack.setCurrentWidget(self.recipe_list_view)

    def show_calendar(self):
        self.calendar_list_view.refresh_view()
        self.stack.setCurrentWidget(self.calendar_list_view)

    def show_stats(self):
        self.stats_view.refresh_view()
        self.stack.setCurrentWidget(self.stats_view)

    def show_recipe_detail(self, parent_view, recipe):
        detail_view = RecipeDetailView(self, parent_view, recipe)
        self.stack.addWidget(detail_view)
        self.stack.setCurrentWidget(detail_view)

    def show_edit_recipe(self, parent_widget, recipe):
        form = RecipeForm(self, parent_widget, recipe)
        self.stack.addWidget(form)
        self.stack.setCurrentWidget(form)

    def show_add_recipe(self, parent_widget):
        self.show_edit_recipe(parent_widget, None)

    def show_calendar_dialog(self, parent_widget, recipe):
        dialog = CalendarDialog(self, parent_widget, recipe["name"])
        self.stack.addWidget(dialog)
        self.stack.setCurrentWidget(dialog)
