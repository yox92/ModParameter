import { Locale } from "./Locale";
import { Item } from "./Item";
import { ItemProps } from "./ItemProps";
import {Ammo} from "./Ammo";

export class Templates<T extends ItemProps | Ammo> {
    locale: Locale;
    item: Item<T>;

    constructor(locale: Locale, item: Item<T>) {
        this.locale = locale;
        this.item = item;
    }
}