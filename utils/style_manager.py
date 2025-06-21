import os

from PyQt5.QtWidgets import QApplication


def update_stylesheets(stylesheet_name=None):
    style = ""
    paths = [os.path.join("assets", "styles", "style.qss")]
    if stylesheet_name:
        paths.append(os.path.join("assets", "styles", stylesheet_name+".qss"))
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            style += f.read() + "\n"

    QApplication.instance().setStyleSheet(style)