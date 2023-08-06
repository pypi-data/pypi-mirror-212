import logging

from app.config import Configurator, ensure_config_exists
from app.converter import Converter


def main():
    """
    Main function of the program.
    """
    # Configurator
    ensure_config_exists()
    configurator = Configurator()

    # Logging configuration
    logging.basicConfig(
        format="%(asctime)s %(process)d %(levelname)s %(message)s",
        level=configurator.logging_level,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Converter
    converter = Converter(configurator)
    converter.convert()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
