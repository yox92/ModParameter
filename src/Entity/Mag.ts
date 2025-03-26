export class Mag {
    name: string;
    counts: number;
    penality: boolean;
    resize: boolean;
    fastLoad: boolean;
    ids: string[];

    constructor(aiming: Mag) {
        Object.assign(this, aiming);
    }
}
export function createMag(data: any): Mag {
    return new Mag({
        name: data.name,
        counts: data.counts,
        penality: data.penality,
        resize: data.resize,
        fastLoad: data.resize,
        ids: data.ids,
    });
}
