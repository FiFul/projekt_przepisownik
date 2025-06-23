from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy

from controller.recipe_controller import RecipeController
from utils.style_manager import update_stylesheets
from view.widgets.clickable_label import ClickableLabel
from view.widgets.content_section import ContentSection
from view.widgets.sidebar_button import SidebarButton


class HomepageView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Strona Główna")

        spacer_small = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer_big = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Witaj, oto twoja propozycja przepisu na dziś!"))

        self.new_recipe_button = SidebarButton("Inny przepis")
        self.new_recipe_button.clicked.connect(self.get_random_recipe)
        self.layout.addWidget(self.new_recipe_button)

        self.title_layout = QHBoxLayout()
        self.title_layout.setSpacing(50)

        self.image_label = ClickableLabel("Brak zdjęcia")
        self.image_label.unsetCursor()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(250, 160)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setScaledContents(True)

        self.title_layout.addWidget(self.image_label)

        self.title_label = QLabel()
        self.title_label.setStyleSheet(
            "QLabel { background: transparent; font-family: 'Verdana'; font-weight: bold; font-size: 32px;}")
        self.title_layout.addWidget(self.title_label)

        self.layout.addLayout(self.title_layout)

        self.main_content_layout = QHBoxLayout()
        self.main_content_layout.setSpacing(50)

        self.ingredients_title_label = QLabel("Składniki")
        self.ingredients_title_label.setObjectName("sectionTitleLabel")
        self.ingredients_label = QLabel()
        self.ingredients_label.setObjectName("sectionContentLabel")
        self.instructions_title_label = QLabel("Instrukcje")
        self.instructions_title_label.setObjectName("sectionTitleLabel")
        self.instructions_label = QLabel()
        self.instructions_label.setObjectName("sectionContentLabel")
        self.tags_title_label = QLabel("Tagi")
        self.tags_title_label.setObjectName("sectionTitleLabel")
        self.tags_label = QLabel()
        self.tags_label.setObjectName("sectionContentLabel")

        self.layout.addItem(spacer_big)

        self.main_content_layout.addLayout(ContentSection(self.ingredients_title_label, self.ingredients_label))
        self.main_content_layout.addLayout(ContentSection(self.instructions_title_label, self.instructions_label))
        self.main_content_layout.addStretch()
        self.layout.addLayout(self.main_content_layout)
        self.layout.addItem(spacer_big)

        self.layout.addLayout(ContentSection(self.tags_title_label, self.tags_label))
        self.layout.addStretch()

        self.setLayout(self.layout)

        self.get_random_recipe()
        self.refresh_view()

    def refresh_view(self):
        update_stylesheets("home_section")

        self.image_path = self.recipe_of_the_day["image_path"]
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Brak zdjęcia")

        self.title_label.setText(self.recipe_of_the_day['name'])
        self.ingredients_label.setText('\n'.join(self.recipe_of_the_day['ingredients']))
        self.instructions_label.setText(self.recipe_of_the_day['instructions'])
        self.tags_label.setText(', '.join(self.recipe_of_the_day['tags']))

    def get_random_recipe(self):
        self.recipe_of_the_day = RecipeController.instance().get_random_recipe()
        self.refresh_view()