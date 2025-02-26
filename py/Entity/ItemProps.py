class ItemProps:
    def __init__(self, **props):
        self.CameraSnap = props.get('CameraSnap')
        self.AimSensitivity = props.get('AimSensitivity')
        self.Ergonomics = props.get('Ergonomics')
        self.RecoilCamera = props.get('RecoilCamera')
        self.RecoilForceBack = props.get('RecoilForceBack')
        self.RecoilForceUp = props.get('RecoilForceUp')
        self.Weight = props.get('Weight')
        self.bFirerate = props.get('bFirerate')

def create_item_props(data):
    return ItemProps(
        CameraSnap=data.get('CameraSnap'),
        AimSensitivity=data.get('AimSensitivity'),
        Ergonomics=data.get('Ergonomics'),
        RecoilCamera=data.get('RecoilCamera'),
        RecoilForceBack=data.get('RecoilForceBack'),
        RecoilForceUp=data.get('RecoilForceUp'),
        Weight=data.get('Weight'),
        bFirerate=data.get('bFirerate')
    )
