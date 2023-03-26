import math
import pygame
from framework.ecs import Processor
from framework.components import Position, Scale, Text


class TextRenderer(Processor):
    def __init__(self, screen, assets):
        super().__init__()
        self.screen = screen
        self.assets = assets
        self.add_listener("component_added", self.on_component_added)
        
    def on_component_added(self, entity, component):
        if isinstance(component, Text):
            # print("text component added", entity, component)
            if component.image is None:
                component.image = self.assets.create_text(
                    component.text, component.font, component.size, component.color)

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
        for ent, (pos, text) in self.world.get_components(Position, Text):
            image = text.image
            if image is None:
                print("text image is None", ent, text)
                continue

            scale = self.world.try_component(ent, Scale)
            if scale is not None:
                # this might be very inefficient, I'm not sure... but it works
                image = pygame.transform.scale_by(image, (scale.x, scale.y))
            if pos.angle != 0:
                image = self.rotate_image(image, pos.angle)
            # offset the text's rect based on the anchor
            px, py = pos.x, pos.y
            width, height = text.image.get_size()
            if text.anchor_x == "center":
                px -= width // 2
            elif text.anchor_x == "right":
                px -= width
            if text.anchor_y == "center":
                py -= height // 2
            elif text.anchor_y == "bottom":
                py -= height
            blits.append((image, (px, py), text.depth))
        # sort by depth
        blits.sort(key=lambda x: x[2])
        # map just the blits
        blits = map(lambda x: x[:2], blits)
        self.screen.blits(blits)
