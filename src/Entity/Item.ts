import { ItemProps } from "./ItemProps";
export class Item {
    _id: string;
    _name: string;
    _parent: string;
    _props: ItemProps;

    constructor(id: string, name: string, parent: string, props: ItemProps) {
        this._id = id;
        this._name = name;
        this._parent = parent;
        this._props = props;
    }
}