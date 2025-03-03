import customtkinter as ctk

class Utils:
    def __init__(self, root):
        self.root = root

    @staticmethod
    def configure_grid(frame, rows, cols, weight=1):
        for r in range(rows):
            frame.grid_rowconfigure(r, weight=weight)
        for c in range(cols):
            frame.grid_columnconfigure(c, weight=weight)

    @staticmethod
    def clear_frame(frame):
        for child in frame.winfo_children():
            child.destroy()
        rows, cols = frame.grid_size()
        for i in range(cols):
            frame.grid_columnconfigure(i, weight=0)
        for j in range(rows):
            frame.grid_rowconfigure(j, weight=0)

    @staticmethod
    def clear_config_row_col(frame):
        for i in range(frame.grid_size()[1]):
            frame.grid_rowconfigure(i, weight=0)

        for j in range(frame.grid_size()[0]):
            frame.grid_columnconfigure(j, weight=0)

    @staticmethod
    def search_by_name(loaded_data, name):
        matches = []
        for data in loaded_data:
            name_field = data.get("locale", {}).get("Name")
            if isinstance(name_field, str) and name.lower() in name_field.lower():
                cleaned_name = data.get("locale", {}).get("ShortName")
                matches.append(cleaned_name)
        return matches

