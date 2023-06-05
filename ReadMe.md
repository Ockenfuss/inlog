# Inlog

Input Logger - Python module to parse config files and create corresponding logfiles for simulation results.


<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Motivation](#motivation)
- [Usage](#usage)

<!-- /code_chunk_output -->

## Motivation
When writing python programs which serve more than one task, it is likely that you have some parameters in your code which determine the output of your program. It might be tempting to specify the values of these parameters within your code for every run, but this practice does not allow to reproduce your results afterwards. Therefore, a strict separation between program code and input parameters is favorable, e.g. in the form of separate `.ini` or `.yaml` files. Additionally, it must be clear which input file must be processed by which program, including the program version, to produce the existing result. `Inlog` tries to provide this information by producing logfiles for every output file of a program. These logfiles include the input parameters, input data files, information about the program and information about the output produced. If similar logfiles already exist for the input data, their content will be added as a preface. The following provides a visualization of this model:

```text
(--input data)             |-----------------|         --output data
(--input logfile)     ===> | Python program  | ===>    --output logfile ===> ...
--input parameters         |-----------------|
```

## Usage
See also the examples folder.
```python
from inlog import Input as Inp
inp=Inp.Input("config.ini",version="1.2.3")
inp.convert_type(int, "option2")
inp.convert_array(int, "numbers", removeSpaces=True)
inp.show_data()
inp.get("option2")
inp.add_outfile('outputfile.dat')
inp.write_log('outputfile.dat', ['inputfile.dat'], file_ext="log")
```

## Roadmap
* JSON or another input format. Ideally with implicit type information, such that `convert_type` is not necessary anymore