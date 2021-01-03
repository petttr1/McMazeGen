from abc import ABC, abstractmethod


class SpawnerMob(ABC):
    def __init__(self):
        super().__init__()

    def generate_mob_string(self, mob):
        return {'id': mob.id}
