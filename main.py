import pygame

from pacman import init_game
from framework.ecs import World
from framework.viewport import Viewport
from framework.asset_cache import AssetCache

# note to self, a system does not need to actually query components, it could just be something that
# runs every frame, like a timer or input manager

# TODO: some kind of game loading system so each can have its own viewport config
game = "pacman"

res_x = 1280
res_y = 720
view_x = res_x // 2
view_y = res_y // 2
view_zoom = 2
view_scale = 1
if game == "pacman":
    view_zoom = 1
    res_x = 896
    res_y = 1152
    view_x = res_x
    view_y = res_y


assets = AssetCache()


def init(screen, world):
    init_game(world, screen, assets)


def start():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    screen = pygame.display.set_mode((res_x, res_y))
    # viewport so that we can render all the game stuff to it, and then scale it up to the screen
    viewport = Viewport(view_x, view_y, scale=view_scale, zoom=view_zoom)
    pygame.display.set_caption("ECS Arcade")
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
