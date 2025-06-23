from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

from controller.recipe_controller import RecipeController
from utils.pixmap_generator import generate_pixmap
from view.widgets.clickable_label import ClickableLabel
from view.widgets.content_section import ContentSection
from view.widgets.return_button import ReturnButton


class RecipeDetailView(QWidget):
    def __init__(self, main_window, parent_widget, recipe):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Szczegóły Przepisu")
        self.parent_widget = parent_widget
        self.recipe = recipe


        spacer_small = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer_big = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout = QVBoxLayout()

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)


        self.return_button = ReturnButton(self.close_view)
        self.button_layout.addWidget(self.return_button)

        self.button_layout.addStretch()
        self.button_layout.setAlignment(Qt.AlignTop)
        self.buttons_size = 100

        self.calendar_button = QPushButton()
        self.calendar_button.setIcon(QIcon(f"assets/icons/icon_calendar.png"))
        self.calendar_button.setIconSize(QSize(self.buttons_size, self.buttons_size))
        self.calendar_button.setToolTip("Sprawdź w kalendarzu")
        self.calendar_button.setCursor(Qt.PointingHandCursor)
        self.calendar_button.setFixedSize(QSize(self.buttons_size, self.buttons_size))
        self.calendar_button.setObjectName('topButton')
        self.calendar_button.clicked.connect(self.open_calendar)
        self.button_layout.addWidget(self.calendar_button)

        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon(f"assets/icons/icon_edit.png"))
        self.edit_button.setIconSize(QSize(self.buttons_size, self.buttons_size))
        self.edit_button.setToolTip("Edytuj")
        self.edit_button.setCursor(Qt.PointingHandCursor)
        self.edit_button.setFixedSize(QSize(self.buttons_size, self.buttons_size))
        self.edit_button.setObjectName('topButton')
        self.edit_button.clicked.connect(self.edit_recipe)
        self.button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon(f"assets/icons/icon_delete.png"))
        self.delete_button.setIconSize(QSize(self.buttons_size, self.buttons_size))
        self.delete_button.setToolTip("Usuń")
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setFixedSize(QSize(self.buttons_size, self.buttons_size))
        self.delete_button.setObjectName('topButton')
        self.delete_button.clicked.connect(self.delete_recipe)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)
        self.layout.addItem(spacer_small)

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
        self.title_label.setStyleSheet("QLabel { background: transparent; font-family: 'Verdana'; font-weight: bold; font-size: 32px;}")
        self.title_layout.addWidget(self.title_label)

        self.layout.addLayout(self.title_layout)

        self.main_content_layout = QHBoxLayout()
        self.main_content_layout.setSpacing(50)

        self.ingredients_title_label = QLabel("Składniki")
        self.ingredients_title_label.setFixedWidth(250)
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

        self.main_content_layout.addLayout(ContentSection(self.ingredients_title_label,self.ingredients_label))
        self.main_content_layout.addLayout(ContentSection(self.instructions_title_label,self.instructions_label))
        self.main_content_layout.addStretch()
        self.layout.addLayout(self.main_content_layout)
        self.layout.addItem(spacer_big)

        self.layout.addLayout(ContentSection(self.tags_title_label, self.tags_label))
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.refresh_view()

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
        self.image_path = self.recipe["image_path"]
        if self.image_path:
            pixmap = generate_pixmap(self.image_path, self.image_label.width(), self.image_label.height())
            self.image_label.setPixmap(pixmap)
        self.title_label.setText(self.recipe['name'])
        self.ingredients_label.setText('\n'.join(self.recipe['ingredients']))
        self.instructions_label.setText(self.recipe['instructions'])
        self.tags_label.setText(', '.join(self.recipe['tags']))

    def update_recipe(self, name, ingredients, instructions, tags, image_path):
        self.recipe['name'] = name
        self.recipe['ingredients'] = ingredients
        self.recipe['instructions'] = instructions
        self.recipe['tags'] = tags
        self.recipe['image_path'] = image_path if image_path else ""