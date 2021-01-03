from ChestItem import ChestItem
from random import sample, randint


class Armor(ChestItem):
    def __init__(self):
        super().__init__()
        self.armors = ['iron_chestplate', 'golden_chestplate', 'iron_boots', 'golden_boots',
                       'iron_helmet', 'golden_helmet', 'iron_leggings', 'golden_leggings', 'shield']
        self.id = sample(self.armors, 1)[0]
        self.count = 1

    def enchant(self):
        enchantments = ['blast_protection', 'unbreaking',
                        'protection', 'projectile_protection', 'thorns']
        chosen = sample(enchantments, randint(1, 3))
        self.tag = {'Enchantments': [{'id': c, 'lvl': 1} for c in chosen]}

    def generate_item_string(self, slot):
        return super().generate_item_string(self, slot)
