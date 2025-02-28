import {Locale} from "./Locale";
import {Item} from "./Item";

export class Root {
    locale: Locale;
    item: Item;

    constructor(locale: Locale, item: Item) {
        this.locale = locale;
        this.item = item;
    }
}