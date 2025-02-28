import { ItemProps } from "./ItemProps";
export class Item {
    _id: string;
    _name: string;
    _props: ItemProps;

    constructor(id: string, name: string, props: ItemProps) {
        this._id = id;
        this._name = name;
        this._props = props;
    }
}