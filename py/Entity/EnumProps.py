from enum import Enum

class EnumProps(Enum):
    CAMERA_SNAP = "CameraSnap", "Speed Camera Movement During Recoil"
    AIM_SENSITIVITY = "AimSensitivity", "Aiming Sensitivity"
    ERGONOMICS = "Ergonomics", "Ergonomics Value"
    RECOIL_CAMERA = "RecoilCamera", "Upward Camera Kick On Shoot"
    RECOL_DISPERSION = "RecolDispersion", "Determines bullet spread when firing"
    RECOIL_FORCE_BACK = "RecoilForceBack", "Horizontal recoil"
    RECOIL_FORCE_UP = "RecoilForceUp", "Vertical recoil"
    WEIGHT = "Weight", "Weapon Weight"
    AMMO_CALIBER = "ammoCaliber", "Calibers of Ammo"
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

    @classmethod
    def get_label_by_code(cls, code):
        for prop in cls:
            if prop.code == code:
                return prop.label
        raise ValueError(f"Aucun 'code' trouvé pour le label : {code}")

    def __str__(self):
        return f"{self.label} ({self.code})"

