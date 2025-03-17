export class EnumUtils {
    static getAllValues<T>(enumObj: T): string[] {
        return Object.values(enumObj);
    }

    static getEnumKeyByValue<T>(enumObj: T, value: string): string | undefined {
        return Object.keys(enumObj).find(key => (enumObj as any)[key] === value);
    }

    static getValueByKey<T>(enumObj: T, key: string): string | undefined {
        return (enumObj as any)[key];
    }
}