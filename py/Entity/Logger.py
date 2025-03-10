import logging
import traceback
import inspect
from config import LOG_FILE_PATH

class Logger:
    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        self.logger = logging.getLogger("Logger")
        if not self.logger.hasHandlers():
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

        log_function = {
            "info": self.logger.info,
            "debug": self.logger.debug,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "critical": self.logger.critical
        }.get(level.lower(), self.logger.info)

        log_function(log_message)

    def log_error(self, exception):
        frame = inspect.currentframe().f_back.f_back
        module = inspect.getmodule(frame)
        class_name = frame.f_locals.get("self", None).__class__.__name__ if "self" in frame.f_locals else "N/A"
        method_name = frame.f_code.co_name

        error_message = f"{module.__name__ if module else 'N/A'} - {class_name}.{method_name}() : {str(exception)}"
        self.logger.error(error_message)
        self.logger.error(traceback.format_exc())

