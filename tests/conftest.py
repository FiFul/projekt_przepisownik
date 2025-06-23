import pytest
import json
from model.database import Database

@pytest.fixture
def temp_database(tmp_path):
    # Przygotuj osobne pliki
    recipe_file = tmp_path / "test_recipes.json"
    cook_history_file = tmp_path / "test_cook_history.json"

    # Stwórz puste pliki
    recipe_file.write_text("[]", encoding="utf-8")
    cook_history_file.write_text("[]", encoding="utf-8")

    # Zresetuj singleton i stwórz nową instancję
    Database._instance = None
    db = Database(str(recipe_file), str(cook_history_file))

    return db
