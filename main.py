import os
import random
import pygame
import esper
import yaml
from dataclasses import dataclass as component
from framework.asset_cache import AssetCache
from components import Wiggle
from framework.components import Position, Sprite, Agent
from framework.systems import InputManager, SpriteRenderer


class RandomMovement(esper.Processor):
    def process(self, dt, events):
        for ent, (pos, wiggle) in self.world.get_components(Position, Wiggle):
            magnitude = wiggle.magnitude
            pos.x += random.randint(-1, 1) * magnitude
            pos.y += random.randint(-1, 1) * magnitude

# note to self, a system does not need to actually query components, it could just be something that
# runs every frame, like a timer or input manager


class Controller(esper.Processor):
    def __init__(self):
        super().__init__()
        self.input = None

    def toggle_agent_wiggle(self):
        for ent, (agent) in self.world.get_components(Agent):
            if self.world.has_components(ent, Wiggle):
                self.world.remove_component(ent, Wiggle)
            else:
                self.world.add_component(ent, Wiggle(magnitude=5))

    def process(self, dt, events):
        if self.input is None:
            self.input = self.world.get_processor(InputManager)
        if self.input is not None:
            if self.input.key_pressed(pygame.K_SPACE):
                self.toggle_agent_wiggle()
            if self.input.key_pressed(pygame.K_F5):
                ents = self.world._entities
                print(f"Entities: {ents}")
                yaml.dump(ents, open("save.yaml", "w"))


assets = AssetCache()


def init(screen, world):
    skull_image = assets.load_image("red_skull.png")
    blue_skull_image = assets.load_image("blue_skull.png")

    world.add_processor(InputManager())
    world.add_processor(SpriteRenderer(screen))
    world.add_processor(Controller())
    world.add_processor(RandomMovement())
    
    # check if we have a saved game
    if os.path.exists("save.yaml"):
        ents = yaml.load(open("save.yaml", "r"), Loader=yaml.FullLoader)
        print(f"Loaded entities: {ents}")
        for ent, comps in ents.items():
            print(f"Adding entity {ent} with components {comps}")
            entity = world.create_entity()
            for comp in comps.values():
                # if the component is a sprite, we need to load the image from the asset cache
                if isinstance(comp, Sprite):
                    comp.image = assets.load_image(comp.image_name)
                    comp.rect = comp.image.get_rect()
                world.add_component(entity, comp)
    else:
        skull = world.create_entity()
        world.add_component(skull, Position(400, 300))
        world.add_component(skull, Sprite(image_name="red_skull.png",
                                        image=skull_image, rect=skull_image.get_rect()))
        world.add_component(skull, Agent(name="Skull"))

        blue_skull = world.create_entity()
        world.add_component(blue_skull, Position(408, 300))
        world.add_component(blue_skull, Sprite(image_name="blue_skull.png",
                                            image=blue_skull_image, rect=blue_skull_image.get_rect()))
        world.add_component(blue_skull, Agent(name="Blue Skull"))


def start():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("ECS Game Test")
    world = esper.World()
    clock = pygame.time.Clock()
    init(screen, world)

    running = True
    while running:
        dt = clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))
        world.process(dt, events)
        pygame.display.flip()


if __name__ == "__main__":
    start()
    pygame.quit()
