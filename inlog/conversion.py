def config_to_dict(configparser):
        options={}
        for sec in configparser:
            if not (sec in options):
                options[sec]={}
            for key in configparser[sec]:
                options[sec][key]=configparser[sec][key]
        return options