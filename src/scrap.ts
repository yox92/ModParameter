import axios from 'axios';
import {Item} from './Entity/Item';
import {ItemProps} from './Entity/ItemProps';
import {Locale} from './Entity/Locale';
import fs from 'fs';
import path from 'path';
import {Root} from "./Entity/Root";
import {WeaponList} from "./ListIdItem/WeaponList";

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
        Velocity: itemData._props.Velocity,
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
    const weaponList = new (WeaponList);
    const basePath = path.join(__dirname, 'InputJSONScrap');

    if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, {recursive: true});
    }

    for (const id of weaponList.getIds()) {
        try {
            const root = await fetchItemData(id);
            const cleanName = root.locale.ShortName
                .replace(/\s+/g, '_')
                .replace(/[\/\\?%*:|"<>]/g, '');
            const filePath = path.join(basePath, `${cleanName}.json`);
            fs.writeFileSync(filePath, JSON.stringify(root, null, 2), 'utf-8');
            console.log(`Saved item to ${filePath}`);
        } catch (error) {
            console.error(`Failed to fetch data for ID: ${id}`, error);
        }
    }
}

main();
