from esper import Processor


class EventHandler(Processor):
    def melee_handler(self, attacker_ent, target_ent):
        self.world.message_log.add_message("Attack!")

    def process(self):
        for event in self.world.events:
            if event := event.get("melee"):
                self.melee_handler(event["attacker"], event["target"])
        
        self.world.events = []
