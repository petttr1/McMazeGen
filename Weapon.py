from ChestItem import ChestItem
from random import sample, randint


class Weapon(ChestItem):
    def __init__(self):
        super().__init__()
        self.weapons = ['iron_axe', 'golden_axe', 'stone_axe', 'bow']
        self.id = sample(self.weapons, 1)[0]
        self.count = 1

    def enchant(self):
        enchantments = ['looting', 'unbreaking',
                        'knockback', 'fire_aspect', 'sharpness', 'smite']
        chosen = sample(enchantments, randint(1, 3))
        self.tag = {'Enchantments': [{'id': c, 'lvl': 1} for c in chosen]}

    def generate_item_string(self, slot):
        return super().generate_item_string(self, slot)
