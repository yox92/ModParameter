import axios from 'axios';
import { AssaultRifleList } from 'Id/AssaultRifleList';
import { Item } from 'Entity/Item';
import { ItemProps } from 'Entity/ItemProps';
import fs from 'fs';
import path from 'path';

const baseURL = 'https://db.sp-tarkov.com/api/item';

const __dirname = path.resolve();

async function fetchItemData(id: string): Promise<Item> {
    const url = `${baseURL}?id=${id}&locale=en`;
    const response = await axios.get(url);
    const itemData = response.data.item;
    const itemPropsData = itemData._props;

    const itemProps = new ItemProps({
        CameraSnap: itemPropsData.CameraSnap,
        AimSensitivity: itemPropsData.AimSensitivity,
        Ergonomics: itemPropsData.Ergonomics,
        RecoilCamera: itemPropsData.RecoilCamera,
        RecoilForceBack: itemPropsData.RecoilForceBack,
        RecoilForceUp: itemPropsData.RecoilForceUp,
        Velocity: itemPropsData.Velocity,
        Weight: itemPropsData.Weight,
        ammoCaliber: itemPropsData.ammoCaliber,
        bFirerate : itemPropsData.bFirerate,
    });
    return new Item(itemData._id, itemData._name, itemData._parent, itemProps);
}

function cleanFileName(filename: string): string {
    // Retirer le préfixe 'weapon_' si présent
    const prefix = 'weapon_';
    if (filename.startsWith(prefix)) {
        filename = filename.substring(prefix.length);
    }
    // Remplace les caractères non alphanumériques par des underscores et convertit en minuscules
    return filename.replace(/[^a-z0-9]/gi, '_').toLowerCase();
}

async function main() {
    const rifleList = new AssaultRifleList();
    const basePath = path.join(__dirname, 'output'); // Définis un chemin de base pour les fichiers de sortie

    if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, { recursive: true }); // Crée le répertoire s'il n'existe pas
    }

    for (const id of rifleList.getIds()) {
        try {
            const item = await fetchItemData(id);
            const cleanName = cleanFileName(item._name);
            const filePath = path.join(basePath, `${cleanName}.json`); // Construis le chemin du fichier
            fs.writeFileSync(filePath, JSON.stringify(item, null, 2), 'utf-8'); // Écrit l'objet dans un fichier JSON
            console.log(`Saved item to ${filePath}`);
        } catch (error) {
            console.error(`Failed to fetch data for ID: ${id}`, error);
        }
    }
}

main();
