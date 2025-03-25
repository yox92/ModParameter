from enum import Enum

class EnumMedic(Enum):
    STACKMAXSIZE = ("StackMaxSize","Max number")
    STACKOBJECTSCOUNT = ("StackObjectsCount","??")
    MAXHPRESOURCE = ("MaxHpResource","Usage number")
    HPRESOURCERATE = ("hpResourceRate","Hp regen on usage")
    MEDUSETIME = ("medUseTime","time to use medic (seconds)")
    EFFECTS_DAMAGE = ("effects_damage","")

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
