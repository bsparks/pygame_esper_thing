import math
import os
import random
import pygame
import yaml
from dataclasses import dataclass as component
from asteroids import DestroySystem, PlayerController, Thruster, AsteroidsPhysics
from asteroids.components import DestroyAfter
from framework.ecs import World
from framework.systems.background import BackgroundSystem
from framework.viewport import Viewport
from framework.asset_cache import AssetCache
from framework.components import AngularVelocity, Animation, BackgroundImage, MountPoint, Player, Position, Sprite, Agent, Text, Velocity, Scale
from framework.systems import InputManager, SpriteRenderer, SpriteAnimator, TextRenderer, MountingSystem


# note to self, a system does not need to actually query components, it could just be something that
# runs every frame, like a timer or input manager


assets = AssetCache()


def init(screen, world):
    starfield = assets.load_image("starfield6.png")

    # thruster_anim = assets.create_animation("thruster_1", "Thruster_01.png", 16, [0, 1, 2, 3], 10, True)
    # assets.save_animation(thruster_anim, "thruster_1.yaml")
    thruster_anim_data = assets.load_animation("thruster_1.yaml")
    thruster_anim = Animation(
        speed=thruster_anim_data.speed,
        loop=thruster_anim_data.loop,
        playing=True,
        frames=SpriteAnimator.create_frames(
            assets.load_image("Thruster_01.png"), thruster_anim_data.frames, thruster_anim_data.size),
    )

    fx_02_anim_data = assets.load_animation("fx_02.yaml")
    fx_02_anim = Animation(
        speed=fx_02_anim_data.speed,
        loop=fx_02_anim_data.loop,
        playing=True,
        frames=SpriteAnimator.create_frames(
            assets.load_image(fx_02_anim_data.image_name), fx_02_anim_data.frames, fx_02_anim_data.size),
    )

    world.add_processor(InputManager())
    world.add_processor(PlayerController(screen, assets))
    world.add_processor(DestroySystem())
    world.add_processor(AsteroidsPhysics(screen))
    world.add_processor(BackgroundSystem(screen, assets))
    world.add_processor(MountingSystem())
    world.add_processor(SpriteAnimator())
    world.add_processor(SpriteRenderer(screen, assets))
    world.add_processor(TextRenderer(screen, assets))

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

        for i in range(5):
            xl_asteroid = world.create_entity()
            world.add_component(xl_asteroid, Position(
                random.randint(-20, 500), random.randint(-20, 500)))
            world.add_component(xl_asteroid, Sprite(
                image_name="xl_asteroid.png"))
            world.add_component(xl_asteroid, Velocity(
                random.randint(-10, 20), random.randint(-10, 20)))
            world.add_component(
                xl_asteroid, AngularVelocity(random.randint(-10, 10)))
            
        for i in range(5):
            asteroid = world.create_entity()
            world.add_component(asteroid, Position(
                random.randint(-20, 500), random.randint(-20, 500)))
            world.add_component(asteroid, Sprite(
                image_name="asteroid_l.png"))
            world.add_component(asteroid, Velocity(
                random.randint(-10, 20), random.randint(-10, 20)))
            world.add_component(
                asteroid, AngularVelocity(random.randint(-10, 10)))

        ship = world.create_entity()
        world.add_component(ship, Position(50, 200))
        world.add_component(ship, Velocity())
        world.add_component(ship, Sprite(image_name="ship1.png"))
        world.add_component(ship, Player(name="Starman"))

        bullet = world.create_entity()
        world.add_component(bullet, Position(54, 200))
        world.add_component(bullet, fx_02_anim)
        world.add_component(bullet, Sprite(
            image_name=fx_02_anim_data.image_name))
        world.add_component(bullet, Velocity(0, 0))
        world.add_component(bullet, DestroyAfter(after=4))

        thruster = world.create_entity()
        world.add_component(thruster, Position(50, 200))
        world.add_component(thruster, Sprite(
            image_name="Thruster_01.png", anchor_x="left", depth=-1))
        world.add_component(thruster, thruster_anim)
        world.add_component(thruster, MountPoint(parent=ship, x=-24, y=0))
        world.add_component(thruster, Thruster(power=50, owner=ship))

        text1 = world.create_entity()
        world.add_component(text1, Position(screen.get_width() // 2, 24))
        world.add_component(text1, Text(text="Asteroids!",
                            font="PressStart2P-Regular.ttf", size=16))

        bg = world.create_entity()
        world.add_component(bg, Position(0, 0))
        world.add_component(bg, BackgroundImage(
            image_name="starfield6.png", anchor_x=0, anchor_y=0, repeat_x=True, repeat_y=True))


def start():
    pygame.init()
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    # viewport so that we can render all the game stuff to it, and then scale it up to the screen
    # viewport = Viewport(screen_width // 2, screen_height // 2, 2, 2)
    viewport = Viewport(screen_width // 2, screen_height // 2, 1, 2)
    pygame.display.set_caption("ECS Game Test")
    world = World()
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
        viewport.update(dt)

        # clear the viewport with black
        viewport.fill((0, 0, 0))

        # update the game world, this will blit all the sprites to the viewport
        world.process(dt, events)

        # draw the scaled surface onto the screen
        screen.blit(viewport.get_render_surface(), viewport.get_rect())

        pygame.display.flip()


if __name__ == "__main__":
    start()
    pygame.quit()
