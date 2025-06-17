import tkinter as tk
from tkinter import ttk
from view.recipe_detail_view import RecipeDetailView
from view.recipe_edit_view import RecipeEditView


class RecipeListView(tk.Toplevel):
    def __init__(self, master, recipe_controller, calendar_controller):
        super().__init__(master)
        self.title("Lista przepisów")

        self.recipe_controller = recipe_controller
        self.calendar_controller = calendar_controller

        # Przycisk dodawania nowego przepisu
        add_button = tk.Button(self, text="Dodaj przepis", command=self.add_recipe)
        add_button.pack(side='top', pady=5)

        # Dropdown do wyboru rodzaju filtru: tag lub składnik
        self.filter_option = tk.StringVar(value="tag")
        filter_type_menu = tk.OptionMenu(
            self, self.filter_option, "tag", "ingredient",
            command=lambda _: self.update_filter_options()
        )
        filter_type_menu.pack(side='top', padx=5, pady=2)

        # Dropdown z dynamicznie uzupełnianą listą tagów/składników
        self.filter_var = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(self, textvariable=self.filter_var)
        self.filter_dropdown.pack(side='top', padx=5, pady=2)

        # Przycisk do zastosowania filtra
        filter_button = tk.Button(self, text="Filtruj", command=self.apply_filter)
        filter_button.pack(side='top', pady=5)

        # Lista przepisów
        self.recipe_listbox = tk.Listbox(self, width=50)
        self.recipe_listbox.pack(padx=10, pady=10)
        self.recipe_listbox.bind("<Double-Button-1>", self.open_selected_recipe)

        # Załaduj wszystkie przepisy na start
        self.update_filter_options()
        self.display_recipes(self.recipe_controller.get_recipes())

    def add_recipe(self):
        RecipeEditView(self.recipe_controller, on_save=self.refresh_recipes)

    def open_selected_recipe(self, event):
        selection = self.recipe_listbox.curselection()
        if selection:
            index = selection[0]
            recipe = self.recipes_to_display[index]
            RecipeDetailView(self, self.recipe_controller, recipe)#,on_update=self.refresh_recipes)

    def display_recipes(self, recipes):
        self.recipes_to_display = recipes
        self.recipe_listbox.delete(0, tk.END)
        for recipe in recipes:
            self.recipe_listbox.insert(tk.END, recipe.name)

    def update_filter_options(self):
        if self.filter_option.get() == "tag":
            options = self.recipe_controller.db.get_all_tags()
        else:
            options = self.recipe_controller.db.get_all_ingredients()
        self.filter_dropdown['values'] = options

    def apply_filter(self):
        value = self.filter_var.get()
        if not value:
            return

        if self.filter_option.get() == "tag":
            filtered = self.recipe_controller.get_recipes_by_tag(value)
        else:
            filtered = [
                r for r in self.recipe_controller.get_recipes()
                if value.lower() in [i.lower() for i in r.ingredients]
            ]
        self.display_recipes(filtered)

    def refresh_recipes(self):
        self.display_recipes(self.recipe_controller.get_recipes())
        self.update_filter_options()
