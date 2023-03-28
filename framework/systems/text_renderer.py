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
        self.texts = {}

    def on_component_added(self, entity, component):
        if isinstance(component, Text):
            self.create_text_image(entity, component)

    def create_text_image(self, entity, component):
        # print("text component added", entity, component)
        self.texts[entity] = component.text
        component.image = self.assets.create_text(
            component.text, component.font, component.size, component.color, cache=component.cache)
        return component.image

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
            text_changed = self.texts.get(ent) != text.text
            if image is None or text_changed:
                print(f"TextRenderer: {ent} {pos} {text} {text_changed}")
                image = self.create_text_image(ent, text)

            scale = self.world.try_component(ent, Scale)
            if scale is not None:
                # this might be very inefficient, I'm not sure... but it works
                image = pygame.transform.scale_by(image, (scale.x, scale.y))
            if pos.angle != 0:
                image = self.rotate_image(image, pos.angle)

            # offset the text's rect based on the anchor
            px, py = pos.x, pos.y
            width, height = text.image.get_size()
            px -= width * text.anchor_x
            py -= height * text.anchor_y

            blits.append((image, (px, py), text.depth))
        # sort by depth
        blits.sort(key=lambda x: x[2])
        # map just the blits
        blits = map(lambda x: x[:2], blits)
        self.screen.blits(blits)
