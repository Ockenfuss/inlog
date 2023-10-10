import inlog as inl
import argparse
from pathlib import Path

#specify the version number of this program
VERSION="1.0"

#provide the config file as a command line argument
par=argparse.ArgumentParser()
par.add_argument('infile')
args=par.parse_args()
infile=Path(args.infile)

#create the input object using the config file and the version number
if infile.suffix==".yaml":
    config=inl.load_yaml(infile,version=VERSION)
elif infile.suffix==".ini":
    config=inl.load_ini(infile,version=VERSION)
    #In case of .ini, all input parameters are strings. Convert some of them to an integer
    config.convert_type(int, "section1","start")
    config.convert_type(int, "section1","increment")
    config.convert_type(int, "section1","stop")


#print the input parameters
config.show_data()

#create some data based on the input parameters. In this case, just a simple range[start, stop, increment]
data=list(range(config.get("section1","start"),config.get("section1","stop"),config.get("section1","increment")))

#save the created data as intermediate result
#Here, we use the shorthand config["intermediate"] notation. It searches the config tree depth first for the given key(s). 
with open(config["intermediate"], "w") as f:
    f.write("\n".join([str(x) for x in data]))

# if you tell the logger the filename of the saved file, it will place a hash of this file in the log.
config.set_outfile(config["intermediate"])

#write a log. Default is json format. By default, the Logger will replace the extension of all given filenames with '.log'
config.write_log(config["intermediate"])