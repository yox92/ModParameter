import {JsonFileService} from "./JsonFileService";
import {AimingService} from "./AimingService";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {Aiming, createAiming} from "../Entity/Aiming";
import {DatabaseService} from "@spt/services/DatabaseService";


export class PmcService {
    private readonly logger: ILogger;
    private readonly dataService: DatabaseService;
    private readonly jsonFileService: JsonFileService;
    private readonly aimingService: AimingService;

    constructor(logger: ILogger, dataService: DatabaseService) {
        this.logger = logger;
        this.dataService = dataService;

        this.jsonFileService = new JsonFileService(logger);
        this.aimingService = new AimingService(logger);
    }

    public updatePmc(): void {
        const aimingFile = this.jsonFileService.loadJsonAimingFile();

        if (!aimingFile) {
            this.logger.debug("[ModParameter] Skipping PMC update.");
            return;
        }

        const {jsonData} = aimingFile;

        const aimingJson: Aiming = createAiming(jsonData);
        if (!aimingJson) {
            this.logger.debug(`[ModParameter] Invalid Json PMC update.`);
            return;
        }

        this.aimingService.applyModifications(aimingJson, this.dataService);
    }

}