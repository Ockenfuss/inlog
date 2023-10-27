# What's New
## 2.1.2
Bugfix: Support json logs which have text log dependencies for flowchart generation
Bugfix: Removing duplicate lines not working in flowchart generation

## 2.1.1
Bugfix: Remove three debug print statements

## 2.1.0
Big refactor: Separate all tree logic from the Logger class into a separate tree class

### Bugfixes
- def_opts is now working and tested
- Accessing multiple options in a subtree with `get()` is now marking all options in the subtree as accessed
- Remove mutable default arguments. This causes issues if multiple Logger objects are used in the same program.

## 2.0.0
Initial release to pypi