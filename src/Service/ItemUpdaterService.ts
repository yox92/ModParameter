import {ILogger} from "../Entity/Logger";
import {createItemProps} from "../Entity/ItemProps";


export class ItemUpdaterService {
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.logger = logger;
    }

    /**
     * Validates and casts a value to an integer **only if it's not already an integer**.
     * Returns null if the value is invalid or zero.
     * @param value The value to check
     * @returns The formatted integer or `null` if invalid
     */
    private validateAndCastInt(value: any): number | null {
        if (typeof value !== "number" || isNaN(value) || value === 0) {
            return null; // Mark as invalid
        }

        if (Number.isInteger(value)) {
            return value;
        }

        return Math.floor(value);
    }

    /**
     * Validates and casts a value to a float (max 2 decimal places) **only if it's not already a float**.
     * Returns `null` if the value is invalid or zero.
     * @param value The value to check
     * @param decimal decimal number
     * @returns The formatted float or `null` if invalid
     */
    private validateAndCastFloat(value: any, decimal: number): number | null {
        if (typeof value !== "number" || isNaN(value) || value === 0) {
            return null;
        }

        if (!Number.isInteger(value)) {
            return value;
        }

        return parseFloat(value.toFixed(decimal));
    }

    /**
     * Applies modifications from a JSON item to an SPT item.
     * If any value is invalid, the modification is skipped for that item.
     * @param jsonItem The weapon data from JSON
     * @param sptItem The weapon data from the SPT database
     * @returns true if the item was modified, false if skipped
     */
    public applyModifications(jsonItem: any, sptItem: any): boolean {
        if (!(jsonItem.item._props && jsonItem.item._id && jsonItem.item)) {
            this.logger.warning(`[ItemUpdaterService] Invalid JSON`);
            return false;
        }

        const itemProps = createItemProps(jsonItem.item._props);

        const updatedProps = {
            CameraSnap: this.validateAndCastFloat(itemProps.CameraSnap, 2),
            AimSensitivity: this.validateAndCastFloat(itemProps.AimSensitivity, 2),
            Ergonomics: this.validateAndCastInt(itemProps.Ergonomics),
            RecoilCamera: this.validateAndCastFloat(itemProps.RecoilCamera, 3),
            RecolDispersion: this.validateAndCastInt(itemProps.RecolDispersion),
            RecoilForceBack: this.validateAndCastInt(itemProps.RecoilForceBack),
            RecoilForceUp: this.validateAndCastInt(itemProps.RecoilForceUp),
            Weight: this.validateAndCastFloat(itemProps.Weight, 2),
            bFirerate: this.validateAndCastInt(itemProps.bFirerate),
        };

        const invalidProps = Object.entries(updatedProps).filter(([_, value]) => value === null);

        if (invalidProps.length > 0) {
            this.logger.warning(`[ItemUpdaterService] Skipping weapon: ${jsonItem.item._name} (ID: ${jsonItem.item._id}) due to invalid values: ${invalidProps.map(([key]) => key).join(", ")}`);
            return false;
        }

        if (Object.values(updatedProps).some(value => value === null)) {
            this.logger.warning(`[ItemUpdaterService] Skipping weapon id :  ${jsonItem.item._id} name : ${jsonItem.item._name} due to invalid values.`);
            return false;
        }

        for (const key in updatedProps) {
            sptItem._props[key] = updatedProps[key];
        }

        return true;
    }
}
