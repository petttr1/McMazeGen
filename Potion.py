from ChestItem import ChestItem
from random import sample, randint


class Potion(ChestItem):
    def __init__(self):
        super().__init__()
        self.potions = ['splash_potion']
        self.id = sample(self.potions, 1)[0]
        self.count = 1

    def enchant(self):
        enchantments = ['minecraft:healing', 'minecraft:fire_resistance',
                        'minecraft:night_vision', 'minecraft:strength', 'minecraft:long_weakness', 'minecraft:regeneration']
        chosen = sample(enchantments, 1)[0]
        self.tag = {'Potion': f"\'{chosen}\'"}

    def generate_item_string(self, slot):
        return super().generate_item_string(self, slot)
