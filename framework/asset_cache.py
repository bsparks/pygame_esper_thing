import os
import pygame
import yaml

class AnimationData:
    def __init__(self, data):
        self.name = data['name']
        self.image_name = data['image_name']
        self.frames = data['frames']
        self.speed = data['speed']
        self.loop = data['loop']
        self.size = data['size']

class AssetCache:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music = None
        self.fonts = {}
        self.texts = {}
        self.animations = {}
        self.basePath = "./assets"
        
    def set_base_path(self, path):
        self.basePath = path
        
    def load_image(self, filename):
        if filename not in self.images:
            path = os.path.join(f"{self.basePath}/images/", filename)
            self.images[filename] = pygame.image.load(path).convert_alpha()
        return self.images[filename]
    
    def load_animation(self, filename):
        if filename not in self.animations:
            path = os.path.join(f"{self.basePath}/animations/", filename)
            # an animation is stored as a yaml file
            data = yaml.load(open(path, "r"), Loader=yaml.FullLoader)
            self.animations[filename] = AnimationData(data)
        return self.animations[filename]
    
    def create_animation(self, name, image_name, size, frames, speed, loop):
        anim = AnimationData({
            "name": name,
            "image_name": image_name,
            "size": size,
            "frames": frames,
            "speed": speed,
            "loop": loop
        })
        self.animations[name] = anim
        return anim
    
    def save_animation(self, animation, filename):
        path = os.path.join(f"{self.basePath}/animations/", filename)
        data = {
            "name": animation.name,
            "image_name": animation.image_name,
            "size": animation.size,
            "frames": animation.frames,
            "speed": animation.speed,
            "loop": animation.loop
        }
        yaml.dump(data, open(path, "w"))
    
    def load_sound(self, filename):
        if filename not in self.sounds:
            path = os.path.join(f"{self.basePath}/audio/", filename)
            self.sounds[filename] = pygame.mixer.Sound(path)
        return self.sounds[filename]
    
    def load_music(self, filename):
        if self.music is None:
            path = os.path.join(f"{self.basePath}/audio/", filename)
            self.music = pygame.mixer.music.load(path)
        return self.music
    
    def create_font(self, font = "Arial", size = 30):
        if font not in self.fonts:
            if font.endswith(".ttf"):
                path = os.path.join(f"{self.basePath}/fonts/", font)
                self.fonts[font] = pygame.font.Font(path, size)
            else:
                self.fonts[font] = pygame.font.SysFont(font, size)

        return self.fonts[font]