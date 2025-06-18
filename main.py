from PyQt5.QtWidgets import QApplication
import sys

from controller.recipe_controller import RecipeController
from controller.calendar_controller import CalendarController
from model.database import Database
from view.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    recipe_controller = RecipeController(Database())
    calendar_controller = CalendarController(recipe_controller.db)

    window = MainWindow(recipe_controller, calendar_controller)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
