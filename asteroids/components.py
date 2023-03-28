from yaml import YAMLObject
from framework.components import component

# these are the game specific components

@component
class Thruster(YAMLObject):
    yaml_tag = "!Thruster"
    owner: int = -1
    enabled: bool = True
    power: float = 1
    angle: float = 0

@component
class Wiggle(YAMLObject):
    yaml_tag = "!Wiggle"
    magnitude: int = 1
