from datetime import date

class CookHistory:
    def __init__(self, recipe_name: str, cook_date: date):
        self.recipe_name = recipe_name
        self.cook_date = cook_date
