from Entity.EffectDamage import EffectDamage
from Entity.EnumMedic import EnumMedic


class Medic:
    def __init__(self, effects_damage=None, **props):
        self._MaxHpResource = (
            props.get(EnumMedic.MAXHPRESOURCE.label, None),
            EnumMedic.MAXHPRESOURCE.label
        )
        self._hpResourceRate = (
            props.get(EnumMedic.HPRESOURCERATE.label, None),
            EnumMedic.HPRESOURCERATE.label
        )
        self._medUseTime = (
            props.get(EnumMedic.MEDUSETIME.label, None),
            EnumMedic.MEDUSETIME.label
        )
        self._priceFactor = (
            props.get(EnumMedic.PRICEFACTOR.label, None),
            EnumMedic.PRICEFACTOR.label
        )
        self._effects_damage = EffectDamage.from_data(effects_damage)

    @property
    def MaxHpResource(self):
        return self._MaxHpResource

    @property
    def hpResourceRate(self):
        return self._hpResourceRate

    @property
    def medUseTime(self):
        return self._medUseTime

    @property
    def effects_damage(self):
        return self._effects_damage

    @property
    def priceFactor(self):
        return self._priceFactor

    @classmethod
    def from_data(cls, data: dict):
        effects_damage = data.get("effects_damage", {})
        props = {k: v for k, v in data.items() if k != "effects_damage"}
        return cls(effects_damage=effects_damage, **props)

    def iterate_key_and_values(self,include_effects_damage=False):
        for enum_field in EnumMedic:
            attr_name = enum_field.label
            value = getattr(self, attr_name, None)
            if isinstance(value, tuple) and len(value) == 2:
                yield attr_name, value[0]
            else:
                yield attr_name, value
        if include_effects_damage:
            yield "effects_damage", self.effects_damage

    def get_instance_attributes(self):
        return vars(self)

    def get_attribute_value(self, attr_name):
        return getattr(self, attr_name, None)

    def get_value_by_label(self, label):
        if label == "effects_damage":
            return self.effects_damage
        for attr_name in self.get_instance_attributes():
            attr_value = self.get_attribute_value(attr_name)
            if isinstance(attr_value, tuple) and len(attr_value) == 2:
                numeric_value, attr_label = attr_value
                if attr_label == label:
                    return numeric_value
        raise ValueError(f"Le label '{label}' n'a pas été trouvé dans Medic.")

    def set_value(self, label: str, value):
        for enum_field in EnumMedic:
            if enum_field.label == label:
                attr_name = f"_{label}"  # car tous tes attributs sont préfixés d’un "_"
                if hasattr(self, attr_name):
                    setattr(self, attr_name, (value, label))
                    return
                else:
                    raise AttributeError(f"L'attribut '{attr_name}' n'existe pas dans Medic.")

        if label == "effects_damage":
            if isinstance(value, EffectDamage):
                self._effects_damage = value
            elif isinstance(value, dict):
                self._effects_damage = EffectDamage.from_data(value)
            else:
                raise ValueError("effects_damage must be an EffectDamage or dict.")
            return

        raise ValueError(f"Le label '{label}' n'existe pas dans EnumMedic ou n'est pas modifiable.")

    def to_dict(self):
        return {
            field.label: getattr(self, field.label, None)
            for field in EnumMedic
        }

    def __iter__(self):
        return (key for key in self.__dict__.keys())

    def __eq__(self, other):
        if not isinstance(other, Medic):
            return False

        for label, value in self.iterate_key_and_values(include_effects_damage=True):
            try:
                other_value = other.get_value_by_label(label)
            except ValueError:
                return False

            if value != other_value:
                return False

        return True


