
# Step-by-Step Guide to Update SDK on PyPI

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- pip
- setuptools
- wheel
- twine

You can install these using the following commands:
```bash
pip install --upgrade pip setuptools wheel twine
```

### 1. Update Version Number

Update the version number in `setup.py` and `__init__.py` files.

### 2. Build the Distribution

Navigate to the root directory of your project and build the distribution files:
```bash
python setup.py sdist bdist_wheel
```

### 3. Upload to PyPI

Use `twine` to upload the distribution files to PyPI:
```bash
twine upload dist/*
```

### 4. Verify the Upload

After uploading, verify that your package has been updated on PyPI by visiting your package's page.

## Additional Resources

- [PyPI - Uploading Packages](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)
- [TestPyPI](https://test.pypi.org/)
- [twine Documentation](https://twine.readthedocs.io/en/latest/)