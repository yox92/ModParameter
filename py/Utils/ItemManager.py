from py.Entity.ItemProps import ItemProps


class ItemManager:
    def __init__(self):
        self.key_value = {key: 0 for key in vars(ItemProps()).keys()}

    def get_value(self, key):
        if key in self.key_value:
            return self.key_value[key]
        else:
            raise KeyError(f"La clé '{key}' n'existe pas dans KeyValue.")

    def set_value_and_transform_like_multi(self, key, value):
        print(key, value)
        if key in self.key_value:
            self.key_value[key] = 1 + (value / 100)
        else:
            raise KeyError(f"La clé '{key}' n'existe pas dans KeyValue.")

    def iterate_key_values(self):
        for key, value in self.key_value.items():
            yield key, value

    def iterate_key_values_where_key_ve_change(self):
        for key, value in self.key_value.items():
            if value != 0:
                yield key, value

    def __repr__(self):
        return f"KeyValue({self.key_value})"

    def __getitem__(self, key):
        return self.get_value(key)

    def __setitem__(self, key, value):
        self.set_value_and_transform_like_multi(key, value)

