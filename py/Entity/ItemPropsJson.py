class ItemPropsJson:
    def __init__(self, **props):
        self._CameraSnap = props.get("CameraSnap", None)
        self._AimSensitivity = props.get("AimSensitivity", None)
        self._Ergonomics = props.get("Ergonomics", None)
        self._RecoilCamera = props.get("RecoilCamera", None)
        self._RecoilForceBack = props.get("RecoilForceBack", None)
        self._RecoilForceUp = props.get("RecoilForceUp", None)
        self._Velocity = props.get("Velocity", None)
        self._Weight = props.get("Weight", None)
        self._ammoCaliber = props.get("ammoCaliber", None)
        self._bFirerate = props.get("bFirerate", None)

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
    def Velocity(self):
        return self._Velocity

    @property
    def Weight(self):
        return self._Weight

    @property
    def ammoCaliber(self):
        return self._ammoCaliber

    @property
    def bFirerate(self):
        return self._bFirerate

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return (f"ItemPropsEmpty("
                f"CameraSnap={self.CameraSnap}, "
                f"AimSensitivity={self.AimSensitivity}, "
                f"Ergonomics={self.Ergonomics}, "
                f"RecoilCamera={self.RecoilCamera}, "
                f"RecoilForceBack={self.RecoilForceBack}, "
                f"RecoilForceUp={self.RecoilForceUp}, "
                f"Velocity={self.Velocity}, "
                f"Weight={self.Weight}, "
                f"ammoCaliber={self.ammoCaliber}, "
                f"bFirerate={self.bFirerate})")
