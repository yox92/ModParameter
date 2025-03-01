from CustomWeapon.py.Entity.ItemProps import ItemProps

class ItemManager:
    def __init__(self):
        self.key_value = {key: 0 for key in vars(ItemProps()).keys()}

    def get_value(self, key):
        if key in self.key_value:
            return self.key_value[key]
        else:
            raise KeyError(f"La clé '{key}' n'existe pas dans KeyValue.")

    def set_value(self, key, value):
        if key in self.key_value:
            self.key_value[key] = 1 + (value / 100)
        else:
            raise KeyError(f"La clé '{key}' n'existe pas dans KeyValue.")

    def list_keys(self):
        return list(self.key_value.keys())

    def list_value(self):
        return list(self.key_value.values())

    def __repr__(self):
        return f"KeyValue({self.key_value})"
