from Entity.EnumAiming import EnumAiming

class AimingManager:
    def __init__(self):
        self.key_value = {aiming.label: 0 for aiming in EnumAiming}

    def get_value(self, key):
        if key in self.key_value:
            return self.key_value[key]
        else:
            raise KeyError(f"La clé '{key}' n'existe pas dans KeyValue.")

    def get_key(self, value):
        if value in self.key_value:
            return self.key_value[value]
        else:
            raise KeyError(f"La clé '{value}' n'existe pas dans KeyValue.")

    def iterate_key_and_values(self):
        for key, value in self.key_value.items():
            yield key, value

    def update_from_props_json(self, key, value):
        if key in self.key_value:
            self.key_value[key] = value


    def __repr__(self):
        return f"KeyValue({self.key_value})"

    def __getitem__(self, key):
        return self.get_value(key)


    def __eq__(self, other):
        if not isinstance(other, AimingManager):
            return False
        return self.key_value == other.key_value

