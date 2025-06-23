import os
import random
import json
from collections import Counter
from datetime import datetime, date, timedelta
from model.cook_history import CookHistory
from utils.singleton_class import SingletonClass
from utils.translator import translate_day_to_polish


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
        return sorted(self.recipes, key=lambda recipe: recipe['name'].lower())

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

    def get_all_tags(self):
        res = list({tag for recipe in self.recipes for tag in recipe["tags"] if tag})
        res.sort()
        return res

    def get_all_ingredients(self):
        res = list({ing for recipe in self.recipes for ing in recipe["ingredients"] if ing})
        res.sort()
        return res

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

        result = [CookHistory(entry["recipe_name"], datetime.fromisoformat(entry["cook_date"]).date()) for entry in data if entry["recipe_name"] == recipe_name]
        return sorted(result, key=lambda r: r.cook_date, reverse=True)

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
        recipes = self.get_all_recipes()
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

    def history_stats(self):
        recipes = self.get_all_recipes()
        history = []

        for r in recipes:
            history.extend(self.get_cook_history(r["name"]))

        count = Counter([h.recipe_name for h in history])
        most_common = count.most_common(1)[0]
        least_common = count.most_common()[-1]
        avg = sum(count.values()) / len(count)

        return most_common, least_common, avg

    def last_cooked(self):
        recipes = self.get_all_recipes()
        history = []

        for r in recipes:
            history.extend(self.get_cook_history(r["name"]))

        last_cook = max(h.cook_date for h in history)
        days_since = (date.today() - last_cook).days
        recent = sorted(history, key=lambda h: h.cook_date, reverse=True)[0]

        return days_since, recent

    def activity_in_time(self):
        recipes = self.get_all_recipes()
        history = []

        for r in recipes:
            history.extend(self.get_cook_history(r["name"]))

        weekdays = [datetime.combine(h.cook_date, datetime.min.time()).strftime('%A') for h in history]
        weekday_counter = Counter(weekdays)
        common_day = weekday_counter.most_common(1)[0]


        # Oblicz ostatnie 6 miesięcy
        today = datetime.today()
        recent_months = [(today.replace(day=1) - timedelta(days=30 * i)).strftime('%Y-%m') for i in
                         reversed(range(6))]

        # Zlicz liczbę gotowań na miesiąc
        months = reversed([h.cook_date.strftime('%Y-%m') for h in history])
        monthly_counter = Counter(months)

        max_val = max([monthly_counter[m] for m in recent_months if m in monthly_counter], default=1)


        return translate_day_to_polish(common_day[0]), recent_months, monthly_counter, max_val