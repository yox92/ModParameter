export class Stamina {
    SprintDrainRate: number;
    JumpConsumption: number;
    StandupConsumption: number;
    BaseRestorationRate: number;
    AimDrainRate: number;

    constructor(stamina: Partial<Stamina>) {
        Object.assign(this, stamina);
    }
}
export function createStamina(data: any): Stamina {
    return new Stamina({
        SprintDrainRate: data.SprintDrainRate,
        JumpConsumption: data.JumpConsumption,
        StandupConsumption: data.StandupConsumption,
        BaseRestorationRate: data.BaseRestorationRate,
        AimDrainRate: data.AimDrainRate
    });
}