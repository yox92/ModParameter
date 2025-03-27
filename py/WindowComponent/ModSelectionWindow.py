import customtkinter as ctk
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox

from Entity import Caliber, Root, Logger, CategoryColor
from Entity.Bag import Bag
from Entity.EnumBagSize import EnumBagSize
from Entity.EnumMagSize import EnumMagSize
from Entity.Mag import Mag
from Entity.MedicCat import MedicalCat
from Entity.WindowType import WindowType
from Utils import WindowUtils
from Utils.ImageUtils import ImageUtils
from Utils.JsonUtils import JsonUtils
from Utils.Utils import Utils
from WindowComponent.AmmoMod import AmmoMod
from WindowComponent.MedicMod import MedicMod
from WindowComponent.PmcMod import PmcMod
from WindowComponent.CaliberWeaponsMod import CaliberWeaponsMod
from WindowComponent.SingleWeaponMod import SingleWeaponMod
from WindowComponent.ListItemAlreadyMod import ListItemAlreadyMod

WINDOW_TITLE = "ModParameter App"
POP_UP_DELETE_TITLE = "All Delete Or Choice Which One?"
POP_UP_CATEGORIES_TITLE = "Categorie to Delete?"
MESSAGE_DELETE = "Choose an option: Delete All Item By categories or Select a Mod to Delete"
MESSAGE_CATEGORIES_DELETE = "Choose an option: Delete All Ammo/Weapons/Medical"
WINDOW_GEOMETRY = "870x650"
APPEARANCE_MODE = "dark"
DETAIL_WINDOW_TITLE = "Detail windows"
DETAIL_WINDOW_WIDTH = 900
DETAIL_WINDOW_HEIGHT = 700
WINDOW_OFFSET = 10


class ModSelectionWindow:
    def __init__(self, root):
        self.list_medic_select = None
        self.medic_image = None
        self.button_medic = None
        self.frame_top_5 = None
        self.entry = None
        self.loaded_data_ammo = None
        self.button_delete_mod = None
        self.button_all_ammo_tracer = None
        self.list_json_name_all_mod = None
        self.logger = Logger()
        self.button_frame = None
        self.button_view_all_ammo_mod = None
        self.button_view_all_weapons_mod = None
        self.list_json_name_mod_ammo = None
        self.file_path_from_load_all_ammo = None
        self.file_path_from_load_all_medic = None
        self.data_json_from_load_all_ammo = None
        self.data_json_from_load_all_medic = None
        self.list_ammo_select = None
        self.root = root
        self.frame_top_2 = None
        self.ammo_image = None
        self.frames_buttons = None
        self.button_ammo = None
        self.frame_top_3 = None
        ctk.set_appearance_mode(APPEARANCE_MODE)
        self.button_pmc = None
        self.loaded_data = None
        self.frame_top_4 = None
        self.main_frame_top = None
        self.main_frame_bot = None
        self.frame_bot_bot = None
        self.frame_bot_top = None
        self.frame_top_1 = None
        self.weapon_image = None
        self.caliber_image = None
        self.pmc_image = None
        self.buttonWeapon = None
        self.button_caliber = None
        self.detail_window = None
        self.framesBotRecherche = []
        self.list_json_name_mod_weapons = []
        self.framesBotCaliber = []
        self.framesButtonRecherche = []
        self.message_not_find = []

        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)

        self.run()

    def run(self):
        self.loaded_data = JsonUtils.load_all_json_files_without_mod()
        self.loaded_data_ammo = JsonUtils.load_all_json_files_without_mod_ammo()
        self.loaded_data_medic = JsonUtils.load_all_json_files_without_mod_medic()
        self.list_json_name_mod_weapons = JsonUtils.load_all_json_files_weapons_mod()
        self.list_json_name_mod_ammo = JsonUtils.load_all_name_json_files_ammo_mod()
        self.create_frame_main()
        self.create_image_var()
        self.create_frame_top()
        self.create_buttons_for_choice()

    def create_image_var(self):
        self.caliber_image: CTkImage = ImageUtils.create_image_var("caliber")
        self.weapon_image: CTkImage = ImageUtils.create_image_var("weapon")
        self.pmc_image: CTkImage = ImageUtils.create_image_var("pmc")
        self.ammo_image: CTkImage = ImageUtils.create_image_var("ammo")
        self.medic_image: CTkImage = ImageUtils.create_image_var("medic")
        self.stim_image: CTkImage = ImageUtils.create_image_var("stim")
        self.painkiller_image: CTkImage = ImageUtils.create_image_var("painkiller")
        self.salewa_image: CTkImage = ImageUtils.create_image_var("salewa")
        self.bandage_image: CTkImage = ImageUtils.create_image_var("bandage")
        self.bag_mag_image: CTkImage = ImageUtils.create_image_var("mbag")
        self.bag_image: CTkImage = ImageUtils.create_image_var("bag")
        self.mag_image: CTkImage = ImageUtils.create_image_var("mag")

    def create_frame_main(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=8)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.active_window_list_weapons_already_mod()
        self.active_window_list_ammo_already_mod()

    def active_window_list_weapons_already_mod(self):
        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.grid(row=2, column=0, pady=5)
        self.button_view_all_weapons_mod = ctk.CTkButton(
            self.button_frame,
            text="All Saved Weapons Mod",
            compound="top",
            fg_color="green",
            text_color="black",
            hover_color="white",
            font=("Arial", 15, "bold"),
            height=10,
            width=10,
            command=self.show_all_weapons_mod
        )
        self.button_view_all_weapons_mod.grid(row=0, column=0, padx=10)
        if self.list_json_name_mod_weapons:
            self.button_view_all_weapons_mod.configure(text="All Saved Weapons Mod")
        else:
            self.button_view_all_weapons_mod.configure(text="No weapons mod find")
        self.button_view_all_medic_mod = ctk.CTkButton(
            self.button_frame,
            text="All Saved Medic Mod",
            compound="top",
            fg_color="cyan",
            text_color="black",
            hover_color="white",
            font=("Arial", 15, "bold"),
            height=10,
            width=10,
            command=self.show_all_medic_mod
        )
        self.button_view_all_medic_mod.grid(row=0, column=2, padx=10)

    def active_window_list_ammo_already_mod(self):
        self.button_view_all_ammo_mod = ctk.CTkButton(
            self.button_frame,
            text="All Saved Ammo Mod",
            compound="top",
            fg_color="yellow",
            text_color="black",
            hover_color="white",
            font=("Arial", 15, "bold"),
            height=10,
            width=10,
            command=self.show_all_ammo_mod
        )
        self.button_view_all_ammo_mod.grid(row=0, column=1, padx=10)
        self.button_all_ammo_tracer = ctk.CTkButton(
            self.button_frame,
            text="All Ammo Tracer ?",
            compound="top",
            fg_color="blue",
            text_color="white",
            hover_color="black",
            font=("Arial", 15, "bold"),
            height=10,
            width=10,
            command=self.all_ammo_tracer
        )
        self.button_all_ammo_tracer.grid(row=0, column=3, padx=10)
        self.button_delete_mod = ctk.CTkButton(
            self.button_frame,
            text="Select mod to DELETE",
            compound="top",
            fg_color="RED",
            text_color="white",
            hover_color="black",
            font=("Arial", 15, "bold"),
            height=10,
            width=10,
            command=self.all_mod_to_delete
        )
        self.button_delete_mod.grid(row=0, column=4, padx=10)
        if self.list_json_name_mod_ammo:
            self.button_view_all_ammo_mod.configure(text="All Saved Ammo Mod")
        else:
            self.button_view_all_ammo_mod.configure(text="All Saved Ammo Mod")

    def all_ammo_tracer(self):
        msg_choice = CTkMessagebox(title="All Ammo Tracer ?",
                                   message="Would you like all the bullets in the game to become tracer rounds",
                                   icon="warning", option_1="No", option_2="Yes")
        response = msg_choice.get()

        if response == "Yes":
            msg_color = CTkMessagebox(title="Which color ?",
                                      message="Which color do you want to apply ",
                                      icon="info", option_1="Cancel", option_2="Green", option_3="Red", )
            response_color = msg_color.get()

            if response_color == "Red":
                self.apply_all_ammo_tracer(False)
            elif response_color == "Green":
                self.apply_all_ammo_tracer(True)
            else:
                print("Too bad, wise decision")
        elif response == "No":
            self.remove_tracer()

    def remove_tracer(self):
        JsonUtils.update_tracer(False, False)

    def apply_all_ammo_tracer(self, color: bool):
        list_path_ammo: list = []
        list_path_ammo_mod_without_mod_at_the_end = JsonUtils.get_file_path_json_all_mod_ammo(True)

        for data in self.loaded_data_ammo:
            if data["file_path"] not in list_path_ammo_mod_without_mod_at_the_end:
                list_path_ammo.append(data["file_path"])

        if list_path_ammo_mod_without_mod_at_the_end:
            Utils.apply_tracer_to_ammo_with_mod_exist_already(color)
        JsonUtils.update_tracer(True, color)

    def all_mod_to_delete(self):
        msg_choice = CTkMessagebox(title=POP_UP_DELETE_TITLE,
                                   message=MESSAGE_DELETE,
                                   icon="warning", option_1="Select categories", option_2="Select One")
        response = msg_choice.get()
        if response == "Select categories":
            msg_choice_bis = CTkMessagebox(title=POP_UP_CATEGORIES_TITLE,
                                           message=MESSAGE_CATEGORIES_DELETE,
                                           icon="warning", option_1="All Ammos", option_2="All Weapons",
                                           option_3="All medicals")
            responseBis = msg_choice_bis.get()
            if responseBis == "ALl Ammo":
                ModSelectionWindow.delete_all_items(WindowType.AMMO)
            elif responseBis == "All Weapons":
                ModSelectionWindow.delete_all_items(WindowType.WEAPON)
            elif responseBis == "All medicals":
                ModSelectionWindow.delete_all_items(WindowType.MEDIC)
            else:
                print("no choice")
        elif response == "Select One":
            self.list_json_name_all_mod = JsonUtils.load_all_name_json_mod()
            if self.list_json_name_all_mod:
                self.detail_window = ctk.CTkToplevel(self.root)
                self.focus_new_window()
                ListItemAlreadyMod(self.detail_window,
                                   self.root,
                                   self.detail_window,
                                   self.list_json_name_all_mod,
                                   self, WindowType.DELETE)
        else:
            print("no choice")

    def create_frame_top(self):
        self.main_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame_bot = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame_top.grid(row=0, column=0, sticky="nsew")
        self.main_frame_bot.grid(row=1, column=0, sticky="nsew")
        self.main_frame_top.grid_columnconfigure(0, weight=1)
        self.main_frame_top.grid_columnconfigure(1, weight=1)
        self.main_frame_top.grid_columnconfigure(2, weight=1)
        self.main_frame_top.grid_columnconfigure(3, weight=1)
        self.main_frame_top.grid_columnconfigure(4, weight=1)
        self.main_frame_top.grid_columnconfigure(5, weight=1)
        self.main_frame_top.grid_rowconfigure(0, weight=1)

        self.frame_top_1 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_2 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_3 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_4 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_5 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_6 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_1.grid(row=0, column=0, sticky="nsew")
        self.frame_top_2.grid(row=0, column=1, sticky="nsew")
        self.frame_top_3.grid(row=0, column=2, sticky="nsew")
        self.frame_top_4.grid(row=0, column=3, sticky="nsew")
        self.frame_top_5.grid(row=0, column=4, sticky="nsew")
        self.frame_top_6.grid(row=0, column=5, sticky="nsew")

    def show_all_weapons_mod(self):
        self.list_json_name_mod_weapons = JsonUtils.load_all_json_files_weapons_mod()
        if self.list_json_name_mod_weapons:
            self.detail_window = ctk.CTkToplevel(self.root)

            self.focus_new_window()

            ListItemAlreadyMod(self.detail_window,
                               self.root,
                               self.detail_window,
                               self.list_json_name_mod_weapons,
                               self, WindowType.WEAPON)
        else:
            self.buttonWeapon.configure(text="No weapons mod find")

    def show_all_medic_mod(self):
        self.list_json_name_mod_medic = JsonUtils.load_all_json_files_medic_mod()
        if self.list_json_name_mod_medic:
            self.detail_window = ctk.CTkToplevel(self.root)

            self.focus_new_window()

            ListItemAlreadyMod(self.detail_window,
                               self.root,
                               self.detail_window,
                               self.list_json_name_mod_medic,
                               self, WindowType.MEDIC)
        else:
            self.buttonWeapon.configure(text="No medic mod find")

    def show_all_ammo_mod(self):
        self.list_json_name_mod_ammo = JsonUtils.load_all_name_json_files_ammo_mod()
        if self.list_json_name_mod_ammo:
            self.detail_window = ctk.CTkToplevel(self.root)

            self.focus_new_window()

            ListItemAlreadyMod(self.detail_window,
                               self.root,
                               self.detail_window,
                               self.list_json_name_mod_ammo,
                               self, WindowType.AMMO)
        else:
            self.buttonWeapon.configure(text="All Saved Ammo Mod")

    def create_buttons_for_choice(self):
        self.buttonWeapon = ctk.CTkButton(
            self.frame_top_1,
            image=self.weapon_image,
            text="Specific Weapon",
            compound="bottom",
            fg_color="transparent",
            text_color="orange",
            hover_color="whitesmoke",
            font=("Arial", 16, "bold"),
            command=lambda: self.generate_bot_frame_weapon_and_ammo(WindowType.WEAPON)
        )
        self.buttonWeapon.pack(side="top", anchor="center",
                               expand=True, fill="both")

        self.button_caliber = ctk.CTkButton(
            self.frame_top_2,
            image=self.caliber_image,
            text="Weapons by Caliber",
            compound="bottom",
            fg_color="transparent",
            text_color="Crimson",
            hover_color="whitesmoke",
            font=("Arial", 16, "bold"),
            command=lambda: self.generate_list_button(WindowType.CALIBER)
        )
        self.button_caliber.pack(side="top", anchor="center",
                                 expand=True, fill="both")
        self.button_ammo = ctk.CTkButton(
            self.frame_top_3,
            image=self.ammo_image,
            text="Ammo",
            compound="bottom",
            fg_color="transparent",
            text_color="FireBrick",
            hover_color="whitesmoke",
            font=("Arial", 16, "bold"),
            command=self.ammo_window
        )
        self.button_ammo.pack(side="top", anchor="center",
                              expand=True, fill="both")
        self.button_pmc = ctk.CTkButton(
            self.frame_top_4,
            image=self.pmc_image,
            text="PMC",
            compound="bottom",
            fg_color="transparent",
            text_color="green",
            hover_color="whitesmoke",
            font=("Arial", 16, "bold"),
            command=self.pmc_window
        )
        self.button_pmc.pack(side="top", anchor="center",
                             expand=True, fill="both")
        self.button_medic = ctk.CTkButton(
            self.frame_top_5,
            image=self.medic_image,
            text="Medical",
            compound="bottom",
            fg_color="transparent",
            text_color="red",
            hover_color="whitesmoke",
            font=("Arial", 16, "bold"),
            command=lambda: self.generate_list_button(WindowType.MEDIC)
        )
        self.button_medic.pack(side="top", anchor="center",
                               expand=True, fill="both")
        self.button_mag = ctk.CTkButton(
            self.frame_top_6,
            image=self.bag_mag_image,
            text="Bag / Mag",
            compound="bottom",
            fg_color="transparent",
            text_color="cyan",
            hover_color="whitesmoke",
            font=("Arial", 16, "bold"),
            command=lambda: self.generate_list_button(WindowType.MAG)
        )
        self.button_mag.pack(side="top", anchor="center",
                               expand=True, fill="both")
        self.frames_buttons = {
            "weapon": self.buttonWeapon,
            "caliber": self.button_caliber,
            "pmc": self.button_pmc,
            "ammo": self.button_ammo,
            "medic": self.button_medic,
            "mag": self.button_mag
        }

    def generate_list_button(self, choice_window: WindowType):
        if choice_window == WindowType.AMMO:
            WindowUtils.lock_choice_frame("ammo", self.frames_buttons)
        elif choice_window == WindowType.CALIBER:
            WindowUtils.lock_choice_frame("caliber", self.frames_buttons)
        elif choice_window == WindowType.MEDIC:
            WindowUtils.lock_choice_frame("medic", self.frames_buttons)
        elif choice_window == WindowType.MAG:
            WindowUtils.lock_choice_frame("mag", self.frames_buttons)

        Utils.clear_frame(self.main_frame_bot)
        if choice_window == WindowType.AMMO or choice_window == WindowType.CALIBER:
            Utils.create_grid_row_col_config(self.main_frame_bot, 5, 5)
            Utils.create_5x5_bottom(self.framesBotCaliber, self.main_frame_bot, choice_window)
            self.create_buttons_for_calibers_ammo(choice_window)
        elif choice_window == WindowType.MEDIC:
            Utils.create_grid_row_col_config(self.main_frame_bot, 1, 4)
            Utils.create_1x4_bottom(self.framesBotCaliber, self.main_frame_bot)
            self.create_buttons_for_medic(choice_window)
        elif choice_window == WindowType.MAG:
            Utils.create_grid_row_col_config(self.main_frame_bot, 1, 2)
            Utils.create_1x2_bottom(self.framesBotCaliber, self.main_frame_bot)
            self.create_buttons_for_bag_mag()

    def pmc_window(self):
        WindowUtils.lock_choice_frame("pmc", self.frames_buttons)

        Utils.clear_frame(self.main_frame_bot)
        self.detail_window = ctk.CTkToplevel(self.root)

        self.focus_new_window()

        PmcMod(self.detail_window,
               self.root,
               self.detail_window,
               self)

    def create_frame_bot_find_weapon(self):
        Utils.clear_frame(self.main_frame_bot)
        Utils.clear_config_row_col(self.main_frame_bot)

        self.main_frame_bot.grid_columnconfigure(0, weight=1)
        self.main_frame_bot.grid_columnconfigure(1, weight=0)
        self.main_frame_bot.grid_rowconfigure(0, weight=1)
        self.main_frame_bot.grid_rowconfigure(1, weight=10)

        self.frame_bot_top = ctk.CTkFrame(self.main_frame_bot, fg_color="transparent")
        self.frame_bot_bot = ctk.CTkFrame(self.main_frame_bot, fg_color="transparent")

        self.frame_bot_top.grid(row=0, column=0, sticky="nsew")
        self.frame_bot_bot.grid(row=1, column=0, sticky="nsew")

    def generate_bot_frame_weapon_and_ammo(self, choice_window: WindowType):
        self.create_frame_bot_find_weapon()

        Utils.create_grid_row_col_config(self.frame_bot_top, 1, 1)
        Utils.create_grid_row_col_config(self.frame_bot_bot, 3, 3)
        if choice_window == WindowType.WEAPON:
            WindowUtils.lock_choice_frame("weapon", self.frames_buttons)
            self.create_bind_entry_bar(self.frame_bot_top)
            self.entry.bind("<KeyRelease>", self.search_name)
        elif choice_window == WindowType.AMMO:
            self.populate_buttons(self.list_ammo_select, choice_window)
        elif choice_window == WindowType.MEDIC:
            self.populate_buttons(self.list_medic_select, choice_window)

    def ammo_window(self):
        WindowUtils.lock_choice_frame("ammo", self.frames_buttons)
        self.generate_list_button(WindowType.AMMO)

    def medic_window(self):
        WindowUtils.lock_choice_frame("medic", self.frames_buttons)
        self.generate_list_button(WindowType.MEDIC)

    def search_name(self, event=None):
        name_to_search = self.entry.get()
        if len(name_to_search) >= 2:
            self.clear_recherche_frame()
            results = self.find_name_in_loaded_data(name_to_search)
            if results:
                self.populate_buttons(results, WindowType.WEAPON)
            else:
                label = ctk.CTkLabel(self.frame_bot_bot, text="No matching name found.")
                label.grid(row=0, column=0, sticky="nsew")
                self.message_not_find.append(label)
        else:
            self.clear_recherche_frame()

    def populate_buttons(self, results, window_type: WindowType):
        max_items = 20
        items_per_row = 5
        total_rows = (max_items + items_per_row - 1) // items_per_row

        Utils.configure_grid(
            self.frame_bot_bot,
            rows=total_rows,
            cols=items_per_row,
            weight=1)
        if window_type == WindowType.AMMO or window_type == WindowType.MEDIC:
            results = [{"short_name": root.locale.ShortName, "name": root.locale.Name} for root in results]
            button = ctk.CTkButton(self.frame_bot_top,
                                   text="<== BACK ==>",
                                   command=self.ammo_window,
                                   fg_color="orange",
                                   font=("Arial", 20, "bold"),
                                   text_color="black")
            button.grid(row=2, column=0, padx=5, pady=5)
            if window_type == WindowType.AMMO:
                button.configure(command=self.ammo_window)
            elif window_type == WindowType.MEDIC:
                button.configure(command=self.medic_window)

        for idx, result in enumerate(results[:max_items]):
            frame_recherche_m = ctk.CTkFrame(self.frame_bot_bot, fg_color="transparent")
            row, col = divmod(idx, items_per_row)
            frame_recherche_m.grid(row=row,
                                   column=col,
                                   padx=5,
                                   pady=5,
                                   sticky="nsew")
            self.framesBotRecherche.append(frame_recherche_m)

            button = ctk.CTkButton(frame_recherche_m,
                                   font=("Arial", 20, "bold"),
                                   text_color="black")
            button.pack(expand=True)
            if window_type == WindowType.WEAPON:
                button.configure(text=result,
                                 command=lambda r=result: self.on_click_result(r,
                                                                               window_type))
            elif window_type == WindowType.AMMO:
                button.configure(text=result["short_name"],
                                 command=lambda r=result: self.on_click_result(r["name"],
                                                                               window_type))
            elif window_type == WindowType.MEDIC:
                button.configure(text=result["short_name"],
                                 command=lambda r=result: self.on_click_result(r["name"],
                                                                               window_type))
            self.framesButtonRecherche.append(button)

    def on_click_result(self, result, window_type: WindowType):
        if window_type == WindowType.WEAPON:
            for data in self.loaded_data:
                if data['locale']['ShortName'] == result:
                    file_path = data['file_path']
                    self.open_specific_window(file_path, WindowType.WEAPON)
                    break
            else:
                self.logger.log("info", f"File ignore : {result}")
        elif window_type == WindowType.AMMO:
            json_filename = self.sanitize_filename(result)
            matching_file = next(
                (fp for fp in self.file_path_from_load_all_ammo if fp.endswith(json_filename)),
                None)
            if matching_file:
                self.open_specific_window(matching_file, WindowType.AMMO)
            else:
                raise FileNotFoundError(f"File '{json_filename}' do not existe / not find")
        elif window_type == WindowType.MEDIC:
            json_filename = self.sanitize_filename(result)
            matching_file = next(
                (fp for fp in self.file_path_from_load_all_medic if fp.endswith(json_filename)),
                None)
            if matching_file:
                self.open_specific_window(matching_file, WindowType.MEDIC)
            else:
                raise FileNotFoundError(f"File '{json_filename}' do not existe / not find")

    @staticmethod
    def sanitize_filename(name: str) -> str:
        return name.replace('(', '') \
            .replace(')', '') \
            .replace(' ', '_') \
            .replace('/', '') \
            .replace('\\', '') + ".json"

    def find_name_in_loaded_data(self, name):
        matches = []
        for data in self.loaded_data:
            name_field = data.get("locale", {}).get("Name")
            if isinstance(name_field, str) and name.lower() in name_field.lower():
                cleaned_name = (data.get("locale", {}).get("ShortName"))
                matches.append(cleaned_name)
        return matches

    def create_bind_entry_bar(self, frame):
        self.entry = ctk.CTkEntry(frame, placeholder_text="Weapons text ...", width=400)
        self.entry.pack(side="top", anchor="center")

    def create_buttons_for_calibers_ammo(self, choice_window: WindowType):
        row = 1
        column = 0
        available_frames = len(self.framesBotCaliber)
        calibers_to_display = []
        grenade_fusion_done = False
        for label, code, categorie in Caliber.enumerate_calibers():
            if choice_window == WindowType.WEAPON and label in {Caliber.GRENADE_40x46.label, Caliber.UTYOS_AGS.label,
                                                                Caliber.Caliber40mmRU.label}:
                continue
            if label == Caliber.Caliber40mmRU.label:
                continue
            if label in {Caliber.GRENADE_40x46.label, Caliber.Caliber40mmRU.label}:
                if not grenade_fusion_done:
                    calibers_to_display.append((Caliber.to_tuple(Caliber.GRENADE_40x46)))
                    grenade_fusion_done = True
                continue
            if label == Caliber.UTYOS_AGS.label:
                calibers_to_display.append((label, code, categorie))

            calibers_to_display.append((label, code, categorie))

        if len(calibers_to_display) != available_frames:
            calibers_to_display = calibers_to_display[:available_frames]

        for idx, (label, code, categorie) in enumerate(calibers_to_display):

            color = CategoryColor.get(categorie)
            idx: int

            button = ctk.CTkButton(
                self.framesBotCaliber[idx],
                text=label,
                width=150,
                text_color="black",
                fg_color=color,
                font=("Arial", 15, "bold")
            )

            button.pack(side="top", anchor="center")

            if choice_window == WindowType.AMMO:
                button.configure(command=lambda r=code: self.ammo_button_press(r, choice_window))
            elif choice_window == WindowType.CALIBER:
                button.configure(command=lambda r=code: self.open_specific_window(r, choice_window))

            column += 1
            if column >= 5:
                column = 0
                row += 1

    def create_buttons_for_medic(self, choice_window: WindowType):
        column = 0
        for idx, (label, code) in enumerate(MedicalCat.enumerate_medical()):
            idx: int
            button = ctk.CTkButton(
                self.framesBotCaliber[idx],
                image=self.stim_image,
                text=label,
                width=150,
                compound="bottom",
                fg_color="transparent",
                text_color="white",
                font=("Arial", 20, "bold")
            )
            if label == MedicalCat.STIMULATOR.label:
                button.configure(image=self.stim_image)
            elif label == MedicalCat.DRUGS.label:
                button.configure(image=self.painkiller_image)
            elif label == MedicalCat.MEDKIT.label:
                button.configure(image=self.salewa_image)
            elif label == MedicalCat.MEDICAL.label:
                button.configure(image=self.bandage_image)

            button.pack(side="top", anchor="center")
            button.configure(command=lambda parent=code: self.medic_button_press(parent, choice_window))
            column += 1

    def create_buttons_for_bag_mag(self):
        buttons_data = [
            ("Bag", self.bag_image, "code_a"),
            ("Magazine", self.mag_image, "code_b"),
        ]

        for idx, (label, image, code) in enumerate(buttons_data):
            button = ctk.CTkButton(
                self.framesBotCaliber[idx],  # ou un autre index si besoin
                image=image,
                text=label,
                width=150,
                compound="bottom",
                fg_color="transparent",
                text_color="white",
                font=("Arial", 20, "bold")
            )
            button.pack(side="top", anchor="center")
            if label == "Magazine":
                button.configure(command=lambda parent=code: self.mag_button_press())
            elif label == "Bag":
                button.configure(command=lambda parent=code: self.bag_button_press())

    def mag_button_press(self):
        self.create_frame_bot_find_weapon()
        Utils.create_grid_row_col_config(self.frame_bot_top, 1, 1)
        Utils.create_grid_row_col_config(self.frame_bot_bot, 3, 3)
        label = ctk.CTkLabel(self.frame_bot_bot,
                             text=f"Groups magazines into categories \n based on their ammo capacity",
                             height=20, font=("Arial", 13, "bold"),)
        label.grid(row=4,
                   column=1,
                   sticky="ew",
                   pady=10)
        max_items = 15
        items_per_row = 3
        total_rows = (max_items + items_per_row - 1) // items_per_row
        Utils.configure_grid(
            self.frame_bot_bot,
            rows=total_rows,
            cols=items_per_row,
            weight=1)
        button = ctk.CTkButton(self.frame_bot_top,
                               text="<== BACK ==>",
                               command=self.mag_window,
                               fg_color="orange",
                               font=("Arial", 20, "bold"),
                               text_color="black")
        button.grid(row=2, column=0, padx=5, pady=5)

        for idx, result in enumerate(EnumMagSize.list_values()):
            frame_recherche_m = ctk.CTkFrame(self.frame_bot_bot, fg_color="transparent")
            row, col = divmod(idx, items_per_row)
            frame_recherche_m.grid(row=row,
                                   column=col,
                                   padx=5,
                                   pady=5,
                                   sticky="nsew")
            button = ctk.CTkButton(frame_recherche_m,
                                   font=("Arial", 20, "bold"),
                                   text=result,
                                   text_color="black",
                                   command=lambda r=result: self.on_click_result_mag(r))
            button.pack(expand=True)

    def bag_button_press(self):
        self.create_frame_bot_find_weapon()
        Utils.create_grid_row_col_config(self.frame_bot_top, 1, 1)
        Utils.create_grid_row_col_config(self.frame_bot_bot, 3, 2)
        label = ctk.CTkLabel(self.frame_bot_bot,
                             text=f"Defines categories of bags based \n on how many slots they offer",
                             height=20, font=("Arial", 13, "bold"), )
        label.grid(row=4,
                   column=1,
                   sticky="ew",
                   pady=10)
        max_items = 5
        items_per_row = 3
        total_rows = (max_items + items_per_row - 1) // items_per_row
        Utils.configure_grid(
            self.frame_bot_bot,
            rows=total_rows,
            cols=items_per_row,
            weight=1)
        button = ctk.CTkButton(self.frame_bot_top,
                               text="<== BACK ==>",
                               command=self.bag_window,
                               fg_color="orange",
                               font=("Arial", 20, "bold"),
                               text_color="black")
        button.grid(row=2, column=0, padx=5, pady=5)

        for idx, result in enumerate(EnumBagSize.list_values()):
            frame_recherche_m = ctk.CTkFrame(self.frame_bot_bot, fg_color="transparent")
            row, col = divmod(idx, items_per_row)
            frame_recherche_m.grid(row=row,
                                   column=col,
                                   padx=5,
                                   pady=5,
                                   sticky="nsew")
            button = ctk.CTkButton(frame_recherche_m,
                                   font=("Arial", 20, "bold"),
                                   text=result,
                                   text_color="black",
                                   command=lambda r=result: self.on_click_result_bag(r))
            button.pack(expand=True)

    def on_click_result_mag(self, result):
        Utils.clear_frame(self.main_frame_bot)
        Utils.clear_config_row_col(self.main_frame_bot)
        self.create_frame_bot_find_weapon()
        Utils.create_grid_row_col_config(self.frame_bot_top, 1, 1)
        Utils.create_grid_row_col_config(self.frame_bot_bot, 4, 3)

        data = JsonUtils.load_mag()
        mag_obj = Mag(title=result, **data[result])

        button = ctk.CTkButton(self.frame_bot_top,
                               text="<== BACK ==>",
                               command=self.mag_button_press,
                               fg_color="orange",
                               font=("Arial", 20, "bold"),
                               text_color="black")
        button.grid(row=0, column=0, padx=5, pady=5)

        label_count = ctk.CTkLabel(
            self.frame_bot_bot,
            text=f"{len(mag_obj.ids)} Magazines",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        label_count.grid(row=0, column=1, padx=10, pady=10, sticky="w")




        switch_var = ctk.BooleanVar(value=mag_obj.penality)
        switch_penalty = ctk.CTkSwitch(
            self.frame_bot_bot,
            text="",
            variable=switch_var,
            width=50,
            command=lambda: label.configure(text=f"Remove Penalty (Ergo etc...) : {switch_var.get()}")
        )
        switch_penalty.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        label = ctk.CTkLabel(self.frame_bot_bot, text=f"Remove Penalty (Ergo etc...) : {switch_var.get()}")
        label.grid(row=1, column=0, sticky="nsew")

        switch_var2 = ctk.BooleanVar(value=mag_obj.resize)

        label2 = ctk.CTkLabel(self.frame_bot_bot, text=f"{Utils.size_magazine(result)} : {switch_var2.get()}")
        label2.grid(row=2, column=0, sticky="nsew")

        switch_size = ctk.CTkSwitch(
            self.frame_bot_bot,
            text="",
            variable=switch_var2,
            width=50,
            command=lambda: label2.configure(text=f"{Utils.size_magazine(result)} : {switch_var2.get()}")
        )
        switch_size.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        switch_var3 = ctk.BooleanVar(value=mag_obj.fastLoad)

        label3 = ctk.CTkLabel(self.frame_bot_bot, text=f"Fast load : {switch_var3.get()}")
        label3.grid(row=3, column=0, sticky="nsew")

        switch_speed = ctk.CTkSwitch(
            self.frame_bot_bot,
            text="",
            variable=switch_var3,
            width=50,
            command=lambda: label3.configure(text=f"Fast load : {switch_var3.get()}")
        )
        switch_speed.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        label4 = ctk.CTkLabel(self.frame_bot_bot, text=f"number ammo on magazines :")
        label4.grid(row=4, column=0, sticky="nsew")
        label5 = ctk.CTkLabel(self.frame_bot_bot, font=("Arial", 18, "bold"), text=f"{str(mag_obj.counts)} ammo(s)")
        label5.grid(row=4, column=2,sticky="w")
        [min_value, max_value] = Utils.max_min_slider_mag(result)
        slider = ctk.CTkSlider(self.frame_bot_bot,
                               from_=min_value, to=max_value,
                               command=lambda value: label5.configure(
                                   text=f"{int(value)} ammo(s)"))
        slider.set(mag_obj.counts or 1)
        slider.grid(row=4, column=1, sticky=ctk.W, padx=10)

        validate_button = ctk.CTkButton(
            self.frame_bot_bot,
            text="Validate",
            fg_color="green",
            command=lambda: self.apply_mag(data, result, switch_var, switch_var2, switch_var3, slider)
        )
        validate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=50)
        reset_button = ctk.CTkButton(
            self.frame_bot_bot,
            text="Reset",
            fg_color="red",
            command=lambda: self.reset_mag(result, data)
        )
        reset_button.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

    def on_click_result_bag(self, result):
        Utils.clear_frame(self.main_frame_bot)
        Utils.clear_config_row_col(self.main_frame_bot)
        self.create_frame_bot_find_weapon()
        Utils.create_grid_row_col_config(self.frame_bot_top, 1, 1)
        Utils.create_grid_row_col_config(self.frame_bot_bot, 4, 3)
        data_load = False
        if not JsonUtils.bag_exist(result):
            data = JsonUtils.load_bag(result)

        else:
            data = JsonUtils.load_bag_mod(result)
            self.logger.log("info","Bag save load")
            data_load = True

        category_data = data.get(result)
        penality = category_data.get("penality")
        excluded_filter = category_data.get("excludedFilter")
        size = category_data.get("size")

        button = ctk.CTkButton(self.frame_bot_top,
                               text="<== BACK ==>",
                               command=self.bag_button_press,
                               fg_color="orange",
                               font=("Arial", 20, "bold"),
                               text_color="black")
        button.grid(row=0, column=0, padx=5, pady=5)

        label_count = ctk.CTkLabel(
            self.frame_bot_bot,
            text=f"{len(category_data.get("ids", {}))} Bags",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        label_count.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        switch_var = ctk.BooleanVar(value=penality)
        switch_penalty = ctk.CTkSwitch(
            self.frame_bot_bot,
            text="",
            variable=switch_var,
            width=50,
            command=lambda: label.configure(text=f"Disable content restrictions : {switch_var.get()}")
        )
        switch_penalty.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        label = ctk.CTkLabel(self.frame_bot_bot, text=f"Disable content restrictions : {switch_var.get()}")
        label.grid(row=1, column=0, sticky="nsew")

        switch_var2 = ctk.BooleanVar(value=excluded_filter)
        switch_excludedFilter = ctk.CTkSwitch(
            self.frame_bot_bot,
            text="",
            variable=switch_var2,
            width=50,
            command=lambda: label2.configure(text=f"Remove Penalty (Ergo etc...) :  {switch_var2.get()}")
        )
        switch_excludedFilter.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        label2 = ctk.CTkLabel(self.frame_bot_bot, text=f"Remove Penalty (Ergo etc...) : {switch_var.get()}")
        label2.grid(row=2, column=0, sticky="nsew")

        label4 = ctk.CTkLabel(self.frame_bot_bot, text=f"Improve size BackPack on + %:")
        label4.grid(row=3, column=0, sticky="nsew")
        label5 = ctk.CTkLabel(self.frame_bot_bot, font=("Arial", 18, "bold"), text=f"+{str(size)}%")
        label5.grid(row=3, column=2,sticky="w")
        [min_value, max_value] = Utils.max_min_slider_bag(result)
        slider = ctk.CTkSlider(self.frame_bot_bot,
                               from_=min_value, to=max_value,
                               command=lambda value: label5.configure(
                                   text=f"+{int(value)}%"))
        slider.set(size)
        slider.grid(row=3, column=1, sticky=ctk.W, padx=10)

        validate_button = ctk.CTkButton(
            self.frame_bot_bot,
            text="Validate",
            fg_color="green",
            command=lambda: self.apply_bag( result, switch_var, switch_var2,  slider)
        )
        validate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=50)
        reset_button = ctk.CTkButton(
            self.frame_bot_bot,
            text="Reset",
            fg_color="red",
            command=lambda: self.reset_bag(result, data_load)
        )
        reset_button.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

    def apply_bag(self, result, switch_var, switch_var2, slider):
        Utils.apply_bag_value(  result, switch_var,switch_var2, slider)
        self.bag_button_press()

    def reset_bag(self, result, data_load):
        if data_load:
            JsonUtils.delete_bag_mod(result)
        self.bag_button_press()

    def apply_mag(self, data, result, switch_var, switch_var2, switch_var3, slider):
        Utils.save_mag_values(data,
                              result,
                              switch_var,
                              switch_var2,
                              switch_var3,
                              slider)
        self.mag_button_press()

    def reset_mag(self, result, data):
        counts = Utils.slider_start(result)
        Utils.reset_mag(result, counts, data)
        self.mag_button_press()

    def mag_window(self):
        WindowUtils.lock_choice_frame("mag", self.frames_buttons)
        self.generate_list_button(WindowType.MAG)

    def bag_window(self):
        WindowUtils.lock_choice_frame("mag", self.frames_buttons)
        self.generate_list_button(WindowType.MAG)

    def ammo_button_press(self, caliber_select, choice_window):
        if not self.data_json_from_load_all_ammo:
            (self.data_json_from_load_all_ammo,
             self.file_path_from_load_all_ammo) = JsonUtils.load_all_json_ammo()

        root_list = [Root.from_data(data, WindowType.AMMO) for data in self.data_json_from_load_all_ammo]

        if caliber_select == Caliber.GRENADE_40x46.code:
            filtered_roots = [
                root for root in root_list
                if root.item.props.get_value_by_label("Caliber") in {caliber_select, "Caliber40mmRU"}
            ]

        else:
            filtered_roots = [
                root for root in root_list
                if root.item.props.get_value_by_label("Caliber") == caliber_select
            ]
        self.list_ammo_select = filtered_roots
        self.generate_bot_frame_weapon_and_ammo(choice_window)

    def medic_button_press(self, parent, choice_window):

        if not self.data_json_from_load_all_medic:
            (self.data_json_from_load_all_medic,
             self.file_path_from_load_all_medic) = JsonUtils.load_all_json_medic()

        root_list = [Root.from_data(data, WindowType.MEDIC) for data in self.data_json_from_load_all_medic]
        filtered_roots = [
            root for root in root_list
            if root.item.parent == parent
        ]
        self.list_medic_select = filtered_roots
        self.generate_bot_frame_weapon_and_ammo(choice_window)

    def clear_recherche_frame(self):
        for frame in self.framesBotRecherche:
            frame.destroy()
        for frame in self.framesButtonRecherche:
            frame.destroy()
        for frame in self.message_not_find:
            frame.destroy()
        self.framesBotRecherche.clear()
        self.framesButtonRecherche.clear()
        self.message_not_find.clear()

    def open_specific_window(self, send_value, window_type: WindowType):
        self.detail_window = ctk.CTkToplevel(self.root)

        self.detail_window.title(DETAIL_WINDOW_TITLE)

        position_x, position_y = self.calculate_window_position(DETAIL_WINDOW_WIDTH, DETAIL_WINDOW_HEIGHT)
        self.detail_window.geometry(f"{DETAIL_WINDOW_WIDTH}x{DETAIL_WINDOW_HEIGHT}+{position_x}+{position_y}")

        self.focus_new_window()

        if window_type == WindowType.WEAPON:
            SingleWeaponMod(self.detail_window,
                            self.root,
                            send_value,
                            self)
        elif window_type == WindowType.CALIBER:
            CaliberWeaponsMod(self.detail_window,
                              self.root,
                              self.detail_window,
                              send_value,
                              self)
        elif window_type == WindowType.AMMO:
            AmmoMod(self.detail_window,
                    self.root,
                    self.detail_window,
                    send_value,
                    self)
        elif window_type == WindowType.MEDIC:
            MedicMod(self.detail_window,
                     self.root,
                     self.detail_window,
                     send_value,
                     self)

    def open_weapon_specific_window_from_list(self, name, window_type):
        list_for_data = None
        name_without_mod = name.replace("_mod.json", ".json")
        if window_type == WindowType.AMMO:
            list_for_data = self.loaded_data_ammo
        elif window_type == window_type.WEAPON:
            list_for_data = self.loaded_data
        elif window_type == window_type.MEDIC:
            list_for_data = self.loaded_data_medic
        for data in list_for_data:
            if data['file_path'].endswith(name_without_mod):
                file_path = data['file_path']
                self.open_specific_window(file_path, window_type)

    def calculate_window_position(self, window_width, window_height):
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        position_x = root_x + root_width + WINDOW_OFFSET
        position_y = root_y + (root_height // 2) - (window_height // 2)

        return position_x, position_y

    def focus_new_window(self):
        self.detail_window.grab_set()
        self.detail_window.focus_force()
        self.root.attributes('-disabled', True)

    @staticmethod
    def delete_all_items(window_type: WindowType):
        JsonUtils.delete_all_mod(window_type)
