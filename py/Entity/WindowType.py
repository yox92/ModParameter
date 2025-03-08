from enum import Enum

# use when methode share by différents class to know where the value come from
class WindowType(Enum):
    WEAPON = "weapon"
    CALIBER = "caliber"
    AMMO = "ammo"
