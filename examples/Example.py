from inlog import Input as Inp
import argparse
import numpy as np
from pathlib import Path

#########################################################################
#An Example program on how to use the input logger. Call this program as "python3 Example.py Example.ini -s"
#########################################################################

#specify an arbitrary version number
VERSION="2.0"

#provide the ini file as a command line argument
par=argparse.ArgumentParser()
par.add_argument('infile')
par.add_argument('-s',action='store_true')
args=par.parse_args()

#create the input object using the ini file and the version number
inp=Inp.Input(args.infile,version=VERSION)

#initially, all input parameters are strings. Convert some of them.
inp.convert_type(int, "option2")
inp.convert_type(Path, "data")
inp.convert_array(int, "numbers", section="special", removeSpaces=True)

#print the input parameters
inp.show_data()

#read some data from a filename defined as an input parameter. You can use the shorthand inp["data"] notation, if the parameter is in the 'standard' section
data=np.genfromtxt(inp["data"])

#if you want to access parameters not in the 'standard' section, you have to use the 'get' method and specify the section
array=np.array(inp.get('numbers', section="special"))

#save an intermediate result
if args.s:
    np.savetxt(inp["intermediate"],data+array)
    # if you tell inlog the filename of the saved file, it will place a hash of this file in the log.
    inp.set_outfile(inp["intermediate"])
    #write a log. Default is json format. By default, inlog will replace the extension of all given filenames with '.log'
    inp.write_log(inp["intermediate"], inp["data"])


#########################################################################
#Now start from scratch and read the previously saved file for another processing step.
#########################################################################
inp=Inp.Input(args.infile,version=VERSION)
#print the input parameters
inp.show_data()
#Read the original and intermediate data
dat1=np.genfromtxt(inp["data"])
dat2=np.genfromtxt(inp["intermediate"])

if args.s:
    #save the final result
    np.savetxt(inp["result"],dat1+dat2)
    inp.set_outfile(inp["result"])
    #In this processing step, we only accessed a few of the input parameters. To keep the log simple, we can tell inlog to only log the accessed parameters.
    inp.write_log(inp["result"], [inp["data"],inp["intermediate"]], accessed_only=True)