from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel

from controller.recipe_controller import RecipeController
from view.recipe_detail_view import RecipeDetailView


class RecipeForm(QWidget):
    def __init__(self, main_window, parent_widget, recipe):
        super().__init__()
        self.setWindowTitle("Edytuj przepis" if recipe else "Nowy Przepis")
        self.main_window = main_window
        self.parent_widget = parent_widget
        self.editing = recipe is not None
        self.original_recipe = recipe

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("Tytuł"))
        layout.addWidget(self.title_input)

        self.ingredients_input = QTextEdit()
        layout.addWidget(QLabel("Składniki"))
        layout.addWidget(self.ingredients_input)

        self.instructions_input = QTextEdit()
        layout.addWidget(QLabel("Instrukcje"))
        layout.addWidget(self.instructions_input)

        self.tags_input = QLineEdit()
        layout.addWidget(QLabel("Tagi"))
        layout.addWidget(self.tags_input)

        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.save_recipe)
        layout.addWidget(save_button)

        self.setLayout(layout)

        if recipe:
            self.populate_fields(recipe)

    def populate_fields(self, recipe):
        self.title_input.setText(recipe["name"])
        self.ingredients_input.setPlainText("\n".join(recipe["ingredients"]))
        self.tags_input.setText(",".join(recipe["tags"]))
        instructions = recipe["instructions"]
        if isinstance(instructions, list):
            instructions = "\n".join(instructions)
        self.instructions_input.setPlainText(instructions)

    def save_recipe(self):
        name = self.title_input.text()
        ingredients = self.ingredients_input.toPlainText().split('\n')
        instructions = self.instructions_input.toPlainText()
        tags = [tag.strip() for tag in self.tags_input.text().split(',')]

        if self.editing:
            RecipeController.instance().update_recipe(
                self.original_recipe, name, ingredients, instructions, tags
            )
            if type(self.parent_widget) is RecipeDetailView:
                self.parent_widget.update_recipe(name, ingredients, instructions, tags)
        else:
            RecipeController.instance().add_recipe(name, ingredients, instructions, tags)

        self.close_view()

    def close_view(self):
        self.main_window.stack.setCurrentWidget(self.parent_widget)
        self.main_window.stack.currentWidget().refresh_view()
        self.close()