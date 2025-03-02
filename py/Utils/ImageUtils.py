import os
from PIL import Image
import customtkinter as ctk

from config import IMAGES_DIR

class ImageUtils:

    @staticmethod
    def create_image_var(image_name: str):
        size = (150, 150)
        image_path = IMAGES_DIR / ImageUtils.find_image_on_directory(image_name)
        try:
            image = Image.open(image_path)
            return ctk.CTkImage(image, size=size)
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'ouverture de l'image '{image_path}': {e}")

    @staticmethod
    def find_image_on_directory(image_name):
        matching_files = [f for f in os.listdir(IMAGES_DIR) if image_name.lower() in f.lower()]
        if not matching_files:
            raise FileNotFoundError(
                f"Aucune image contenant le mot '{image_name}' n'a été trouvée dans '{IMAGES_DIR}'.")
        else:
            return matching_files[0]