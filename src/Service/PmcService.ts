import {JsonFileService} from "./JsonFileService";
import {IDatabaseServer} from "../Entity/DatabaseServer";
import {ILogger} from "../Entity/Logger";
import {AimingService} from "./AimingService";


export class PmcService {
    private readonly logger: ILogger;
    private readonly database: IDatabaseServer;
    private readonly jsonFileService: JsonFileService;
    private readonly aimingService: AimingService;

    constructor(logger: ILogger, database: IDatabaseServer) {
        this.logger = logger;
        this.database = database;

        this.jsonFileService = new JsonFileService(logger);
        this.aimingService = new AimingService(logger);
    }

    /**
     *
     */
    public updatePmc(): void {
        const tables = this.database.getTables();
        const {data} = this.jsonFileService.loadJsonAimingFile();

        const SptAiming = tables.globals.config.Aiming;

        this.aimingService.applyModifications(data, SptAiming)


    }
}