from Entity.EnumAiming import EnumAiming

class Aiming:
    def __init__(self, **props):
        self._AimPunchMagnitude = (
            props.get(EnumAiming.AIM_PUNCH_MAGNITUDE.label, None),
            EnumAiming.AIM_PUNCH_MAGNITUDE.label
        )
        self._ProceduralIntensityByPoseStanding = (
            props.get(EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_STANDING.label, None),
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_STANDING.label
        )
        self._ProceduralIntensityByPoseCrouching = (
            props.get(EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_CROUCHING.label, None),
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_CROUCHING.label
        )
        self._ProceduralIntensityByPoseProne = (
            props.get(EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_PRONE.label, None),
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_PRONE.label
        )
        self._RecoilDamping = (
            props.get(EnumAiming.RECOIL_DAMPING.label, None),
            EnumAiming.RECOIL_DAMPING.label
        )
        self._RecoilHandDamping = (
            props.get(EnumAiming.RECOIL_HAND_DAMPING.label, None),
            EnumAiming.RECOIL_HAND_DAMPING.label
        )
        self._RecoilIntensityStanding = (
            props.get(EnumAiming.RECOIL_INTENSITY_BY_POSE_STANDING.label, None),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_STANDING.label
        )
        self._RecoilIntensityCrouching = (
            props.get(EnumAiming.RECOIL_INTENSITY_BY_POSE_CROUCHING.label, None),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_CROUCHING.label
        )
        self._RecoilIntensityProne = (
            props.get(EnumAiming.RECOIL_INTENSITY_BY_POSE_PRONE.label, None),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_PRONE.label
        )

    @property
    def AimPunchMagnitude(self):
        return self._AimPunchMagnitude

    @property
    def ProceduralIntensityByPoseStanding(self):
        return self._ProceduralIntensityByPoseStanding

    @property
    def ProceduralIntensityByPoseCrouching(self):
        return self._ProceduralIntensityByPoseCrouching

    @property
    def ProceduralIntensityByPoseProne(self):
        return self._ProceduralIntensityByPoseProne

    @property
    def RecoilDamping(self):
        return self._RecoilDamping

    @property
    def RecoilHandDamping(self):
        return self._RecoilHandDamping

    @property
    def RecoilIntensityStanding(self):
        return self._RecoilIntensityStanding

    @property
    def RecoilIntensityCrouching(self):
        return self._RecoilIntensityCrouching

    @property
    def RecoilIntensityProne(self):
        return self._RecoilIntensityProne

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)

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
        raise ValueError(f"Le label '{label}' n'a pas été trouvé dans Aiming.")

    def __repr__(self):
        return (f"Aiming("
                f"AimPunchMagnitude={self.AimPunchMagnitude}, "
                f"ProceduralIntensityByPoseStanding={self.ProceduralIntensityByPoseStanding}, "
                f"ProceduralIntensityByPoseCrouching={self.ProceduralIntensityByPoseCrouching}, "
                f"ProceduralIntensityByPoseProne={self.ProceduralIntensityByPoseProne}, "
                f"RecoilDamping={self.RecoilDamping}, "
                f"RecoilHandDamping={self.RecoilHandDamping}, "
                f"RecoilIntensityStanding={self.RecoilIntensityStanding}, "
                f"RecoilIntensityCrouching={self.RecoilIntensityCrouching}, "
                f"RecoilIntensityProne={self.RecoilIntensityProne})")

    def __iter__(self):
        return (key for key in self.__dict__.keys())
