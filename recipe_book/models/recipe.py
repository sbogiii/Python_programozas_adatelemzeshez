class Recipe:
    def __init__(self, name, category, ingredients, instructions):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.instructions = instructions

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "ingredients": self.ingredients,
            "steps": self.steps
        }
    
    def from_dict(data):
        return Recipe(
            name=data["name"],
            category=data["category"],
            ingredients=data["ingredients"],
            instructions=data["instructions"]
        )