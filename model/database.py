import os
import random
import json
from datetime import datetime, date
from model.cook_history import CookHistory
from utils.singleton_class import SingletonClass

class Database(SingletonClass):
    def __init__(self, recipe_file='data/recipes.json', cook_history_file='data/cook_history.json'):
        super().__init__()
        self.recipe_file = recipe_file
        self.cook_history_file = cook_history_file
        self.recipes = []
        self.load()

    def load(self):
        try:
            with open(self.recipe_file, 'r', encoding='utf-8') as f:
                self.recipes = json.load(f)
        except FileNotFoundError:
            self.recipes = []

    def save(self):
        with open(self.recipe_file, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)

    def add_recipe(self, recipe):
        self.recipes.append(recipe)
        self.save()

    def get_all_recipes(self):
        return self.recipes

    def get_recipe_by_title(self, name):
        return next((r for r in self.recipes if r["name"] == name), None)

    def update_recipe(self, recipe, name, ingredients, instructions, tags, image_path):
        idx = self.recipes.index(recipe)
        self.recipes[idx] = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "tags": tags,
            "image_path": image_path or ""
        }
        self.save()

    def delete_recipe(self, recipe):
        self.recipes = [r for r in self.recipes if r['name'] != recipe['name']]
        if recipe.get("image_path"):
            try:
                os.remove(recipe["image_path"])
            except FileNotFoundError:
                pass
        self.save()

    def filter_recipes_by_tag(self, tag):
        return [r for r in self.recipes if tag in r.get("tags", [])]

    def get_all_tags(self):
        return list({tag for recipe in self.recipes for tag in recipe.get("tags", [])})

    def log_cook_date(self, recipe_name, cook_date):
        try:
            with open(self.cook_history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append({
            "recipe_name": recipe_name,
            "cook_date": cook_date.isoformat()
        })

        with open(self.cook_history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get_cook_history(self, recipe_name):
        try:
            with open(self.cook_history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        return [
            CookHistory(entry["recipe_name"], datetime.fromisoformat(entry["cook_date"]).date())
            for entry in data if entry["recipe_name"] == recipe_name
        ]

    def clear_cook_history(self, recipe_name):
        try:
            with open(self.cook_history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data = [entry for entry in data if entry["recipe_name"] != recipe_name]

        with open(self.cook_history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get_random_recipe(self):
        return random.choice(self.recipes) if self.recipes else None

    def apply_filters(self, ingredients, tags):
        recipes = self.recipes
        if tags:
            recipes = [r for r in recipes if tags in r.get("tags", [])]
        if ingredients:
            recipes = [r for r in recipes if ingredients in r.get("ingredients", [])]
        return recipes

    def days_cooked(self, recipe_name):
        history = self.get_cook_history(recipe_name)
        last_date = max(entry.cook_date for entry in history)
        days_ago = (date.today() - last_date).days
        return days_ago