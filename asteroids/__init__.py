import random

from .components import *
from .physics import *
from .player import Controller as PlayerController


class RandomMovement(Processor):
    def process(self, dt, events):
        for ent, (pos, wiggle) in self.world.get_components(Position, Wiggle):
            magnitude = wiggle.magnitude
            pos.x += random.randint(-1, 1) * magnitude
            pos.y += random.randint(-1, 1) * magnitude
