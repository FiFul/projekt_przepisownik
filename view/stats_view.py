from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from collections import Counter

class StatsView(QWidget):
    def __init__(self, recipe_controller, calendar_controller):
        super().__init__()
        self.setWindowTitle("Statystyki")
        layout = QVBoxLayout()

        recipes = recipe_controller.get_recipes()
        history = []
        for r in recipes:
            history.extend(calendar_controller.get_history(r["name"]))

        layout.addWidget(QLabel(f"Liczba przepisów: {len(recipes)}"))

        if history:
            count = Counter([h.recipe_name for h in history])
            most_common = count.most_common(1)[0]
            least_common = count.most_common()[-1]

            layout.addWidget(QLabel(f"Najczęściej gotowany przepis: {most_common[0]} ({most_common[1]} razy)"))
            layout.addWidget(QLabel(f"Najrzadziej gotowany przepis: {least_common[0]} ({least_common[1]} razy)"))
        else:
            layout.addWidget(QLabel("Brak historii gotowania"))

        tags = recipe_controller.get_all_tags()
        if tags:
            layout.addWidget(QLabel("Tagi: " + ", ".join(tags)))
        else:
            layout.addWidget(QLabel("Brak tagów"))

        self.setLayout(layout)
