#!/usr/bin/env python

import re
from setuptools import setup, find_packages, find_namespace_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

def GetVersion():
    with open("aiearth/openapi/__init__.py") as f:
        return re.findall(r"__version__\s*=\s*\"([.\d]+)\"", f.read())[0]

__version__ = GetVersion()
requirements = open("requirements.txt").readlines()

packages = find_namespace_packages(include=['aiearth.*'], exclude=['test', 'tests'])
setup(
    name="aiearth-openapi",
    version=__version__,
    author='AI Earth developer team',
    author_email='aiearth@service.aliyun.com',
    license="APACHE LICENSE, VERSION 2.0",
    description="AIEarth Engine Python SDK OpenAPI",
    url="https://engine-aiearth.aliyun.com/",
    packages=packages,
    python_requires=">=3.8.0",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)
