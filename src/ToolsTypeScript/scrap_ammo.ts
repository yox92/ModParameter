import axios from 'axios';
import {Ammo} from '../Entity/Ammo';
import {Locale} from '../Entity/Locale';
import fs from 'fs';
import path from 'path';
import {Templates} from "../Entity/Templates";
import {AmmoList} from "../ListIdItem/AmmoEnum";
import PQueue from "p-queue";
import {config} from "../config";
import {Item} from "../Entity/Item";

const baseURL = 'https://db.sp-tarkov.com/api/item';

/**
 * ammo from DB SP API.
 *
 * @param id - ID use.
 * @returns {Promise<{ ammo: Ammo, locale: Locale }>} - Object containing the formatted properties.
 */
async function fetchAmmoData(id: string): Promise<Templates<Ammo>> {
    const url = `${baseURL}?id=${id}&locale=en`;
    const response = await axios.get(url);

    const rootData = response.data as Templates<any>;
    const itemData = rootData.item;
    const localeData = rootData.locale;

    const ammoProps = new Ammo({
        ArmorDamage: itemData._props.ArmorDamage,
        Caliber: itemData._props.Caliber,
        Damage: itemData._props.Damage,
        PenetrationPower: itemData._props.PenetrationPower,
        StackMaxSize: itemData._props.StackMaxSize,
        Tracer: itemData._props.Tracer,
        TracerColor: itemData._props.TracerColor,
        InitialSpeed: itemData._props.InitialSpeed,
        BallisticCoeficient: Math.round(itemData._props.BallisticCoeficient * 1000),
        BulletMassGram: Math.round(itemData._props.BulletMassGram * 100),
        ProjectileCount: itemData._props.ProjectileCount,
        ammoAccr: itemData._props.ammoAccr,
        ammoRec: itemData._props.ammoRec,
    });

    const locale = new Locale({
        Name: localeData.Name,
        ShortName: localeData.ShortName,
    });

    const item = new Item<Ammo>(itemData._id, itemData._name, ammoProps);

    return new Templates<Ammo>(locale, item);
}

async function main() {
    const ammoList = new AmmoList();
    const ids = ammoList.getIds();
    const basePath = config.jsonAmmoFolderPathNew;

    if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, {recursive: true});
    } else {
        fs.readdirSync(basePath).forEach(file => {
            if (file.endsWith(".json")) {
                fs.unlinkSync(path.join(basePath, file));
            }
        });
        console.log(`🗑️ Deleted all existing JSON files in ${basePath}`);
    }

    const queue = new PQueue({concurrency: 5});
    const createdFiles = new Set<string>();

    const tasks = ids.map(id => queue.add(async () => {
        try {
            await delay(500);
            const root = await fetchAmmoData(id);
            const locale = root.locale;

            const cleanName = locale.Name.replace(/\s+/g, '_').replace(/[^\w.-]/g, '');
            const filePath = path.join(basePath, `${cleanName}.json`);

            await fs.promises.writeFile(
                filePath,
                JSON.stringify({item: root.item, locale: root.locale}, null, 2),
                'utf-8'
            );

            createdFiles.add(filePath);

            console.log(`✅ Saved ammo data to ${filePath}`);
        } catch (error) {
            console.error(`❌ Failed to fetch data for ID: ${id}`, error);
        }
    }));

    await Promise.all(tasks);

    const filesInDirectory = new Set(
        fs.readdirSync(basePath)
            .filter(file => file.endsWith(".json"))
            .map(file => file.replace(".json", ""))
    );

    const missingIds: string[] = [];

    for (const id of ids) {
        try {
            const {locale} = await fetchAmmoData(id);
            const expectedFileName = locale.ShortName.replace(/\s+/g, '_').replace(/[^\w.-]/g, '');

            if (!filesInDirectory.has(expectedFileName)) {
                missingIds.push(id);
            }
        } catch (error) {
            console.error(`❌ Error fetching data for ID: ${id}`, error);
            missingIds.push(id);
        }
    }

    console.log("\n=== 🔍 Verification of created files ===");
    console.log(`🎯 Total Ammo to Create: ${ids.length}`);
    console.log(`📂 Files Created: ${filesInDirectory.size}`);

    if (missingIds.length > 0) {
        console.warn(`⚠️ ${missingIds.length} ammo items did not generate a JSON file:`);
        console.warn(missingIds.join(", "));
    } else {
        console.log("✅ All ammo items have successfully generated JSON files.");
    }
}

/**
 * Add a delay to prevent API overload
 */
function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

main().catch(console.error);
