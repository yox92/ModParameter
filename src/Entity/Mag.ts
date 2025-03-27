export class Mag {
    name: string;
    counts: number;
    penality: boolean;
    resize: boolean;
    fastLoad: boolean;
    ids: string[];

    constructor(name: string, data: IMagJson) {
        this.name = name;
        this.counts = data.counts;
        this.penality = data.penality;
        this.resize = data.resize;
        this.fastLoad = data.fastLoad;
        this.ids = data.ids;
    }

    toJson(): IMagJson {
        return {
            counts: this.counts,
            penality: this.penality,
            resize: this.resize,
            fastLoad: this.fastLoad,
            ids: this.ids
        };
    }
}

export interface IMagJson {
    counts: number;
    penality: boolean;
    resize: boolean;
    fastLoad: boolean;
    ids: string[];
}
export type MagJsonFile = Record<string, IMagJson>;