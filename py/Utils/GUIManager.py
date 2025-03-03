import customtkinter as ctk
from customtkinter import CTkImage
from Utils.ImageUtils import ImageUtils

class GUIManager:
    def __init__(self, root, title="CustomWeapon App", width=800, height=600):
        self.root = root
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        ctk.set_appearance_mode("dark")

