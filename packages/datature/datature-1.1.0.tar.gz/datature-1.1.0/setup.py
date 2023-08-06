#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   setup.py
@Author  :   Raighne.Weng
@Version :   1.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Setup module
'''

import re
import setuptools

# read the contents of your README file
with open("readme.md", "r", encoding="utf8") as rd:
    long_description = rd.read()

# read the version number
with open('datature/__init__.py', "r", encoding="utf8") as rd:
    version = re.search(r'SDK_VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
                        rd.read()).group(1)

setuptools.setup(
    name="datature",
    version=version,
    author="Raighne Weng",
    author_email="raighne@datature.io",
    long_description_content_type="text/markdown",
    long_description=long_description,
    description="Python bindings for the Datature API",
    packages=setuptools.find_namespace_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests", "google-crc32c", "pyhumps", "pyyaml", "inquirer", "halo",
        "filetype", "opencv-python", "alive-progress", "pydicom", "nibabel",
        "pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
    ],
    extras_require={
        'docs': ["sphinx", "sphinx-rtd-theme", "sphinx_markdown_builder"]
    },
    entry_points={
        'console_scripts': ['datature=datature.cli.main:main'],
    },
)
