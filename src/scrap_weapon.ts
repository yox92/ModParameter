import axios from 'axios';
import {Item} from './Entity/Item';
import {ItemProps} from './Entity/ItemProps';
import {Locale} from './Entity/Locale';
import fs from 'fs';
import path from 'path';
import {Templates} from "./Entity/Templates";
import {WeaponList} from "./ListIdItem/WeaponList";
import PQueue from "p-queue";
import {config} from "./config";

const baseURL = 'https://db.sp-tarkov.com/api/item';

/**
 * item from DB SP API.
 *
 * @param id - ID use.
 * @returns {Promise<Templates>} - Object containing the formatted properties.
 */
async function fetchItemData(id: string): Promise<Templates<any>> {
    const url = `${baseURL}?id=${id}&locale=en`;
    const response = await axios.get(url);

    const rootData = response.data as Templates<any>;
    const itemData = rootData.item;
    const localeData = rootData.locale;

    const itemProps = new ItemProps({
        CameraSnap: itemData._props.CameraSnap,
        AimSensitivity: itemData._props.AimSensitivity,
        Ergonomics: itemData._props.Ergonomics,
        RecoilCamera: itemData._props.RecoilCamera,
        RecoilForceBack: itemData._props.RecoilForceBack,
        RecoilForceUp: itemData._props.RecoilForceUp,
        RecolDispersion: itemData._props.RecolDispersion,
        Weight: itemData._props.Weight,
        ammoCaliber: itemData._props.ammoCaliber,
        bFirerate: itemData._props.bFirerate,
    });


    const locale = new Locale({
        Name: localeData.Name,
        ShortName: localeData.ShortName,
    });

    const item = new Item(itemData._id, itemData._name, itemProps);

    return new Templates<ItemProps>(locale, item);

}

async function main() {
    const weaponList = new WeaponList();
    const ids = weaponList.getIds();
    const basePath = config.jsonWeaponFolderPath;

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
            await delay(500)
            const root = await fetchItemData(id);
            const cleanName = root.locale.ShortName.replace(/\s+/g, '_').replace(/[^\w.-]/g, '');
            const filePath = path.join(basePath, `${cleanName}.json`);

            await fs.promises.writeFile(
                filePath,
                JSON.stringify({item: root.item, locale: root.locale}, null, 2),
                'utf-8'
            );

            createdFiles.add(filePath);

            console.log(`✅ Saved item to ${filePath}`);
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
            const root = await fetchItemData(id);
            const expectedFileName = root.locale.ShortName
                .replace(/\s+/g, '_')
                .replace(/[^\w.-]/g, '');

            if (!filesInDirectory.has(expectedFileName)) {
                missingIds.push(id);
            }
        } catch (error) {
            console.error(`❌ Error fetching data for ID: ${id}`, error);
            missingIds.push(id);
        }
    }

    console.log("\n=== 🔍 Verification of created files ===");
    console.log(`🎯 Total Weapons to Create: ${ids.length}`);
    console.log(`📂 Files Created: ${filesInDirectory.size}`);
}

/**
 * Add a delay to prevent API overload
 */
function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

main().catch(console.error);