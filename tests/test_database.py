from model.database import Database

def test_add_and_load_recipe_from_file():
    db = Database.instance()
    recipe = {
        "name": "Sernik",
        "ingredients": ["ser", "jajka"],
        "instructions": "Piec",
        "tags": ["deser"],
        "image_path": ""
    }

    db.add_recipe(recipe)
    loaded = db.get_all_recipes()

    assert any(r["name"] == "Sernik" for r in loaded)

def test_delete_recipe_and_save():
    db = Database.instance()
    recipe = {
        "name": "Kopytka",
        "ingredients": ["ziemniaki"],
        "instructions": "Gotuj",
        "tags": ["obiad"],
        "image_path": ""
    }

    db.add_recipe(recipe)
    db.delete_recipe(recipe)

    assert not any(r["name"] == "Kopytka" for r in db.get_all_recipes())

def test_clear_cook_history():
    db = Database.instance()
    recipe = {
        "name": "Barszcz",
        "ingredients": ["buraki"],
        "instructions": "Gotuj",
        "tags": ["zupa"],
        "image_path": "",
        "cook_history": ["2024-01-01", "2024-02-02"]
    }

    db.add_recipe(recipe)
    db.clear_cook_history(recipe)

    updated = db.get_recipe_by_title("Barszcz")
    assert updated["cook_history"] == []
