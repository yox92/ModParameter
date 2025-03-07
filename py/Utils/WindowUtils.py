from Utils import Utils


class WindowUtils:
    @staticmethod
    def window_protocol(frame, detail_window, root, main):
        frame.protocol("WM_DELETE_WINDOW",
                       lambda:
                       WindowUtils.close_window(detail_window,
                                                root, main))
        return  frame

    @staticmethod
    def close_window(detail_window, root, main):
        detail_window.grab_release()
        root.attributes('-disabled', False)
        detail_window.destroy()
        WindowUtils.unlock_all_frame(main.frames_buttons)

    @staticmethod
    def frame_color_risky_range(name, value, label):
        if Utils.is_value_outside_limits_weapons(name, value):
            label.configure(text_color="red")
        else:
            label.configure(text_color="white")

    @staticmethod
    def lock_choice_frame(locked_frame, frames):
        for frame, button in frames.items():
            if frame == locked_frame:
                button.configure(state="disabled")
            else:
                button.configure(state="normal")

    @staticmethod
    def unlock_all_frame(frames):
        for frame, button in frames.items():
            button.configure(state="normal")


