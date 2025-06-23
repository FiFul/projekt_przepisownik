import os
import shutil
from model.database import Database

TEST_DATA_PATH = "tests/test_data/recipes.json"

@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path):
    test_json_path = tmp_path / "recipes.json"
    os.makedirs(tmp_path, exist_ok=True)
    test_json_path.write_text("[]")

    # Nadpisujemy ścieżkę pliku JSON w Database
    Database._instance = None
    db = Database.instance()
    db._data_file = str(test_json_path)
    db._recipes = []
    yield
    Database._instance = None  # Reset DB singleton po teście
