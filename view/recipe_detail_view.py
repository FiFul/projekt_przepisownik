from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from view.calendar_dialog import CalendarDialog


class RecipeDetailView(QWidget):
    def __init__(self, recipe, recipe_controller, calendar_controller):
        super().__init__()
        self.setWindowTitle("Szczegóły Przepisu")

        self.recipe = recipe
        self.recipe_controller = recipe_controller
        self.calendar_controller = calendar_controller

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Tytuł: {recipe['name']}"))
        layout.addWidget(QLabel(f"Składniki: {recipe['ingredients']}"))
        layout.addWidget(QLabel(f"Instrukcje: {recipe['instructions']}"))
        layout.addWidget(QLabel(f"Tagi: {recipe['tags']}"))


        edit_button = QPushButton("Edytuj")
        edit_button.clicked.connect(self.edit_recipe)
        layout.addWidget(edit_button)

        delete_button = QPushButton("Usuń")
        delete_button.clicked.connect(self.delete_recipe)
        layout.addWidget(delete_button)

        calendar_button = QPushButton("Wybierz dzień gotowania")
        calendar_button.clicked.connect(self.open_calendar)
        layout.addWidget(calendar_button)

        self.setLayout(layout)

    def delete_recipe(self):
        self.recipe_controller.delete_recipe(self.recipe)
        self.close()

    def edit_recipe(self):
        from view.recipe_form import RecipeForm
        self.recipe_controller.delete_recipe(self.recipe)
        self.form.show()
        self.close()

    def open_calendar(self):
        dialog = CalendarDialog(self, self.calendar_controller, self.recipe['name'])
        dialog.exec_()