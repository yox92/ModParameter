import customtkinter


class ProgressBar:
    def __init__(self, parent):
        # Barre de progression initiale
        self.my_progressbar = customtkinter.CTkProgressBar(parent,
                                                           orientation="horizontal",
                                                           width=200,
                                                           height=30,
                                                           corner_radius=20,
                                                           border_width=2,
                                                           progress_color="green",
                                                           mode="determinate",
                                                           determinate_speed=5)
        self.my_progressbar.grid(row=11, column=1, columnspan=1, padx=10, pady=10)
        self.my_progressbar.set(0)

        self.my_label = customtkinter.CTkLabel(parent, text="0%", font=("Helvetica", 18))

        self.current_value = 0
        self.is_running = False

    def statut_progress_bar(self):
        return self.is_running

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.current_value = 0
            self.increment_progress()
        else:
            return False

    def increment_progress(self):
        if self.current_value <= 100:
            self.my_progressbar.set(self.current_value / 100)
            self.my_label.configure(text=f"{self.current_value}%")
            self.current_value += 1  # Incrémenter la valeur
            self.my_progressbar.after(50, self.increment_progress)
        else:
            self.is_running = False
