import {IEffectDamageProps} from "@spt/models/eft/common/tables/ITemplateItem";

export class Medic {
    StackMaxSize: number;
    StackObjectsCount: number;
    MaxHpResource: number;
    hpResourceRate: number;
    medUseTime: number;
    effects_damage: Record<string, IEffectDamageProps>;

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

    })
}