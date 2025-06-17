import tkinter as tk
from tkinter import simpledialog


class CalendarView(simpledialog.Dialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Kalendarz gotowania")

    def body(self, master):
        tk.Label(master, text="Nazwa przepisu do zapisania jako gotowany dziś:").pack()
        self.recipe_name_entry = tk.Entry(master)
        self.recipe_name_entry.pack()

        tk.Label(master, text="Historia gotowania przepisu:").pack(pady=(10,0))
        self.history_box = tk.Text(master, height=5, width=40)
        self.history_box.pack()
        return self.recipe_name_entry

    def apply(self):
        name = self.recipe_name_entry.get()
        self.controller.log_cook(name)
        history = self.controller.get_history(name)
        self.history_box.delete('1.0', tk.END)
        for entry in history:
            self.history_box.insert(tk.END, f"{entry.cook_date}\n")
