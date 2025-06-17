import tkinter as tk
from tkinter import simpledialog


class RecipeForm(simpledialog.Dialog):
    def __init__(self, parent, controller, edit_mode=False, recipe=None):
        self.controller = controller
        self.edit_mode = edit_mode
        self.recipe = recipe
        super().__init__(parent, title="Edytuj przepis" if edit_mode else "Dodaj przepis")

    def body(self, master):
        tk.Label(master, text="Nazwa:").grid(row=0)
        tk.Label(master, text="Składniki (po przecinku):").grid(row=1)
        tk.Label(master, text="Instrukcje:").grid(row=2)
        tk.Label(master, text="Tagi (po przecinku):").grid(row=3)

        self.name = tk.Entry(master)
        self.ingredients = tk.Entry(master)
        self.instructions = tk.Entry(master)
        self.tags = tk.Entry(master)

        self.name.grid(row=0, column=1)
        self.ingredients.grid(row=1, column=1)
        self.instructions.grid(row=2, column=1)
        self.tags.grid(row=3, column=1)

        if self.edit_mode and self.recipe:
            self.name.insert(0, self.recipe.name)
            self.ingredients.insert(0, ', '.join(self.recipe.ingredients))
            self.instructions.insert(0, self.recipe.instructions)
            self.tags.insert(0, ', '.join(self.recipe.tags))

        return self.name

    def apply(self):
        name = self.name.get()
        ingredients = self.ingredients.get().split(',')
        instructions = self.instructions.get()
        tags = self.tags.get().split(',')

        if self.edit_mode and self.recipe:
            self.controller.update_recipe(self.recipe.name, name, ingredients, instructions, tags)
        else:
            self.controller.add_recipe(name, ingredients, instructions, tags)
