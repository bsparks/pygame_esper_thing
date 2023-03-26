import math
import esper
import pygame
from framework.components import Position, Scale, Sprite


class SpriteRenderer(esper.Processor):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        
    def rotate_image(self, image, angle):
        # Calculate the center of the image
        center = image.get_rect().center
        
        # Rotate the image
        rotated_image = pygame.transform.rotate(image, angle)
        
        # Calculate the new rect of the rotated image
        rect = rotated_image.get_rect(center=center)
        
        # Create a new surface and blit the rotated image onto it
        new_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        new_surface.blit(rotated_image, rect)
        
        return new_surface

    def process(self, dt, events):
        blits = []
        for ent, (pos, sprite) in self.world.get_components(Position, Sprite):
            image = sprite.image
            scale = self.world.try_component(ent, Scale)
            if scale is not None:
                # this might be very inefficient, I'm not sure... but it works
                image = pygame.transform.scale_by(image, (scale.x, scale.y))
            if pos.angle != 0:
                image = self.rotate_image(image, pos.angle)
            # offset the sprite's rect based on the anchor
            px, py = pos.x, pos.y
            width, height = sprite.image.get_size()
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
