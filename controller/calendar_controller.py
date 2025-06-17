from model.database import Database


class CalendarController:
    def __init__(self, db: Database):
        self.db = db

    def log_cook(self, recipe_name: str):
        self.db.log_cook(recipe_name)

    def get_history(self, recipe_name: str):
        return self.db.get_cook_history(recipe_name)
