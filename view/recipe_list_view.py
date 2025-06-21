from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QComboBox, QLabel, QHBoxLayout

from controller.recipe_controller import RecipeController

class RecipeListView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Lista Przepisów")

        layout = QVBoxLayout()

        self.add_button = QPushButton("Dodaj przepis")
        self.add_button.clicked.connect(self.add_recipe)
        layout.addWidget(self.add_button)

        self.tag_filter_label = QLabel("Filtruj po tagu:")
        layout.addWidget(self.tag_filter_label)

        self.tag_filter_box = QComboBox()
        layout.addWidget(self.tag_filter_box)

        self.ingredient_filter_label = QLabel("Filtruj po składniku:")
        layout.addWidget(self.ingredient_filter_label)

        self.ingredient_filter_box = QComboBox()
        layout.addWidget(self.ingredient_filter_box)

        button_layout = QHBoxLayout()

        self.filter_button = QPushButton("Filtruj")
        self.filter_button.clicked.connect(self.apply_filters)
        button_layout.addWidget(self.filter_button)

        self.clear_button = QPushButton("Wyczyść")
        self.clear_button.clicked.connect(self.clear_filters)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        self.recipe_list = QListWidget()
        self.recipe_list.itemDoubleClicked.connect(self.open_selected_recipe)
        layout.addWidget(self.recipe_list)

        self.setLayout(layout)

        self.update_filter_options()
        self.display_recipes(RecipeController.instance().get_recipes())

    def update_filter_options(self):
        self.tag_filter_box.clear()
        self.ingredient_filter_box.clear()

        tags = RecipeController.instance().get_all_tags()
        ingredients = RecipeController.instance().get_all_ingredients()

        self.tag_filter_box.addItem("")  # Opcja 'brak filtru'
        self.ingredient_filter_box.addItem("")

        self.tag_filter_box.addItems(sorted(tags))
        self.ingredient_filter_box.addItems(sorted(ingredients))

    def apply_filters(self):
        selected_tag = self.tag_filter_box.currentText()
        selected_ingredient = self.ingredient_filter_box.currentText()

        recipes = RecipeController.instance().get_recipes()

        if selected_tag:
            recipes = [r for r in recipes if selected_tag in r["tags"]]

        if selected_ingredient:
            recipes = [r for r in recipes if selected_ingredient in r["ingredients"]]

        self.display_recipes(recipes)

    def clear_filters(self):
        # Resetujemy wartości w comboBoxach do pustej (brak filtru)
        self.tag_filter_box.setCurrentIndex(0)
        self.ingredient_filter_box.setCurrentIndex(0)

        # Pokaż wszystkie przepisy bez filtrów
        self.display_recipes(RecipeController.instance().get_recipes())

    def display_recipes(self, recipes):
        self.recipe_list.clear()
        for recipe in recipes:
            self.recipe_list.addItem(recipe["name"])

    def open_selected_recipe(self, item):
        recipe = RecipeController.instance().get_recipe_by_title(item.text())
        self.main_window.show_recipe_detail(self, recipe)

    def add_recipe(self):
        self.main_window.show_add_recipe(self)

    def refresh_view(self):
        self.display_recipes(RecipeController.instance().get_recipes())