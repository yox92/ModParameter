import * as fs from "fs";
import * as path from "path";
import {config} from "../config";
import {createItemProps} from "../Entity/ItemProps";

async function processWeaponFiles() {
    const jsonWeaponFolderPath = config.jsonWeaponFolderPath;
    const jsonWCaliberFolderPath = config.jsonWCaliberFolderPath;

    if (!fs.existsSync(jsonWeaponFolderPath)) {
        console.error(`❌ Le dossier ${jsonWeaponFolderPath} n'existe pas.`);
        return;
    }

    if (!fs.existsSync(jsonWCaliberFolderPath)) {
        console.error(`❌ Le dossier ${jsonWCaliberFolderPath} n'existe pas.`);
        return;
    }

    const files = fs.readdirSync(jsonWeaponFolderPath).filter(file => file.endsWith(".json") && !file.endsWith(".mod.json"));
    const ammoCaliberSet = new Set<string>();

    for (const file of files) {
        try {
            const filePath = path.join(jsonWeaponFolderPath, file);
            const rawData = fs.readFileSync(filePath, "utf-8");
            const jsonData = JSON.parse(rawData);

            if (!jsonData.item._props || !jsonData.item) {
                console.warn(`⚠️ Fichier ignoré (données invalides) : ${file}`);
                continue;
            }

            const itemProps = createItemProps(jsonData.item._props);

            ammoCaliberSet.add(itemProps.ammoCaliber);

            console.log(`✅ Traitement de ${file}, calibre: ${itemProps.ammoCaliber}`);
        } catch (error) {
            console.error(`❌ Erreur lors de la lecture de ${file}:`, error);
        }
    }

    generateAmmoCaliberFiles(ammoCaliberSet);
}

function generateAmmoCaliberFiles(ammoCalibers: Set<string>) {
    const outputPath = path.join(config.jsonWCaliberFolderPath);


    const ignoredCalibers = new Set([
        "Caliber9x18PMM",
        "Caliber20g",
        "Caliber762x25TT"]);

    if (!fs.existsSync(outputPath)) {
        fs.mkdirSync(outputPath, {recursive: true});
    }

    for (const caliber of ammoCalibers) {
        if (ignoredCalibers.has(caliber)) {
            console.log(`🚫 Ignoré: ${caliber}`);
            continue;
        }

        const fileName = `${caliber}.json`;
        const filePath = path.join(outputPath, fileName);

        if (fs.existsSync(filePath)) {
            try {
                fs.unlinkSync(filePath);
                console.log(`🗑️ Supprimé : ${filePath}`);
            } catch (error) {
                console.error(`❌ Erreur lors de la suppression de ${fileName}:`, error);
                continue;
            }
        }
        
        const jsonData = {
            CameraSnap: 1.0,
            AimSensitivity: 1.0,
            Ergonomics: 1.0,
            RecoilCamera: 1.0,
            RecoilForceBack: 1.0,
            RecoilForceUp: 1.0,
            RecolDispersion: 1.0,
            Weight: 1.0,
            ammoCaliber: caliber,
            bFirerate: 1.0
        };

        try {
            fs.writeFileSync(filePath, JSON.stringify(jsonData, null, 2), "utf-8");
            console.log(`📄 Fichier créé : ${filePath}`);
        } catch (error) {
            console.error(`❌ Erreur lors de la création du fichier ${fileName}:`, error);
        }
    }
}

// Exécution principale
processWeaponFiles();
