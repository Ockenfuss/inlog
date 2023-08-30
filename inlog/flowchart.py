#!/usr/bin/env python3
import sys
import json
from pathlib import Path
import hashlib

MERMAID_CODE=[]

def make_nodes_noloop(jlog, filename, id):
    filename=Path(filename).name
    self_id=id
    MERMAID_CODE.append(f"    id{self_id}[{filename}]")
    if "dependencies" in jlog:
        for name, dep in jlog["dependencies"].items():
            dep_id=id+1
            id=make_nodes(dep, name, dep_id)
            progamname=Path(jlog["program"]).name
            MERMAID_CODE.append(f"    id{dep_id} --> |{progamname}| id{self_id}")
    return id

def _hash_name(name):
    return hashlib.md5(name.encode()).hexdigest()

def make_nodes(jlog, filename):
    self_hash=_hash_name(filename)
    filename=Path(filename).name
    MERMAID_CODE.append(f"    id_{self_hash}[{filename}]")
    if "dependencies" in jlog:
        for name, dep in jlog["dependencies"].items():
            dep_hash=_hash_name(name)
            make_nodes(dep, name)
            progamname=Path(jlog["program"]).name
            MERMAID_CODE.append(f"    id_{dep_hash} --> |{progamname}| id_{self_hash}")

jlog={}
with open(sys.argv[1], 'r') as f:
    jlog.update(json.load(f))

MERMAID_CODE.append("flowchart TD")
# make_nodes_noloop(jlog, sys.argv[1], 1)
make_nodes(jlog, sys.argv[1])
MERMAID_CODE=list(dict.fromkeys(MERMAID_CODE)) #remove duplicates
print("\n".join(MERMAID_CODE))


        