import logging

class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Create a console handler and set the formatter
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Set the level for console logs
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # Create a file handler and set the formatter
        file_handler = logging.FileHandler("logs/logfile.log")
        file_handler.setLevel(logging.DEBUG)  # Set the level for file logs
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

# Instantiate the custom logger
logger = CustomLogger("custom_logger")
logger.setLevel(logging.DEBUG)