from enum import Enum

class EnumAmmo(Enum):
    ARMOR_DAMAGE = "ArmorDamage", "Armor damage inflicted 1-500"
    CALIBER = "Caliber", "Type of ammunition caliber"
    DAMAGE = "Damage", "Damage dealt to target 1-450"
    PENETRATION_POWER = "PenetrationPower", "Penetration power 1-70"
    STACK_MAX_SIZE = "StackMaxSize", "Maximum stack size in inventory 1-9999"
    TRACER = "Tracer", "Indicates (true, false) if the bullet is a tracer round"
    TRACERCOLOR = "TracerColor", "Color about tracer Green / Red"
    INITIAL_SPEED = "InitialSpeed", "Projectile speed at firing 100-2000"
    BALLISTIC_COEFICIENT = "BallisticCoeficient", "Ballistic coeficient (12-499)"
    BULLET_MASSGRAM = "BulletMassGram", "Bullet mass in centigrams (9-8001)"
    AMMO_ACCR = "ammoAccr", "Ammo accuracy (-200 - +500)"
    AMMO_REC = "ammoRec", "Recoil (-198 - +100)"
    PROJECTILE_COUNT = "ProjectileCount", "Projectile count (1-50)"

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
