from model.database import Database
from utils.singleton_class import SingletonClass


class RecipeController(SingletonClass):

    def get_recipes(self):
        recipes = Database.instance().get_all_recipes()
        return sorted(recipes, key=lambda recipe: recipe["name"].lower())

    def get_recipe_by_title(self, name):
        return Database.instance().get_recipe_by_title(name)

    def add_recipe(self, name, ingredients, instructions, tags):
        recipe = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "tags": tags,
            "image_path": ""  # lub obsłuż opcjonalnie
        }
        Database.instance().add_recipe(recipe)

    def delete_recipe(self, recipe):
        Database.instance().delete_recipe(recipe)

    def filter_recipes_by_tag(self, tag):
        return Database.instance().filter_recipes_by_tag(tag)

    def get_all_tags(self):
        return list({tag for recipe in self.get_recipes() for tag in recipe["tags"]})

    def get_all_ingredients(self):
        return list({ing for recipe in self.get_recipes() for ing in recipe["ingredients"]})

    def update_recipe(self, original_recipe, name, ingredients, instructions, tags):
        Database.instance().update_recipe(original_recipe, name, ingredients, instructions, tags)

    def clear_cook_history(self, recipe):
        Database.instance().clear_cook_history(recipe)