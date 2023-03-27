import pygame
from framework.components import Audio, Music
from framework.ecs import Processor


class AudioSystem(Processor):
    def __init__(self, assets):
        super().__init__()
        self.assets = assets

    def on_component_added(self, entity, component):
        if isinstance(component, Audio):
            if component.sound is None:
                component.sound = self.assets.load_sound(component.sound_name)

    def process(self, world, dt):
        for ent, (audio) in self.world.get_components(Audio):
            if audio.play and not audio.playing:
                audio.play = False
                audio.playing = True
                audio.sound.play()

            if audio.stop and audio.playing:
                audio.stop = False
                audio.playing = False
                audio.sound.stop()

        for ent, (music) in self.world.get_components(Music):
            # TODO: what happens if there is more than one music entity?
            if music.play and not music.playing:
                music.play = False
                music.playing = True
                self.assets.load_music(music.music_name)
                pygame.mixer.music.play(-1 if music.loop else 0)
                pygame.mixer.music.set_volume(music.volume)
                
            if music.stop and music.playing:
                music.stop = False
                music.playing = False
                pygame.mixer.music.stop()
