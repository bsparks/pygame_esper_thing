from framework.ecs import Processor
from framework.components import DestroyAfter, DestroyOnOutOfBounds, Position


class DestroySystem(Processor):
    def process(self, dt, events):
        for ent, (pos, destroy) in self.world.get_components(Position, DestroyOnOutOfBounds):
            if pos.x < 0 or pos.x > self.screen.get_width() or pos.y < 0 or pos.y > self.screen.get_height():
                self.world.delete_entity(ent)

        for ent, (destroy) in self.world.get_component(DestroyAfter):
            destroy.time += dt
            # print(f"destroying {ent} in {destroy.after - destroy.time:.2f} seconds")
            if destroy.time >= destroy.after:
                self.world.delete_entity(ent)
