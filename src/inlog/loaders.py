from .Logger import Logger
import configparser
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
    config = configparser.ConfigParser()
    config._interpolation = configparser.ExtendedInterpolation()
    config.read(ini_file)
    config_dict= _configparser_to_dict(config)
    logger=Logger(config_dict, version, def_opts=def_opts)
    logger.filename=ini_file
    return logger

def load_yaml(yaml_file, version, def_opts={}):
    if not _has_yaml:
        raise ImportError("You need to install pyyaml to use yaml files (contained in inlog[extras])")

    with open(yaml_file) as f:
        config_dict = yaml.safe_load(f)
    logger=Logger(config_dict, version, def_opts=def_opts)
    logger.filename=yaml_file
    return logger

def load_json(json_file, version, def_opts={}):
    with open(json_file) as f:
        config_dict = json.load(f)
    logger=Logger(config_dict, version, def_opts=def_opts)
    logger.filename=json_file
    return logger