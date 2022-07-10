import os
from configparser import ConfigParser

config_file_path = os.path.join(os.path.dirname(__file__), "configs", "config.ini")
configs = ConfigParser()
configs.read(config_file_path)

def baseConfig() -> dict:
    """
    """
    return{
        "API": configs["API"],
        "SMSWITHOUTBORDERS": configs["SMSWITHOUTBORDERS"],
        "CONTACTS": configs["CONTACTS"]
    }
