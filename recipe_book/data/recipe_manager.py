import json
from pathlib import Path
from models.recipe import Recipe

filepath = Path("recipes.json")
recipes = []

def load_recipes():
    """Betölti a recepteket a recipes.json fájlból a recipes listába."""
    global recipes
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                recipes.append(Recipe.from_dict(item))

def save_recipes():
    """Elmenti a recipes lista aktuális állapotát a recipes.json fájlba."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump([recipe.to_dict() for recipe in recipes], file, indent=2, ensure_ascii=False)

def add_recipe(recipe):
    """Hozzáad egy új receptet a recipes listához. Hozzáadás előtt ellenőrzi, hogy az adott recept létezik-e már.
    Ha igen, hamis értékkel tér vissza, nem történik változtatás, ha nem, hozzáadja a receptet a listához, majd a save_recipes függvény meghívásával elmenti a recipes.json-ba."""
    for r in recipes:
        if r.name.lower() == recipe.name.lower():
            return False
    recipes.append(recipe)
    save_recipes()
    return True

def delete_recipe(recipe_name):
    """Ellenőrzi, hogy egy recept létezik-e, ha igen kitörli az adott receptet a listából, 
    majd a save_recipes függvény meghívásával elmenti a változtatásokat a recipes.json fájlba. Ha nem, hamis értékkel tér vissza."""
    for r in recipes:
        if r.name.lower() == recipe_name.lower():
            recipes.remove(r)
            save_recipes()
            return True
    return False 

def search_by_name(name):
    """Receptnév szerint keres a receptek között, és azokat adja vissza amelyek egyeznek a kereséssel (nem case-sensitive)."""
    return [r for r in recipes if name.lower() in r.name.lower()]

def filter_by_category(category):
    """Kategória szerint keres a receptek között, és azokat adja vissza amelyek egyeznek a kereséssel (nem case-sensitive)."""
    return [r for r in recipes if r.category.lower() == category.lower()]

def filter_by_ingredient(ingredients):
    """Összetevők szerint keres a receptek között, majd mindet kilistázza, amelyik tartalmazza az összes kiválasztott összetevőt."""
    result = []
    for r in recipes:
        if all(ing.lower() in [i.lower() for i in r.ingredients] for ing in ingredients):
            result.append(r)
    return result