""" Setup.py file for bipy package
"""
from setuptools import setup

setup(
    name="widgets4py",
    version="0.1.0",
    author="Ajeet Singh",
    author_email="singajeet@gmail.com",
    packages=["widgets4py"],
    url="https://github.com/singajeet/widgets4py",
    license="LICENSE.txt",
    description="HTML based widgets to be used on python app",
    long_description=open('README.txt').read(),
    install_requires=["Config"]
)
