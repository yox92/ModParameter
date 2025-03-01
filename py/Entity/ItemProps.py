class ItemProps:
    def __init__(self, **props):
        self._CameraSnap = props.get('CameraSnap', None)
        self._AimSensitivity = props.get('AimSensitivity', None)
        self._Ergonomics = props.get('Ergonomics', None)
        self._RecoilCamera = props.get('RecoilCamera', None)
        self._RecoilForceBack = props.get('RecoilForceBack', None)
        self._RecoilForceUp = props.get('RecoilForceUp', None)
        self._Velocity = props.get('Velocity', None)
        self._Weight = props.get('Weight', None)
        self._ammoCaliber = props.get('ammoCaliber', None)
        self._bFirerate = props.get('bFirerate', None)

    @property
    def CameraSnap(self):
        return self._CameraSnap

    @property
    def AimSensitivity(self):
        return self.AimSensitivity

    @property
    def Ergonomics(self):
        return self.Ergonomics

    @property
    def RecoilCamera(self):
        return self.RecoilCamera

    @property
    def RecoilForceBack(self):
        return self.RecoilForceBack

    @property
    def RecoilForceUp(self):
        return self.RecoilForceUp

    @property
    def Velocity(self):
        return self.Velocity

    @property
    def Weight(self):
        return self.Weight

    @property
    def ammoCaliber(self):
        return self.Weight

    @property
    def bFirerate(self):
        return self.bFirerate

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)

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
        """Permet d'itérer sur les noms des attributs."""
        return (key for key in self.__dict__.keys())


