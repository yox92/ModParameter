import { ItemProps } from "./ItemProps";
import {Ammo} from "./Ammo";
export class Item<T extends ItemProps | Ammo> {
    _id: string;
    _name: string;
    _props: T;

    constructor(id: string, name: string, props: T) {
        this._id = id;
        this._name = name;
        this._props = props;
    }
}