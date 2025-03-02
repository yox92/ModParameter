from enum import Enum
class EnumProps(Enum):
    CAMERA_SNAP = "CameraSnap", "Speed Camera Movement During Recoil"
    AIM_SENSITIVITY = "AimSensitivity", "Aiming Sensitivity"
    ERGONOMICS = "Ergonomics", "Ergonomics Value"
    RECOIL_CAMERA = "RecoilCamera", "Upward Camera Kick On Shoot"
    RECOIL_FORCE_BACK = "RecoilForceBack", "Horizontal recoil"
    RECOIL_FORCE_UP = "RecoilForceUp", "Vertical recoil"
    VELOCITY = "Velocity", "Bullet Velocity"
    WEIGHT = "Weight", "Weapon Weight"
    AMMO_CALIBER = "ammoCaliber", "Caliber of Ammo"
    FIRE_RATE = "bFirerate", "Rate of Fire"

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

    def __str__(self):
        return f"{self.label} ({self.code})"
