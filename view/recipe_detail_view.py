from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from controller.recipe_controller import RecipeController


class RecipeDetailView(QWidget):
    def __init__(self, main_window, parent_widget, recipe):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Szczegóły Przepisu")
        self.parent_widget = parent_widget
        self.recipe = recipe

        layout = QVBoxLayout()

        return_button = QPushButton("Powrót")
        return_button.clicked.connect(self.close_view)
        layout.addWidget(return_button)

        self.title_label = QLabel(f"Tytuł: {recipe['name']}")
        self.ingredients_label = QLabel(f"Składniki: {', '.join(recipe['ingredients'])}")
        self.instructions_label = QLabel(f"Instrukcje: {recipe['instructions']}")
        self.tags_label = QLabel(f"Tagi: {', '.join(recipe['tags'])}")

        layout.addWidget(self.title_label)
        layout.addWidget(self.ingredients_label)
        layout.addWidget(self.instructions_label)
        layout.addWidget(self.tags_label)


        edit_button = QPushButton("Edytuj")
        edit_button.clicked.connect(self.edit_recipe)
        layout.addWidget(edit_button)

        delete_button = QPushButton("Usuń")
        delete_button.clicked.connect(self.delete_recipe)
        layout.addWidget(delete_button)

        calendar_button = QPushButton("Sprawdź w kalendarzu")
        calendar_button.clicked.connect(self.open_calendar)
        layout.addWidget(calendar_button)

        self.setLayout(layout)

    def delete_recipe(self):
        RecipeController.instance().clear_cook_history(self.recipe['name'])
        RecipeController.instance().delete_recipe(self.recipe)
        self.close_view()

    def edit_recipe(self):
        self.main_window.show_edit_recipe(self, self.recipe)

    def open_calendar(self):
        self.main_window.show_calendar_dialog(self, self.recipe)

    def close_view(self):
        self.main_window.stack.setCurrentWidget(self.parent_widget)
        self.main_window.stack.currentWidget().refresh_view()
        self.close()

    def refresh_view(self):
        self.title_label.setText(f"Tytuł: {self.recipe['name']}")
        self.ingredients_label.setText(f"Składniki: {', '.join(self.recipe['ingredients'])}")
        self.instructions_label.setText(f"Instrukcje: {self.recipe['instructions']}")
        self.tags_label.setText(f"Tagi: {', '.join(self.recipe['tags'])}")

    def update_recipe(self, name, ingredients, instructions, tags):
        self.recipe['name'] = name
        self.recipe['ingredients'] = ingredients
        self.recipe['instructions'] = instructions
        self.recipe['tags'] = tags