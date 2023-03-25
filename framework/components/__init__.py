import pygame
from dataclasses import dataclass as component, field

from yaml import YAMLObject


@component
class Position(YAMLObject):
    yaml_tag = "!Position"
    x: float = 0
    y: float = 0
    angle: float = 0


@component
class Scale(YAMLObject):
    yaml_tag = "!Scale"
    x: float = 1
    y: float = 1


@component
class Velocity(YAMLObject):
    yaml_tag = "!Velocity"
    x: float = 0
    y: float = 0


@component
class Text(YAMLObject):
    yaml_tag = "!Text"
    text: str = ""
    font: str = "default"
    color: str = "white"
    size: int = 24
    anchor_x: str = "center"
    anchor_y: str = "center"
    depth: int = 0


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
class Animation(YAMLObject):
    yaml_tag = "!Animation"
    frames: list = field(default_factory=list)
    speed: float = 0.1
    frame: int = 0
    time: float = 0
    loop: bool = True
    playing: bool = False

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['frames']
        return state


@component
class Agent(YAMLObject):
    yaml_tag = "!Agent"
    name: str = "Agent"


@component
class Player(YAMLObject):
    yaml_tag = "!Player"
    name: str = "Player"
