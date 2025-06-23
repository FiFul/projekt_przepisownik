import os
import shutil
from uuid import uuid4

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QFileDialog, QHBoxLayout

from controller.recipe_controller import RecipeController
from model import recipe
from utils.pixmap_generator import generate_pixmap
from view.recipe_detail_view import RecipeDetailView
from view.widgets.clickable_label import ClickableLabel
from view.widgets.return_button import ReturnButton
from view.widgets.sidebar_button import SidebarButton


class RecipeForm(QWidget):
    def __init__(self, main_window, parent_widget, recipe):
        super().__init__()
        self.setWindowTitle("Edytuj przepis" if recipe else "Nowy Przepis")
        self.main_window = main_window
        self.parent_widget = parent_widget
        self.editing = recipe is not None
        self.original_recipe = recipe
        self.image_path = None

        layout = QVBoxLayout()
        layout.setSpacing(10)
        title_layout = QHBoxLayout()
        title_layout.setSpacing(50)

        btn_back = ReturnButton(self.close_view)
        layout.addWidget(btn_back)

        self.image_label = ClickableLabel("Wybierz zdjęcie")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(250, 160)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setScaledContents(True)
        self.image_label.clicked.connect(self.select_image)
        title_layout.addWidget(self.image_label)

        self.title_input = QLineEdit()
        self.title_input.setObjectName("titleInput")
        self.title_input.setPlaceholderText("Nazwa przepisu")
        title_layout.addWidget(self.title_input)

        layout.addLayout(title_layout)


        label_ingr = QLabel("Składniki:")
        label_inst = QLabel("Instrukcje:")
        label_tags = QLabel("Tagi:")
        for l in [label_ingr, label_inst, label_tags]:
            l.setObjectName("formLabel")
        self.ingredients_input = QTextEdit()
        layout.addWidget(label_ingr)
        layout.addWidget(self.ingredients_input)

        self.instructions_input = QTextEdit()
        layout.addWidget(label_inst)
        layout.addWidget(self.instructions_input)

        self.tags_input = QLineEdit()
        layout.addWidget(label_tags)
        layout.addWidget(self.tags_input)

        btn_save = SidebarButton("Zapisz")
        btn_save.setFixedSize(QSize(200, 50))
        btn_save.clicked.connect(self.save_recipe)
        layout.addWidget(btn_save)

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
        self.image_path = recipe["image_path"]
        if self.image_path:
            pixmap = generate_pixmap(self.image_path, self.image_label.width(), self.image_label.height())
            self.image_label.setPixmap(pixmap)

    def save_recipe(self):
        name = self.title_input.text()
        ingredients = self.ingredients_input.toPlainText().split('\n')
        instructions = self.instructions_input.toPlainText()
        tags = [tag.strip() for tag in self.tags_input.text().split(',')]

        if self.editing:
            RecipeController.instance().update_recipe(self.original_recipe, name, ingredients, instructions, tags, self.image_path)
            if type(self.parent_widget) is RecipeDetailView:
                self.parent_widget.update_recipe(name, ingredients, instructions, tags, self.image_path)
        else:
            RecipeController.instance().add_recipe(name, ingredients, instructions, tags, self.image_path)
            detail_view = RecipeDetailView(self.main_window, self.parent_widget, RecipeController.instance().get_recipe_by_title(name))
            self.main_window.stack.addWidget(detail_view)
            self.parent_widget = detail_view

        self.close_view()

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz obraz", "", "Obrazy (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            os.makedirs("data", exist_ok=True)
            if self.image_path and os.path.exists(self.image_path):
                os.remove(self.image_path)
            ext = os.path.splitext(file_name)[1]
            new_filename = f"{uuid4().hex}{ext}"
            target_path = os.path.join("data", new_filename)
            shutil.copy(file_name, target_path)
            self.image_path = target_path
            pixmap = QPixmap(self.image_path)
            label_width = self.width()
            label_height = int(0.75 * self.height())

            pixmap_ratio = pixmap.width() / pixmap.height()
            label_ratio = label_width / label_height

            if label_ratio > pixmap_ratio:
                scaled_height = int(pixmap.width() / label_ratio)
                y_offset = (pixmap.height() - scaled_height) // 2
                cropped = pixmap.copy(0, y_offset, pixmap.width(), scaled_height)
            else:
                scaled_width = int(pixmap.height() * label_ratio)
                x_offset = (pixmap.width() - scaled_width) // 2
                cropped = pixmap.copy(x_offset, 0, scaled_width, pixmap.height())

            scaled_pixmap = cropped.scaled(label_width, label_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
    
    def close_view(self):
        self.main_window.stack.setCurrentWidget(self.parent_widget)
        self.main_window.stack.currentWidget().refresh_view()
        self.close()