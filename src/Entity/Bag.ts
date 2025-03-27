export class Bag {
    id: string;
    name: string;
    Grids: Record<string, IGridJson>;

    constructor(id: string, name: string, grids: Record<string, IGridJson>) {
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
    resize: number;
    excludedFilter: boolean;
    ids: Record<string, Bag>;

    constructor(size: number, penality: boolean, resize: number, excludedFilter: boolean, ids: Record<string, Bag>) {
        this.size = size;
        this.penality = penality;
        this.excludedFilter = excludedFilter;
        this.resize = resize;
        this.ids = ids;
    }

    static fromJson(data: any): BagCat {
        if (!data || typeof data !== "object" || !data.ids) {
            throw new Error("Invalid BagCat JSON structure");
        }

        const ids: Record<string, Bag> = {};
        for (const [bagId, bagData] of Object.entries(data.ids)) {
            ids[bagId] = Bag.fromJson(bagId, bagData);
        }

        return new BagCat(data.size, data.penality, data.excludedFilter, data.resize, ids);
    }
}

export interface IGridJson {
    cellsH: number;
    cellsV: number;
}

export interface IBagJson {
    name: string;
    Grids: Record<string, IGridJson>;
}

export interface IBagCatJson {
    size: number;
    penality: boolean;
    resize: boolean;
    excludedFilter: boolean;
    ids: Record<string, IBagJson>;
}