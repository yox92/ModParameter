from msilib.schema import Property

from Entity.EnumMedic import EnumMedic


class Medic:
    def __init__(self, **props):
        self._StackMaxSize = (
            props.get(EnumMedic.StackMaxSize.label, None),
            EnumMedic.StackMaxSize.label
        )
        self._StackObjectsCount = (
            props.get(EnumMedic.StackObjectsCount.label, None),
            EnumMedic.StackObjectsCount.label
        )
        self._MaxHpResource = (
            props.get(EnumMedic.MaxHpResource.label, None),
            EnumMedic.MaxHpResource.label
        )
        self._hpResourceRate = (
            props.get(EnumMedic.hpResourceRate.label, None),
            EnumMedic.hpResourceRate.label
        )
        self._medUseTime = (
            props.get(EnumMedic.medUseTime.label, None),
            EnumMedic.medUseTime.label
        )
        self._medUseTime = (
            props.get(EnumMedic.effects_damage.label, None),
            EnumMedic.effects_damage.label
        )

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
        def medUseTime(self):
            return self._medUseTime

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
        raise ValueError(f"Le label '{label}' n'a pas été trouvé dans Ammo.")

    def __iter__(self):
        return (key for key in self.__dict__.keys())
