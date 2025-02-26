import customtkinter as ctk  # Utiliser l'alias ctk pour customtkinter

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI")
        self.root.rowconfigure(0, weight=1)
        self.root.geometry('960x540')

        ctk.set_appearance_mode("System")  # Light/Dark/Blue/System
        ctk.set_default_color_theme("blue")  # Plusieurs thèmes disponibles

        # Cadre pour la recherche
        self.search_frame = ctk.CTkFrame(self.root)
        self.search_frame.pack(expand=True, fill='both')

        # Cadre pour les détails qui est initialement caché
        self.detail_frame = ctk.CTkFrame(self.root)

        # Widgets pour le cadre de recherche
        self.entry = ctk.CTkEntry(self.search_frame, width=480, placeholder_text="Type here...")
        self.entry.pack(pady=20)

    def show_details(self):
        # Cache le cadre de recherche et montre le cadre de détails
        self.search_frame.pack_forget()
        self.detail_frame.pack(expand=True, fill='both')
        self.load_item_details()

    def show_search(self):
        # Cache le cadre de détails et montre le cadre de recherche
        self.detail_frame.pack_forget()
        self.search_frame.pack(expand=True, fill='both')

    def load_item_details(self):
        # Nettoyons et mettons quelques détails
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(self.detail_frame, text="Here are item details!")
        label.pack(pady=10)

        # Bouton de retour à la recherche
        back_button = ctk.CTkButton(self.detail_frame, text="Back to Search", command=self.show_search)
        back_button.pack(pady=10)
