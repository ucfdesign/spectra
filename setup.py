#!/usr/bin/env python
################################################################################
#
# setup.py
#
# Copyright (c) 2021, Triple Dot Engineering LLC
#
# This file defines the package installation.
#
################################################################################
import setuptools

with open('./README.md') as fh:
    long_description = fh.read()

with open('./src/spectra/__init__.py') as fh:
    version_line = [ ln for ln in fh.read().splitlines() if ln.startswith('version = ') ][0]
    version = version_line.split(' = ')[-1]

#with open('./requirements.txt') as f:
#    requirements = f.read().splitlines()

setuptools.setup(
    name='spectra',
    version=version,
    description='Spectra - Organizational data tool suite',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Triple Dot Engineering',
    url='https://triple.engineering',
    package_dir = {
        "": "Src"
    },
    packages=[
        'spectra',
        #'spectra.cli'
    ],
    #package_data={"prism": ["templates/*"]},
    entry_points = {
        'console_scripts': [
            'spectra = spectra.cli.__main__:main',
            'spectra2 = spectra:run'
        ],
    },
    license="MIT",
    #install_requires=requirements,
    #package_dir={'': 'src'},
    #scripts=['scripts/trivium'],
    python_requires=">=3.6"
)
