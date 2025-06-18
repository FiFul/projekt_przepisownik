from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from datetime import date

class CalendarListView(QWidget):
    def __init__(self, recipe_controller, calendar_controller):
        super().__init__()
        self.setWindowTitle("Kalendarz gotowania")
        self.recipe_controller = recipe_controller
        self.calendar_controller = calendar_controller

        self.layout = QVBoxLayout()
        self.recipe_list = QListWidget()
        self.layout.addWidget(self.recipe_list)

        self.refresh_button = QPushButton("Odśwież")
        self.refresh_button.clicked.connect(self.display_recipes)
        self.layout.addWidget(self.refresh_button)

        self.recipe_list.itemDoubleClicked.connect(self.open_selected_recipe)
        self.setLayout(self.layout)

        self.display_recipes()

    def display_recipes(self):
        self.recipe_list.clear()
        recipes = self.recipe_controller.get_recipes()
        for recipe in recipes:
            name = recipe.get("name", "Brak nazwy")
            history = self.calendar_controller.get_history(name)

            if history:
                last_date = max(entry.cook_date for entry in history)
                days_ago = (date.today() - last_date).days
                label = f"{name} — ostatnio {days_ago} dni temu"
            else:
                label = f"{name} — nigdy nie gotowane"

            self.recipe_list.addItem(label)

    def open_selected_recipe(self, item):
        text = item.text().split(" — ")[0]  # Nazwa przepisu
        recipe = next((r for r in self.recipe_controller.get_recipes() if r["name"] == text), None)
        if recipe:
            from view.recipe_detail_view import RecipeDetailView
            self.detail_view = RecipeDetailView(recipe, self.recipe_controller, self.calendar_controller)
            self.detail_view.show()
        else:
            QMessageBox.warning(self, "Błąd", "Nie znaleziono przepisu.")
