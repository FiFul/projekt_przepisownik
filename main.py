from PyQt5.QtWidgets import QApplication
import sys

from view.main_window import MainWindow
from controller.calendar_controller import CalendarController
from controller.recipe_controller import RecipeController
from model.database import Database

def main():
    #SINGLETONY
    database = Database.instance()
    calendar_controller = CalendarController.instance()
    recipe_controller = RecipeController.instance()

    app = QApplication(sys.argv)

    with open("assets/style.qss", "r") as file:
        style = file.read()
        app.setStyleSheet(style)

    window = MainWindow()
    window.showFullScreen()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
