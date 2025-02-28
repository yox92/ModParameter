import {Locale} from "./Locale";
import {Item} from "./Item";

export class WeaponJson {
    Locale: Locale;
    Item: Item;

    constructor(locale: Locale, item: Item) {
        this.Locale = locale;
        this.Item = item;
    }
}