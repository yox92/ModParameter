import {JsonFileService} from "./JsonFileService";
import {AimingService} from "./AimingService";
import {ILogger} from "@spt-server/models/spt/utils/ILogger";
import {IDatabaseTables} from "@spt-server/models/spt/server/IDatabaseTables";
import {Aiming, createAiming} from "../Entity/Aiming";


export class PmcService {
    private readonly logger: ILogger;
    private readonly iDatabaseTables: IDatabaseTables;
    private readonly jsonFileService: JsonFileService;
    private readonly aimingService: AimingService;

    constructor(logger: ILogger, iDatabaseTables: IDatabaseTables) {
        this.logger = logger;
        this.iDatabaseTables = iDatabaseTables;

        this.jsonFileService = new JsonFileService(logger);
        this.aimingService = new AimingService(logger);
    }

    public updatePmc(): void {
        const aimingFile = this.jsonFileService.loadJsonAimingFile();

        if (!aimingFile) {
            this.logger.warning("[AttributMod] No valid file found. Skipping PMC update.");
            return;
        }

        const {jsonData} = aimingFile;

        const aimingJson: Aiming = createAiming(jsonData);
        if (!aimingJson) {
            this.logger.warning(`[AttributMod] Invalid Json PMC update.`);
            return;
        }

        this.aimingService.applyModifications(aimingJson, this.iDatabaseTables);
    }

}