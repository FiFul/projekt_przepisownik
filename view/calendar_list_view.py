from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
from datetime import date

from controller.calendar_controller import CalendarController
from controller.recipe_controller import RecipeController
from model.database import Database
from utils.style_manager import update_stylesheets


class CalendarListView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Kalendarz gotowania")

        self.layout = QVBoxLayout()
        self.recipe_list = QListWidget()
        self.layout.addWidget(self.recipe_list)

        self.recipe_list.itemClicked.connect(self.open_selected_recipe)
        self.setLayout(self.layout)

        self.display_recipes()

    def display_recipes(self):
        self.recipe_list.clear()
        recipes = RecipeController.instance().get_recipes()

        sortable_recipes = []
        for recipe in recipes:
            name = recipe.get("name", "Brak nazwy")
            history = CalendarController.instance().get_history(name)

            if history:
                days_ago = Database.instance().days_cooked(name)
            else:
                days_ago = float('inf')

            sortable_recipes.append((days_ago, name))

        sortable_recipes.sort(reverse=True)

        for days_ago, name in sortable_recipes:
            if days_ago == float('inf'):
                label = f"Nigdy nie gotowano \t{name}"
            else:
                label = f"{days_ago} dni temu \t{name}"

            self.recipe_list.addItem(label)

    def open_selected_recipe(self, item):
        text = item.text().split("\t")[1]
        recipe = RecipeController.instance().get_recipe_by_title(text)
        self.main_window.show_recipe_detail(self, recipe)

    def refresh_view(self):
        update_stylesheets("calendar_section")
        self.display_recipes()