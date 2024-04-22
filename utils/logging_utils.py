import logging

def configure_logging():
    logging.basicConfig(filename="setup.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")