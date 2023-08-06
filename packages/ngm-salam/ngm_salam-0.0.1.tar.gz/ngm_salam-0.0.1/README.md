### Install, during dev:

```bash
pip install -e .
```

### Build:

```bash
pip install build
python -m build --sdist .
python -m build --wheel .
```

### Publish:

```bash
python -m twine upload dist/salam-0.0.1.tar.gz dist/salam-0.0.1-py3-none-any.whl
```
