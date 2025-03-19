export class Aiming {
    AimPunchMagnitude: number;
    ProceduralIntensityByPoseStanding: number;
    ProceduralIntensityByPoseCrouching: number;
    ProceduralIntensityByPoseProne: number;
    RecoilDamping: number;
    RecoilHandDamping: number;
    RecoilIntensityStanding: number;
    RecoilIntensityCrouching: number;
    RecoilIntensityProne: number;
    AimProceduralIntensity: number;
    constructor(aiming: Partial<Aiming>) {
        Object.assign(this, aiming);
    }
}
export function createAiming(data: any): Aiming {
    return new Aiming({
        AimPunchMagnitude: data.AimPunchMagnitude,
        ProceduralIntensityByPoseStanding: data.ProceduralIntensityByPoseStanding,
        ProceduralIntensityByPoseCrouching: data.ProceduralIntensityByPoseCrouching,
        ProceduralIntensityByPoseProne: data.ProceduralIntensityByPoseProne,
        RecoilDamping: data.RecoilDamping,
        RecoilHandDamping: data.RecoilHandDamping,
        RecoilIntensityStanding: data.RecoilIntensityStanding,
        RecoilIntensityCrouching: data.RecoilIntensityCrouching,
        RecoilIntensityProne: data.RecoilIntensityProne,
        AimProceduralIntensity: data.AimProceduralIntensity,
    });
}
