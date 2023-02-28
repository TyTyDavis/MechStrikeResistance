from esper import Processor
import random

from components import components


class EventHandler(Processor):
    def melee_handler(self, attacker_ent, target_ent):
        attack_component = self.world.component_for_entity(attacker_ent, components.Attack)
        damage = random.randint(1, attack_component.melee_damage)
        hp = self.world.component_for_entity(target_ent, components.HitPoints)
        hp.hp -= damage
        self.world.message_log.add_message(f"{damage} damage!")

    def process(self):
        for event in self.world.events:
            if event := event.get("melee"):
                self.melee_handler(event["attacker"], event["target"])
        
        self.world.events = []
