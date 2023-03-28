from framework.systems import (AudioSystem, BackgroundSystem, InputManager,
                               SpriteAnimator, SpriteRenderer, TextRenderer,
                               DestroySystem)
from .player import PlayerController
from framework.components import Music, Player, Position, Text, Score

FONT_NAME = "PressStart2P-Regular.ttf"
FONT_SIZE = 32


def init_game(world, screen, assets):
    world.add_processor(InputManager())
    world.add_processor(AudioSystem(assets))
    world.add_processor(PlayerController(screen, assets))
    world.add_processor(DestroySystem())
    world.add_processor(BackgroundSystem(screen, assets))
    world.add_processor(SpriteAnimator())
    world.add_processor(SpriteRenderer(screen, assets))
    world.add_processor(TextRenderer(screen, assets))

    music = world.create_entity()
    world.add_component(music, Music(
        "pacman_beginning.wav", play=True, loop=False))

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