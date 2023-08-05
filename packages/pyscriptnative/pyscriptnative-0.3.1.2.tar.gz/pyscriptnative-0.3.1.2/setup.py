import re
from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pyscriptnative.py').read(),
    re.M
    ).group(1)

setup(
    name='pyscriptnative',
    version=version,
    description='pyscriptnative brings the support for Python scripting on the web of py-script in Flask.',
    long_description=long_description,
    url="https://github.com/AquaQuokka/pyscriptnative",
    author="AquaQuokka",
    license='BSD-3-Clause',
    py_modules=['pyscriptnative'],
    scripts=['pyscriptnative.py'],
    install_requires=["flask", "jinja2"],
)
