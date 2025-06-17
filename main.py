from controller.recipe_controller import RecipeController
from controller.calendar_controller import CalendarController
from model.database import Database
from view.main_window import MainWindow
import tkinter as tk


def main():
    root = tk.Tk()
    recipe_controller = RecipeController(Database())
    calendar_controller = CalendarController(recipe_controller.db)
    app = MainWindow(root, recipe_controller, calendar_controller)
    app.pack(fill='both', expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()