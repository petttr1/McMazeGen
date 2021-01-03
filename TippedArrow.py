from ChestItem import ChestItem
from random import sample, randint


class TippedArrow(ChestItem):
    def __init__(self):
        super().__init__()
        self.potions = ['tipped_arrow']
        self.id = sample(self.potions, 1)[0]
        self.count = randint(5, 15)

    def enchant(self):
        enchantments = ['minecraft:harming', 'minecraft:poison',
                        'minecraft:slowness', 'minecraft:weakness']
        chosen = sample(enchantments, 1)[0]
        self.tag = {'Potion': f"\'{chosen}\'"}

    def generate_item_string(self, slot):
        return super().generate_item_string(self, slot)
