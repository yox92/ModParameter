import axios from 'axios';
import {Locale} from '../Entity/Locale';
import fs from 'fs';
import path from 'path';
import {Templates} from "../Entity/Templates";
import PQueue from "p-queue";
import {config} from "../config";
import {Item} from "../Entity/Item";
import {EnumUtils} from "../Service/EnumUtils";
import {Medic} from "../Entity/Medic";
import {MedicEnum} from "../ListIdItem/MedicEnum";

const baseURL = 'https://db.sp-tarkov.com/api/item';

/**
 * medic from DB SP API.
 *
 * @param id - ID use.
 * @returns {Promise<{ medic: Medic, locale: Locale }>} - Object containing the formatted properties.
 */
async function fetchMedicData(id: string): Promise<Templates<Medic>> {
    const url = `${baseURL}?id=${id}&locale=en`;
    const response = await axios.get(url);

    const rootData = response.data as Templates<any>;
    const itemData = rootData.item;
    const localeData = rootData.locale;

    const medicProps = new Medic({
         StackMaxSize: itemData._props.StackMaxSize,
         StackObjectsCount: itemData._props.StackObjectsCount,
         MaxHpResource: itemData._props.MaxHpResource,
         hpResourceRate: itemData._props.hpResourceRate,
         medUseTime: itemData._props.medUseTime,
         effects_damage: itemData._props.effects_damage,
    });

    const locale = new Locale({
        Name: localeData.Name,
        ShortName: localeData.ShortName,
    });

    const item = new Item<Medic>(itemData._id, itemData._name, medicProps, itemData._parent);

    return new Templates<Medic>(locale, item);
}

async function main() {
    const ids: string[] = EnumUtils.getAllValues(MedicEnum)
    const basePath = config.jsonMedicFolderPathNew;

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
            const root = await fetchMedicData(id);
            const locale = root.locale;

            const cleanName = locale.Name.replace(/\s+/g, '_').replace(/[^\w.-]/g, '');
            const filePath = path.join(basePath, `${cleanName}.json`);

            await fs.promises.writeFile(
                filePath,
                JSON.stringify({item: root.item, locale: root.locale}, null, 2),
                'utf-8'
            );

            createdFiles.add(filePath);

            console.log(`✅ Saved medic data to ${filePath}`);
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
            const {locale} = await fetchMedicData(id);
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
