import math
import os
import random
import pygame
import esper
import yaml
from dataclasses import dataclass as component
from framework.viewport import Viewport
from framework.asset_cache import AssetCache
from components import Wiggle
from framework.components import Animation, Player, Position, Sprite, Agent, Text, Velocity, Scale
from framework.systems import InputManager, SpriteRenderer
from framework.systems.sprite_animator import SpriteAnimator

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
                
    def control_player_ship(self, dt):
        for ent, (player, pos, vel) in self.world.get_components(Player, Position, Velocity):
            thrust = 50
            # the pos.angle is in degrees, and is the forward direction of the ship
            # the ship starts at 0 degrees, which is to the right, and the sprite is facing right
            angle_radians = math.radians(pos.angle)
            vel_x = thrust * dt * math.cos(angle_radians)
            vel_y = -thrust * dt * math.sin(angle_radians)
            
            if self.input.key_down(pygame.K_UP):
                vel.x += vel_x
                vel.y += vel_y
            if self.input.key_down(pygame.K_DOWN):
                # reverse thrust
                vel.x -= vel_x
                vel.y -= vel_y
            if self.input.key_down(pygame.K_LEFT):
                pos.angle -= 5
            if self.input.key_down(pygame.K_RIGHT):
                pos.angle += 5

    def process(self, dt, events):
        if self.input is None:
            self.input = self.world.get_processor(InputManager)
        if self.input is not None:
            self.control_player_ship(dt)
            if self.input.key_pressed(pygame.K_SPACE):
                self.toggle_agent_wiggle()
            if self.input.key_pressed(pygame.K_F5):
                ents = self.world._entities
                print(f"Entities: {ents}")
                yaml.dump(ents, open("save.yaml", "w"))


class AsteroidsPhysics(esper.Processor):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

    def process(self, dt, events):
        # get all entities with a position and velocity
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            # cap velocity at max_speed
            vel.x = max(min(vel.x, vel.max_speed), -vel.max_speed)
            vel.y = max(min(vel.y, vel.max_speed), -vel.max_speed)

            pos.x += vel.x * dt
            pos.y += vel.y * dt
            # handle wrapping
            wrap_buffer = 10  # how far off screen before we wrap to try to make it look smooth
            if pos.x < 0 - wrap_buffer:
                pos.x = self.screen.get_width()
            elif pos.x > self.screen.get_width() + wrap_buffer:
                pos.x = 0
            if pos.y < 0 - wrap_buffer:
                pos.y = self.screen.get_height()
            elif pos.y > self.screen.get_height() + wrap_buffer:
                pos.y = 0


assets = AssetCache()


def init(screen, world):
    skull_image = assets.load_image("red_skull.png")
    blue_skull_image = assets.load_image("blue_skull.png")
    chicken_image = assets.load_image("chicken.png")

    # chicken_flap_anim = assets.create_animation("chicken_flap", "chicken.png", 32, [0, 1, 2, 3, 4, 5], 10, True)
    # assets.save_animation(chicken_flap_anim, "chicken_flap.yaml")
    chicken_flap_anim_data = assets.load_animation("chicken_flap.yaml")
    chicken_flap_anim = Animation(
        speed=chicken_flap_anim_data.speed,
        loop=chicken_flap_anim_data.loop,
        playing=True,
        frames=SpriteAnimator.create_frames(
            chicken_image, chicken_flap_anim_data.frames, chicken_flap_anim_data.size),
    )

    world.add_processor(InputManager())
    world.add_processor(AsteroidsPhysics(screen))
    world.add_processor(SpriteAnimator())
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
        world.add_component(skull, Position(50, 300, 0))
        world.add_component(skull, Velocity(
            random.randint(10, 20), random.randint(10, 20)))
        world.add_component(skull, Sprite(image_name="red_skull.png",
                                          image=skull_image, rect=skull_image.get_rect()))
        world.add_component(skull, Agent(name="Skull"))

        blue_skull = world.create_entity()
        world.add_component(blue_skull, Position(100, 300))
        world.add_component(blue_skull, Sprite(image_name="blue_skull.png",
                                               image=blue_skull_image, rect=blue_skull_image.get_rect()))
        world.add_component(blue_skull, Agent(name="Blue Skull"))

        chicken = world.create_entity()
        world.add_component(chicken, Position(50, 100))
        world.add_component(chicken, Sprite(image_name="chicken.png",
                                            image=chicken_image, rect=chicken_image.get_rect()))
        world.add_component(chicken, chicken_flap_anim)
        world.add_component(chicken, Velocity())
        world.add_component(chicken, Scale(2, 2))
        world.add_component(chicken, Agent(name="Chicken"))

        ship = world.create_entity()
        world.add_component(ship, Position(50, 200))
        world.add_component(ship, Velocity())
        world.add_component(ship, Sprite(image_name="ship1.png",
                            image=assets.load_image("ship1.png")))
        world.add_component(ship, Player(name="Starman"))


def start():
    pygame.init()
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    # viewport so that we can render all the game stuff to it, and then scale it up to the screen
    # viewport = Viewport(screen_width // 2, screen_height // 2, 2, 2)
    viewport = Viewport(screen_width // 2, screen_height // 2, 1, 2)
    pygame.display.set_caption("ECS Game Test")
    world = esper.World()
    clock = pygame.time.Clock()
    init(viewport, world)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # update the viewport to get the scaled surface setup
        viewport.update()
        
        # clear the viewport with black
        viewport.fill((0, 0, 0))

        # update the game world, this will blit all the sprites to the viewport
        world.process(dt, events)

        # draw the scaled surface onto the screen
        screen.blit(viewport.get_render_surface(), (0, 0))

        pygame.display.flip()


if __name__ == "__main__":
    start()
    pygame.quit()
