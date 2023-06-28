import re

class AnimationNaming:
    DIRECTIONS_MAP = {
        "L": "left", "R": "right", "U": "up", "D": "down",
        "LU": "left,up", "LD": "left,down", "RU": "right,up", "RD": "right,down",
        "C": "center", "H": "horizontal", "V": "vertical",
        "F": "forward", "B": "backward",
        "FL": "forward,left", "FR": "forward,right", 
        "BL": "backward,left", "BR": "backward,right"
    }
    
    @staticmethod
    def _inverse_map(value):
        for k, v in AnimationNaming.DIRECTIONS_MAP.items():
            if v == value:
                return k
        return None

    @staticmethod
    def _parse_parts(part):
        parts = re.findall(r"\b\w+\b", part)
        return ''.join(p.capitalize() for p in parts)

    @staticmethod
    def _parse_direction(direction):
        parts = re.findall(r"\b\w+\b", direction)
        return ''.join(p[0].upper() for p in parts)
    
    def encoder(self, action, direction=None, secondary_action=None, variant=None, meters=None, suffix=None, **kwargs):
        if not action:
            raise ValueError("Action can't be empty")

        name = action.lower()

        if direction:
            name += self._parse_direction(direction)
        if secondary_action:
            name += self._parse_parts(secondary_action)
        if variant:
            name += str(variant).zfill(3)
        if meters:
            x, y = meters.split(',')
            name += str(x.zfill(3)+'x'+y.zfill(3))
        if suffix:
            name += suffix.capitalize()
        return name

    def decoder(self, name):
        results = {'action': None, 'direction': None, 'secondary_action': None, 'variant': None, 'meters': None, 'suffix': None}

        action_match = re.match(r'^[a-z]+', name)
        if action_match:
            results['action'] = action_match.group()
            name = name[len(action_match.group()):]

        direction_match = re.match(r'[A-Z]{1,2}(?=[A-Z][a-z]|$)', name)
        if direction_match:
            results['direction'] = self.DIRECTIONS_MAP.get(direction_match.group(), '')
            name = name[len(direction_match.group()):]

        secondary_action_end_index = min((i for i, ch in enumerate(name) if ch.isdigit()), default=len(name))
        if secondary_action_end_index > 0:
            secondary_action = name[:secondary_action_end_index]
            results['secondary_action'] = ','.join(word.lower() for word in re.findall(r'[A-Z][^A-Z]*', secondary_action))
            name = name[secondary_action_end_index:]

        variant_and_meters_match = re.match(r'(?P<variant>\d{3}(?!x\d{3}))?(?P<meters>\d{3}x\d{3})?', name)
        if variant_and_meters_match:
            results['variant'] = variant_and_meters_match.group('variant').lstrip('0') if variant_and_meters_match.group('variant') else None
            if variant_and_meters_match.group('meters'):
                x, y = variant_and_meters_match.group('meters').split('x')
                results['meters'] = str(int(x)) + 'x' + str(int(y))
            name = name[len(variant_and_meters_match.group()):]

        if name:
            results['suffix'] = name.lower()

        return results

    def simplifier(self, name, decoder = False):
        decode = self.decoder(name)

        formatted_direction = decode['direction'].replace(', ', ',') if decode['direction'] else ''
        
        direction_abbreviation = self._inverse_map(formatted_direction) or ''
        
        func = lambda x: ''.join(word.strip().capitalize() for word in x.split(','))
        secondary_actions = func(decode['secondary_action']) if decode['secondary_action'] else ''
    
        variant = decode['variant'].lstrip('0') if decode['variant'] else ''
    
        meters = decode['meters'].replace('0x', 'x') if decode['meters'] and decode['meters'] != '0x0' else ''
        if meters:
            meters = '_' + meters + '_'
    
        suffix = decode['suffix'].capitalize() if decode['suffix'] else ''
        
        nice_name = decode['action'] + direction_abbreviation + secondary_actions + variant + meters + suffix 
        if decoder:
            return [nice_name, decode]
        return nice_name
