from model.database import Database
from utils.singleton_class import SingletonClass

class CalendarController(SingletonClass):

    def log_cook(self, recipe_name: str, cook_date):
        Database.instance().log_cook_date(recipe_name, cook_date)

    def get_history(self, recipe_name: str):
        return Database.instance().get_cook_history(recipe_name)

    def clear_history(self, recipe_name: str):
        Database.instance().clear_cook_history(recipe_name)