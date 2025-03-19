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

    public validateValidationFireRate(value: any): number | null {
        let intValue = Number(value);
        if (isNaN(intValue) || intValue < 0) {
            return null;
        }

        intValue = Math.floor(intValue);

        if (intValue === 0) {
            return 50;
        }

        const remainder = intValue % 50;

        if (remainder < 25) {
            intValue -= remainder;
        } else {
            intValue += (50 - remainder);
        }

        return intValue;
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
        if (value === 0) {
            return 0;
        }

        if (Number.isInteger(value)) {
            return value;
        }

        return Math.floor(value);
    }


    /**
     * Converts an integer value into a float by applying a division factor.
     * - Ensures the input is valid before processing.
     * - Applies a division by a thousand multiplier to obtain the float value.
     * - Adjusts precision if needed to maintain expected formatting.
     */
    public validateIntToFloatFromValueWithThousandMulti(value: number): number | null {
        if (typeof value !== "number" || isNaN(value)) {
            return null;
        } else if (value < 10) {
            return 0.01
        } else if (value > 501) {
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
     * Validates and adjusts the mass of a bullet in grams.
     * - Returns `null` if the input is not a number.
     * - Limits the value to a minimum of 0.08 and a maximum of 80.0.
     * - Converts the value to grams by dividing by 100.
     * - Adjusts decimal precision based on input value.
     */
    public validateBulletMassGram(value: number): number | null {
        if (typeof value !== "number" || isNaN(value)) {
            return null;
        } else if (value > 8001) {
            return 80.0
        } else if (value <= 8) {
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
