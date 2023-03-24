import pygame
from dataclasses import dataclass as component, field

from yaml import YAMLObject


@component
class Position(YAMLObject):
    yaml_tag = "!Position"
    x: int = 0
    y: int = 0


@component
class Sprite(YAMLObject):
    yaml_tag = "!Sprite"
    image: pygame.Surface = field(repr=False, default=None)
    image_name: str = ""
    rect: pygame.Rect = None
    anchor_x: str = "center"
    anchor_y: str = "center"
    depth: int = 0

    # this is to prevent the image from being pickled (or trying and failing)
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']
        del state['rect']
        return state


@component
class Agent(YAMLObject):
    yaml_tag = "!Agent"
    name: str = "Agent"


@component
class Player(YAMLObject):
    yaml_tag = "!Player"
    name: str = "Player"
