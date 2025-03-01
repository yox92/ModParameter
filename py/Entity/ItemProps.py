class ItemProps:
    def __init__(self, **props):
        self.CameraSnap = props.get('CameraSnap', None)
        self.AimSensitivity = props.get('AimSensitivity', None)
        self.Ergonomics = props.get('Ergonomics', None)
        self.RecoilCamera = props.get('RecoilCamera', None)
        self.RecoilForceBack = props.get('RecoilForceBack', None)
        self.RecoilForceUp = props.get('RecoilForceUp', None)
        self.Weight = props.get('Weight', None)
        self.bFirerate = props.get('bFirerate', None)

    def get_property(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            raise AttributeError(f"Property '{name}' does not exist in ItemProps")

    def set_property(self, name, value):
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            raise AttributeError(f"Property '{name}' does not exist in ItemProps")

    def get_CameraSnap(self):
        return self.CameraSnap

    def set_CameraSnap(self, CameraSnap):
        self.CameraSnap = CameraSnap

    def get_AimSensitivity(self):
        return self.AimSensitivity

    def set_AimSensitivity(self, AimSensitivity):
        self.AimSensitivity = AimSensitivity

    def get_Ergonomics(self):
        return self.Ergonomics

    def set_Ergonomics(self, Ergonomics):
        self.Ergonomics = Ergonomics

    def get_RecoilCamera(self):
        return self.RecoilCamera

    def set_RecoilCamera(self, RecoilCamera):
        self.RecoilCamera = RecoilCamera

    def get_RecoilForceBack(self):
        return self.RecoilForceBack

    def set_RecoilForceBack(self, RecoilForceBack):
        self.RecoilForceBack = RecoilForceBack

    def get_RecoilForceUp(self):
        return self.RecoilForceUp

    def set_RecoilForceUp(self, RecoilForceUp):
        self.RecoilForceUp = RecoilForceUp

    def get_Weight(self):
        return self.Weight

    def set_Weight(self, Weight):
        self.Weight = Weight

    def get_bFirerate(self):
        return self.bFirerate

    def set_bFirerate(self, bFirerate):
        self.bFirerate = bFirerate

    def __repr__(self):
        return (f"ItemProps(CameraSnap={self.CameraSnap}, AimSensitivity={self.AimSensitivity}, "
                f"Ergonomics={self.Ergonomics}, RecoilCamera={self.RecoilCamera}, "
                f"RecoilForceBack={self.RecoilForceBack}, RecoilForceUp={self.RecoilForceUp}, "
                f"Weight={self.Weight}, bFirerate={self.bFirerate})")

    @classmethod
    def from_data(cls, data: dict):
        return cls(
            CameraSnap=data.get("CameraSnap"),
            AimSensitivity=data.get("AimSensitivity"),
            Ergonomics=data.get("Ergonomics"),
            RecoilCamera=data.get("RecoilCamera"),
            RecoilForceBack=data.get("RecoilForceBack"),
            RecoilForceUp=data.get("RecoilForceUp"),
            Weight=data.get("Weight"),
            bFirerate=data.get("bFirerate")
        )
