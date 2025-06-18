from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from view.calendar_dialog import CalendarDialog
from view.recipe_form import RecipeForm


class RecipeDetailView(QWidget):
    def __init__(self, main_window, parent_widget, recipe, recipe_controller, calendar_controller):
        super().__init__()
        self.setWindowTitle("Szczegóły Przepisu")
        self.main_window = main_window
        self.parent_widget = parent_widget
        self.recipe = recipe
        self.recipe_controller = recipe_controller
        self.calendar_controller = calendar_controller

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
        self.recipe_controller.clear_cook_history(self.recipe['name'])
        self.recipe_controller.delete_recipe(self.recipe)
        self.close_view()

    def edit_recipe(self):
        self.main_window.show_edit_recipe(self, self.recipe)
        #self.form = RecipeForm(self.recipe_controller, recipe=self.recipe)
        #self.form.show()
        #self.close()

    def open_calendar(self):
        self.main_window.show_calendar_dialog(self, self.recipe)
        #dialog = CalendarDialog(self, self.calendar_controller, self.recipe['name'])
        #dialog.exec_()

    def close_view(self):
        self.main_window.stack.setCurrentWidget(self.parent_widget)
        self.main_window.stack.currentWidget().refresh_view()
        self.close()

    def refresh_view(self):
        self.title_label.setText(f"Tytuł: {self.recipe['name']}")
        self.ingredients_label.setText(f"Składniki: {', '.join(self.recipe['ingredients'])}")
        self.instructions_label.setText(f"Instrukcje: {self.recipe['instructions']}")
        self.tags_label.setText(f"Tagi: {', '.join(self.recipe['tags'])}")