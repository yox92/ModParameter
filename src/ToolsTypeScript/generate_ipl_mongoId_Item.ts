import * as fs from "fs";
import * as path from "path";
import {WeaponEnum} from "../ListIdItem/WeaponEnum";
import {EnumUtils} from "../Service/EnumUtils";
import {mongoid} from "mongoid-js";

const path_to_directory_trader = path.resolve(__dirname, "external/server/project/assets/database/traders");
const file_name_where_find = "assort.json";
const outputFileAmmo = path.resolve(__dirname, "ipl_mongo_ipl_clone_ammo.json");
const outputFileWeapon = path.resolve(__dirname, "ipl_mongo_ipl_clone_weapon.json");

/**
 * 📌 Fonction pour générer un identifiant MongoDB-like
 */
function generateMongoObjectId(): string {
return mongoid()
}

/**
 * 📌 Charge les mappings existants depuis le fichier JSON
 */
function loadExistingMappings(): Record<string, string> {
    try {
        if (!fs.existsSync(outputFileWeapon)) {
            console.warn(`⚠️ Fichier ${outputFileWeapon} introuvable, création d'un nouveau.`);
            return {};
        }

        const data = fs.readFileSync(outputFileWeapon, "utf-8").trim();
        return data ? JSON.parse(data) : {};
    } catch (error) {
        console.error("❌ Erreur lors du chargement du fichier JSON :", error);
        return {};
    }
}

/**
 * 📌 Sauvegarde le JSON des mappings (_id -> nouvel ID)
 */
function saveMappings(mappings: Record<string, string>) {
    try {
        fs.writeFileSync(outputFileWeapon, JSON.stringify(mappings, null, 4), "utf-8");
        console.log(`✅ Fichier mis à jour : ${outputFileWeapon}`);
    } catch (error) {
        console.error("❌ Erreur lors de l'écriture du fichier JSON :", error);
    }
}

async function fetchData(ids: string[]): Promise<void> {
    const mappings = loadExistingMappings();

    if (!fs.existsSync(path_to_directory_trader)) {
        console.error(`❌ Le répertoire ${path_to_directory_trader} est introuvable.`);
        return;
    }

    // 📂 Lecture des dossiers dans le répertoire des marchands
    const traderDirs = fs.readdirSync(path_to_directory_trader, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => path.join(path_to_directory_trader, dirent.name));

    const idCounts: Record<string, number> = {};
    const missingIds = new Set(ids);

    for (const traderDir of traderDirs) {
        const assortPath = path.join(traderDir, file_name_where_find);

        if (!fs.existsSync(assortPath)) {
            console.warn(`⚠️ Fichier introuvable : ${assortPath}, on passe.`);
            continue;
        }

        try {
            const data = JSON.parse(fs.readFileSync(assortPath, "utf-8"));
            if (!data.items || !Array.isArray(data.items)) {
                console.warn(`⚠️ Format invalide dans ${assortPath}, on passe.`);
                continue;
            }

            for (const item of data.items) {
                if (item._tpl && ids.includes(item._tpl) && item._id && item.parentId === "hideout") {
                    missingIds.delete(item._tpl);

                    if (!mappings[item._id]) {
                        mappings[item._id] = generateMongoObjectId();
                        console.log(`🆕 Associe _id ${item._id} → Nouvel ID ${mappings[item._id]}`);

                        idCounts[item._tpl] = (idCounts[item._tpl] || 0) + 1;
                    }
                }
            }
        } catch (error) {
            console.error(`❌ Erreur de lecture du fichier ${assortPath} :`, error);
        }
    }

    saveMappings(mappings);

    console.log("\n📊 Statistiques des ID ajoutés :");
    Object.entries(idCounts).forEach(([tpl, count]) => {
        console.log(`➡️ ${tpl}: ${count} nouveaux IDs`);
    });

    if (missingIds.size > 0) {
        console.warn("\n⚠️ Les _tpl suivants n'ont pas été trouvés dans les fichiers :");
        console.warn([...missingIds].join(", "));
    }
}

/**
 * 📌 Exécution principale
 */
async function main() {
     // const idsAmmos: string[] = EnumUtils.getAllValues(AmmoEnum)
    // await fetchData(idsAmmos);

    const idsWeapon: string[] = EnumUtils.getAllValues(WeaponEnum)
    await fetchData(idsWeapon);
}

main().catch(console.error);
