from yaml import YAMLObject
from dataclasses import dataclass as component


@component
class DestroyAfter(YAMLObject):
    yaml_tag = "!DestroyAfter"
    time: float = 0
    after: float = 0


@component
class DestroyOnCollision(YAMLObject):
    yaml_tag = "!DestroyOnCollision"
    owner: int = -1


@component
class DestroyOnOutOfBounds(YAMLObject):
    yaml_tag = "!DestroyOnOutOfBounds"
