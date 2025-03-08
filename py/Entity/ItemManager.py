from enum import Enum

from Entity import EnumAmmo
from Entity.EnumProps import EnumProps
from typing import Union


class ItemManager:
    def __init__(self, enum_type: Union[type(EnumProps), type(EnumAmmo)]):
        if not issubclass(enum_type, Enum):
            raise TypeError("enum_type doit être soit EnumProps soit EnumAmmo.")

        self.enum_type = enum_type
        self.key_value = {prop.label: 0 for prop in self.enum_type}

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

    def set_value_and_transform_like_multi(self, key, value):
        if key in self.key_value:
            if isinstance(value, (float, int)):
                if isinstance(value, int):
                    value_float = float(value)
                else:
                    value_float = value

                transformed_value = 1 + (value_float / 100)

                transformed_value = max(0.01, min(transformed_value, 1.99))

                if 0.1 <= transformed_value <= 2.0:
                    transformed_value = round(transformed_value, 2)
                elif 0.01 <= transformed_value < 0.1:
                    transformed_value = round(transformed_value, 3)

                self.key_value[key] = transformed_value
        else:
            raise KeyError(f"La clé '{key}' n'existe pas dans KeyValue.")

    def iterate_key(self):
        for key, value in self.key_value.items():
            yield key

    def iterate_key_and_values(self):
        for key, value in self.key_value.items():
            yield key, value

    def iterate_key_values_where_key_ve_change(self, original_value):
        if not isinstance(original_value, type(self)):
            raise TypeError(f"need to be same class for comparing : {type(self).__name__}")
        for key, value in self.iterate_key_and_values():
            original_val = original_value.key_value.get(key, None)
            if original_value.key_value.get(key, None) != value:
                yield key, value

    def update_from_props_json(self, key, value):
        if key in self.key_value:
            self.key_value[key] = value

    def update_from_json(self, json_data):
        for key, value in json_data.items():
            if key in self.key_value:
                self.key_value[key] = value

    def all_values_are_one(self):
        return all(
            value == 1.0
            for key, value in self.key_value.items()
            if isinstance(value, (int, float))
        )

    def copy_to_with_inverted_values(self, target_manager):
        if not isinstance(target_manager, ItemManager):
            raise TypeError("Le gestionnaire cible doit être une instance de ItemManager.")

        for key, value in self.iterate_key_and_values():
            if isinstance(value, (int, float)):
                if 0.01 <= value <= 2.0:
                    target_manager.key_value[key] = int(100 * value - 100)
                else:
                    raise ValueError(
                        f"La valeur '{value}' pour la clé '{key}' est hors des limites autorisées (0.01 à 2.0)."
                    )

    def lambda_value(self, item_manager):
        result_manager = ItemManager(EnumProps)

        for key, value in self.iterate_key_and_values():
            if isinstance(value, (float, int)):
                old_value = item_manager.key_value.get(key)
                if isinstance(old_value, (float, int)):
                    if value != 0:
                        result_manager.key_value[key] = int(((old_value - value) / value) * 100)

        return result_manager

    def __repr__(self):
        return f"KeyValue({self.key_value})"

    def __getitem__(self, key):
        return self.get_value(key)

    def __setitem__(self, key, value):
        self.set_value_and_transform_like_multi(key, value)

    def __eq__(self, other):
        if not isinstance(other, ItemManager):
            return False
        return self.key_value == other.key_value
