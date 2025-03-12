import customtkinter as ctk
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox

from Entity import Caliber, Root, Logger
from Entity.WindowType import WindowType
from Utils import WindowUtils
from Utils.ImageUtils import ImageUtils
from Utils.JsonUtils import JsonUtils
from Utils.Utils import Utils
from WindowComponent.AmmoMod import AmmoMod
from WindowComponent.PmcMod import PmcMod
from WindowComponent.CaliberWeaponsMod import CaliberWeaponsMod
from WindowComponent.SingleWeaponMod import SingleWeaponMod
from WindowComponent.ListItemAlreadyMod import ListItemAlreadyMod

WINDOW_TITLE = "ModParameter App"
WINDOW_GEOMETRY = "800x600"
APPEARANCE_MODE = "dark"
DETAIL_WINDOW_TITLE = "Detail windows"
DETAIL_WINDOW_WIDTH = 900
DETAIL_WINDOW_HEIGHT = 600
WINDOW_OFFSET = 10


class ModSelectionWindow:
    def __init__(self, root):
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
        self.data_json_from_load_all_ammo = None
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
        self.button_all_ammo_tracer.grid(row=0, column=2, padx=10)
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
        self.button_delete_mod.grid(row=0, column=3, padx=10)
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
            print("Too bad, wise decision")

    def apply_all_ammo_tracer(self, color: bool):
        list_path_ammo: list = []
        list_path_ammo_mod_without_mod_at_the_end = JsonUtils.get_file_path_json_all_mod_ammo(True)

        for data in self.loaded_data_ammo:
            if data["file_path"] not in list_path_ammo_mod_without_mod_at_the_end:
                list_path_ammo.append(data["file_path"])

        if list_path_ammo:
            Utils.apply_tracer_to_ammo_no_mod_again(list_path_ammo, color)

        if list_path_ammo_mod_without_mod_at_the_end:
            Utils.apply_tracer_to_ammo_with_mod_exist_already(color)

    def all_mod_to_delete(self):
        msg_choice = CTkMessagebox(title="All Delete Or Choice Which One?",
                                   message="Choose an option: Delete All Ammo / Delete All Weapons / Select a Mod to Delete",
                                   icon="warning", option_1="All Ammo", option_2="All Weapons", option_3="Select One")
        response = msg_choice.get()
        if response == "All Ammo":
            ModSelectionWindow.delete_all_weapons(WindowType.AMMO)
        elif response == "All Weapons":
            ModSelectionWindow.delete_all_weapons(WindowType.WEAPON)
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
            text="One Specific Weapon",
            compound="bottom",
            fg_color="transparent",
            text_color="orange",
            hover_color="whitesmoke",
            font=("Arial", 18, "bold"),
            command=lambda: self.generate_bot_frame_weapon_and_ammo(WindowType.WEAPON)
        )
        self.buttonWeapon.pack(side="top", anchor="center",
                               expand=True, fill="both")

        self.button_caliber = ctk.CTkButton(
            self.frame_top_2,
            image=self.caliber_image,
            text="Weapons by Ballistics",
            compound="bottom",
            fg_color="transparent",
            text_color="Crimson",
            hover_color="whitesmoke",
            font=("Arial", 18, "bold"),
            command=lambda: self.generate_list_button_caliber_ammo(WindowType.CALIBER)
        )
        self.button_caliber.pack(side="top", anchor="center",
                                 expand=True, fill="both")
        self.button_ammo = ctk.CTkButton(
            self.frame_top_3,
            image=self.ammo_image,
            text="Ammo Attributes",
            compound="bottom",
            fg_color="transparent",
            text_color="FireBrick",
            hover_color="whitesmoke",
            font=("Arial", 18, "bold"),
            command=self.ammo_window
        )
        self.button_ammo.pack(side="top", anchor="center",
                              expand=True, fill="both")
        self.button_pmc = ctk.CTkButton(
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
        self.button_pmc.pack(side="top", anchor="center",
                             expand=True, fill="both")
        self.frames_buttons = {
            "weapon": self.buttonWeapon,
            "caliber": self.button_caliber,
            "pmc": self.button_pmc,
            "ammo": self.button_ammo
        }

    def generate_list_button_caliber_ammo(self, choice_window: WindowType):
        if choice_window == WindowType.AMMO:
            WindowUtils.lock_choice_frame("ammo", self.frames_buttons)
        elif choice_window == WindowType.CALIBER:
            WindowUtils.lock_choice_frame("caliber", self.frames_buttons)

        Utils.clear_frame(self.main_frame_bot)
        Utils.create_grid_row_col_config(self.main_frame_bot, 4, 5)
        Utils.create_5x4_bottom(self.framesBotCaliber, self.main_frame_bot)

        self.create_buttons_for_calibers_ammo(choice_window)

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

    def ammo_window(self):
        WindowUtils.lock_choice_frame("ammo", self.frames_buttons)
        self.generate_list_button_caliber_ammo(WindowType.AMMO)

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
        if window_type == WindowType.AMMO:
            results = [{"short_name": root.locale.ShortName, "name": root.locale.Name} for root in results]

            button = ctk.CTkButton(self.frame_bot_top,
                                   text="<== BACK ==>",
                                   command=self.ammo_window,
                                   fg_color="orange",
                                   font=("Arial", 20, "bold"),
                                   text_color="black")
            button.grid(row=2, column=0, padx=5, pady=5)

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
            self.framesButtonRecherche.append(button)

    def on_click_result(self, result, window_type: WindowType):
        if window_type == WindowType.WEAPON:
            for data in self.loaded_data:
                if data['locale']['ShortName'] == result:
                    file_path = data['file_path']
                    self.open_weapon_specific_window(file_path, WindowType.WEAPON)
                    break
            else:
                self.logger.log("info", f"File ignore : {result}")
        elif window_type == WindowType.AMMO:
            json_filename = f"{result.replace('(', '').replace(')', '').replace(' ', '_').replace('/', '').replace('\\', '')}.json"
            matching_file = next(
                (fp for fp in self.file_path_from_load_all_ammo if fp.endswith(json_filename)),
                None)
            if matching_file:
                self.open_weapon_specific_window(matching_file, WindowType.AMMO)
            else:
                raise FileNotFoundError(f"File '{json_filename}' do not existe / not find")

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
        colors = ["dodgerblue", "peru", "mediumseagreen", "khaki"]

        if len(self.framesBotCaliber) < Caliber.count():
            self.logger.log("error", "Erreur : 'framesBotCaliber' no enought frames")
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
                font=("Arial", 15, "bold"))
            button.pack(side="top", anchor="center")
            if choice_window == WindowType.AMMO:
                button.configure(command=lambda r=caliber.code: self.ammo_button_press(r, choice_window))
            elif choice_window == WindowType.CALIBER:
                button.configure(command=lambda r=caliber.code: self.open_weapon_specific_window(r, choice_window))

            column += 1
            if column > 4:
                column = 0
                row += 1

    def ammo_button_press(self, caliber_select, choice_window):
        if not self.data_json_from_load_all_ammo:
            (self.data_json_from_load_all_ammo,
             self.file_path_from_load_all_ammo) = JsonUtils.load_all_json_ammo()

        root_list = [Root.from_data(data, WindowType.AMMO) for data in self.data_json_from_load_all_ammo]

        filtered_roots = [
            root for root in root_list
            if root.item.props.get_value_by_label("Caliber") == caliber_select
        ]
        self.list_ammo_select = filtered_roots

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

    def open_weapon_specific_window(self, send_value, window_type: WindowType):
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

    def open_weapon_specific_window_from_list(self, name, windowType):
        list_for_data = None
        name_without_mod = name.replace("_mod.json", ".json")
        if windowType == WindowType.AMMO:
            list_for_data = self.loaded_data_ammo
        elif windowType == windowType.WEAPON:
            list_for_data = self.loaded_data
        for data in list_for_data:
            if data['file_path'].endswith(name_without_mod):
                file_path = data['file_path']
                self.open_weapon_specific_window(file_path, windowType)

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
    def delete_all_weapons(window_type: WindowType):
        JsonUtils.delete_all_mod(window_type)
