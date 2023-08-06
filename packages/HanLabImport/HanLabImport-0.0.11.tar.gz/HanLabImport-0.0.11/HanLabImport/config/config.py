"""
Read Han Lab configuration file

"""

from configparser import ConfigParser
from pathlib import Path
import warnings


def _get_config(configname="HanLab.cfg"):
    config = ConfigParser()

    # config = configparser.ConfigParser(
    #     converters={
    #         "list": lambda x: list(
    #             x.strip("(").strip("[").strip("]").strip(")").split(",")
    #         )
    #     }
    # )

    # define three possible locations:
    HanLab_current_config = Path.cwd() / configname
    HanLab_home_config = Path.home() / configname

    cfg_folder = str(Path(__file__).parent)

    config_file_path = Path(cfg_folder) / configname
    config_read_list = [config_file_path, HanLab_home_config, HanLab_current_config]

    # user defined takes precedence
    config.read(config_read_list)

    configDict = config._sections

    return configDict


HanLab_CONFIG = _get_config()
