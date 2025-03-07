from enum import Enum

class EnumAmmo(Enum):
    ARMOR_DAMAGE = "ArmorDamage", "Armor damage inflicted"
    CALIBER = "Caliber", "Type of ammunition caliber"
    DAMAGE = "Damage", "Damage dealt to target"
    INITIAL_SPEED = "InitialSpeed", "Projectile speed at firing"
    PENETRATION_POWER = "PenetrationPower", "Penetration power"
    STACK_MAX_SIZE = "StackMaxSize", "Maximum stack size in inventory"
    TRACER = "Tracer", "Indicates (true, false) if the bullet is a tracer round"

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
        raise ValueError(f"No 'code' found for the label: {label}")

    @classmethod
    def get_label_by_code(cls, code):
        for prop in cls:
            if prop.code == code:
                return prop.label
        raise ValueError(f"No 'label' found for the code: {code}")

    def __str__(self):
        return f"{self.label} ({self.code})"
