from enum import Enum

class EnumMedic(Enum):
    MAXHPRESOURCE = ("MaxHpResource","Usage number (0-10000)")
    HPRESOURCERATE = ("hpResourceRate","Hp regen on usage (0-1000)")
    MEDUSETIME = ("medUseTime","time to use medic (seconds) (1-20)")
    PRICEFACTOR = "priceFactor", "multiply price. (2 = x2 etc)  (0,01-100)"
    EFFECTS_DAMAGE = ("effects_damage","Effect medic item :")

    @property
    def label(self):
        return self.value[0]

    @property
    def code(self):
        return self.value[1]

    @classmethod
    def get_code_by_label(cls, label):
        for prop in cls:
            if prop.label == label:
                return prop.code
        raise ValueError(f"Aucun 'code' trouvé pour le label : {label}")

    @classmethod
    def get_label_by_code(cls, code):
        for prop in cls:
            if prop.code == code:
                return prop.label
        raise ValueError(f"Aucun 'code' trouvé pour le label : {code}")

    def __str__(self):
        return f"{self.label} ({self.code})"
