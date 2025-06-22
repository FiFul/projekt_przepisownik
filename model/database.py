from model.cook_history import CookHistory
import json

from utils.singleton_class import SingletonClass


class Database(SingletonClass):
    def __init__(self, filename='data/recipes.json'):
        super().__init__()
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

    def update_recipe(self, recipe, name, ingredients, instructions, tags, image_path):
        id = self.recipes.index(recipe)
        self.recipes[id]["name"] = name
        self.recipes[id]["ingredients"] = ingredients
        self.recipes[id]["instructions"] = instructions
        self.recipes[id]["tags"] = tags
        self.recipes[id]["image_path"] = image_path if image_path else ""
        self.save()

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


    def log_cook_date(self, recipe_name, cook_date):
        try:
            with open("data/cook_history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        # Dodajemy nowy wpis
        data.append({
            "recipe_name": recipe_name,
            "cook_date": cook_date.isoformat()
        })

        with open("data/cook_history.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_cook_history(self, recipe_name):
        try:
            with open("data/cook_history.json", "r", encoding="utf-8") as f:
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
            with open("data/cook_history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        # Filtrowanie historii bez wpisów dla danego przepisu
        data = [entry for entry in data if entry["recipe_name"] != recipe_name]

        with open("data/cook_history.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)