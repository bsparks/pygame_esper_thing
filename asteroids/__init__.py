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


class DestroySystem(Processor):
    def process(self, dt, events):
        for ent, (pos, destroy) in self.world.get_components(Position, DestroyOnOutOfBounds):
            if pos.x < 0 or pos.x > self.screen.get_width() or pos.y < 0 or pos.y > self.screen.get_height():
                self.world.delete_entity(ent)

        for ent, (destroy) in self.world.get_component(DestroyAfter):
            destroy.time += dt
            if destroy.time >= destroy.after:
                self.world.delete_entity(ent)
