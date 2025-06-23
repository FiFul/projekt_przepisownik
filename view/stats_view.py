from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
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
        self.build_stats()

    def build_stats(self):
        clear_layout(self.layout)
        self.layout.addWidget(self.build_section_summary())
        self.layout.addWidget(self.build_section_activity())


    def build_section_summary(self):
        box = QGroupBox("Podsumowanie")
        layout = QVBoxLayout()
        recipes = RecipeController.instance().get_recipes()
        history = []

        for r in recipes:
            history.extend(CalendarController.instance().get_history(r["name"]))

        layout.addWidget(QLabel(f"Liczba przepisów: {len(recipes)}"))

        if history:
            count = Counter([h.recipe_name for h in history])
            most_common = count.most_common(1)[0]
            least_common = count.most_common()[-1]
            avg = sum(count.values()) / len(count)

            layout.addWidget(QLabel(f"Najczęściej gotowany przepis: {most_common[0]} ({most_common[1]} razy)"))
            layout.addWidget(QLabel(f"Najrzadziej gotowany przepis: {least_common[0]} ({least_common[1]} razy)"))
            layout.addWidget(QLabel(f"Średnia liczba gotowań na przepis: {avg:.2f}"))

            last_cook = max(h.cook_date for h in history)
            days_since = (date.today() - last_cook).days
            layout.addWidget(QLabel(f"Ostatnie gotowanie było {days_since} dni temu"))

            recent = sorted(history, key=lambda h: h.cook_date, reverse=True)[0]
            layout.addWidget(QLabel(f"Najnowszy gotowany przepis: {recent.recipe_name} ({recent.cook_date})"))
        else:
            layout.addWidget(QLabel("Brak historii gotowania"))

        box.setLayout(layout)
        return box

    def build_section_activity(self):
        box = QGroupBox("Aktywność w czasie")
        layout = QVBoxLayout()
        history = []

        for r in RecipeController.instance().get_recipes():
            history.extend(CalendarController.instance().get_history(r["name"]))

        if history:
            weekdays = [datetime.combine(h.cook_date, datetime.min.time()).strftime('%A') for h in history]
            weekday_counter = Counter(weekdays)
            common_day = weekday_counter.most_common(1)[0]
            layout.addWidget(QLabel(f"Najczęstszy dzień tygodnia gotowania: {common_day[0]}"))

            # Oblicz ostatnie 6 miesięcy
            today = datetime.today()
            recent_months = [(today.replace(day=1) - timedelta(days=30 * i)).strftime('%Y-%m') for i in
                             reversed(range(6))]

            # Zlicz liczbę gotowań na miesiąc
            months = [h.cook_date.strftime('%Y-%m') for h in history]
            monthly_counter = Counter(months)

            layout.addWidget(QLabel("Gotowania w ostatnich 6 miesiącach:"))
            max_val = max([monthly_counter[m] for m in recent_months if m in monthly_counter], default=1)

            for month in recent_months:
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