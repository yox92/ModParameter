from enum import Enum


class EnumAiming(Enum):
    PROCEDURAL_INTENSITY_BY_POSE_STANDING = ("ProceduralIntensityByPoseStanding",
                                             "Lower value reduces BREATHING sway when \n "
                                             " aiming while STANDING")

    PROCEDURAL_INTENSITY_BY_POSE_CROUCHING = ("ProceduralIntensityByPoseCrouching",
                                              "Lower value reduces BREATHING sway when "
                                              "\n aiming while CROUCHING")

    PROCEDURAL_INTENSITY_BY_POSE_PRONE = ("ProceduralIntensityByPoseProne",
                                          ("Lower value reduces BREATHING sway "
                                           "when \n aiming while PRONE"))
    RECOIL_INTENSITY_BY_POSE_STANDING = ("RecoilIntensityStanding",
                                         "Lower value reduces RECOIL while STANDING")
    RECOIL_INTENSITY_BY_POSE_CROUCHING = ("RecoilIntensityCrouching",
                                          "Lower value reduces RECOIL while CROUCHING")
    RECOIL_INTENSITY_BY_POSE_PRONE = ("RecoilIntensityProne",
                                      "Lower value reduces RECOIL while PRONE")

    AIM_PUNCH_MAGNITUDE = "AimPunchMagnitude", "Lower value decrease aim displacement when hit."

    RECOIL_DAMPING = ("RecoilDamping",
                      ("Lower value reduces vertical gun movement \n"
                       "animation when firing"))
    RECOIL_HAND_DAMPING = ("RecoilHandDamping",
                           ("Lower value reduces effect visual forward and \n "
                            "backward gun movement when firing"))

    AIM_PROCEDURAL_INTENSITY = ("AimProceduralIntensity",
                                "Lower value reduces movement \n while walking on aiming")
    STAMINA_DRAIN = ("AimDrainRate",
                                "Lower value reduces Consumption \n Blue stamina when you Aiming")
    STAMINA_SPRINT = ("SprintDrainRate",
                                "Lower value reduces Consumption \n Green stamina when you Sprint")
    STAMINA_JUMP = ("JumpConsumption",
                                "Lower value reduces Consumption \n Green stamina when you JumP")
    STAMINA_STANDUP = ("StandupConsumption",
                                "Lower value reduces Consumption \n Green stamina when you stand-uP")
    STAMINA_RESTORATION = ("BaseRestorationRate",
                                "Upper value improve  \n Green stamina Restoration")

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
