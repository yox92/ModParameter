export class Locale {
    Name: string;
    ShortName: string;

    constructor(props: Partial<Locale>) {
        Object.assign(this, props);
    }
}
export function createLocale(data: any): Locale {
    return new Locale({
        Name: data.Name,
        ShortName: data.ShortName
    });
}