import numpy as np
import sys
import configparser
import os
import __main__
import datetime
import hashlib
import warnings
from pathlib import Path
import json
from inlog.conversion import config_to_dict
import json
from collections import defaultdict

STANDARD_SECTION="standard"


class Input(object):
    """Parser to read inputfiles and create logs.

    Example usage:\n
    import argparse
    VERSION="1.1"
    par=argparse.ArgumentParser()
    par.add_argument('infile')
    par.add_argument('number', type=int)
    par.add_argument('-s',action='store_true')
    args=par.parse_args()
    inp=Inp.Input(args.infile,version=VERSION)
    inp.convert_type(int, "option2")
    """

    def __init__(self,infilename, version, def_opts={}):
        """Create Input parser.

        Arguments:
            object {Input} -- the parser object\n
            infilename {str or Path or None} -- the file with the input options. Set to 'None' if not given.\n
            version {str} -- version of the program\n

        Keyword Arguments:
            def_opts {dict} -- dictionary with default input options and values. (default: {{}})
        """
        self.filename=infilename
        self.version=version
        self.creation_date=datetime.datetime.now()
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        self.outfilename=[]
        for sec in def_opts:
            # self.options[sec]={}
            self.config.add_section(sec)
            for key in def_opts[sec]:
                # self.options[sec][key]=def_opts[sec][key]
                self.config.set(sec, key, def_opts[sec][key])
        if self.filename is not None:
            self.filename=Path(self.filename)
            with open(self.filename) as f:#Check for existence
                pass
            self.config.read(self.filename)
        self.options=config_to_dict(self.config)
        self.accessed=defaultdict(lambda: defaultdict(bool))

    def _getKey(self, option, section):
        """Possibility to transform requests for keys"""
        # if option==None:
        #     option=list(self.options[section].keys())[0]#possibility to specify standard option
        # option=option.lower()
        return option, section

    def listKeys(self, section):
        """Return all keys in a given section
        
        Arguments:
            section {key} -- The key of the section
        
        Returns:
            dict_keys -- The keys available within the section.
        """
        if section==None:
            section=="DEFAULT"
        return self.options[section].keys()
    def get(self,  option, section=STANDARD_SECTION):
        """Return the specified option.

        Keyword Arguments:
            option {string} -- The option to be returned.
            section {string} -- The section where the option is located. (default: {First section})

        Returns:
            value -- value for the given option in the given section 
        """
        option, section=self._getKey(option, section)
        self.accessed[section][option]=True
        return self.options[section][option]

    def set(self, value, option, section=STANDARD_SECTION):
        """Set an option to a specific value.

        Arguments:
            value {obj} -- Value to be placed in the options dictionary.

        Keyword Arguments:
            option {str} -- Option to be set. (default: {None})
            section {str} -- Section where the option is located. (default: {None})
        """
        option, section=self._getKey(option, section)
        self.options[section][option]=value
    
    def __getitem__(self, key):
        """Allow for shorthand notation to get an option from the standard section."""
        return self.get(key)
    def __setitem__(self, key, value):
        """Allow for shorthand notation to set an option from the standard section."""
        return self.set(value, key)

    def convert_type(self, dtype, option, section=STANDARD_SECTION):
        """Convert an input option from string to a given type.

        Arguments:
            dtype {func} -- Type conversion function. Typical are int, float or Path. bool is also allowed.

        Keyword Arguments:
            option {string} -- The option to be converted. (default: {None})
            section {string} -- The section where the option is located (default: {None})
        """
        option, section=self._getKey(option, section)
        if dtype==bool:
            conversion_func=lambda val: val.lower() in ("true", "yes", "1", "t")
        else:
            conversion_func=dtype
        self.set(conversion_func(self.options[section][option]),option=option, section=section)

    def convert_array(self, dtype, option, section=STANDARD_SECTION, sep=",", removeSpaces=False):
        """Convert an input option from string to an array of the given type.

        Arguments:
            dtype {type} -- Type to convert the array element, e.g. str, int, float

        Keyword Arguments:
            option {string} -- The option to be converted. (default: {None})
            section {string } -- The section where the option is located (default: {None})
            sep {string} -- The separator between the array values (default: {","})
            removeSpaces {bool} -- Remove spaces in the elements when converting to string array. (default: {False})
        """
        option, section=self._getKey(option, section)
        array=self.options[section][option].split(sep)
        if removeSpaces:
            array=[x.strip() for x in array]
        array=[a for a in array if a]
        array=[dtype(a) for a in array]
        self.set(array, option, section)
    
    def add_outfile(self, output_files):
        """Add the given filename(s) to the list of outputfiles of your program. They will be listed in the logfile, together with their hash value.
        
        Arguments:
            output_files {string or Path or list} -- The paths of the outputfiles. Relative paths will be interpreted relative to the current working directory.
        """
        if isinstance(output_files, str) or isinstance(output_files, Path):
            output_files=[output_files]
        output_files=[Path(p).resolve() for p in output_files]
        for path in output_files:
            if not path.exists():
                warnings.warn(f"At the moment, there is no such file: {path}")
            self.outfilename.append(path)
    def set_outfile(self, output_files):
        """Set the given filename(s) as the list of outputfiles of your program. They will be listed in the logfile, together with their hash value.
        
        Arguments:
            output_files {string or list of strings} -- The paths of the outputfiles. Relative paths will be interpreted relative to the current working directory.
        """
        self.outfilename=[]
        self.add_outfile(output_files)

    def hash_file(self, file):
        """Calculate the hash of a file.
        
        Arguments:
            file {str or Path} -- The path of the file
        
        Returns:
            str -- The hexadecimal sha256 hash of the file.
        """
        BLOCK_SIZE = 65536 # The size of each read from the file
        file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(file, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
        return file_hash.hexdigest() # Get the hexadecimal digest of the hash

    def _create_log_txt(self, accessed_only=False):
        """Create a log of the Input object.

        Example:
        Program: Progam1.py
        Version: 1.0.0
        Input options: Config1.ini
        **************************
        ---DEFAULT---
        **************************
        ---Sec1---
        user: 1.0

        Returns:
            array -- array with lines including linebreak.
        """
        log=[]
        log.append("cd "+os.getcwd())
        log.append("python3 "+" ".join(sys.argv))
        log.append("# <Date> "+str(datetime.datetime.now()))
        log.append("# <Program> "+__main__.__file__)
        log.append("# <Version> "+str(self.version))
        log.append("# <Input> "+str(self.filename))
        log.append("# <Runtime> "+str(datetime.datetime.now()-self.creation_date))
        log.append("#**************************")
        for sec in self.options.keys():
            log.append("#---"+str(sec)+"---")
            for opt in self.options[sec].keys():
                if self.accessed[sec][opt] or not accessed_only:
                    log.append("#"+str(opt)+": " + str(self.options[sec][opt]))
        if len(self.outfilename)>0:
            log.append("#**************************")
            log.append("#Output files created:")
            for path in self.outfilename:
                log.append("# <PATH> "+str(path))
                log.append("# <HASH> "+self.hash_file(path))
        log=[l+"\n" for l in log]
        return log
    

    def _create_log_dict(self, accessed_only=False):
        """Create a log dictionary of the Input object.

        Example:
        {
            "dependencies": {"log1.log"{...}, "log2.log": {...}}
            "date": "2020-01-01 12:00:00",
            "program": "Program1.py",
            "version": "1.0.0",
            "input": "Config1.ini",
            "runtime": "0:00:00",
            "options": {
                "DEFAULT": {},
                "Sec1": {
                    "user": 1.0
                }
            },
            "output_files": [
                {
                    "path": "output.txt",
                    "hash": "1234567890abcdef"
                }
            ]
        }

        Returns:
            dict -- dictionary with the log information.
        """
        log={}
        log["date"]=str(datetime.datetime.now())
        log["program"]=__main__.__file__
        log["version"]=self.version
        log["input"]=str(self.filename)
        log["runtime"]=str(datetime.datetime.now()-self.creation_date)
        log["options"]=config_to_dict(self.config) #take the configparser-expanded, but not user-converted version for the log
        if accessed_only:
            log["options"]={sec: {opt: val for opt, val in self.options[sec].items() if self.accessed[sec][opt]} for sec in self.options.keys()} #only accessed options
            log["options"]= {sec: val for sec, val in log["options"].items() if len(val)>0} #remove empty sections
        log["output_files"]=[{"path": str(path), "hash": self.hash_file(path)} for path in self.outfilename]
        return log

    def show_data(self):
        """Print log."""
        print(*self._create_log_txt())

    def _write_log_txt(self, new_logs, old_logs, accessed_only=False):
        old_lines=[]
        log=self._create_log_txt(accessed_only=accessed_only)
        for old in old_logs:
            with open(old, "r") as oldfile:
                old_lines.extend(oldfile.readlines())
                old_lines[-1]=old_lines[-1].strip("\n")+"\n"
                old_lines.extend(f"# <Logfile> {old}\n") #This has to happen at the old logs! This way, even manually created logfiles get the path appended.
                old_lines.extend("#=========================================\n")
        for new in new_logs:
            with open(new, "w") as newfile:
                newfile.writelines(old_lines)
                newfile.writelines(log)
    
    def _write_log_json(self, new_logs: list, old_logs: list, accessed_only=False):
        dependencies={}
        for old in old_logs:
            try:
                with open(old, "r") as oldfile:
                    old_json=json.load(oldfile)
                    dependencies[str(old.resolve())]=old_json
            except json.decoder.JSONDecodeError:
                with open(old, "r") as oldfile:
                    dependencies[str(old.resolve())]={"text":oldfile.readlines()}
        log_json={}
        log_json.update(self._create_log_dict(accessed_only=accessed_only))
        log_json["dependencies"]=dependencies
        for new in new_logs:
            with open(new, "w") as newfile:
                json.dump(log_json, newfile, indent=4, default=str)

    def write_log(self, new_logs, old_logs=[], file_ext='log', format='json', accessed_only=True):
        """Write log to files.

        Read all old logfiles, combine with the log of the current program and save them to the new locations.

        Arguments:
            new_logs {str or Path or iterable of str, Path} -- New logfiles to be created.
            old_logs {str or Path or iterable of str, Path} -- Old logfiles

        Keyword Arguments:
            file_ext {str} -- if set, the file extensions in the provided logfile locations are replaced by 'file_ext' before the function is executed. (default: {log})
        """
        if isinstance(new_logs, str) or isinstance(new_logs, Path):
            new_logs=[new_logs]
        if isinstance(old_logs, str) or isinstance(old_logs, Path):
            old_logs=[old_logs]
        old_logs=[Path(p) for p in old_logs]
        new_logs=[Path(p) for p in new_logs]
        if file_ext!=None:
            file_ext=file_ext.strip(".")
            old_logs=[logfile.with_suffix("."+file_ext) for logfile in old_logs]
            new_logs=[logfile.with_suffix("."+file_ext) for logfile in new_logs]
        if format=='json':
            self._write_log_json(new_logs, old_logs, accessed_only)
        elif format=='txt':
            self._write_log_txt(new_logs, old_logs, accessed_only)
        else:
            raise ValueError(f"Unknown format: {format}")



