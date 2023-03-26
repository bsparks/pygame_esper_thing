import pygame


"""
This class provides a viewport into the game world. It allows us to zoom in and out of the game world.
"""


class Viewport:
    def __init__(self, width, height, scale=1, zoom=1):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.scale = scale
        self.zoom = zoom
        self.screen_surface = pygame.display.get_surface()
        self.scaled_surface = pygame.Surface(
            (self.width * self.scale, self.height * self.scale))
        self.zoomed_surface = None

    def update(self):
        pygame.transform.scale(self.screen_surface, (self.width *
                               self.scale, self.height * self.scale), self.scaled_surface)

    def get_render_surface(self):
        if self.zoom != 1:
            maintain_aspect_ratio = True
            zoomed_width = self.width * self.scale * self.zoom
            zoomed_height = self.height * self.scale * self.zoom
            if maintain_aspect_ratio:
                zoomed_height = int(zoomed_width / self.width * self.height)
            self.zoomed_surface = pygame.transform.scale(
                self.scaled_surface, (zoomed_width, zoomed_height))

        return self.zoomed_surface if self.zoomed_surface is not None else self.scaled_surface

    def blit(self, source, dest, area=None, special_flags=0):
        scaled_dest = (dest[0] * self.scale, dest[1] * self.scale)
        scaled_area = None if area is None else (
            area[0] * self.scale, area[1] * self.scale, area[2] * self.scale, area[3] * self.scale)
        self.scaled_surface.blit(
            source, scaled_dest, scaled_area, special_flags)

    def blits(self, sources_and_dests, special_flags=0):
        scaled_sources_and_dests = []
        for source, dest in sources_and_dests:
            scaled_dest = (dest[0] * self.scale, dest[1] * self.scale)
            scaled_sources_and_dests.append((source, scaled_dest))
        self.scaled_surface.blits(scaled_sources_and_dests, special_flags)

    def fill(self, color):
        self.scaled_surface.fill(color)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
