import { ItemProps } from "./ItemProps";
import {Ammo} from "./Ammo";
import {Medic} from "./Medic";
export class Item<T extends ItemProps | Ammo | Medic> {
    _id: string;
    _name: string;
    _parent: string;
    _props: T;

    constructor(id: string, name: string, props: T, parent: string) {
        this._id = id;
        this._name = name;
        this._props = props;
        this._parent = parent;
    }
}