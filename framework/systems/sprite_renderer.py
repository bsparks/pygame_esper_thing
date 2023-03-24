import esper
from framework.components import Position, Sprite


class SpriteRenderer(esper.Processor):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

    def process(self, dt, events):
        blits = []
        for ent, (pos, sprite) in self.world.get_components(Position, Sprite):
            # offset the sprite's rect based on the anchor
            px, py = pos.x, pos.y
            width, height = sprite.image.get_size()
            if sprite.anchor_x == "center":
                px -= width // 2
            elif sprite.anchor_x == "right":
                px -= width
            if sprite.anchor_y == "center":
                py -= height // 2
            elif sprite.anchor_y == "bottom":
                py -= height
            blits.append((sprite.image, (px, py), sprite.depth))
        # sort by depth
        blits.sort(key=lambda x: x[2])
        # map just the blits
        blits = map(lambda x: x[:2], blits)
        self.screen.blits(blits)
