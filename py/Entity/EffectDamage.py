from Entity.Effect import Effect
from Entity.EnumEffectName import EnumEffectName


class EffectDamage:
    def __init__(self, effects=None):
        self.effects = effects or {}

    @classmethod
    def from_data(cls, data):
        if not isinstance(data, dict):
            return cls()

        effects = {}

        valid_names = {e.value for e in EnumEffectName}

        for effect_name, effect_data in data.items():
            if effect_name in valid_names and isinstance(effect_data, dict):
                effects[effect_name] = Effect.from_dict(effect_data)
        return cls(effects)

    def add_effect(self, name: str, effect: 'Effect'):
        self.effects[name] = effect

    def get_effect(self, name):
        return self.effects.get(name)

    def to_dict(self):
        return {name: vars(effect) for name, effect in self.effects.items()}

    def __iter__(self):
        return iter(self.effects.items())
