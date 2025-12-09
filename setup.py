from setuptools import setup, find_packages

setup(
    name="phacav",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "noise",
        "pytest",
    ],
) 