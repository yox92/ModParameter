# ModParameter App

## Table des matières
1. [Aperçu du projet](#aperçu-du-projet)
2. [Fonctionnalités principales](#fonctionnalités-principales)
3. [Lancement de l’application](#lancement-de-lapplication)
4. [Structure du projet](#structure-du-projet)

6. [Utilisation générale](#utilisation-générale)
7. [Focus sur les classes principales](#focus-sur-les-classes-principales)
   - [ModSelectionWindow](#modselectionwindow--menu-principal)
   - [CaliberWeaponsMod](#caliberweaponsmod--modification-groupée-par-calibre)
   - [SingleWeaponMod](#singleweaponmod--modification-ciblée-dune-unique-arme)
   - [AmmoMod](#ammomod--modification-de-munitions)
   - [ListItemAlreadyMod](#listitemalreadymod--liste-et-suppression-de-fichiers-mod)
8. [Dépendances](#dépendances)

---

## Aperçu du projet
1. **ModParameter App** est une application Python conçue pour créer et gérer des “mods” (fichiers `*_mod.json`) 
relatifs à différents éléments d’un jeu (armes, munitions, PMC). Elle utilise **[customtkinter](https://github.com/TomSchimansky/CustomTkinter)** 
pour son interface graphique et manipule des **fichiers JSON** pour charger, modifier ou supprimer des valeurs de configuration.
2. Les fichiers `*_mod.json` sont par la suite récupéré par le projet TypeScript pour mapper dans les Objets de la `BDD SPT`

---

## Fonctionnalités principales

1. **Interface graphique intuitive**  
   - Menu principal avec choix de modification (armes, munitions, PMC).  
   - Fenêtres dédiées pour configurer un objet ou un groupe d’objets.

2. **Gestion centralisée de Mods**  
   - Création automatique de fichiers `*_mod.json` pour séparer les modifications du fichier de base.
   - Les fichiers `*_mod.json` sont placé par python dans :
     - JsonFiles/Weapons
     - JsonFiles/Ammo
     - JsonFiles/PMC
   - Suppression ciblée ou globale de ces fichiers `*_mod.json`, permettant de revenir à l’état “vanilla”.

3. **Recherche et tri**  
   - Filtrer des armes via leur nom.  
   - Sélectionner toutes les armes d’un même calibre.
   - Sélectionner les balles par leur calibres
   - Lister toutes les munitions / armes déjà modifiées.

4. **Suppression**  
   - supprimer les fichiers `*_mod.json` des armes/balles/PMC :
     - Suppression globale
     - Suppression ciblée
     - Remettre les valeurs d'origine = suppression `*_mod.json`

5. **Édition et contrôle**  
   - Barres de glissement (sliders) pour ajuster en pourcentage les valeurs numériques %.  
   - Champs de saisie pour fixer manuellement des valeurs.  
   - switch boolean
   - Indicateurs d’éventuels dépassements (seuils de sécurité) ou d’erreur d’entrée.

6. **Feedback visuel**  
   - Barres de progression pour afficher l’évolution de l’opération.  
   - Étiquettes de statut (ex. “Changes applied successfully” ou “All modifications removed”).

---

# Lancement de l’application
## Python
- Placez-vous à la racine du projet.
- le main.py se trouve dans le répertoire main
- La fenêtre ModParameter App s’affiche, proposant différents choix.

##  fichier .EXE
- Tout le packaging est réalisé avec `pyinstaller`
- un fichier `buildExeFile.bat` permet la fabrication du fichier `*.exe`
- par défault, il est généré à la racine du projet dans `py'

- le fichier exe est configuré pour être executé dans l'arborescence inférieure du dossier py `config.py`
- la structure doit être :
  - NameModeFolder <==> `*.exe`
    - **py**
      - JsonFiles
        - Weapons  **Json File HERE**
        - Ammo     **Json File HERE**
        - Calibers **Json File HERE**
        - PMC      **Json File HERE**
    - **src** ==> TypeScript SPT

---

## Structure du projet Python

.
├── Entity/
│   ├── Caliber.py         
│   ├── EnumProps.py       # Enum pour les propriétés d'armes
│   ├── EnumAmmo.py        # Enum pour les propriétés de munitions
│   ├── Item.py
│   ├── ItemManager.py     # Mapper pour facilité la manipulation du Props `ItemProps.py`
│   ├── ItemProps.py
│   ├── Logger.py
│   ├── Root.py
│   └── WindowType.py
├── Utils/
│   ├── ImageUtils.py
│   ├── JsonUtils.py
│   ├── Utils.py
│   └── WindowUtils.py
├── WindowComponent/
│   ├── AmmoMod.py            # Modification d'une munition
│   ├── CaliberWeaponsMod.py  # Modification groupée par calibre
│   ├── ListItemAlreadyMod.py # Liste + suppression de fichiers mod existants
│   ├── PmcMod.py
│   ├── ModSelectionWindow.py     # Classe principale (menu)
│   ├── ProgressBar.py
│   └── SingleWeaponMod.py    # Modification d'une arme précise
├── requirements.txt
└── main.py                   # Point d'entrée

---

# Utilisation Générale
### Menu Principal

- **One Specific Weapon** : Trouver et ajuster une seule arme.
- **Weapons by Ballistics** : Trier les armes par calibre.
- **Ammo Attributes** : Modifier les attributs des munitions.
- **PMC Attributes** : Ajuster les attributs des personnages.

### Modification

- Selon la fenêtre ouverte, vous trouverez des sliders (pourcentage) ou des champs de texte (valeurs absolues).
- Cliquez sur **Apply** pour créer ou mettre à jour le fichier `*_mod.json`

- En bas de la fenêtre principale, des boutons vous montrent la liste des armes ou munitions déjà modifiées.
Vous pouvez supprimer certains ou tous les fichiers *_mod.json.
- vous avez aussi la possibilité d'appliquer la propriété "balles traçantes" à toutes les balles du jeu.

### Retour ou Fermeture
- Fermez la fenêtre secondaire pour revenir au menu principal.
- Quittez l'application ou sélectionnez une autre action.


### Liste et Suppression de Mods
- En bas de la fenêtre principale, des boutons permettent d'afficher la liste des armes ou munitions déjà modifiées.
- Vous pouvez supprimer certains ou tous les fichiers `*_mod.json`.

# Focus sur les Classes Principales

## **ModSelectionWindow** – Menu Principal
- **Fichier** : `ModSelectionWindow.py`
- **Rôle** : Créer la fenêtre principale avec 8 choix possibles (dont 5 vers des classes spécialisées).
- **Points clés** :
  - Gestion des boutons **All Saved Weapons Mod, All Saved Ammo Mod**, etc.
  - Ouverture et fermeture de fenêtres secondaires (`Toplevel`).
  - Suppression globale de Mods (tous les `*_mod.json` d’un certain type).

## **CaliberWeaponsMod** – Modification Groupée par Calibre
- **Fichier** : `WindowComponent/CaliberWeaponsMod.py`
- **Rôle** : Lister toutes les armes d’un calibre donné et appliquer des changements massifs (ex. +20% de dégâts).
- **Points clés** :
  - Sélection/désélection d’armes.
  - Sliders pour ajuster les attributs (dégâts, recul, précision, etc.).
  - Création/suppression automatique de fichiers `*_mod.json`.
  - Pour ce module un fichier de configuration = un calibre
    - Dans le dossier : `JsonFiles/Calibers`

## **SingleWeaponMod** – Modification Ciblée d’une Unique Arme
- **Fichier** : `WindowComponent/SingleWeaponMod.py`
- **Rôle** : Gérer la modification d’une arme précise (via barre de recherche ou liste globale).
- **Points clés** :
  - Chargement du fichier JSON original et vérification d’un éventuel `*_mod.json`.
  - Sliders pour ajustements en pourcentage.
  - Réinitialisation possible si toutes les valeurs reviennent à l’origine.

## **AmmoMod** – Modification de Munitions
- **Fichier** : `WindowComponent/AmmoMod.py`
- **Rôle** : Personnalisation des attributs de munitions (pénétration, dommages, tracer, etc.).
- **Points clés** :
  - Champs de texte (ex. pénétration) et switch (ex. ammo tracer on/off).
  - Contrôle de validité (limites hautes/basses).
  - Création/effacement d’un `*_mod.json` pour activer/désactiver le mod.

## ListItemAlreadyMod – *Liste et suppression de fichiers mod*
- **Fichier** : `WindowComponent/ListItemAlreadyMod.py`  
- **Rôle** : Affiche toutes les armes ou munitions qui ont déjà un `*_mod.json`, ou permet, selon le *WindowType*, de supprimer ces fichiers en un clic.  
- **Points clés** :
  1. **Liste défilante**   
     - Chaque élément est représenté par un bouton.
  2. **Consultation / Suppression**  
     - **Consultation** : Pour `WEAPON` ou `AMMO`, chaque clic sur un bouton ouvre la fenêtre de détail (via `SingleWeaponMod`, `AmmoMod`, etc.).  
     - **Suppression** :  chaque clic sur un bouton supprime immédiatement le `*_mod.json` correspondant à l’élément sélectionné (arme ou munition).
       - La liste est mise à jour (rafraîchie) après la suppression pour ne plus afficher l’élément.  
  3. **Modes d’affichage** :  
     - Ajuste l’interface (taille de la fenêtre, couleur des boutons) en fonction du type d’élément (arme ou munition) et de l’action (simple consultation ou suppression).
  4. **Paramètres** :  
     - `window_type` : un énumérateur (`WindowType`) permettant de distinguer l’opération attendue (WEAPON, AMMO, DELETE).  
     - `weapon_list` : liste d’éléments (armes ou tuples) déjà modifiés et détectés comme `*_mod.json`.

**Exemple d’usage** :
- Depuis la fenêtre principale, vous cliquez sur “All Saved Weapons Mod” :  
  - `ListItemAlreadyMod` est ouverte avec `window_type=WEAPON`, affichant la liste de tous les fichiers `_mod.json` existants pour les armes.  
  - Un clic sur un item ouvre `SingleWeaponMod` pour cette arme.  
- Depuis la fenêtre principale, vous cliquez sur “Select mod to DELETE” :  
  - `ListItemAlreadyMod` est lancée avec `window_type=DELETE`.  
  - Tous les `*_mod.json` (armes et munitions) sont listés et un clic sur l’un d’eux le supprime instantanément. 
  - La liste est automatiquement rafraîchie.

## JsonUtils – *Gestion des fichiers JSON*
- **Fichier** : `Utils/JsonUtils.py`  
- **Rôle** : Centraliser toutes les opérations sur les fichiers JSON, que ce soit pour :
  - **Charger** et **enregistrer** des données (création/suppression de `_mod.json`).
  - **Manipuler** des attributs particuliers (mises à jour, multiplications de valeurs, etc.).
  - **Rechercher** des fichiers correspondants (ex. `find_json_file_with_name`, `find_caliber_json_config`).

- **Fonctionnalités clés** :  
  1. **Chargement et validation de JSON**  
     - Méthodes comme `load_json` ou `load_json_and_add_path` s’assurent que le fichier existe et qu’il contient un JSON valide.  
     - Si un fichier est introuvable ou son contenu illisible, une exception est levée (ex. `FileNotFoundError`, `ValueError`).  

  2. **Gestion des `_mod.json`**  
     - `file_mod_exist(file_path)`, `return_json_mod(file_path)` vérifient et retournent un éventuel fichier `_mod.json` associé à un JSON de base.  
     - `save_json_as_new_file(data, file_path_new_json)` crée un fichier `_mod.json` en supprimant l’ancien s’il existe déjà.  

  3. **Operations CRUD (Create, Read, Update, Delete)**  
     - **Create** : `save_json_as_new_file` ou `write_json` génère un fichier, soit neuf, soit en écrasant l’ancien.  
     - **Read** : `load_json`, `find_caliber_json_config`, ou d’autres méthodes pour localiser un fichier dans les dossiers (`JSON_FILES_DIR_WEAPONS`, etc.).  
     - **Update** : 
       - `update_json_value` et `update_json_caliber` modifient les clés/valeurs selon le `WindowType` (arme, munition, calibre, PMC…).  
       - `update_json_in_new_file_multi_choice` ajoute un chemin partiel dans l’arborescence JSON (`["item", "_props", key]`) pour appliquer la nouvelle valeur.  
       - `update_or_multiply_final_key` gère, pour les armes à *WindowType.CALIBER*, un produit par pourcentage (ex. +20%).  
     - **Delete** : 
       - `delete_file_if_exists` supprime un fichier s’il est présent.  
       - `delete_all_mod` (pour `WindowType.AMMO` ou `WindowType.WEAPON`) efface tous les `_mod.json` existants dans un répertoire.

  4. **Filtrage et récupération en masse**  
     - Méthodes comme `load_all_json_files_without_mod`, `load_all_json_files_weapons_mod` ou `load_all_json_ammo` facilitent le chargement groupé de fichiers.  
     - `load_all_name_json_mod` retourne notamment toutes les armes et munitions sous forme de liste, ce qui est utile pour la classe `ListItemAlreadyMod`.

- **Exemple d’utilisation** :  
  - **Création d’un nouveau mod** : On charge d’abord le JSON d’origine via `load_json(...)`. Puis on modifie la structure en appelant `update_json_in_new_file_multi_choice` et enfin `save_json_as_new_file(...)` qui génère le fichier `_mod.json`.  
  - **Suppression** : Dans l’interface, un clic sur un bouton *Delete* appelle `delete_file_if_exists(...)` pour effacer le `*_mod.json`, et l’UI se met à jour en conséquence.  
  - **Modification groupée** : Pour toutes les armes d’un calibre, on liste leurs fichiers JSON d’origine, on applique les changements avec un coefficient, puis on sauvegarde chaque arme avec `_mod.json`.

Ce module **JsonUtils** est donc au cœur de votre application, car il uniformise l’accès aux données **JSON** et leur mise à jour. Il simplifie également l’implémentation de nouvelles règles ou le support de nouveaux types d’objets en garantissant une interface de lecture/écriture cohérente.
---
## Utils – *Fonctions utilitaires*
- **Fichier** : `Utils/Utils.py`  
- **Rôle** : Fournir diverses fonctions génériques ou spécialisées, utiles à l’interface et à la manipulation de données.  

##### Principales responsabilités
1. **Gestion des interfaces**  
   - **Nettoyage et configuration de widgets** :  
     - `clear_frame` : Efface le contenu d’une frame et réinitialise son découpage en lignes/colonnes.  
     - `configure_grid`, `create_grid_row_col_config` : Aide à configurer les grilles (lignes, colonnes, poids de redimensionnement, etc.).
   - **Aide à la création de sous-frames** (ex. `create_5x4_bottom`) pour organiser dynamiquement des panneaux ou boutons.

2. **Gestion des valeurs numériques**  
   - `float_to_scaled_int` : Convertit un float en un entier *scaled_int* et un facteur d’échelle *scale_factor*.  
   - `determine_format_spec` : Calcule un format (`.2f`, `.3f`, etc.) pour afficher un nombre avec le nombre de décimales adéquat.

3. **Filtrage et déplacements de fichiers**  
   - `remove_file_by_name`, `move_file_between_lists`, `transfer_file_between_lists` : Ces méthodes servent à gérer la liste des chemins de fichiers (p. ex. déplacer un fichier d’une liste “source” vers une liste “cible”). 
   - `transform_list_of_strings`, `remove_jon_extension`, etc. : Fonctions auxiliaires pour uniformiser les noms de fichiers (lowercase, retrait du `.json`…).

4. **Vérification de valeurs limites**  
   - `is_value_outside_limits_weapons`, `is_value_outside_limits_ammo`, `is_value_outside_limits_aiming` : Détermine si un pourcentage ou une valeur (ex. dégâts de munition, cadence de tir) dépasse un seuil.  
   - Les seuils sont définis dans des `dict` spécifiques (p. ex. dégâts min/max = `(1, 450)`).

5. **Gestion de l’interface en cas d’erreur**  
   - `block_all_input_before_correction`, `disable_all_widgets_recursive`, `enable_all_widgets_recursive` : Permettent de **désactiver/réactiver** en masse les widgets (boutons, sliders, etc.) de manière hiérarchique.  
   - `unlock_all`, `unlock_all_buttons_recursive` : Permet de redonner la main à l’utilisateur une fois l’erreur résolue.

6. **Méthodes spécifiques pour munitions traçantes**  
   - `apply_tracer_to_ammo_no_mod_again`, `apply_tracer_to_ammo_with_mod_exist_already` : Applique la propriété “tracer” (booléenne ou couleur) à toutes les munitions, y compris celles qui disposent déjà d’un `*_mod.json`.

#### Exemples d’usage
- **Gestion de la fenêtre** : Dans `ModSelectionWindow`, on appelle `Utils.clear_frame` pour vider la zone avant de recréer des boutons.  
- **Contrôle de saisie** : Dans `AmmoMod`, si l’utilisateur entre une valeur hors limite, `Utils.is_value_outside_limits_ammo` renvoie `True`, ce qui bloque les contrôles et affiche un message d’erreur.
- **Modification globale** : Dans `apply_tracer_to_ammo_no_mod_again`, on parcourt chaque fichier de munition, on utilise `JsonUtils` pour charger et sauvegarder, et on insère l’info “tracer = true + red/green” via `Utils.modify_json_value`.

En résumé, **`Utils.py`** agit comme une boîte à outils pour d’autres classes (interface ou manipulation de données), afin d’éviter la duplication de code et de regrouper la logique “utilitaire” en un seul endroit.
---

## config.py – *Gestion des chemins et validation de l’arborescence*

- **Fichier** : `config.py`
- **Rôle** :  
  - Centraliser les chemins (path) vers les répertoires du projet (ex. `JsonFiles/Weapons`, `JsonFiles/Ammo`, etc.)  
  - Vérifier que l’arborescence du projet est cohérente (dossiers existants et non vides)  
  - Valider les fichiers JSON (ex. corriger certaines valeurs par défaut pour les calibres)

#### Variables principales
1. **`BASE_DIR`** : Le dossier de base, déterminé selon que l’application est exécutée en `.exe` (mode “frozen”) ou en script Python classique.  
2. **`JSON_FILES_DIR_*`** : Références aux sous-dossiers où se trouvent les armes (`Weaps`), les calibres (`Calibers`), les PNJ (`PMC`), les munitions (`Ammo`), etc.  
3. **`IMAGES_DIR`** : Contient vos ressources graphiques (icônes, images).

#### Fonctions principales
1. **`check_project_structure()`**  
   - Vérifie l’existence des dossiers listés dans `REQUIRED_DIRS`.  
   - S’assure qu’ils ne sont pas vides.  
   - Valide aussi le format JSON de tous les fichiers *.json* dans chaque dossier (si un fichier est corrompu, lève une erreur).

2. **`check_and_fix_json_caliber_files()`**  
   - Parcourt tous les JSON relatifs aux calibres.  
   - Si une valeur numéraire (int/float) est trop faible ou nulle, la corrige à `1.0` pour éviter les divisions par zéro ou configurations invalides.  
   - Affiche un récapitulatif des fichiers modifiés, du nombre de fichiers manquants ou supplémentaires selon un plafond/maximum attendu (`caliber_max_min_count`).

3. **`check_json_files(directory)`**  
   - Valide chaque fichier du répertoire passé en paramètre pour s’assurer qu’il contient un JSON valide (ex. pas de `JSONDecodeError`).

4. **`relatif_path(path)`**  
   - Renvoie un chemin relatif à `BASE_DIR`, utile pour afficher des chemins plus courts dans les logs.

#### Exemples d’utilisation

- **Au lancement** : Dans `main.py` (ou équivalent), on appelle ces fonctions pour vérifier que la structure du projet est correcte (dossiers et JSON), et on corrige éventuellement des valeurs pour les calibres.  
- **En mode exécutable** : La logique détecte si l’application est lancée via un `.exe` (PyInstaller ou similaire). Dans ce cas, le chemin racine (`BASE_DIR`) est modifié en conséquence.  
- **Journalisation** : Lorsqu’il manque des dossiers ou que des JSON sont illisibles, le script affiche des messages d’erreur et peut stopper l’exécution pour éviter des plantages ultérieurs.

Ce fichier **`config.py`** est donc essentiel pour maintenir un environnement cohérent : il garantit que toutes les ressources (fichiers JSON ou dossiers) sont en place et valides avant de démarrer le cœur de l’application.
---

## Exemples de fichiers JSON

Cette application se base sur des fichiers JSON pour décrire les objets (armes, munitions, etc.) que vous souhaitez modifier. Ci-dessous, deux exemples de fichiers, l’un pour une munition (`.json` à placer dans `JsonFiles/Ammo/`), et l’autre pour une arme (`.json` à placer dans `JsonFiles/Weapons/`).

### Exemple : Munition

#### Fichier : `45_ACP_AP.json`

```json
{
  "item": {
    "_id": "5efb0cabfb3e451d70735af5",
    "_name": "patron_1143x23_acp_ap",
    "_props": {
      "ArmorDamage": 48,
      "Caliber": "Caliber1143x23ACP",
      "Damage": 66,
      "InitialSpeed": 299,
      "PenetrationPower": 38,
      "StackMaxSize": 50,
      "Tracer": false,
      "TracerColor": "red"
    }
  },
  "locale": {
    "Name": ".45 ACP AP",
    "ShortName": "AP"
  }
}
```

### Exemple : Arme

#### Fichier : `weapon_kbp_9a91_9x39.json`

```json
{
  "item": {
    "_id": "644674a13d52156624001fbc",
    "_name": "weapon_kbp_9a91_9x39",
    "_props": {
      "CameraSnap": 2.2,
      "AimSensitivity": 0.65,
      "Ergonomics": 50,
      "RecoilCamera": 0.05,
      "RecoilForceBack": 280,
      "RecoilForceUp": 110,
      "RecolDispersion": 14,
      "Weight": 0.92,
      "ammoCaliber": "Caliber9x39",
      "bFirerate": 700
    }
  },
  "locale": {
    "Name": "KBP 9A-91 9x39 compact assault rifle",
    "ShortName": "9A-91"
  }
}
```

Avec ce type de structuration, l’application peut identifier facilement chaque objet (via `item._id` et `item._name`),
récupérer et afficher ses propriétés (`_props`), puis créer (ou mettre à jour) des mods séparés (`*_mod.json`) afin de ne jamais altérer vos fichiers de base.

### Explication
- Lorsqu’un fichier JSON est chargé, ses valeurs sont extraites et utilisées pour initialiser un objet `Ammo`.
- `props.get(EnumAmmo.DAMAGE.label, None)` permet de récupérer la valeur de l’attribut dans le fichier JSON.
- Chaque propriété est stockée sous forme d’un tuple contenant la valeur et son label d’origine pour assurer un suivi clair.
- La méthode `convert_to_boolean` est utilisée pour convertir certains attributs (`TracerColor`) String ==> Boolean en format approprié.

Ce modèle est également utilisé pour les objets `Weapon`, suivant la même logique de liaison entre le JSON et les objets Python manipulés dans l’application.


## Dépendances
- **Python** 3.9+
- **customtkinter**
- **CTkMessagebox**
- **Pillow**
- (Consultez `requirements.txt` pour la liste complète des bibliothèques nécessaires.)

