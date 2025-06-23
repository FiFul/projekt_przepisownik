from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QComboBox, QLabel, QHBoxLayout, QScrollArea, \
    QGridLayout, QSpacerItem, QSizePolicy

from controller.recipe_controller import RecipeController
from utils.style_manager import update_stylesheets
from view.widgets.menu_button import MenuButton
from view.widgets.recipe_tile import RecipeTile
from view.widgets.sidebar_button import SidebarButton


class RecipeListView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Lista Przepisów")

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)

        self.grid_layout.setVerticalSpacing(30)
        self.grid_layout.setHorizontalSpacing(30)

        self.scroll.setWidget(self.grid_container)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.scroll)
        self.scroll.setObjectName("scrollArea")
        self.grid_container.setObjectName("gridContainer")

        sidebar = QVBoxLayout()

        self.add_button = SidebarButton("Dodaj przepis")
        self.add_button.clicked.connect(self.add_recipe)
        sidebar.addWidget(self.add_button)

        sidebar.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.ingredient_filter_box = QComboBox()
        sidebar.addWidget(self.ingredient_filter_box)

        self.tag_filter_box = QComboBox()
        sidebar.addWidget(self.tag_filter_box)

        self.filter_button = SidebarButton("Zastosuj filtry")
        self.filter_button.clicked.connect(self.apply_filters)
        sidebar.addWidget(self.filter_button)

        self.clear_button = SidebarButton("Wyczyść filtry")
        self.clear_button.clicked.connect(self.clear_filters)
        sidebar.addWidget(self.clear_button)

        sidebar.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(sidebar)
        self.refresh_view()

    def update_filter_options(self):
        self.tag_filter_box.clear()
        self.ingredient_filter_box.clear()

        tags = RecipeController.instance().get_all_tags()
        ingredients = RecipeController.instance().get_all_ingredients()

        self.ingredient_filter_box.addItem("Wybierz filtr składnika")
        self.tag_filter_box.addItem("Wybierz filtr tagu")
        self.ingredient_filter_box.model().item(0).setEnabled(False)
        self.tag_filter_box.model().item(0).setEnabled(False)

        self.ingredient_filter_box.addItems(sorted(ingredients))
        self.tag_filter_box.addItems(sorted(tags))

    def apply_filters(self):
        selected_ingredient = self.ingredient_filter_box.currentText()
        selected_tag = self.tag_filter_box.currentText()

        if selected_ingredient == "Wybierz filtr składnika":
            selected_ingredient = ""

        if selected_tag == "Wybierz filtr tagu":
            selected_tag = ""

        recipes = RecipeController.instance().apply_filters(selected_ingredient, selected_tag)

        self.display_recipes(recipes)

    def clear_filters(self):
        # Resetujemy wartości w comboBoxach do pustej (brak filtru)
        self.tag_filter_box.setCurrentIndex(0)
        self.ingredient_filter_box.setCurrentIndex(0)

        # Pokaż wszystkie przepisy bez filtrów
        self.display_recipes(RecipeController.instance().get_recipes())

    def display_recipes(self, recipes):
        # Czyść poprzednie widżety
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        cols = 5  # Liczba kolumn
        for index, recipe in enumerate(recipes):
            tile = RecipeTile(recipe)
            tile.clicked.connect(self.open_selected_recipe)
            row = index // cols
            col = index % cols
            self.grid_layout.addWidget(tile, row, col)

    def open_selected_recipe(self, recipe):
        self.main_window.show_recipe_detail(self, recipe)

    def add_recipe(self):
        self.main_window.show_add_recipe(self)

    def refresh_view(self):
        update_stylesheets("recipes_section")
        self.update_filter_options()
        self.display_recipes(RecipeController.instance().get_recipes())
