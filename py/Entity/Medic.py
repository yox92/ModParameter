from Entity.EffectDamage import EffectDamage
from Entity.EnumMedic import EnumMedic


class Medic:
    def __init__(self, effects_damage=None, **props):
        self._StackMaxSize = (
            props.get(EnumMedic.STACKMAXSIZE.label, None),
            EnumMedic.STACKMAXSIZE.label
        )
        self._StackObjectsCount = (
            props.get(EnumMedic.STACKOBJECTSCOUNT.label, None),
            EnumMedic.STACKOBJECTSCOUNT.label
        )
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
        self._effects_damage = EffectDamage.from_data(effects_damage)

    @property
    def StackMaxSize(self):
        return self._StackMaxSize

    @property
    def StackObjectsCount(self):
        return self._StackObjectsCount

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

    @classmethod
    def from_data(cls, data: dict):
        effects_damage = data.get("effects_damage", {})
        props = {k: v for k, v in data.items() if k != "effects_damage"}
        return cls(effects_damage=effects_damage, **props)
    def get_instance_attributes(self):
        return vars(self)

    def get_attribute_value(self, attr_name):
        return getattr(self, attr_name, None)

    def get_value_by_label(self, label):
        for attr_name in self.get_instance_attributes():
            attr_value = self.get_attribute_value(attr_name)
            if isinstance(attr_value, tuple) and len(attr_value) == 2:
                numeric_value, attr_label = attr_value
                if attr_label == label:
                    return numeric_value
        raise ValueError(f"Le label '{label}' n'a pas été trouvé dans Medic.")

    def __iter__(self):
        return (key for key in self.__dict__.keys())
