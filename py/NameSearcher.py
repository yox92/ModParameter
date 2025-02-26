import os
import json

class NameSearcher:
    def __init__(self, master, entry_widget, result_label):
        self.master = master
        self.entry_widget = entry_widget
        self.result_label = result_label
        self.entry_widget.bind("<KeyRelease>", self.search_name)  # Lier l'événement de relâchement de touche

    def search_name(self, event=None):  # Ajouter event=None pour gérer l'événement passé par bind
        name_to_search = self.entry_widget.get()
        if len(name_to_search) >= 3:
            result = self.find_name_in_files(name_to_search)
            self.result_label.config(text=result)
        else:
            self.result_label.config(text="")

    def find_name_in_files(self, name):
        directory_path = '../src/output'
        matches = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if name.lower() in data.get("_name", "").lower():
                        matches.append(data['_name'])
        if matches:
            return "Noms trouvés : " + ", ".join(matches)
        else:
            return "Aucun nom correspondant trouvé."