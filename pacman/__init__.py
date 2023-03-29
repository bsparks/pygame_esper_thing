from framework.systems import (AudioSystem, BackgroundSystem, InputManager,
                               SpriteAnimator, SpriteRenderer, TextRenderer,
                               DestroySystem, TileMapRenderer)
from .player import PlayerController
from framework.components import Music, Player, Position, Text, Score, Sprite, Animation, TileMap

FONT_NAME = "PressStart2P-Regular.ttf"
FONT_SIZE = 32


def init_game(world, screen, assets):
    world.add_processor(InputManager())
    world.add_processor(AudioSystem(assets))
    world.add_processor(PlayerController(screen, assets))
    world.add_processor(DestroySystem())
    world.add_processor(BackgroundSystem(screen, assets))
    world.add_processor(TileMapRenderer(screen, assets))
    world.add_processor(SpriteAnimator(screen, assets))
    world.add_processor(SpriteRenderer(screen, assets))
    world.add_processor(TextRenderer(screen, assets))

    music = world.create_entity()
    world.add_component(music, Music(
        "pacman_beginning.wav", play=True, loop=False))

    level = world.create_entity()
    world.add_component(level, Position(x=0, y=96))
    world.add_component(level, TileMap(name="level1", tileset="pacman_classic", width=28, height=31, tile_size=32, data=[
        7, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 13, 6, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 0,
        8, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 1,
        8, 27, 45, 17, 17, 18, 27, 45, 17, 17, 17, 18, 27, 35, 32, 27, 45, 17, 17, 17, 18, 27, 45, 17, 17, 18, 27, 1,
        8, 41, 35, 20, 20, 32, 27, 35, 20, 20, 20, 32, 27, 35, 32, 27, 35, 20, 20, 20, 32, 27, 35, 20, 20, 32, 41, 1,
        8, 27, 47, 11, 11, 36, 27, 47, 11, 11, 11, 36, 27, 47, 36, 27, 47, 11, 11, 11, 36, 27, 47, 11, 11, 36, 27, 1,
        8, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 1,
        8, 27, 45, 17, 17, 18, 27, 45, 44, 27, 45, 17, 17, 17, 17, 17, 17, 18, 27, 45, 44, 27, 45, 17, 17, 18, 27, 1,
        8, 27, 47, 11, 11, 36, 27, 35, 32, 27, 47, 11, 11, 40, 33, 11, 11, 36, 27, 35, 32, 27, 47, 11, 11, 36, 27, 1,
        8, 27, 27, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 27, 27, 1,
        15, 3, 3, 3, 3, 44, 27, 35, 42, 17, 17, 18, 20, 35, 32, 20, 45, 17, 17, 43, 32, 27, 45, 3, 3, 3, 3, 14,
        20, 20, 20, 20, 20, 8, 27, 35, 33, 11, 11, 36, 20, 47, 36, 20, 47, 11, 11, 40, 32, 27, 1, 20, 20, 20, 20, 20,
        20, 20, 20, 20, 20, 8, 27, 35, 32, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 35, 32, 27, 1, 20, 20, 20, 20, 20,
        20, 20, 20, 20, 20, 8, 27, 35, 32, 20, 39, 10, 26, 20, 20, 19, 3, 38, 20, 35, 32, 27, 1, 20, 20, 20, 20, 20,
        23, 23, 23, 23, 23, 36, 27, 47, 36, 20, 1, 20, 20, 20, 20, 20, 20, 8, 20, 47, 36, 27, 37, 23, 23, 23, 23, 23,
        20, 20, 20, 20, 20, 20, 27, 20, 20, 20, 1, 20, 20, 20, 20, 20, 20, 8, 20, 20, 20, 27, 20, 20, 20, 20, 20, 20,
        3, 3, 3, 3, 3, 18, 27, 45, 44, 20, 1, 20, 20, 20, 20, 20, 20, 8, 20, 45, 44, 27, 45, 3, 3, 3, 3, 3,
        20, 20, 20, 20, 20, 8, 27, 35, 32, 20, 12, 23, 23, 23, 23, 23, 23, 5, 20, 35, 32, 27, 1, 20, 20, 20, 20, 20,
        20, 20, 20, 20, 20, 8, 27, 35, 32, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 35, 32, 27, 1, 20, 20, 20, 20, 20,
        20, 20, 20, 20, 20, 8, 27, 35, 32, 20, 45, 17, 17, 17, 17, 17, 17, 18, 20, 35, 32, 27, 1, 20, 20, 20, 20, 20,
        7, 23, 23, 23, 23, 36, 27, 47, 36, 20, 47, 11, 11, 40, 33, 11, 11, 36, 20, 47, 36, 27, 37, 23, 23, 23, 23, 0,
        8, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 1,
        8, 27, 45, 17, 24, 44, 27, 45, 17, 17, 17, 18, 27, 35, 32, 27, 45, 17, 17, 17, 18, 27, 45, 24, 17, 18, 27, 1,
        8, 27, 47, 11, 40, 32, 27, 47, 11, 11, 11, 36, 27, 47, 36, 27, 47, 11, 11, 11, 36, 27, 35, 33, 11, 36, 27, 1,
        8, 41, 27, 27, 35, 32, 27, 27, 27, 27, 27, 27, 27, 20, 20, 27, 27, 27, 27, 27, 27, 27, 35, 32, 27, 27, 41, 1,
        9, 17, 18, 27, 35, 32, 27, 45, 44, 27, 45, 17, 17, 17, 17, 17, 17, 18, 27, 45, 44, 27, 35, 32, 27, 45, 24, 2,
        21, 11, 36, 27, 47, 36, 27, 35, 32, 27, 47, 11, 11, 40, 33, 11, 11, 36, 27, 35, 32, 27, 47, 36, 27, 47, 11, 16,
        8, 27, 27, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 35, 32, 27, 27, 27, 27, 27, 27, 1,
        8, 27, 45, 17, 17, 17, 17, 43, 42, 17, 17, 18, 27, 35, 32, 27, 45, 17, 17, 43, 42, 17, 17, 17, 17, 18, 27, 1,
        8, 27, 47, 11, 11, 11, 11, 11, 11, 11, 11, 36, 27, 47, 36, 27, 47, 11, 11, 11, 11, 11, 11, 11, 11, 36, 27, 1,
        8, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 1,
        15, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 14
    ]))

    score_label = world.create_entity()
    world.add_component(score_label, Position(x=10, y=8))
    world.add_component(score_label, Text(
        text="SCORE", font=FONT_NAME, size=FONT_SIZE, anchor_x=0, anchor_y=0))

    score = world.create_entity()
    world.add_component(score, Position(x=10, y=50))
    world.add_component(score, Text(
        text=str(0).zfill(6), font=FONT_NAME, size=FONT_SIZE, anchor_x=0, anchor_y=0, cache=False))

    ready_label = world.create_entity()
    world.add_component(ready_label, Position(x=352, y=640))
    world.add_component(ready_label, Text(
        text="READY!", font=FONT_NAME, size=FONT_SIZE, anchor_x=0, anchor_y=0, color=(255, 255, 0)))

    player = world.create_entity()
    world.add_component(player, Player(name="Pacman"))
    world.add_component(player, Position(14*32, 26.5*32))
    world.add_component(player, Score(text_entity=score))
    world.add_component(player, Sprite(image_name="pacman.png"))
    world.add_component(player, Animation(
        name="pacman_move_right", playing=True))
