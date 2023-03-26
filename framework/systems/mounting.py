import math

from pygame import Vector2
from framework.components import Position, MountPoint, Sprite
from framework.ecs import Processor


class MountingSystem(Processor):
    def process(self, dt, events):
        for ent, (pos, mount) in self.world.get_components(Position, MountPoint):
            if mount.parent != -1:
                if self.world.entity_exists(mount.parent):
                    parent_pos = self.world.try_component(
                        mount.parent, Position)
                    if parent_pos is not None:
                        # Calculate the position of the child entity relative to the parent entity's position
                        relative_pos = Vector2(mount.x, mount.y)
                        # Rotate the relative position vector around the parent entity's position by the parent entity's angle
                        relative_pos.rotate_ip(-parent_pos.angle)
                        pos.angle = parent_pos.angle
                        # Set the position of the child entity based on the parent position and the rotated relative position
                        pos.x = relative_pos.x + parent_pos.x
                        pos.y = relative_pos.y + parent_pos.y
