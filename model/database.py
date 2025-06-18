from model.recipe import Recipe
from model.cook_history import CookHistory
from typing import List
import datetime
import json
import os


class Database:
    def __init__(self, filename='recipes.json'):
        self.filename = filename
        self.recipes = []
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.recipes = json.load(f)
        except FileNotFoundError:
            self.recipes = []

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)

    def add_recipe(self, recipe):
        self.recipes.append(recipe)
        self.save()

    def get_all_recipes(self):
        return self.recipes

    def get_recipe_by_title(self, name):
        for recipe in self.recipes:
            if recipe["name"] == name:
                return recipe
        return None

    def delete_recipe(self, recipe):
        self.recipes = [r for r in self.recipes if r['name'] != recipe['name']]
        self.save()

    def filter_recipes_by_tag(self, tag):
        return [r for r in self.recipes if tag in r["tags"]]

    def get_all_tags(self):
        tags = set()
        for recipe in self.recipes:
            tags.update(recipe.get("tags", []))
        return list(tags)

    def update_recipe(self, original, updated):
        index = self.recipes.index(original)
        self.recipes[index] = updated
        self.save()

    def log_cook_date(self, recipe_name, cook_date):
        try:
            with open("cook_history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        # Dodajemy nowy wpis
        data.append({
            "recipe_name": recipe_name,
            "cook_date": cook_date.isoformat()
        })

        with open("cook_history.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_cook_history(self, recipe_name):
        try:
            with open("cook_history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        # Filtrujemy po nazwie przepisu i tworzymy obiekty CookHistory
        from datetime import datetime
        history = []
        for entry in data:
            if entry["recipe_name"] == recipe_name:
                cook_date = datetime.fromisoformat(entry["cook_date"]).date()
                history.append(CookHistory(recipe_name, cook_date))
        return history

    def clear_cook_history(self, recipe_name):
        try:
            with open("cook_history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        # Filtrowanie historii bez wpisów dla danego przepisu
        data = [entry for entry in data if entry["recipe_name"] != recipe_name]

        with open("cook_history.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)