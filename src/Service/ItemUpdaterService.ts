import {ILogger} from "../Entity/Logger";
import {createItemProps} from "../Entity/ItemProps";
import {createItemAmmo} from "../Entity/Ammo";


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

    private validateString(value: any, isTracerColor: boolean = false): string | null {
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

    private validateBoolean(value: any): boolean | null {
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
     * @param jsonItem The item data from JSON
     * @param sptItem The item data from the SPT database
     * @returns true if the item was modified, false if skipped
     */
    public applyModifications(jsonItem: any, sptItem: any): boolean {
        if (!(jsonItem.item._props && jsonItem.item._id && jsonItem.item)) {
            this.logger.warning(`[ItemUpdaterService] Invalid JSON`);
            return false;
        }

        const isWeapon = jsonItem.item._props.bFirerate !== undefined;
        const isAmmo = jsonItem.item._props.ArmorDamage !== undefined;

        if (!isWeapon && !isAmmo) {
            this.logger.warning(`[ItemUpdaterService] Unknown item type, skipping: ${jsonItem.item._name} (ID: ${jsonItem.item._id})`);
            return false;
        }

        let updatedProps: any = {};

        if (isWeapon) {
            const itemProps = createItemProps(jsonItem.item._props);
            updatedProps = {
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
        } else if (isAmmo) {
            const ammoProps = createItemAmmo(jsonItem.item._props);
            updatedProps = {
                ArmorDamage: this.validateAndCastInt(ammoProps.ArmorDamage),
                Damage: this.validateAndCastInt(ammoProps.Damage),
                InitialSpeed: this.validateAndCastInt(ammoProps.InitialSpeed),
                PenetrationPower: this.validateAndCastInt(ammoProps.PenetrationPower),
                StackMaxSize: this.validateAndCastInt(ammoProps.StackMaxSize),
                Tracer: this.validateBoolean(ammoProps.Tracer),
                TracerColor: this.validateString(ammoProps.TracerColor, true),
            };
        }

        const invalidProps = Object.entries(updatedProps).filter(([_, value]) => value === null);

        if (invalidProps.length > 0) {
            this.logger.warning(`[ItemUpdaterService] Skipping ${isWeapon ? "weapon" : "ammo"}: ${jsonItem.item._name} (ID: ${jsonItem.item._id}) due to invalid values: ${invalidProps.map(([key]) => key).join(", ")}`);
            return false;
        }

        if (Object.values(updatedProps).some(value => value === null)) {
            this.logger.warning(`[ItemUpdaterService] Skipping item id :  ${jsonItem.item._id} name : ${jsonItem.item._name} due to invalid values.`);
            return false;
        }

        for (const key in updatedProps) {
            sptItem._props[key] = updatedProps[key];
        }

        this.logger.info(`[ItemUpdaterService] Successfully updated ${isWeapon ? "weapon" : "ammo"}: ${jsonItem.item._name} (ID: ${jsonItem.item._id}) with properties: ${Object.keys(updatedProps).join(", ")}`);

        return true;
    }
}
