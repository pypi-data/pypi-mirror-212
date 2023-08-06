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
python -m twine upload dist/ngm_salam-0.0.1.tar.gz dist/ngm_salam-0.0.1-py3-none-any.whl
```
