from .ChestItem import ChestItem
from random import sample, randint


class Consumable(ChestItem):
    def __init__(self):
        super().__init__()
        self.consumables = [
            'cooked_beef', 'arrow', 'bread'
        ]
        self.id = sample(self.consumables, 1)[0]
        self.count = randint(1, 10)

    def enchant(self):
        # enchantments = ['looting', 'unbreaking',
        #                 'knockback', 'fire_aspect', 'sharpness', 'smite']
        # chosen = sample(enchantments, randint(1, 3))
        # self.tag = {'Enchantments': [{'id': c, 'lvl': 1} for c in chosen]}
        self.tag = {}

    def generate_item_string(self, slot):
        return super().generate_item_string(self, slot)
