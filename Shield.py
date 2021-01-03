from ChestItem import ChestItem
from random import sample, randint


class Shield(ChestItem):
    def __init__(self):
        super().__init__()
        self.id = 'shield'
        self.count = 1

    def enchant(self):
        enchantments = ['unbreaking', 'mending']
        chosen = sample(enchantments, randint(1, 2))
        self.tag = {'Enchantments': [{'id': c, 'lvl': 1} for c in chosen]}

    def generate_item_string(self, slot):
        return super().generate_item_string(self, slot)
