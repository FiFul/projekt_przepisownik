from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)

class RecipeEditView(QWidget):
    def __init__(self, recipe_controller):
        super().__init__()
        self.recipe_controller = recipe_controller
        self.setWindowTitle("Dodaj przepis")

        layout = QVBoxLayout()

        # Tytuł
        layout.addWidget(QLabel("Tytuł:"))
        self.title_entry = QLineEdit()
        layout.addWidget(self.title_entry)

        # Składniki
        layout.addWidget(QLabel("Składniki (oddzielone przecinkami):"))
        self.ingredients_text = QTextEdit()
        layout.addWidget(self.ingredients_text)

        # Instrukcje
        layout.addWidget(QLabel("Instrukcje:"))
        self.instructions_text = QTextEdit()
        layout.addWidget(self.instructions_text)

        # Tagi
        layout.addWidget(QLabel("Tagi (oddzielone przecinkami):"))
        self.tags_entry = QLineEdit()
        layout.addWidget(self.tags_entry)

        # Przycisk zapisu
        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.save)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save(self):
        title = self.title_entry.text()
        ingredients = [i.strip() for i in self.ingredients_text.toPlainText().strip().split(",")]
        instructions = self.instructions_text.toPlainText().strip()
        tags = [t.strip() for t in self.tags_entry.text().strip().split(",")]


        try:
            self.recipe_controller.add_recipe(title, ingredients, instructions, tags)
            QMessageBox.information(self, "Sukces", "Przepis zapisany.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))
