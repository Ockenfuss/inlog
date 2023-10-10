# Example
This folder contains a realistic example how `inlog` can be used.

It consists of two programs, `Script1.py` and `Script2.py`. Both are controlled via some parameters, which are located in the files `Config1.yaml` and `Config2.yaml`. Based on those, `Script1.py` creates some intermediate data and stores it on disk. `Script2.py` reads this data and processes it further. To see it in action, call
```python
python3 Script1.py Config1.yaml
python3 Script2.py Config2.yaml
```

Alternatively, there is an identical version in ini format for each config file. Call
```python
python3 Script1.py Config1.ini
python3 Script2.py Config2.ini
```

This is a visualization of the workflow (created calling `inlog-flowchart FinalResult.log`):
![Mermaid flowchart of FinalResult.svg](Flowchart_FinalResult.svg)