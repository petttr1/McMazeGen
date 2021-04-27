from .SpawnerMob import SpawnerMob
from random import sample, randint


class EquippableMob(SpawnerMob):
    def __init__(self):
        super().__init__()
        types = ['zombie', 'skeleton']
        self.id = sample(types, 1)[0]

    def generate_mob_string(self):
        string = super().generate_mob_string(self)
        return string
