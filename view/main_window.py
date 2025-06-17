import tkinter as tk
from view.recipe_list_view import RecipeListView
from view.calendar_view import CalendarView
from tkinter import simpledialog


class MainWindow(tk.Frame):
    def __init__(self, parent, recipe_controller, calendar_controller):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        self.calendar_controller = calendar_controller

        tk.Label(self, text="Książka Przepisów", font=('Arial', 16)).pack(pady=10)

        tk.Button(self, text="Lista przepisów", command=self.open_recipe_list).pack(pady=5)
        tk.Button(self, text="Kalendarz gotowania", command=self.open_calendar).pack(pady=5)
        tk.Button(self, text="Filtruj po tagu", command=self.filter_by_tag).pack(pady=5)

        self.result_box = tk.Text(self, height=15, width=60)
        self.result_box.pack(pady=10)
        self.refresh_recipes()

    def open_recipe_list(self):
        RecipeListView(self.master, self.recipe_controller, self.calendar_controller)


    def open_calendar(self):
        CalendarView(self.master, self.calendar_controller)

    def filter_by_tag(self):
        tag = simpledialog.askstring("Filtruj", "Podaj tag do filtrowania:")
        if tag:
            recipes = self.recipe_controller.get_recipes_by_tag(tag)
            self.display_recipes(recipes)

    def refresh_recipes(self):
        self.display_recipes(self.recipe_controller.get_recipes())

    def display_recipes(self, recipes):
        self.result_box.delete('1.0', tk.END)
        for r in recipes:
            self.result_box.insert(tk.END, f"{r.name} | Tagi: {', '.join(r.tags)}\n")
