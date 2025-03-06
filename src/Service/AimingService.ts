import {ILogger} from "../Entity/Logger";


export class AimingService {
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.logger = logger;
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
     * Applies modifications from a JSON pmc attributs to an SPT attributs.
     * If any value is invalid, the modification is skipped for that item.
     * @param jsonAiming The pmc attributs data from JSON
     * @param sptAiming The pmc attributs data from the SPT database
     * @returns true if the item was modified, false if skipped
     */
    public applyModifications(jsonAiming: any, sptAiming: any): boolean {
        if (!(sptAiming.globals.Aiming && jsonAiming)) {
            this.logger.warning(`[AimingService] Invalid JSON`);
            return false;
        }

        const aiming = this.createAiming(jsonAiming);
        const updateAiming = this.createAiming(aiming);
        const updateAimingObjects = this.creatObjectAiming(aiming);

        const invalidProps = Object.entries(updateAiming)
            .filter(([_, value]) => value === null)
            .map(([key]) => key);

        Object.entries(updateAimingObjects).forEach(([key, obj]) => {
            Object.entries(obj).forEach(([subKey, value]) => {
                if (value === null) invalidProps.push(`${key}.${subKey}`);
            });
        });

        if (invalidProps.length > 0) {
            this.logger.warning(`[AimingService] Skipping aiming modifications due to invalid values: 
        ${invalidProps.join(", ")}`);
            return false;
        }

        Object.keys(updateAiming).forEach(key => {
            sptAiming.globals.Aiming[key] = updateAiming[key];
        });

        Object.keys(updateAimingObjects).forEach(key => {
            if (!sptAiming.globals.Aiming[key]) {
                sptAiming.globals.Aiming[key] = {};  // Assurer que l'objet existe
            }
            Object.keys(updateAimingObjects[key]).forEach(subKey => {
                sptAiming.globals.Aiming[key][subKey] = updateAimingObjects[key][subKey];
            });
        });

        return true;

    }

    private createAiming(aiming: any) {
        return {
            AimPunchMagnitude: this.validateAndCastFloat(aiming.AimPunchMagnitude, 1),
            RecoilDamping: this.validateAndCastFloat(aiming.RecoilDamping, 1),
            RecoilHandDamping: this.validateAndCastFloat(aiming.RecoilHandDamping, 2),

        };
    }

    private creatObjectAiming(aiming: any) {
        return {
            ProceduralIntensityByPose: {
                x: this.validateAndCastFloat(aiming.ProceduralIntensityByPoseProne, 1),   // x ← Prone
                y: this.validateAndCastFloat(aiming.ProceduralIntensityByPoseCrouching, 1), // y ← Crouching
                z: this.validateAndCastFloat(aiming.ProceduralIntensityByPoseStanding, 1),  // z ← Standing
            },
            RecoilIntensityByPose: {
                x: this.validateAndCastFloat(aiming.RecoilIntensityProne, 1),   // x ← Prone
                y: this.validateAndCastFloat(aiming.RecoilIntensityCrouching, 1), // y ← Crouching
                z: this.validateAndCastFloat(aiming.RecoilIntensityStanding, 1),  // z ← Standing
            },
        };
    }
}
