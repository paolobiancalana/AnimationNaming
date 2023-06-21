# Desc: Class for naming animations

class AnimationNaming:
    def __init__(self, action, direction=None, secondary_action=None, variant=None, meters=None):
        self.action = action
        self.direction = direction
        self.secondary_action = secondary_action
        self.variant = variant
        self.meters = meters

    def create_name(self):
        name = self.action
        if self.direction is not None:
            name += self.direction[0].upper()
        if self.secondary_action is not None:
            name += self.secondary_action.capitalize()
        if self.variant is not None:
            name += str(self.variant)
        if self.meters is not None:
            if 'jump' in self.action and 'x' in self.meters and 'y' in self.meters:
                name += str(self.meters['x']) + 'x' + str(self.meters['y'])
            else:
                name += str(self.meters)
        return name