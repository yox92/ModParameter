import logging
import traceback
import inspect

from config import LOG_FILE_PATH


class Logger:
    def __init__(self):

        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, level, message):

        frame = inspect.currentframe().f_back.f_back
        module = inspect.getmodule(frame)
        class_name = frame.f_locals.get("self", None).__class__.__name__ if "self" in frame.f_locals else "N/A"
        method_name = frame.f_code.co_name

        log_message = f"{module.__name__ if module else 'N/A'} - {class_name}.{method_name}() : {message}"

        if level == "info":
            self.logger.info(log_message)
        elif level == "debug":
            self.logger.debug(log_message)
        elif level == "warning":
            self.logger.warning(log_message)
        elif level == "error":
            self.logger.error(log_message)
        elif level == "critical":
            self.logger.critical(log_message)

    def log_error(self, exception):
        frame = inspect.currentframe().f_back.f_back
        module = inspect.getmodule(frame)
        class_name = frame.f_locals.get("self", None).__class__.__name__ if "self" in frame.f_locals else "N/A"
        method_name = frame.f_code.co_name

        error_message = f"{module.__name__ if module else 'N/A'} - {class_name}.{method_name}() : {str(exception)}"
        self.logger.error(error_message)
        self.logger.error(traceback.format_exc())
