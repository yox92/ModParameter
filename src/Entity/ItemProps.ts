export class ItemProps {
    CameraSnap: number;
    AimSensitivity: number;
    Ergonomics: number;
    RecoilCamera: number;
    RecoilForceBack: number;
    RecoilForceUp: number;
    RecolDispersion: number;
    Weight: number;
    ammoCaliber: string;
    bFirerate: number;
    BackgroundColor: string;
    priceFactor: number;

    constructor(props: Partial<ItemProps>) {
        Object.assign(this, props);
    }
}

export function createItemProps(data: any): ItemProps {
    return new ItemProps({
        CameraSnap: data.CameraSnap,
        AimSensitivity: data.AimSensitivity,
        Ergonomics: data.Ergonomics,
        RecoilCamera: data.RecoilCamera,
        RecoilForceBack: data.RecoilForceBack,
        RecoilForceUp: data.RecoilForceUp,
        RecolDispersion: data.RecolDispersion,
        Weight: data.Weight,
        ammoCaliber: data.ammoCaliber,
        bFirerate: data.bFirerate,
        priceFactor: data.priceFactor,
    });
}