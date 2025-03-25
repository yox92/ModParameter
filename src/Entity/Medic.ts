
export class Medic {
    StackMaxSize: number;
    StackObjectsCount: number;
    MaxHpResource: number;
    hpResourceRate: number;
    medUseTime: number;
    BackgroundColor: string;
    effects_damage: Record<string, IEffectDamageProps>;
    priceFactor: number

    constructor(medic: Partial<Medic>) {
        Object.assign(this, medic);
    }
}

export function createMedic(data: any): Medic {
    return new Medic({
        StackMaxSize: data.StackMaxSize,
        StackObjectsCount: data.StackObjectsCount,
        MaxHpResource: data.MaxHpResource,
        hpResourceRate: data.hpResourceRate,
        medUseTime: data.medUseTime,
        effects_damage: data.effects_damage,
        priceFactor: data.priceFactor
    })
}

export interface IEffectDamageProps {
    delay: number;
    duration: number;
    fadeOut: number;
    cost?: number;
    healthPenaltyMin?: number;
    healthPenaltyMax?: number;
}
