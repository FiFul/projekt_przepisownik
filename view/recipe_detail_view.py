import tkinter as tk
from tkinter import messagebox

from controller.recipe_controller import RecipeController
from model.recipe import Recipe
from view.recipe_form import RecipeForm


class RecipeDetailView(tk.Toplevel):
    def __init__(self, parent, controller: RecipeController, recipe: Recipe, refresh_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.recipe = recipe
        #self.refresh_callback = refresh_callback
        self.refresh_callback = parent.refresh_recipes

        self.title(f"Szczegóły: {recipe.name}")
        self.geometry("500x500")

        tk.Label(self, text=recipe.name, font=("Arial", 16)).pack(pady=5)

        tk.Label(self, text="Składniki:", font=("Arial", 12, 'bold')).pack(anchor='w', padx=10)
        tk.Label(self, text=", ".join(recipe.ingredients)).pack(anchor='w', padx=20)

        tk.Label(self, text="Instrukcje:", font=("Arial", 12, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
        tk.Label(self, text=recipe.instructions, wraplength=450, justify="left").pack(anchor='w', padx=20)

        tk.Label(self, text=f"Tagi: {', '.join(recipe.tags)}").pack(anchor='w', padx=10, pady=(10, 0))

        # Przyciski na dole
        frame = tk.Frame(self)
        frame.pack(side="bottom", pady=15)
        tk.Button(frame, text="Edytuj", command=self.edit_recipe).pack(side='left', padx=5)
        tk.Button(frame, text="Usuń", command=self.delete_recipe).pack(side='left', padx=5)
        tk.Button(frame, text="Zamknij", command=self.destroy).pack(side='left', padx=5)

    def edit_recipe(self):
        RecipeForm(self, self.controller, edit_mode=True, recipe=self.recipe)
        if self.refresh_callback:
            self.refresh_callback()
        self.destroy()

    def delete_recipe(self):
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć ten przepis?"):
            self.controller.delete_recipe(self.recipe.name)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
