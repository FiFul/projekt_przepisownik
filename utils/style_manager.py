import os
import sys

from PyQt5.QtWidgets import QApplication

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def update_stylesheets(stylesheet_name=None):
    style = ""
    paths = [resource_path(os.path.join("assets", "styles", "style.qss"))]
    if stylesheet_name:
        paths.append(resource_path(os.path.join("assets", "styles", f"{stylesheet_name}.qss")))

    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                style += f.read() + "\n"
        except FileNotFoundError:
            print(f"Nie znaleziono pliku stylu: {path}")

    QApplication.instance().setStyleSheet(style)