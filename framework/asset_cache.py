import os
import pygame

class AssetCache:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music = None
        self.fonts = {}
        self.texts = {}
        self.basePath = "./assets"
        
    def set_base_path(self, path):
        self.basePath = path
        
    def load_image(self, filename):
        if filename not in self.images:
            path = os.path.join(f"{self.basePath}/images/", filename)
            self.images[filename] = pygame.image.load(path).convert_alpha()
        return self.images[filename]
    
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