from .SpawnerMob import SpawnerMob
from random import randint


class Spawner:
    def __init__(self):
        self.spawn_range = randint(5, 20)
        self.spawn_count = randint(3, 10)
        self.max_nearby = randint(5, 10)
        self.player_range = randint(10, 25)
        self.delay = 299

    def generate_spawner_string(self, mob):
        return {'SpawnData': mob.generate_mob_string(),
                'Delay': self.delay,
                'SpawnRange': self.spawn_range,
                'SpawnCount': self.spawn_count,
                'MaxNearbyEntities': self.max_nearby,
                'RequiredPlayerRange': self.player_range
                }
