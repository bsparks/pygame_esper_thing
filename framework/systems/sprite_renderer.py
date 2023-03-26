import math
import pygame
from framework.components import Position, Scale, Sprite
from framework.ecs import Processor


class SpriteRenderer(Processor):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

    def rotate_image(self, image, angle, anchor=(0, 0)):
        # Calculate the center of the image based on the anchor
        rect = image.get_rect()
        center = (anchor[0] * rect.width, anchor[1] * rect.height)

        # Rotate the image
        rotated_image = pygame.transform.rotate(image, angle)

        # Calculate the new rect of the rotated image
        rect = rotated_image.get_rect(center=center)

        # Create a new surface and blit the rotated image onto it
        new_surface = pygame.Surface(
            rect.size, pygame.SRCALPHA).convert_alpha()
        new_surface.blit(rotated_image, rect)

        return new_surface

    def process(self, dt, events):
        blits = []
        for ent, (pos, sprite) in self.world.get_components(Position, Sprite):
            if not sprite.enabled:
                continue

            image = sprite.image
            scale = self.world.try_component(ent, Scale)
            if scale is not None:
                # this might be very inefficient, I'm not sure... but it works
                image = pygame.transform.scale_by(image, (scale.x, scale.y))
                image.convert_alpha()
            if pos.angle != 0:
                anchor_x = 0 if sprite.anchor_x == "left" else 0.5 if sprite.anchor_x == "center" else 1
                anchor_y = 0 if sprite.anchor_y == "top" else 0.5 if sprite.anchor_y == "center" else 1
                image = self.rotate_image(
                    image, pos.angle, (anchor_x, anchor_y))
            sprite.rect = image.get_rect()
            # offset the sprite's rect based on the anchor
            px, py = pos.x, pos.y
            width, height = sprite.image.get_size()
            # left, top is default
            if sprite.anchor_x == "center":
                px -= width // 2
            elif sprite.anchor_x == "right":
                px -= width
            if sprite.anchor_y == "center":
                py -= height // 2
            elif sprite.anchor_y == "bottom":
                py -= height
            blits.append((image, (px, py), sprite.depth))
        # sort by depth
        blits.sort(key=lambda x: x[2])
        # map just the blits
        blits = map(lambda x: x[:2], blits)
        self.screen.blits(blits)
