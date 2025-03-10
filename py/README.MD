# ModParameter App

## Table des matières
1. [Aperçu du projet](#aperçu-du-projet)
2. [Fonctionnalités principales](#fonctionnalités-principales)
3. [Structure du projet](#structure-du-projet)
5. [Lancement de l’application](#lancement-de-lapplication)
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
**ModParameter App** est une application Python conçue pour créer et gérer des “mods” (fichiers `*_mod.json`) relatifs à différents éléments d’un jeu (armes, munitions, PNJ, etc.). Elle utilise **[customtkinter](https://github.com/TomSchimansky/CustomTkinter)** pour son interface graphique et manipule des **fichiers JSON** pour charger, modifier ou supprimer des valeurs de configuration.

---

## Fonctionnalités principales
1. **Interface graphique intuitive**  
   - Menu principal avec choix de modification (armes, munitions, etc.).  
   - Fenêtres dédiées pour configurer un objet ou un groupe d’objets.

2. **Gestion centralisée de Mods**  
   - Création automatique de fichiers `*_mod.json` pour séparer les modifications du fichier de base.  
   - Suppression ciblée ou globale de ces fichiers, permettant de revenir à l’état “vanilla”.

3. **Recherche et tri**  
   - Filtrer des armes via leur nom (ou _ShortName_).  
   - Sélectionner toutes les armes d’un même calibre.  
   - Lister toutes les munitions déjà modifiées.

4. **Édition et contrôle**  
   - Barres de glissement (sliders) pour ajuster en pourcentage les stats d’armes.  
   - Champs de saisie pour fixer manuellement des valeurs (ex. pénétration de munitions).  
   - Indicateurs d’éventuels dépassements (ex. seuils de sécurité) ou d’erreur d’entrée.

5. **Feedback visuel**  
   - Barres de progression pour afficher l’évolution de l’opération.  
   - Étiquettes de statut (ex. “Changes applied successfully” ou “All modifications removed”).

---

## Structure du projet

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
│   ├── ProgressBar.py
│   └── SingleWeaponMod.py    # Modification d'une arme précise
├── ModSelectionWindow.py     # Classe principale (menu)
├── requirements.txt
└── main.py                   # Point d'entrée

## Lancement de l’application
- Placez-vous à la racine du projet.
- le main.py se trouve dans le répertoire main
- La fenêtre ModParameter App s’affiche, proposant différents choix.

## Utilisation Générale
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

## Focus sur les Classes Principales

### **ModSelectionWindow** – Menu Principal
- **Fichier** : `ModSelectionWindow.py`
- **Rôle** : Créer la fenêtre principale avec 8 choix possibles (dont 5 vers des classes spécialisées).
- **Points clés** :
  - Gestion des boutons **All Saved Weapons Mod, All Saved Ammo Mod**, etc.
  - Ouverture et fermeture de fenêtres secondaires (`Toplevel`).
  - Suppression globale de Mods (tous les `*_mod.json` d’un certain type).

### **CaliberWeaponsMod** – Modification Groupée par Calibre
- **Fichier** : `WindowComponent/CaliberWeaponsMod.py`
- **Rôle** : Lister toutes les armes d’un calibre donné et appliquer des changements massifs (ex. +20% de dégâts).
- **Points clés** :
  - Sélection/désélection d’armes.
  - Sliders pour ajuster les attributs (dégâts, recul, précision, etc.).
  - Création/suppression automatique de fichiers `*_mod.json`.

### **SingleWeaponMod** – Modification Ciblée d’une Unique Arme
- **Fichier** : `WindowComponent/SingleWeaponMod.py`
- **Rôle** : Gérer la modification d’une arme précise (via barre de recherche ou liste globale).
- **Points clés** :
  - Chargement du fichier JSON original et vérification d’un éventuel `*_mod.json`.
  - Sliders pour ajustements en pourcentage.
  - Réinitialisation possible si toutes les valeurs reviennent à l’origine.

### **AmmoMod** – Modification de Munitions
- **Fichier** : `WindowComponent/AmmoMod.py`
- **Rôle** : Personnalisation des attributs de munitions (pénétration, dommages, tracer, etc.).
- **Points clés** :
  - Champs de texte (ex. pénétration) et switch (ex. ammo tracer on/off).
  - Contrôle de validité (limites hautes/basses).
  - Création/effacement d’un `*_mod.json` pour activer/désactiver le mod.

### **ListItemAlreadyMod** – Liste et Suppression des Mods
- **Fichier** : `WindowComponent/ListItemAlreadyMod.py`
- **Rôle** : Affiche toutes les armes ou munitions ayant un `*_mod.json`.
- **Points clés** :
  - Liste défilante (Scrollbar + Canvas) pour navigation.
  - Boutons pour chaque mod (ligne ou case).
  - **Suppression** : En mode "Delete", un clic supprime immédiatement le fichier `*_mod.json`, avec mise à jour de la liste.
  - **Ouverture** : En mode "consultation" (`WindowType.WEAPON` / `WindowType.AMMO`), un clic ouvre la fenêtre de détail correspondante (`SingleWeaponMod`, `AmmoMod`, etc.).

---

## Dépendances
- **Python** 3.9+
- **customtkinter**
- **CTkMessagebox**
- **Pillow**
- (Consultez `requirements.txt` pour la liste complète des bibliothèques nécessaires.)

