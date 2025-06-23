from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QSpacerItem, QSizePolicy
from collections import Counter
from datetime import date, datetime, timedelta

from controller.calendar_controller import CalendarController
from controller.recipe_controller import RecipeController
from utils.clear_layout import clear_layout
from utils.style_manager import update_stylesheets


class StatsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statystyki")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title1 = QLabel("Podsumowanie")
        self.title1.setObjectName("statsSectionTitle")
        self.title2 = QLabel("Aktywność w czasie")
        self.title2.setObjectName("statsSectionTitle")

        self.build_stats()

    def build_stats(self):
        clear_layout(self.layout)

        self.layout.addWidget(self.title1)
        self.layout.addWidget(self.build_section_summary())
        self.layout.addWidget(self.title2)
        self.layout.addWidget(self.build_section_activity())
        self.layout.addStretch()


    def build_section_summary(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        recipes = RecipeController.instance().get_recipes()
        history = []

        for r in recipes:
            history.extend(CalendarController.instance().get_history(r["name"]))

        layout.addWidget(QLabel(f"Liczba przepisów: <b>{len(recipes)}</b>"))

        if history:
            most_common, least_common, avg = RecipeController.instance().history_stats()

            layout.addWidget(QLabel(f"Najczęściej gotowany przepis: <b>{most_common[0]}</b> ({most_common[1]} razy)"))
            layout.addWidget(QLabel(f"Najrzadziej gotowany przepis: <b>{least_common[0]}</b> ({least_common[1]} razy)"))
            layout.addWidget(QLabel(f"Średnia liczba gotowań na przepis: <b>{avg:.2f}<b>"))

            days_since, recent = CalendarController.instance().last_cook()
            layout.addWidget(QLabel(f"Ostatnie gotowanie było <b>{days_since}</b> dni temu"))

            layout.addWidget(QLabel(f"Najnowszy gotowany przepis: <b>{recent.recipe_name}</b> ({recent.cook_date})"))
        else:
            layout.addWidget(QLabel("Brak historii gotowania"))

        box.setLayout(layout)
        return box

    def build_section_activity(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        history = []

        for r in RecipeController.instance().get_recipes():
            history.extend(CalendarController.instance().get_history(r["name"]))

        if history:
            common_day, recent_months, monthly_counter, max_val = CalendarController.instance().activity_in_time()
            layout.addWidget(QLabel(f"Najczęstszy dzień tygodnia gotowania: <b>{common_day}</b>"))
            layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
            layout.addWidget(QLabel("<b>Wykresy aktywności w ostatnich 6 miesiącach<b>"))

            for month in reversed(recent_months):
                count = monthly_counter.get(month, 0)
                bar = '█' * int((count / max_val) * 30) if max_val > 0 else ''
                layout.addWidget(QLabel(f"{month}: {bar} ({count})"))
        else:
            layout.addWidget(QLabel("Brak danych o aktywności"))

        box.setLayout(layout)
        return box

    def refresh_view(self):
        update_stylesheets("statistics_section")
        self.build_stats()