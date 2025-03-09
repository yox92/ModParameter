import customtkinter

from Entity import Logger

PROGRESS_BAR_WIDTH = 200
PROGRESS_BAR_HEIGHT = 30
PROGRESS_BAR_CORNER_RADIUS = 20
PROGRESS_BAR_BORDER_WIDTH = 2
PROGRESS_BAR_COLOR = "blue"
PROGRESS_BAR_FONT = ("Helvetica", 18)
PROGRESS_INCREMENT_DELAY = 100
PROGRESS_MAX = 50


class ProgressBar:

    def __init__(self, parent):
        self.logger = Logger()
        self.parent = parent
        self.my_progressbar = self.configure_progress_bar()
        self.my_label = customtkinter.CTkLabel(parent, text="0%", font=PROGRESS_BAR_FONT)
        self.current_value = 0
        self.is_running = False
        self.is_finish = False

    def configure_progress_bar(self):
        progress_bar = customtkinter.CTkProgressBar(
            self.parent,
            orientation="horizontal",
            width=PROGRESS_BAR_WIDTH,
            height=PROGRESS_BAR_HEIGHT,
            corner_radius=PROGRESS_BAR_CORNER_RADIUS,
            border_width=PROGRESS_BAR_BORDER_WIDTH,
            progress_color=PROGRESS_BAR_COLOR,
            mode="determinate",
            determinate_speed=5,
        )
        progress_bar.grid(row=11, column=1, columnspan=1, padx=10, pady=10)
        progress_bar.set(0)
        return progress_bar

    def is_progress_running(self):
        return not self.is_finish

    def start(self):
        self.is_running = True
        self.is_finish = False
        self.current_value = 0
        self.increment_progress()

    def increment_progress(self, *args):
        if self.current_value <= PROGRESS_MAX:
            self.my_progressbar.set(self.current_value / PROGRESS_MAX)
            self.current_value += 1
            self.my_progressbar.after(PROGRESS_INCREMENT_DELAY, self.increment_progress)
        else:
            self.is_running = False
            self.is_finish = True

    def configure(self, progress_color=None, **kwargs):
        if progress_color:
            self.my_progressbar.configure(progress_color=progress_color)
        for key, value in kwargs.items():
            setattr(self.my_progressbar, key, value)

