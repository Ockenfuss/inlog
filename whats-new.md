# What's New
## 2.1.0
Big refactor: Separate all tree logic from the Logger class into a separate tree class

### Bugfixes
- def_opts is now working and tested
- Accessing multiple options in a subtree with `get()` is now marking all options in the subtree as accessed
- Remove mutable default arguments. This causes issues if multiple Logger objects are used in the same program.

## 2.0.0
Initial release to pypi