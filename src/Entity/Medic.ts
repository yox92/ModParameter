import {IEffectDamageProps, IEffectsDamage} from "@spt/models/eft/common/tables/ITemplateItem";

export class Medic {
    StackMaxSize: number;
    StackObjectsCount: number;
    MaxHpResource: number;
    hpResourceRate: number;
    medUseTime: number;
    effects_damage: IEffectsDamage[];
    constructor(medic: Partial<Medic>) {
        Object.assign(this, medic);
    }
}
export function createMedic(data: any): Medic {
    return new Medic({

    })
}