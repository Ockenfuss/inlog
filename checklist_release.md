# Steps before a release:

- Run all tests! Use python from the command line to ensure no unnecessary print output remains!
```bash
python3 -m unittest discover -s tests/unit
```

- Bump versions in `pyproject.toml` and `__init__.py`

Release
```bash
python3 -m build
twine upload dist/inlog-2.1.0-py3-none-any.whl dist/inlog-2.1.0.tar.gz
```