from setuptools import setup

name = "types-flake8-bugbear"
description = "Typing stubs for flake8-bugbear"
long_description = '''
## Typing stubs for flake8-bugbear

This is a PEP 561 type stub package for the `flake8-bugbear` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-bugbear`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-bugbear. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `9d6e3564bb00e87304c93cacd3d365a908fe9fd5`.
'''.lstrip()

setup(name=name,
      version="23.6.5.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-bugbear.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['bugbear-stubs'],
      package_data={'bugbear-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
