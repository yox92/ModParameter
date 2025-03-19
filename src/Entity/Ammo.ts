export class Ammo {
    ArmorDamage: number;
    Caliber: string;
    Damage: number;
    InitialSpeed: number;
    PenetrationPower: number;
    StackMaxSize: number;
    Tracer: boolean;
    TracerColor: string;
    BallisticCoeficient: number;
    BulletMassGram: number;
    ProjectileCount: number;
    ammoAccr: number;
    ammoRec: number;
    ExplosionStrength: number;
    MaxExplosionDistance: number;
    FuzeArmTimeSec: number;
    BackgroundColor: string;
    buckshotBullets: number;

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
    TracerColor: data.TracerColor,
    BallisticCoeficient: data.BallisticCoeficient,
    BulletMassGram: data.BulletMassGram,
    ProjectileCount: data.ProjectileCount,
    ammoAccr: data.ammoAccr,
    ammoRec: data.ammoRec,
    ExplosionStrength: data.ExplosionStrength,
    MaxExplosionDistance: data.MaxExplosionDistance,
    FuzeArmTimeSec: data.FuzeArmTimeSec
    });
}