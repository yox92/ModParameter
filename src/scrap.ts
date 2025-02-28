import axios from 'axios';
import {Item} from 'Entity/Item';
import {ItemProps} from 'Entity/ItemProps';
import {Locale} from 'Entity/Locale';
import fs from 'fs';
import path from 'path';
import {WeaponJson} from "Entity/WeaponJson";
import {WeaponList} from "Id/WeaponList";

const baseURL = 'https://db.sp-tarkov.com/api/item';

const __dirname = path.resolve();

/**
 * Récupère les données d'un objet WeaponJson depuis l'API.
 *
 * @param id - L'identifiant de l'objet à récupérer depuis l'API.
 * @returns {Promise<WeaponJson>} - Un objet WeaponJson avec des propriétés formatées.
 */

async function fetchItemData(id: string): Promise<WeaponJson> {
    const url = `${baseURL}?id=${id}&locale=en`;
    const response = await axios.get(url);

    const weaponData = response.data as WeaponJson;
    const itemData = weaponData.Item;
    const localeData = weaponData.Locale;


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
        Item: item,
        Locale: locale,
    };

}


async function main() {
    const weaponList = new (WeaponList);
    const basePath = path.join(__dirname, 'output'); // Définis un chemin de base pour les fichiers de sortie

    if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, {recursive: true}); // Crée le répertoire s'il n'existe pas
    }

    for (const id of weaponList.getIds()) {
        try {
            const weaponData = await fetchItemData(id);
            const cleanName = weaponData.Locale.ShortName;
            const filePath = path.join(basePath, `${cleanName}.json`); // Construis le chemin du fichier
            fs.writeFileSync(filePath, JSON.stringify(weaponData, null, 2), 'utf-8'); // Écrit l'objet dans un fichier JSON
            console.log(`Saved item to ${filePath}`);
        } catch (error) {
            console.error(`Failed to fetch data for ID: ${id}`, error);
        }
    }
}

main();
