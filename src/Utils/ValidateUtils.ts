export class ValidateUtils {

    /**
     * Validates and casts a value to a float with a specified number of decimal places.
     * Returns `null` if the value is invalid, zero, or not a number.
     * @param value The value to check
     * @param decimal Number of decimal places
     * @returns The formatted float or `null` if invalid
     */
    public validateAndCastFloat(value: any, decimal: number): number | null {

        if (typeof value !== "number" || isNaN(value) || value <= 0) {
            return null;
        }

        return parseFloat(value.toFixed(decimal));
    }

    /**
     * Validates and casts a value to an integer **only if it's not already an integer**.
     * Returns null if the value is invalid or zero.
     * @param value The value to check
     * @returns The formatted integer or `null` if invalid
     */
    public validateAndCastInt(value: any): number | null {
        if (typeof value !== "number" || isNaN(value) || value === 0) {
            return null; // Mark as invalid
        }

        if (Number.isInteger(value)) {
            return value;
        }

        return Math.floor(value);
    }
    /**
     * Validates and casts a value to an integer **only if it's not already an integer**.
     * Returns null if the value is invalid.
     * Returns 0 if 0
     * @param value The value to check
     * @returns The formatted integer or if invalid
     */
    public validateAndCastIntNegatifCase(value: any): number | null {
        if (typeof value !== "number" || isNaN(value)) {
            return null;
        }
        if ( value === 0) {
            return 0;
        }

        if (Number.isInteger(value)) {
            return value;
        }

        return Math.floor(value);
    }


    /**
     * We deal with Ballistic * 1000 on Python GUI
     */
    public validateIntToFloatFromValueWithThousandMulti(value: number): number | null {
        if (typeof value !== "number" || isNaN(value)) {
            return null;
        }
        else if (value < 10) {
            return 0.01
        }
        else if (value > 501) {
            return 0.501
        }

        const result = value / 1000;

        let decimalPlaces = 3;

        if (value >= 100 && value <= 500) {

            if (value % 100 === 0) {
                decimalPlaces = 1;
            } else if (value % 10 === 0) {
                decimalPlaces = 2;
            }

        } else if (value >= 10 && value <= 99) {

            if (value % 10 === 0) {
                decimalPlaces = 2;
            }
        }

        return parseFloat(result.toFixed(decimalPlaces));
    }

    /**
     * We deal with BulletMassGram * 100 on Python GUI
     */
    public validateBulletMassGram(value: number): number | null {
        if (typeof value !== "number" || isNaN(value)) {
            return null;
        }
        else if (value > 8001) {
            return 80.0
        }
        else if (value <= 8) {
            return 0.08
        }

        const result = value / 100;

        let decimalPlaces = 2;
        if (value % 100 === 0 || value % 10 === 0) {
            decimalPlaces = 1;
        }
        return parseFloat(result.toFixed(decimalPlaces));
    }

    public validateTracerColor(value: any): string {
        if (typeof value === "boolean") {
            return value ? "tracerGreen" : "red";
        }

        if (typeof value !== "string") {
            return "red";
        }

        return value.trim() !== "" ? value : "red";
    }

    public validateBoolean(value: any): boolean | null {
        if (typeof value === "boolean") {
            return value;
        }
        return null;
    }

    /**
     * Validates and casts a value to a float (max 2 decimal places) **only if it's not already a float**.
     * Returns `null` if the value is invalid or zero.
     * @param value The value to check
     * @param decimal decimal number
     * @returns The formatted float or `null` if invalid
     */
    public validateAndCastFloatItem(value: any, decimal: number): number | null {
        if (typeof value !== "number" || isNaN(value) || value === 0) {
            return null;
        }

        if (!Number.isInteger(value)) {
            return value;
        }

        return parseFloat(value.toFixed(decimal));
    }

}
