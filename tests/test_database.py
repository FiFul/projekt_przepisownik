from model.database import Database

def test_add_and_get_recipe(temp_database):
    db = temp_database
    recipe = {
        "name": "Testowy Przepis",
        "ingredients": ["test"],
        "instructions": "Gotuj",
        "tags": ["test"],
        "image_path": ""
    }

    db.add_recipe(recipe)
    result = db.get_recipe_by_title("Testowy Przepis")

    assert result["name"] == "Testowy Przepis"
    assert result["ingredients"] == ["test"]
    assert result["instructions"] == "Gotuj"
    assert result["tags"] == ["test"]


def test_update_recipe(temp_database):
    db = temp_database
    original = {
        "name": "Stary Przepis",
        "ingredients": ["a"],
        "instructions": "a",
        "tags": ["a"],
        "image_path": ""
    }
    db.add_recipe(original)
    recipe = db.get_recipe_by_title("Stary Przepis")

    db.update_recipe(recipe, "Nowy Przepis", ["b", "c"], "Nowe instrukcje", ["b"], "path.jpg")
    updated = db.get_recipe_by_title("Nowy Przepis")

    assert updated["name"] == "Nowy Przepis"
    assert updated["ingredients"] == ["b", "c"]
    assert updated["instructions"] == "Nowe instrukcje"
    assert updated["tags"] == ["b"]
    assert updated["image_path"] == "path.jpg"


def test_delete_recipe(temp_database):
    db = temp_database
    recipe = {
        "name": "Do Usunięcia",
        "ingredients": ["x"],
        "instructions": "x",
        "tags": ["x"],
        "image_path": ""
    }
    db.add_recipe(recipe)
    to_delete = db.get_recipe_by_title("Do Usunięcia")
    db.delete_recipe(to_delete)

    assert db.get_recipe_by_title("Do Usunięcia") is None


def test_filter_by_tag(temp_database):
    db = temp_database
    db.add_recipe({"name": "Zupa", "ingredients": [], "instructions": "", "tags": ["obiad"], "image_path": ""})
    db.add_recipe({"name": "Ciasto", "ingredients": [], "instructions": "", "tags": ["deser"], "image_path": ""})

    filtered = db.apply_filters("", "deser")
    assert len(filtered) == 1
    assert filtered[0]["name"] == "Ciasto"


def test_cook_history_logging_and_retrieval(temp_database):
    db = temp_database
    recipe_name = "Gotowane"
    db.add_recipe({"name": recipe_name, "ingredients": [], "instructions": "", "tags": [], "image_path": ""})

    from datetime import date
    today = date.today()
    db.log_cook_date(recipe_name, today)

    history = db.get_cook_history(recipe_name)
    assert len(history) == 1
    assert history[0].recipe_name == recipe_name
    assert history[0].cook_date == today


def test_clear_cook_history(temp_database):
    db = temp_database
    recipe_name = "Z historią"
    db.add_recipe({"name": recipe_name, "ingredients": [], "instructions": "", "tags": [], "image_path": ""})

    from datetime import date
    db.log_cook_date(recipe_name, date.today())
    assert len(db.get_cook_history(recipe_name)) > 0

    db.clear_cook_history(recipe_name)
    assert db.get_cook_history(recipe_name) == []
