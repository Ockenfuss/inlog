from .Logger import Logger
import configparser
from pathlib import Path
import json
try:
    import yaml
    _has_yaml=True
except ImportError:
    _has_yaml=False

def _configparser_to_dict(configparser):
        options={}
        for sec in configparser:
            if not (sec in options):
                options[sec]={}
            for key in configparser[sec]:
                options[sec][key]=configparser[sec][key]
        return options

def load_ini(ini_file, version, def_opts={}):
    """Create a logger object from an ini file

    Parameters
    ----------
    ini_file : str, path-like or file-like
        Path to the ini file or file-like object
    version : str
        Version of your program
    def_opts : dict, optional
        Default parameters, used as a fallback if not present in the config file. by default {}

    Returns
    -------
    Logger
        The logger object
    """
    config = configparser.ConfigParser()
    config._interpolation = configparser.ExtendedInterpolation()
    try: #ini_file is a string of path
        p=Path(ini_file)
        config.read(p)
    except TypeError:
        config.read_file(ini_file) #ini_file is a file-like object
    config_dict= _configparser_to_dict(config)
    logger=Logger(config_dict, version, def_opts=def_opts)
    logger.filename=ini_file
    return logger

def load_yaml(yaml_file, version, def_opts={}):
    """Create a logger object from a yaml file

    Parameters
    ----------
    yaml_file : str, path-like or file-like
        Path to the yaml file or file-like object
    version : str
        Version of your program
    def_opts : dict, optional
        Default parameters, used as a fallback if not present in the config file. by default {}

    Returns
    -------
    Logger
        The logger object
    """
    if not _has_yaml:
        raise ImportError("You need to install pyyaml to use yaml files (contained in inlog[extras])")
    try:
        p=Path(yaml_file)
        with open(p) as f:
            config_dict = yaml.safe_load(f)
    except TypeError:
        config_dict = yaml.safe_load(yaml_file)
    logger=Logger(config_dict, version, def_opts=def_opts)
    logger.filename=yaml_file
    return logger

def load_json(json_file, version, def_opts={}):
    """Create a logger object from a json file

    Parameters
    ----------
    json_file : str, path-like or file-like
        Path to the json file or file-like object
    version : str
        Version of your program
    def_opts : dict, optional
        Default parameters, used as a fallback if not present in the config file. by default {}

    Returns
    -------
    Logger
        The logger object
    """
    try:
        p=Path(json_file)
        with open(p) as f:
            config_dict = json.load(f)
    except TypeError:
        config_dict = json.load(json_file)
    logger=Logger(config_dict, version, def_opts=def_opts)
    logger.filename=json_file
    return logger