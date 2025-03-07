import customtkinter as ctk
from customtkinter import CTkImage

from Entity import Caliber
from Utils import WindowUtils
from Utils.ImageUtils import ImageUtils
from Utils.JsonUtils import JsonUtils
from Utils.Utils import Utils
from WindowComponent.PmcMod import PmcMod
from WindowComponent.CaliberWeaponsMod import CaliberWeaponsMod
from WindowComponent.SingleWeaponMod import SingleWeaponMod
from WindowComponent.ListWeponsAlreadyMod import ListWeponsAlreadyMod

WINDOW_TITLE = "CustomWeapon App"
WINDOW_GEOMETRY = "800x600"
APPEARANCE_MODE = "dark"
DETAIL_WINDOW_TITLE = "Detail windows"
DETAIL_WINDOW_WIDTH = 900
DETAIL_WINDOW_HEIGHT = 600
WINDOW_OFFSET = 10


class ModSelectionWindow:
    def __init__(self, root):
        self.root = root
        self.frame_top_2 = None
        self.ammo_image = None
        self.frames_buttons = None
        self.buttonAmmo = None
        self.frame_top_3 = None
        ctk.set_appearance_mode(APPEARANCE_MODE)
        self.buttonPmc = None
        self.loaded_data = None
        self.frame_top_4 = None
        self.main_frame_top = None
        self.main_frame_bot = None
        self.frame_bot_right = None
        self.frame_bot_left = None
        self.frame_top_1 = None
        self.weapon_image = None
        self.caliber_image = None
        self.pmc_image = None
        self.buttonWeapon = None
        self.buttonCaliber = None
        self.detail_window = None
        self.framesBotRecherche = []
        self.list_json_name_mod = []
        self.framesBotCaliber = []
        self.framesButtonRecherche = []
        self.message_not_find = []


        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)

        self.run()

    def run(self):
        self.loaded_data = JsonUtils.load_all_json_files_without_mod()
        self.create_frame_main()
        self.create_image_var()
        self.create_frame_top()
        self.create_buttons_for_choice()

    def create_image_var(self):
        self.caliber_image: CTkImage = ImageUtils.create_image_var("caliber")
        self.weapon_image: CTkImage = ImageUtils.create_image_var("weapon")
        self.pmc_image: CTkImage = ImageUtils.create_image_var("pmc")
        self.ammo_image: CTkImage = ImageUtils.create_image_var("ammo")

    def create_frame_main(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=8)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.active_window_list_weapons_already_mod()

    def active_window_list_weapons_already_mod(self):
        self.buttonWeapon = ctk.CTkButton(
            self.root,
            text="View All Saved Weapons Mod",
            compound="top",
            fg_color="red",
            text_color="white",
            hover_color="orange",
            font=("Arial", 15, "bold"),
            height=10,
            width=10,
            command=self.show_all_weapons_mod
        )
        self.buttonWeapon.grid(row=2, column=0)

        self.main_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame_bot = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame_top.grid(row=0, column=0, sticky="nsew")
        self.main_frame_bot.grid(row=1, column=0, sticky="nsew")

    def create_frame_top(self):
        self.main_frame_top.grid_columnconfigure(0, weight=1)
        self.main_frame_top.grid_columnconfigure(1, weight=1)
        self.main_frame_top.grid_columnconfigure(2, weight=1)
        self.main_frame_top.grid_rowconfigure(0, weight=1)

        self.frame_top_1 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_2 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_3 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_4 = ctk.CTkFrame(self.main_frame_top, fg_color="transparent")
        self.frame_top_1.grid(row=0, column=0, sticky="nsew")
        self.frame_top_2.grid(row=0, column=1, sticky="nsew")
        self.frame_top_3.grid(row=0, column=2, sticky="nsew")
        self.frame_top_4.grid(row=0, column=3, sticky="nsew")

    def show_all_weapons_mod(self):
        self.list_json_name_mod = JsonUtils.load_all_json_files_mod()
        if self.list_json_name_mod:
            self.detail_window = ctk.CTkToplevel(self.root)

            self.focus_new_window()

            ListWeponsAlreadyMod(self.detail_window,
                                 self.root,
                                 self.detail_window,
                                 self.list_json_name_mod,
                                 self)

    def create_buttons_for_choice(self):
        self.buttonWeapon = ctk.CTkButton(
            self.frame_top_1,
            image=self.weapon_image,
            text="One Specific Weapon",
            compound="bottom",
            fg_color="transparent",
            text_color="orange",
            hover_color="whitesmoke",
            font=("Arial", 18, "bold"),
            command=self.case_specific_weapon
        )
        self.buttonWeapon.pack(side="top", anchor="center",
                               expand=True, fill="both")

        self.buttonCaliber = ctk.CTkButton(
            self.frame_top_2,
            image=self.caliber_image,
            text="Weapons by Ballistics",
            compound="bottom",
            fg_color="transparent",
            text_color="Crimson",
            hover_color="whitesmoke",
            font=("Arial", 18, "bold"),
            command=self.case_caliber_weapon
        )
        self.buttonCaliber.pack(side="top", anchor="center",
                                expand=True, fill="both")
        self.buttonAmmo = ctk.CTkButton(
            self.frame_top_3,
            image=self.ammo_image,
            text="Ammo Attributes",
            compound="bottom",
            fg_color="transparent",
            text_color="FireBrick",
            hover_color="whitesmoke",
            font=("Arial", 18, "bold"),
            # command=self.pmc_window
        )
        self.buttonAmmo.pack(side="top", anchor="center",
                             expand=True, fill="both")

        self.buttonPmc = ctk.CTkButton(
            self.frame_top_4,
            image=self.pmc_image,
            text="PMC Attributes",
            compound="bottom",
            fg_color="transparent",
            text_color="green",
            hover_color="whitesmoke",
            font=("Arial", 18, "bold"),
            command=self.pmc_window
        )
        self.buttonPmc.pack(side="top", anchor="center",
                            expand=True, fill="both")
        self.frames_buttons = {
            "weapon": self.buttonWeapon,
            "caliber": self.buttonCaliber,
            "pmc": self.buttonPmc,
            "ammo": self.buttonAmmo
        }

    def on_click_result(self, result):
        for data in self.loaded_data:
            if data['locale']['ShortName'] == result:
                file_path = data['file_path']
                self.open_weapon_specific_window(file_path, True)
                break
        else:
            print(f"File ignore : {result}")

    def create_frame_bot_find_weapon(self):
        Utils.clear_frame(self.main_frame_bot)
        Utils.clear_config_row_col(self.main_frame_bot)

        self.main_frame_bot.grid_columnconfigure(0, weight=1)
        self.main_frame_bot.grid_columnconfigure(1, weight=0)
        self.main_frame_bot.grid_rowconfigure(0, weight=1)
        self.main_frame_bot.grid_rowconfigure(1, weight=10)

        self.frame_bot_left = ctk.CTkFrame(self.main_frame_bot, fg_color="transparent")
        self.frame_bot_right = ctk.CTkFrame(self.main_frame_bot, fg_color="transparent")

        self.frame_bot_left.grid(row=0, column=0, sticky="nsew")
        self.frame_bot_right.grid(row=1, column=0, sticky="nsew")

    def case_specific_weapon(self):
        WindowUtils.lock_choice_frame("weapon", self.frames_buttons)

        self.create_frame_bot_find_weapon()

        Utils.create_grid_row_col_config(self.frame_bot_left, 1, 1)
        Utils.create_grid_row_col_config(self.frame_bot_right, 3, 3)

        self.create_bind_entry_bar(self.frame_bot_left)
        self.entry.bind("<KeyRelease>", self.search_name)

    def case_caliber_weapon(self):
        WindowUtils.lock_choice_frame("caliber", self.frames_buttons)

        Utils.clear_frame(self.main_frame_bot)
        Utils.create_grid_row_col_config(self.main_frame_bot, 4, 5)
        Utils.create_5x4_bottom(self.framesBotCaliber, self.main_frame_bot)

        self.create_buttons_for_calibers()

    def pmc_window(self):
        WindowUtils.lock_choice_frame("pmc", self.frames_buttons)

        Utils.clear_frame(self.main_frame_bot)
        self.detail_window = ctk.CTkToplevel(self.root)

        # self.focus_new_window()

        PmcMod(self.detail_window,
               self.root,
               self.detail_window,
               self)

    def search_name(self, event=None):
        name_to_search = self.entry.get()
        if len(name_to_search) >= 2:
            self.clear_recherche_frame()
            results = self.find_name_in_loaded_data(name_to_search)
            if results:
                self.populate_buttons(results)
            else:
                label = ctk.CTkLabel(self.frame_bot_right, text="No matching name found.")
                label.grid(row=0, column=0, sticky="nsew")
                self.message_not_find.append(label)
        else:
            self.clear_recherche_frame()

    def populate_buttons(self, results):
        max_items = 20
        items_per_row = 5
        total_rows = (max_items + items_per_row - 1) // items_per_row

        Utils.configure_grid(
            self.frame_bot_right,
            rows=total_rows,
            cols=items_per_row,
            weight=1)

        for idx, result in enumerate(results[:max_items]):
            frame_recherche_m = ctk.CTkFrame(self.frame_bot_right, fg_color="transparent")
            row, col = divmod(idx, items_per_row)
            frame_recherche_m.grid(row=row,
                                   column=col,
                                   padx=5,
                                   pady=5,
                                   sticky="nsew")
            self.framesBotRecherche.append(frame_recherche_m)

            button = ctk.CTkButton(frame_recherche_m,
                                   text=result,
                                   command=lambda r=result: self.on_click_result(r),
                                   font=("Arial", 20, "bold"),
                                   text_color="black", )
            button.pack(expand=True)
            self.framesButtonRecherche.append(button)

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

    def create_buttons_for_calibers(self):
        row = 1
        column = 0
        colors = ["dodgerblue", "peru", "mediumseagreen", "khaki"]

        if len(self.framesBotCaliber) < Caliber.count():
            print("Erreur : 'framesBotCaliber' no enought frames")
            return

        for idx, caliber in Caliber.enumerate_calibers():
            idx: int
            caliber: Caliber

            color = colors[idx % 4]
            button = ctk.CTkButton(
                self.framesBotCaliber[idx],
                text=caliber.label,
                width=150,
                text_color="black",
                fg_color=color,
                font=("Arial", 15, "bold"),
                command=lambda r=caliber.code: self.open_weapon_specific_window(r, False))
            button.pack(side="top", anchor="center")

            column += 1
            if column > 4:
                column = 0
                row += 1

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

    def open_weapon_specific_window(self, send_value, only_weapon):
        self.detail_window = ctk.CTkToplevel(self.root)

        self.detail_window.title(DETAIL_WINDOW_TITLE)

        position_x, position_y = self.calculate_window_position(DETAIL_WINDOW_WIDTH, DETAIL_WINDOW_HEIGHT)
        self.detail_window.geometry(f"{DETAIL_WINDOW_WIDTH}x{DETAIL_WINDOW_HEIGHT}+{position_x}+{position_y}")

        self.focus_new_window()

        if only_weapon:
            SingleWeaponMod(self.detail_window,
                            self.root,
                            send_value,
                            self)
        else:
            CaliberWeaponsMod(self.detail_window,
                              self.root,
                              self.detail_window,
                              send_value,
                              self)

    def open_weapon_specific_window_from_list_weapon(self, weapon_name):
        for data in self.loaded_data:
            if data['locale']['ShortName'] == weapon_name:
                file_path = data['file_path']
                self.open_weapon_specific_window(file_path,
                                                 True)

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
