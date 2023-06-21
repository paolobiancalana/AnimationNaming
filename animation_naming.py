# Desc: Class for naming animations
import re

class AnimationNaming:
    def __init__(self, action, direction=None, secondary_action=None, variant=None, meters=None):
        self.action = action
        self.direction = direction
        self.secondary_action = secondary_action
        self.variant = variant
        self.meters = meters

    def create_name(self):
        name = self.action.lower()
        if self.direction is not None:
            if re.search(r',', self.direction):
                directions = re.match(r'([a-zA-Z]+)\W+([a-zA-Z]+)', self.direction).groups()
                name += directions[0][0].upper()+directions[1][0].upper()
            else:
                name += self.direction[0].upper()
        if self.secondary_action is not None:
            name += self.secondary_action.capitalize()
        if self.variant is not None:
            name += str(self.variant)
        if self.meters is not None:
            x, y = self.meters.split(',')
            name += str(x+'x'+y)

        return name
