import os

import yaml
from pydantic import BaseModel, BaseSettings


def yaml_config_settings_source(settings: BaseSettings):
    """
    Custom settings source that reads the settings from a YAML file.
    """
    path = os.getenv("CONFIG_PATH", "config.yaml")
    with open(path, "r") as fh:
        return yaml.safe_load(fh)


def ensure_config_exists():
    """
    Ensure config file exist at the path specified in the environment variable CONFIG_PATH.
    """
    path = os.getenv("CONFIG_PATH", "config.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found at {path}")


class RegexHeuristics(BaseModel):
    """
    Regex heuristics options for applying modifying a line using regex lines.

    True means option is enabled, False means option is disabled.
    """

    remove_pre_tag: bool = True


class ConverterOptions(BaseModel):
    """
    Converter options.

    Attributes
    ----------
    author_rewrite : str
        Will rewrite the author to this value for all the posts.
    links_rewrite : list[dict]
        Will rewrite the links to this value for all the posts.
    header_fields_drop : list[str]
        Will drop the specified header fields from the posts.
    """

    author_rewrite: str = ""
    links_rewrite: list[dict] = []
    header_fields_drop: list[str] = []
    enable_regex_heuristics: bool = True
    regex_heuristics: RegexHeuristics = RegexHeuristics()


class Configurator(BaseSettings):
    """
    Configurator class for the app.

    Attributes
    ----------
    logging_level: str
        The logging level.
    source_path : str
        The path to the Jekyll posts.
    output_path : str
        The path to the Hugo posts.
    converter : str
        The converter that converts the markdown
    """

    logging_level: str = "INFO"
    source_path: str
    output_path: str
    converter: str
    converter_options: ConverterOptions

    class Config:
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (yaml_config_settings_source,)
