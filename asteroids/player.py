import math
import pygame
from asteroids.components import Thruster, Wiggle
from framework.components import Agent, Player, Position, Sprite, Velocity
from framework.ecs import Processor
from framework.systems.input_mgr import InputManager


class Controller(Processor):
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
            my_thruster = -1
            my_thruster_c = None
            my_thruster_sprite = None
            for t_ent, (thruster) in self.world.get_component(Thruster):
                if thruster.owner == ent:
                    thrust = thruster.power
                    my_thruster = t_ent
                    my_thruster_c = thruster
                    break  # only one thruster per ship rn
            if my_thruster != -1:
                if not my_thruster_c.enabled:
                    return
                my_thruster_sprite = self.world.try_component(
                    my_thruster, Sprite)
                if my_thruster_sprite is not None:
                    my_thruster_sprite.enabled = False

            # the pos.angle is in degrees, and is the forward direction of the ship
            # the ship starts at 0 degrees, which is to the right, and the sprite is facing right
            angle_radians = math.radians(pos.angle)
            vel_x = thrust * dt * math.cos(angle_radians)
            vel_y = -thrust * dt * math.sin(angle_radians)

            if self.input.key_down(pygame.K_UP):
                vel.x += vel_x
                vel.y += vel_y
                if my_thruster_sprite is not None:
                    my_thruster_sprite.enabled = True
            if self.input.key_down(pygame.K_DOWN):
                # reverse thrust
                vel.x -= vel_x
                vel.y -= vel_y
                if my_thruster_sprite is not None:
                    my_thruster_sprite.enabled = True
            if self.input.key_down(pygame.K_LEFT):
                pos.angle += 5
            if self.input.key_down(pygame.K_RIGHT):
                pos.angle -= 5

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
