from model.database import Database

class RecipeController:
    def __init__(self, db: Database):
        self.db = db

    def get_recipes(self):
        return self.db.get_all_recipes()

    def get_recipe_by_title(self, name):
        return self.db.get_recipe_by_title(name)

    def add_recipe(self, name, ingredients, instructions, tags):
        recipe = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "tags": tags,
            "image_path": ""  # lub obsłuż opcjonalnie
        }
        self.db.add_recipe(recipe)

    def delete_recipe(self, recipe):
        self.db.delete_recipe(recipe)

    def filter_recipes_by_tag(self, tag):
        return self.db.filter_recipes_by_tag(tag)

    def get_all_tags(self):
        return list({tag for recipe in self.get_recipes() for tag in recipe["tags"]})

    def get_all_ingredients(self):
        return list({ing for recipe in self.get_recipes() for ing in recipe["ingredients"]})

    def update_recipe(self, original_recipe, name, ingredients, instructions, tags):
        updated = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "tags": tags,
            "image_path": original_recipe.get("image_path", "")
        }
        original_recipe["name"] = updated["name"]
        original_recipe["ingredients"] = updated["ingredients"]
        original_recipe["instructions"] = updated["instructions"]
        original_recipe["tags"] = updated["tags"]

    def clear_cook_history(self, recipe):
        self.db.clear_cook_history(recipe)