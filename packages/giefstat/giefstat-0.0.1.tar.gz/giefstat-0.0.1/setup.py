from setuptools import setup, find_packages
import os

VERSION = "0.0.1"
DESCRIPTION = "Package for information estimation, independence test, etc."

setup(
    name="giefstat",
    version=VERSION,
    author="Dreisteine",
    author_email="dreisteine@163.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["scikit-learn", "minepy"],
    keywords=["python", "information estimation"],
    license="MIT",
    url="https://github.com/Ulti-Dreisteine/general-information-estimation-framework",
)