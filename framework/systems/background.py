import math

import pygame
from framework.components import BackgroundImage, Position
from framework.ecs import Processor


class BackgroundSystem(Processor):
    def __init__(self, screen, assets):
        super().__init__()
        self.screen = screen
        self.assets = assets
        self.add_listener("component_added", self.on_component_added)

    def on_component_added(self, entity, component):
        if isinstance(component, BackgroundImage):
            if component.image is None:
                component.image = self.assets.load_image(component.image_name)

    def process(self, dt, events):
        blits = []
        for ent, (pos, bg) in self.world.get_components(Position, BackgroundImage):
            repeat = (bg.repeat_x, bg.repeat_y)
            stretch = bg.stretch
            anchor = (bg.anchor_x, bg.anchor_y)
            image = bg.image
            img_width, img_height = bg.image.get_size()
            px, py = pos.x, pos.y
            offset_x = img_width * anchor[0]
            offset_y = img_height * anchor[1]
            px -= offset_x
            py -= offset_y
            
            # for repeat we will create a bigger surface and blit the image onto it
            if repeat[0] or repeat[1]:
                repeat_x = 0
                repeat_y = 0
                if repeat[0]:
                    # take the width of the image + px and subtract from the screen width to see how much is left to fill
                    width_remain = self.screen.get_width() - (img_width + px)
                    # divide that by the width of the image to see how many times we need to repeat it, round up to the nearest int
                    repeat_x = math.ceil(width_remain / img_width)
                if repeat[1]:
                    # take the height of the image + py and subtract from the screen height to see how much is left to fill
                    height_remain = self.screen.get_height() - (img_height + py)
                    # divide that by the height of the image to see how many times we need to repeat it, round up to the nearest int
                    repeat_y = math.ceil(height_remain / img_height)
                # create a new surface that is the size of the screen
                repeat_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
                for x in range(repeat_x + 1):
                    for y in range(repeat_y + 1):
                        repeat_surface.blit(image, (px + x * img_width, py + y * img_height))
                image = repeat_surface

            blits.append((image, (px, py), bg.depth))

        # sort by depth
        blits.sort(key=lambda x: x[2])
        # map just the blits
        blits = map(lambda x: x[:2], blits)
        self.screen.blits(blits)
