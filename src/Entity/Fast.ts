export class Fast {
    fastload: boolean;
    sizeBag: number;
    sizeMag: number;
    stimNumber: number;
    moreHealHp: number;
    ammoTracer: boolean;
    slotMag: boolean;


    constructor(fast: Fast) {
        Object.assign(this, fast);
    }
}
export function createFast(data: any): Fast {
    return new Fast({
        fastload: data.fastload,
        sizeBag: data.sizeBag,
        sizeMag: data.sizeMag,
        stimNumber: data.stimNumber,
        moreHealHp: data.moreHealHp,
        ammoTracer: data.ammoTracer,
        slotMag: data.slotMag,

    });
}
