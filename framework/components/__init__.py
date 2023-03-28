from dataclasses import dataclass as component
from dataclasses import field

import pygame
from yaml import YAMLObject

from .destroy import *


@component
class Position(YAMLObject):
    yaml_tag = "!Position"
    x: float = 0
    y: float = 0
    angle: float = 0


@component
class MountPoint(YAMLObject):
    yaml_tag = "!MountPoint"
    parent: int = -1
    x: float = 0
    y: float = 0


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
    max_speed: float = 100


@component
class AngularVelocity(YAMLObject):
    yaml_tag = "!AngularVelocity"
    speed: float = 0
    max_speed: float = 100


@component
class Text(YAMLObject):
    yaml_tag = "!Text"
    text: str = ""
    image: pygame.Surface = field(repr=False, default=None)
    font: str = "default"
    color: tuple = (255, 255, 255)
    size: int = 24
    anchor_x: float = 0.5
    anchor_y: float = 0.5
    depth: int = 0
    cache: bool = True

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']
        return state


@component
class Sprite(YAMLObject):
    yaml_tag = "!Sprite"
    image: pygame.Surface = field(repr=False, default=None)
    image_name: str = ""
    rect: pygame.Rect = None
    anchor_x: str = "center"
    anchor_y: str = "center"
    depth: int = 0
    enabled: bool = True

    # this is to prevent the image from being pickled (or trying and failing)
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']
        del state['rect']
        return state


@component
class Animation(YAMLObject):
    yaml_tag = "!Animation"
    name: str = ""
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


@component
class BackgroundImage(YAMLObject):
    yaml_tag = "!BackgroundImage"
    image: pygame.Surface = field(repr=False, default=None)
    image_name: str = ""
    rect: pygame.Rect = None
    anchor_x: float = 0.5
    anchor_y: float = 0.5
    depth: int = 0
    enabled: bool = True
    stretch: bool = False
    repeat_x: bool = False
    repeat_y: bool = False

    # this is to prevent the image from being pickled (or trying and failing)
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']
        del state['rect']
        return state


@component
class Grid(YAMLObject):
    yaml_tag = "!Grid"
    cell_size: int = 32
    num_cells_x: int = 0
    num_cells_y: int = 0
    cells: list = field(default_factory=list)


@component
class Audio(YAMLObject):
    yaml_tag = "!Audio"
    sound: pygame.mixer.Sound = field(repr=False, default=None)
    sound_name: str = ""
    volume: float = 1.0
    playing: bool = False
    loop: bool = False
    channel: int = 0
    play: bool = False
    stop: bool = False

    # this is to prevent the image from being pickled (or trying and failing)
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['sound']
        return state


@component
class Music(YAMLObject):
    yaml_tag = "!Music"
    music_name: str = ""
    volume: float = 1.0
    playing: bool = False
    loop: bool = False
    play: bool = False
    stop: bool = False


@component
class Score(YAMLObject):
    yaml_tag = "!Score"
    value: int = 0
    text_entity: int = -1
