from framework.ecs import Processor
from framework.components import Player, Position, Score, Text

class PlayerController(Processor):
    def __init__(self, screen, assets):
        super().__init__()
        self.screen = screen
        self.assets = assets
        self.timer = 0
        
    def process(self, dt, events):
        self.timer += dt

        update_score = False
        if self.timer > 1:
            update_score = True
            self.timer = 0

        for ent, (player, pos) in self.world.get_components(Player, Position):
            if update_score:
                score = self.world.try_component(ent, Score)
                if score is not None:
                    # print(f"PlayerController: {ent} {player} {pos} {score}")
                    score.value += 1
                    if self.world.entity_exists(score.text_entity):
                        text = self.world.try_component(score.text_entity, Text)
                        if text is not None:
                            text.text = str(score.value).zfill(6)