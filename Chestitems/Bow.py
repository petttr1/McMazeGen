from .ChestItem import ChestItem
from random import sample, randint


class Bow(ChestItem):
    def __init__(self):
        super().__init__()
        self.id = 'bow'
        self.count = 1

    def enchant(self):
        enchantments = ['power', 'flame',
                        'unbreaking', 'mending', 'punch']
        chosen = sample(enchantments, randint(1, 3))
        self.tag = {'Enchantments': [{'id': c, 'lvl': 1} for c in chosen]}

    def generate_item_string(self, slot):
        return super().generate_item_string(self, slot)
