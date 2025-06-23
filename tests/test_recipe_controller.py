from controller.recipe_controller import RecipeController

def test_add_recipe():
    controller = RecipeController.instance()
    controller.add_recipe("Makaron", ["makaron", "sos"], "Gotuj i mieszaj", ["obiad"])

    recipes = controller.get_recipes()
    assert len(recipes) == 1
    assert recipes[0]["name"] == "Makaron"

def test_get_recipe_by_title():
    controller = RecipeController.instance()
    controller.add_recipe("Zupa", ["woda"], "Podgrzej", ["zupa"])

    recipe = controller.get_recipe_by_title("Zupa")
    assert recipe["ingredients"] == ["woda"]

def test_update_recipe():
    controller = RecipeController.instance()
    controller.add_recipe("Pizza", ["ciasto"], "Piec", ["włoskie"])
    original = controller.get_recipe_by_title("Pizza")

    controller.update_recipe(original, "Pizza Margherita", ["ciasto", "ser"], "Piec z serem", ["włoskie", "klasyk"])
    updated = controller.get_recipe_by_title("Pizza Margherita")

    assert updated["ingredients"] == ["ciasto", "ser"]
    assert "Pizza" not in [r["name"] for r in controller.get_recipes()]

def test_delete_recipe():
    controller = RecipeController.instance()
    controller.add_recipe("Pierogi", ["mąka"], "Gotuj", ["polskie"])
    recipe = controller.get_recipe_by_title("Pierogi")

    controller.delete_recipe(recipe)
    assert controller.get_recipe_by_title("Pierogi") is None

def test_filter_by_tag():
    controller = RecipeController.instance()
    controller.add_recipe("Naleśniki", ["jajko"], "Smaż", ["śniadanie"])
    results = controller.filter_recipes_by_tag("śniadanie")

    assert len(results) == 1
    assert results[0]["name"] == "Naleśniki"

def test_get_all_tags_and_ingredients():
    controller = RecipeController.instance()
    controller.add_recipe("Tost", ["chleb", "ser"], "Smaż", ["śniadanie"])
    controller.add_recipe("Sałatka", ["sałata", "ser"], "Wymieszaj", ["obiad"])

    tags = controller.get_all_tags()
    ingredients = controller.get_all_ingredients()

    assert "śniadanie" in tags and "obiad" in tags
    assert "ser" in ingredients and "chleb" in ingredients
