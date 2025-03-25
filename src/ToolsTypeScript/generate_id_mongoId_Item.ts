import * as fs from "fs";
import * as path from "path";
import {mongoid} from "mongoid-js";
import {EnumUtils} from "../Service/EnumUtils";
import {AmmoEnum} from "../ListIdItem/AmmoEnum";
import {WeaponEnum} from "../ListIdItem/WeaponEnum";
import {MedicEnum} from "../ListIdItem/MedicEnum";

const outputFileAmmo = path.resolve(__dirname, "id_mongo_new_id_clone_ammo_.json"); // Fichier de sortie
const outputFileWeapon = path.resolve(__dirname, "id_mongo_new_id_clone_weapon_.json"); // Fichier de sortie
const outputFileMedic = path.resolve(__dirname, "id_mongo_new_id_clone_medic_.json"); // Fichier de sortie

/**
 * Fonction pour générer un identifiant MongoDB
 */
function generateMongoObjectId(): string {
   return mongoid()
}

/**
 *  Charge les mappings existants depuis le fichier JSON
 */
function loadExistingMappings(): Record<string, string> {
    try {
        if (!fs.existsSync(outputFileMedic)) {
            console.warn(`⚠️ Fichier ${outputFileMedic} introuvable, création d'un nouveau.`);
            return {};
        }

        const data = fs.readFileSync(outputFileMedic, "utf-8");
        return data.trim() ? JSON.parse(data) : {};
    } catch (error) {
        console.error("❌ Erreur lors du chargement du fichier JSON :", error);
        return {};
    }
}

/**
 *  Sauvegarde le JSON des mappings (_tpl -> _id généré)
 */
function saveMappings(mappings: Record<string, string>) {
    try {
        fs.writeFileSync(outputFileMedic, JSON.stringify(mappings, null, 4), "utf-8");
        console.log(`✅ Fichier mis à jour : ${outputFileMedic}`);
    } catch (error) {
        console.error("❌ Erreur lors de l'écriture du fichier JSON :", error);
    }
}

/**
 *  Générer un ID unique pour chaque ID de la liste
 */
async function generateAllIds(ids: string[]): Promise<void> {
    const mappings = loadExistingMappings();
    let newEntries = 0;
    let skippedIds = 0;

    console.log(`🔍 Vérification des ${ids.length} IDs de la liste...`);

    const alreadyExistingIds: string[] = [];

    for (const id of ids) {
        if (!mappings[id]) {
            mappings[id] = generateMongoObjectId();
            console.log(`Génération d'un nouvel ID pour : ${id} -> ${mappings[id]}`);
            newEntries++;
        } else {
            alreadyExistingIds.push(id);
        }
    }

    console.log(`🟢 ${alreadyExistingIds.length} IDs étaient déjà présents dans le fichier et n'ont pas été générés.`);
    console.log(`📜 Liste des IDs déjà existants :`, alreadyExistingIds);
    if (newEntries > 0) {
        saveMappings(mappings);
        console.log(`✅ ${newEntries} nouveaux IDs ont été générés.`);
    } else {
        console.log("✅ Tous les IDs existent déjà, rien à faire.");
    }

    if (skippedIds > 0) {
        console.warn(`⚠️ ${skippedIds} IDs étaient invalides et n'ont pas été traités.`);
    }

    console.log(`📊 Résumé final : ${ids.length} IDs à traiter, ${Object.keys(mappings).length} enregistrés, ${skippedIds} ignorés.`);
}

/**
 *  Exécution principale
 */
async function main() {
    // const idsAmmos: string[] = EnumUtils.getAllValues(AmmoEnum)
    // await generateAllIds(idsAmmos);
    //
    // const idsWeapon: string[] = EnumUtils.getAllValues(WeaponEnum)
    // await generateAllIds(idsWeapon);

    const idsMedic: string[] = EnumUtils.getAllValues(MedicEnum)
    await generateAllIds(idsMedic);
}

main().catch(console.error);
