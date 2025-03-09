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

    public validateString(value: any, isTracerColor: boolean = false): string | null {
        if (isTracerColor) {
            if (typeof value === "boolean") {
                return value ? "green" : "red";
            }
        }

        if (typeof value !== "string") {
            return null;
        }

        return value.trim() !== "" ? value : null;
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
