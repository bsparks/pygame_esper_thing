from yaml import YAMLObject
from framework.components import component


@component
class Wiggle(YAMLObject):
    yaml_tag = "!Wiggle"
    magnitude: int = 1
