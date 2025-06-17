from model.recipe import Recipe
from model.cook_history import CookHistory
from typing import List
import datetime
import json
import os


class Database:
    def __init__(self, filepath='recipes.json'):
        self.filepath = filepath
        self.recipes: List[Recipe] = []
        self.history: List[CookHistory] = []
        self.load_data()

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)
        self.save_data()

    def get_recipes(self) -> List[Recipe]:
        return self.recipes

    def get_recipes_by_tag(self, tag: str) -> List[Recipe]:
        return [r for r in self.recipes if tag in r.tags]

    def update_recipe(self, old_name: str, updated_recipe: Recipe):
        for i, r in enumerate(self.recipes):
            if r.name == old_name:
                self.recipes[i] = updated_recipe
                break
        self.save_data()

    def delete_recipe(self, name: str):
        self.recipes = [r for r in self.recipes if r.name != name]
        self.save_data()

    def log_cook(self, recipe_name: str):
        self.history.append(CookHistory(recipe_name, datetime.date.today()))

    def get_cook_history(self, recipe_name: str) -> List[CookHistory]:
        return [h for h in self.history if h.recipe_name == recipe_name]

    def save_data(self):
        data = [r.to_dict() for r in self.recipes]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.recipes = [Recipe.from_dict(r) for r in data]

