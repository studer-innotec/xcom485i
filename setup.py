#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import setuptools

current_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

name = "xcom485i"
version = "0.9"
release = "0.9.2"

setuptools.setup(
    name=name,
    version=release,
    author="Studer Innotec SA",
    author_email="develop@studer-innotec.com",  # create a dev general email
    maintainer_email="develop@studer-innotec.com",
    description="Package that let easily interact with the Xcom-485i device over Modbus RTU",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/studer-innotec/xcom485i",
    project_urls={
        "Documentation": "https://xcom485i.readthedocs.io/en/latest/index.html",
        "Issues tracker": "https://github.com/studer-innotec/xcom485i/issues",
        "Source Code": "https://github.com/studer-innotec/xcom485i",
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6.8',
    install_requires=['uModbus==1.0.3', 'pyserial>=3.4'],
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build'),
            'all_files': ('setup.py', 1)},
    },
)
