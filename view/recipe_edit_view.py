import tkinter as tk

class RecipeEditView(tk.Toplevel):
    def __init__(self, recipe_controller, recipe=None, on_save=None):
        super().__init__()
        self.title("Edytuj przepis" if recipe else "Nowy przepis")
        self.recipe_controller = recipe_controller
        self.recipe = recipe
        self.on_save = on_save

        # Pola formularza
        self.title_entry = tk.Entry(self)
        self.title_entry.insert(0, recipe.title if recipe else "")
        self.title_entry.pack(pady=5)

        self.ingredients_text = tk.Text(self, height=5, width=40)
        if recipe:
            self.ingredients_text.insert("1.0", "\n".join(recipe.ingredients))
        self.ingredients_text.pack(pady=5)

        self.tags_entry = tk.Entry(self)
        if recipe:
            self.tags_entry.insert(0, ", ".join(recipe.tags))
        self.tags_entry.pack(pady=5)

        save_button = tk.Button(self, text="Zapisz", command=self.save)
        save_button.pack(pady=5)

    def save(self):
        title = self.title_entry.get()
        ingredients = self.ingredients_text.get("1.0", tk.END).strip().split("\n")
        tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]

        if self.recipe:
            self.recipe_controller.update_recipe(self.recipe.id, title, ingredients, tags)
        else:
            self.recipe_controller.add_recipe(title, ingredients, tags)

        if self.on_save:
            self.on_save()
        self.destroy()
