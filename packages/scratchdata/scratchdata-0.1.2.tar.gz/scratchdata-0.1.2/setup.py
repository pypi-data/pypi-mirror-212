from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.2'
DESCRIPTION = 'Module for data from scratch'

setup(
    name="scratchdata",
    version=VERSION,
    author="Vyacheslav C.",
    author_email="<vyacheslav_h@icloud.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'scratch', 'data', 'scraper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)