# What's New
## 2.2.1
Add `repr` representation of Logger object.
Bugfix:
- If `__main__.__file__` is not set (e.g. in interactive sessions), the log file could not be created.

## 2.2.0
Logfile names have a naming convention. Instead of replacing the file suffix with `.log`, the suffix is appended by default now.
To get back the old behaviour, use the new argument `ext_modification_mode='replace'` in `write_log()`.

### Deprecations
To allow for backward compatibility, when specifying filenames via `write_log(old_logs=...)` and no old log in the new format (extension appended) is found, we search for the file in the old format (extension replaced). If a file is found, this file is used and a deprecation warning is raised.

## 2.1.4
Raise an error in `load_ini` if file does not exist.

## 2.1.3
Bugfix: CLI arguments not logged in json version of the log.

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