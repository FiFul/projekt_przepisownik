import os


def load_stylesheets(folder_path="assets/styles"):
    style = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".qss"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, "r", encoding="utf-8") as f:
                style += f.read() + "\n"
    return style
