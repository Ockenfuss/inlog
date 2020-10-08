from MyPython import Input as Inp
import argparse
import numpy as np

#########################################################################
#An Example program on how to use the input logger. Call this program as "python3 Example.py Example.ini -s"
#########################################################################
VERSION="1.2"
par=argparse.ArgumentParser()
par.add_argument('infile')
par.add_argument('-s',action='store_true')
args=par.parse_args()
print(args.infile)
inp=Inp.Input(args.infile,version=VERSION)
inp.convert_type(int, "option2")
inp.convert_array(int, "numbers", removeSpaces=True)
inp.show_data()

dat=np.genfromtxt(inp.get("data"))

if args.s:
    inp.add_outfile(inp.get("save"))
    inp.write_log(inp.get("save"), inp.get("data"), file_ext="log")
    np.savetxt(inp.get("save"),dat**2)
