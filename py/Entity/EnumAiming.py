from enum import Enum

class EnumAiming(Enum):
    AIM_PUNCH_MAGNITUDE = "AimPunchMagnitude", "Lower value decrease aim displacement when hit."

    PROCEDURAL_INTENSITY_BY_POSE_STANDING = ("ProceduralIntensityByPoseStanding",
                                             "Lower value reduces weapon sway when \n "
                                             " aiming while standing")

    PROCEDURAL_INTENSITY_BY_POSE_CROUCHING = ("ProceduralIntensityByPoseCrouching",
                                              "Lower value reduces weapon sway when "
                                              "\n aiming while crouching")

    PROCEDURAL_INTENSITY_BY_POSE_PRONE = ("ProceduralIntensityByPoseProne",
                                          ("Lower value reduces weapon sway "
                                           "when \n aiming while prone"))

    RECOIL_DAMPING = ("RecoilDamping",
                      ("Lower value reduces vertical gun movement \n"
                       "animation when firing"))
    RECOIL_HAND_DAMPING = ("RecoilHandDamping",
                           ("Lower value reduces effect visual forward and \n "
                            "backward gun movement when firing"))

    RECOIL_INTENSITY_BY_POSE_STANDING = ("RecoilIntensityStanding",
                                         "Lower value reduces recoil while standing")
    RECOIL_INTENSITY_BY_POSE_CROUCHING = ("RecoilIntensityCrouching",
                                          "Lower value reduces recoil while crouching")
    RECOIL_INTENSITY_BY_POSE_PRONE = ("RecoilIntensityProne",
                                      "Lower value reduces recoil while prone")

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
        raise ValueError(f"Aucun 'code' trouvé pour le label : {label}")

    def __str__(self):
        return f"{self.label} ({self.code})"

