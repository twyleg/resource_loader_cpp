# Copyright (C) 2022 twyleg
from pathlib import Path

import versioneer
from setuptools import find_packages, setup


def read(fname):
    return open(Path(__file__).parent / fname).read()


setup(
    name="resource_loader",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description="C++ static resource loader",
    license="GPL 3.0",
    keywords="C++ resources",
    url="https://github.com/twyleg/resource_loader",
    packages=find_packages(),
    include_package_data=True,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=[
        "jinja2~=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "resource_loader_gen = resource_loader.resource_loader:start",
        ]
    },
)
