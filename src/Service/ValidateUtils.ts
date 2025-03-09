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
}
