import axios from 'axios';
import {Item} from './Entity/Item';
import {ItemProps} from './Entity/ItemProps';
import {Locale} from './Entity/Locale';
import fs from 'fs';
import path from 'path';
import {Root} from "./Entity/Root";
import {WeaponList} from "./ListIdItem/WeaponList";
import PQueue from "p-queue";
import {config} from "./config";

const baseURL = 'https://db.sp-tarkov.com/api/item';

const __dirname = path.resolve();

/**
 * Récupère les données d'un objet WeaponJson depuis l'API.
 *
 * @param id - L'identifiant de l'objet à récupérer depuis l'API.
 * @returns {Promise<Root>} - Un objet WeaponJson avec des propriétés formatées.
 */

async function fetchItemData(id: string): Promise<Root> {
    const url = `${baseURL}?id=${id}&locale=en`;
    const response = await axios.get(url);

    const rootData = response.data as Root;
    const itemData = rootData.item;
    const localeData = rootData.locale;


    const itemProps = new ItemProps({
        CameraSnap: itemData._props.CameraSnap,
        AimSensitivity: itemData._props.AimSensitivity,
        Ergonomics: itemData._props.Ergonomics,
        RecoilCamera: itemData._props.RecoilCamera,
        RecoilForceBack: itemData._props.RecoilForceBack,
        RecoilForceUp: itemData._props.RecoilForceUp,
        Weight: itemData._props.Weight,
        ammoCaliber: itemData._props.ammoCaliber,
        bFirerate: itemData._props.bFirerate,
    });


    const locale = new Locale({
        Name: localeData.Name,
        ShortName: localeData.ShortName,
    });

    const item = new Item(itemData._id, itemData._name, itemProps);

    return {
        item: item,
        locale: locale,
    };

}

async function main() {
    const weaponList = new WeaponList();
    const ids = weaponList.getIds();
    const basePath = config.jsonWeaponFolderPath;

    if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, { recursive: true });
    } else {
        fs.readdirSync(basePath).forEach(file => {
            if (file.endsWith(".json")) {
                fs.unlinkSync(path.join(basePath, file));
            }
        });
        console.log(`🗑️ Deleted all existing JSON files in ${basePath}`);
    }

    const queue = new PQueue({ concurrency: 5 });
    const createdFiles = new Set<string>();

    const tasks = ids.map(id => queue.add(async () => {
        try {
            const root = await fetchItemData(id);
            const cleanName = root.locale.ShortName.replace(/\s+/g, '_').replace(/[^\w.-]/g, '');
            const filePath = path.join(basePath, `${cleanName}.json`);

            await fs.promises.writeFile(filePath, JSON.stringify(root, null, 2), 'utf-8');
            createdFiles.add(filePath);

            console.log(`✅ Saved item to ${filePath}`);
        } catch (error) {
            console.error(`❌ Failed to fetch data for ID: ${id}`, error);
        }
    }));

    await Promise.all(tasks);

    const filesInDirectory = fs.readdirSync(basePath).filter(file => file.endsWith(".json"));

    console.log("\n=== 🔍 Vérification des fichiers créés ===");
    console.log(`🎯 Total Weapons to Create: ${ids.length}`);
    console.log(`📂 Files Created: ${filesInDirectory.length}`);

    if (filesInDirectory.length !== ids.length) {
        console.warn(`⚠️ Mismatch detected! Expected ${ids.length}, but found ${filesInDirectory.length}.`);
    } else {
        console.log("✅ All files were successfully created!");
    }
}

main().catch(console.error);