export class Ammo {
    ArmorDamage: number;
    Caliber: string;
    Damage: number;
    InitialSpeed: number;
    PenetrationPower: number;
    StackMaxSize: number;
    Tracer: boolean;
    constructor(props: Partial<Ammo>) {
        Object.assign(this, props);
    }
}
export function createItemAmmo(data: any): Ammo {
    return new Ammo({
    ArmorDamage: data.ArmorDamage,
    Caliber: data.Caliber,
    Damage: data.Damage,
    InitialSpeed: data.InitialSpeed,
    PenetrationPower: data.PenetrationPower,
    StackMaxSize: data.StackMaxSize,
    Tracer: data.Tracer,
    });
}