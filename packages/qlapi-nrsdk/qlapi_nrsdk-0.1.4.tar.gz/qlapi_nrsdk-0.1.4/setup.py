from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.4'
AUTHOR='eegion'
EMAIL='hehuajun@eegion.com'
REQUIRED = [
    'beautifulsoup',
    "lxml"
]

setup(
    name='qlapi_nrsdk',  # package name
    version=VERSION,  # package version
    author=AUTHOR,
    author_email=EMAIL,
    requires=REQUIRED,
    description='Api for use quanlan device, since v1.1.1',  # package description
    packages=find_packages(),
    package_data={
        "qlapi_nrsdk": ["lib/*.dll"],
        "":["*.txt", "*.md"]
    },
    zip_safe=False,
)