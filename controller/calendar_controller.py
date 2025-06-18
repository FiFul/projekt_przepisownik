from model.database import Database


class CalendarController:
    def __init__(self, db: Database):
        self.db = db

    def log_cook(self, recipe_name: str, cook_date):
        self.db.log_cook_date(recipe_name, cook_date)

    def get_history(self, recipe_name: str):
        return self.db.get_cook_history(recipe_name)

    def clear_history(self, recipe_name: str):
        self.db.clear_cook_history(recipe_name)
