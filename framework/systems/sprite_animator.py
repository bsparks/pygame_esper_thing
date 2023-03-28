from framework.ecs import Processor
from framework.components import Animation, Sprite


class SpriteAnimator(Processor):
    def __init__(self, screen, assets) -> None:
        super().__init__()
        self.screen = screen
        self.assets = assets
        self.add_listener("component_added", self.on_component_added)

    @staticmethod
    def create_frames(image, frames, size):
        frames = [image.subsurface((i * size, 0, size, size)) for i in frames]
        return frames

    def on_component_added(self, entity, component):
        if isinstance(component, Animation):
            self.load_animation(entity, component)

    def load_animation(self, entity, anim):
        if anim.name != "":
            data = self.assets.load_animation(f"{anim.name}.yaml")
            anim.speed = data.speed
            anim.loop = data.loop
            anim.frames = SpriteAnimator.create_frames(
                self.assets.load_image(data.image_name), data.frames, data.size)

    def process(self, dt, events):
        for ent, (sprite, anim) in self.world.get_components(Sprite, Animation):
            if anim.playing:
                anim.time += dt
                if anim.time >= 1 / anim.speed:
                    anim.time = 0
                    anim.frame += 1
                    if anim.frame >= len(anim.frames):
                        if anim.loop:
                            anim.frame = 0
                        else:
                            anim.playing = False
                            anim.frame = len(anim.frames) - 1
                    # only update the image if we are playing
                    sprite.image = anim.frames[anim.frame]
