#!/usr/bin/env python
import setuptools

# # read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="porf",
    version="0.0.5",
    description="Parse OpenRoad Files - RPT file parser for Openlane OpenROAD Static Timing Analysis output files.",
    extras_require={
        "develop": [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx_autodoc_typehints",
            "nbsphinx",
            "myst_parser"
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daquintero/porf",
    author="Dario Quintero",
    author_email="darioaquintero@gmail.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["pandas"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
