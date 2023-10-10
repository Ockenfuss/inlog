import inlog as inl
import argparse
from pathlib import Path

#specify the version number of this program
VERSION="1.0"

#provide the ini file as a command line argument
par=argparse.ArgumentParser()
par.add_argument('infile')
args=par.parse_args()
infile=Path(args.infile)

#create the logger object using the config file and the version number
if infile.suffix==".yaml":
    config=inl.load_yaml(infile,version=VERSION)
elif infile.suffix==".ini":
    config=inl.load_ini(infile,version=VERSION)
    #In case of .ini, all input parameters are strings. Convert some of them to an integer
    config.convert_type(int, "section1","factor")

config.show_data()

#read the data from the intermediate file defined as an input parameter.
with open(config["intermediate"]) as f:
    data=f.readlines()
    data=[int(x.strip()) for x in data]

#multiply every number in data with a factor 
data=[x*config["factor"] for x in data]

#save the created data as final result
with open(config["result"], "w") as f:
    f.write("\n".join([str(x) for x in data]))

# if you tell the logger the filename of the saved file, it will place a hash of this file in the log.
config.set_outfile(config["result"])

#write a log. Telling the logger the filename of the intermediate file, it will include the intermediate log in the final log.Therefore, we store the full history of the data in the final log.
# Default is json format. By default, the Logger will replace the extension of all given filenames with '.log'
config.write_log(config["result"], old_logs=config["intermediate"])