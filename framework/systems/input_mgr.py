
import pygame

from framework.ecs import Processor


class InputManager(Processor):
    def __init__(self):
        super().__init__()
        self.mouse = {"x": 0, "y": 0, "buttons": [False, False, False]}
        self.last_mouse = {"x": 0, "y": 0, "buttons": [False, False, False]}
        self.keyboard = {}
        self.last_keyboard = {}

    def key_pressed(self, key):
        return self.keyboard.get(key, False) and not self.last_keyboard.get(key, False)

    def key_down(self, key):
        return self.keyboard.get(key, False)

    def key_up(self, key):
        return not self.keyboard.get(key, False)

    def mouse_pressed(self, button):
        return self.mouse["buttons"][button - 1] and not self.last_mouse["buttons"][button - 1]

    def mouse_down(self, button):
        return self.mouse["buttons"][button - 1]

    def mouse_up(self, button):
        return not self.mouse["buttons"][button - 1]

    def mouse_delta(self):
        return (self.mouse["x"] - self.last_mouse["x"], self.mouse["y"] - self.last_mouse["y"])

    def mouse_position(self):
        return (self.mouse["x"], self.mouse["y"])

    def process(self, dt, events):
        self.last_keyboard = self.keyboard.copy()
        self.last_mouse = self.mouse.copy()
        # check for keyboard and mouse input
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.mouse["x"], self.mouse["y"] = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse["buttons"][event.button - 1] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse["buttons"][event.button - 1] = False
            elif event.type == pygame.KEYDOWN:
                self.keyboard[event.key] = True
            elif event.type == pygame.KEYUP:
                self.keyboard[event.key] = False
