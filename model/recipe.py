from typing import List


class Recipe:
    def __init__(self, name: str, ingredients: List[str], instructions: str, tags: List[str], image_path: str = ''):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.tags = tags
        self.image_path = image_path

    def to_dict(self):
        return {
            'name': self.name,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'tags': self.tags,
            'image_path': self.image_path
        }

    @staticmethod
    def from_dict(data):
        return Recipe(
            name=data['name'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            tags=data['tags'],
            image_path=data.get('image_path', '')
        )
