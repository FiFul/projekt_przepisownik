from model.recipe import Recipe
from model.database import Database


class RecipeController:
    def __init__(self):
        self.db = Database()

    def add_recipe(self, name, ingredients, instructions, tags, image_path=''):
        recipe = Recipe(name, ingredients, instructions, tags, image_path)
        self.db.add_recipe(recipe)

    def update_recipe(self, old_name, name, ingredients, instructions, tags, image_path=''):
        updated = Recipe(name, ingredients, instructions, tags, image_path)
        self.db.update_recipe(old_name, updated)

    def delete_recipe(self, name):
        self.db.delete_recipe(name)

    def get_recipes(self):
        return self.db.get_recipes()

    def get_recipes_by_tag(self, tag):
        return self.db.get_recipes_by_tag(tag)

