import esper

from framework.components import Animation, Sprite


class SpriteAnimator(esper.Processor):
    @staticmethod
    def create_frames(image, frames, size):
        frames = [image.subsurface((i * size, 0, size, size)) for i in frames]
        return frames

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