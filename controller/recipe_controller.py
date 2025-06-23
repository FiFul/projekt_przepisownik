from model.database import Database
from utils.singleton_class import SingletonClass


class RecipeController(SingletonClass):

    def get_recipes(self):
        return  Database.instance().get_all_recipes()

    def get_recipe_by_title(self, name):
        return Database.instance().get_recipe_by_title(name)

    def add_recipe(self, name, ingredients, instructions, tags, image_path):
        recipe = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "tags": tags,
            "image_path": image_path if image_path else ""
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

    def update_recipe(self, original_recipe, name, ingredients, instructions, tags, image_path):
        Database.instance().update_recipe(original_recipe, name, ingredients, instructions, tags, image_path)

    def clear_cook_history(self, recipe):
        Database.instance().clear_cook_history(recipe)

    def get_random_recipe(self):
        return Database.instance().get_random_recipe()

    def apply_filters(self, ingredients, tags):
        return Database.instance().apply_filters(ingredients, tags)