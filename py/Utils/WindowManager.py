import customtkinter as ctk

from Utils import Utils


class WindowManager:
    @staticmethod
    def window_protocol(frame, detail_window, root):
        frame.protocol("WM_DELETE_WINDOW", lambda: WindowManager.close_window(detail_window, root))
        return  frame

    @staticmethod
    def close_window(detail_window, root):
        detail_window.grab_release()
        root.attributes('-disabled', False)
        detail_window.destroy()

    @staticmethod
    def frame_color_risky_range(name, value, label):
        if Utils.is_value_outside_limits_weapons(name, value):
            label.configure(text_color="red")
        else:
            label.configure(text_color="white")
