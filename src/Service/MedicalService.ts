import {ILogger} from "@spt/models/spt/utils/ILogger";
import {DatabaseService} from "@spt/services/DatabaseService";
import {IGlobals} from "@spt/models/eft/common/IGlobals";
import {ItemHelper} from "@spt/helpers/ItemHelper";

export class MedicalService {
     private readonly logger: ILogger;
    private readonly itemHelper: ItemHelper;
    private readonly dataService: DatabaseService;

    constructor(logger: ILogger, itemHelper: ItemHelper, dataService: DatabaseService) {
       this.logger = logger;
        this.itemHelper = itemHelper;
        this.dataService = dataService
    }


    public applyMedicalBuff(): void {
        const global: IGlobals = this.dataService.getGlobals()
        const buff = global.config.Health.Effects.Stimulator.Buffs


        const [boolpropi, propitalTemplate] = this.itemHelper.getItem('5c0e530286f7747fa1419862')
        if (boolpropi) {
            const propital = propitalTemplate._props
            propital.effects_damage.Pain.duration = 400
            propital.effects_damage.Pain.fadeOut = 1
            propital.medUseTime = 5
        }
        const [booletgc, etgcTemplate] = this.itemHelper.getItem('5c0e534186f7747fa1419867')
        if (booletgc) {
            const etgc = etgcTemplate._props
            etgc.medUseTime = 5
        }
        const [boolzagustin, zagustinTemplate] = this.itemHelper.getItem('5c0e534186f7747fa1419867')
        if (boolzagustin) {
            const zagustin = zagustinTemplate._props
            zagustin.medUseTime = 5
        }
        const [boolAfak, afakTemplate] = this.itemHelper.getItem('5c0e534186f7747fa1419867')
        if (boolAfak) {
            const afak = afakTemplate._props
            afak.hpResourceRate = 1000
            afak.effects_damage.DestroyedPart = {
                "delay": 0,
                "duration": 0,
                "fadeOut": 0,
                "cost": 50,
                "healthPenaltyMin": 20,
                "healthPenaltyMax": 10
            };
            const [boolsalewa, salewaTemplate] = this.itemHelper.getItem('544fb45d4bdc2dee738b4568')
            if (boolsalewa) {
                const salewa = salewaTemplate._props
                salewa.hpResourceRate = 1500
                salewa.effects_damage.DestroyedPart = {
                    "delay": 0,
                    "duration": 0,
                    "fadeOut": 0,
                    "cost": 50,
                    "healthPenaltyMin": 20,
                    "healthPenaltyMax": 10
                };

            }
            const [boolgrizzly, grizzlyTemplate] = this.itemHelper.getItem('590c657e86f77412b013051d')
            if (boolgrizzly) {
                const grizzly = grizzlyTemplate._props
                grizzly.hpResourceRate = 10000
            }


        }
    }

}
