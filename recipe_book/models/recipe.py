class Recipe:
    def __init__(self, name, category, ingredients, instructions):
        """Létrehoz egy új Recipe példányt a megadott adatokkal."""
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.instructions = instructions

    def to_dict(self):
        """A receptet szótárrá alakítja, hogy json-ba menthető legyen."""
        return {
            "name": self.name,
            "category": self.category,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }
    
    def from_dict(data):
        """A szótárból egy Recipe példányt hoz létre."""
        return Recipe(
            name=data["name"],
            category=data["category"],
            ingredients=data["ingredients"],
            instructions=data["instructions"]
        )