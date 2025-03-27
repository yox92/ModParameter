export class Bag {
    id: string;
    name: string;
    Grids: Record<string, IGrid>;

    constructor(id: string, name: string, grids: Record<string, IGrid>) {
        this.id = id;
        this.name = name;
        this.Grids = grids;
    }

    static fromJson(id: string, data: any): Bag {
        return new Bag(id, data.name, data.Grids);
    }
}

export class BagCat {
    size: number;
    penality: boolean;
    resize: boolean;
    ids: Record<string, Bag>;

    constructor(size: number, penality: boolean, resize: boolean, ids: Record<string, Bag>) {
        this.size = size;
        this.penality = penality;
        this.resize = resize;
        this.ids = ids;
    }

    static fromJson(data: any): BagCat {
        const ids: Record<string, Bag> = {};
        for (const [bagId, bagData] of Object.entries(data.ids)) {
            ids[bagId] = Bag.fromJson(bagId, bagData);
        }

        return new BagCat(data.size, data.penality, data.resize, ids);
    }
}

export interface IGrid {
    cellsH: number;
    cellsV: number;
}

export interface IBagJson {
    name: string;
    Grids: Record<string, IGrid>;
}

export interface IBagCatJson {
    size: number;
    penality: boolean;
    resize: boolean;
    ids: Record<string, IBagJson>;
}