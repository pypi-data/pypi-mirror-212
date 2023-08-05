# coding:utf8
from os import path
from easyquotation import __version__
from setuptools import setup
from astartool.setuptool import load_install_requires
from astar_devopstool.common import License, LICENSE_SHORT
# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="snowland-easyquotation",
    version=__version__,
    description="A utility for Fetch China Stock Info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="A.Star",
    author_email="astar@snowland.ltd",
    license=LICENSE_SHORT[License.APACHE],
    url="https://gitee.com/a_star/easyquotation",
    keywords="China stock trade",
    install_requires=load_install_requires(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        License.APACHE.value
    ],
    packages=["easyquotation"],
    package_data={"": ["*.conf"]},
)
