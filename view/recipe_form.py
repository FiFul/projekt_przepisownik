from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel

class RecipeForm(QWidget):
    def __init__(self, recipe_controller, recipe=None):
        super().__init__()
        self.setWindowTitle("Edytuj przepis" if recipe else "Nowy Przepis")

        self.recipe_controller = recipe_controller
        self.editing = recipe is not None
        self.original_recipe = recipe  # zapamiętaj oryginał

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("Tytuł"))
        layout.addWidget(self.title_input)

        self.ingredients_input = QTextEdit()
        layout.addWidget(QLabel("Składniki"))
        layout.addWidget(self.ingredients_input)

        self.tags_input = QLineEdit()
        layout.addWidget(QLabel("Tagi"))
        layout.addWidget(self.tags_input)

        self.instructions_input = QTextEdit()
        layout.addWidget(QLabel("Instrukcje"))
        layout.addWidget(self.instructions_input)

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
        tags = [tag.strip() for tag in self.tags_input.text().split(',')]
        instructions = self.instructions_input.toPlainText()

        if self.editing:
            self.recipe_controller.update_recipe(
                self.original_recipe, name, ingredients, tags, instructions
            )
        else:
            self.recipe_controller.add_recipe(name, ingredients, tags, instructions)

        self.close()
