from framework.components import AngularVelocity, Position, Velocity
from framework.ecs import Processor


class AsteroidsPhysics(Processor):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

    def process(self, dt, events):
        # get all entities with a position and velocity
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            angular_vel = self.world.try_component(ent, AngularVelocity)
            if angular_vel is not None:
                pos.angle += angular_vel.speed * dt

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
