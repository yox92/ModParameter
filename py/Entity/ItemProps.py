from Entity.EnumProps import EnumProps

class ItemProps:
    def __init__(self, **props):
        self._CameraSnap = (
            props.get(EnumProps.CAMERA_SNAP.label, None),
            EnumProps.CAMERA_SNAP.label
        )
        self._AimSensitivity = (
            props.get(EnumProps.AIM_SENSITIVITY.label, None),
            EnumProps.AIM_SENSITIVITY.label
        )
        self._Ergonomics = (
            props.get(EnumProps.ERGONOMICS.label, None),
            EnumProps.ERGONOMICS.label
        )
        self._RecoilCamera = (
            props.get(EnumProps.RECOIL_CAMERA.label, None),
            EnumProps.RECOIL_CAMERA.label
        )
        self._RecolDispersion = (
            props.get(EnumProps.RECOL_DISPERSION.label, None),
            EnumProps.RECOL_DISPERSION.label
        )
        self._RecoilForceBack = (
            props.get(EnumProps.RECOIL_FORCE_BACK.label, None),
            EnumProps.RECOIL_FORCE_BACK.label
        )
        self._RecoilForceUp = (
            props.get(EnumProps.RECOIL_FORCE_UP.label, None),
            EnumProps.RECOIL_FORCE_UP.label
        )
        self._Weight = (
            props.get(EnumProps.WEIGHT.label, None),
            EnumProps.WEIGHT.label
        )
        self._ammoCaliber = (
            props.get(EnumProps.AMMO_CALIBER.label, None),
            EnumProps.AMMO_CALIBER.label
        )
        self._bFirerate = (
            props.get(EnumProps.FIRE_RATE.label, None),
            EnumProps.FIRE_RATE.label
        )

    @property
    def CameraSnap(self):
        return self._CameraSnap

    @property
    def AimSensitivity(self):
        return self._AimSensitivity

    @property
    def Ergonomics(self):
        return self._Ergonomics

    @property
    def RecoilCamera(self):
        return self._RecoilCamera

    @property
    def RecoilForceBack(self):
        return self._RecoilForceBack

    @property
    def RecoilForceUp(self):
        return self._RecoilForceUp

    @property
    def RecolDispersion(self):
        return self._RecolDispersion

    @property
    def Weight(self):
        return self._Weight

    @property
    def ammoCaliber(self):
        return self._Weight

    @property
    def bFirerate(self):
        return self._bFirerate

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
        raise ValueError(f"Le label '{label}' n'a pas été trouvé dans ItemProps.")

    def __repr__(self):
        return (f"ItemProps("
                f"CameraSnap={self.CameraSnap}, "
                f"AimSensitivity={self.AimSensitivity}, "
                f"Ergonomics={self.Ergonomics}, "
                f"RecoilCamera={self.CameraSnap}, "
                f"RecoilForceBack={self.RecoilForceBack}, "
                f"RecoilForceUp={self.RecoilForceBack}, "
                f"Velocity={self.Velocity}, "
                f"Weight={self.Weight}, "
                f"ammoCaliber={self.ammoCaliber}, "
                f"bFirerate={self.bFirerate})")

    def __iter__(self):
        return (key for key in self.__dict__.keys())


