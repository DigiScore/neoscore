import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "brown",
    version = "0.0.1",
    author = "Andrew Yoon",
    author_email = "andrewyoon2@gmail.com",
    description = ("A vector graphics API for music notation"),
    license = "GPL-3",
    keywords = "music graphics",
    url = "https://github.com/ajyoon/brown",
    packages=['brown', 'tests'],
    long_description=read('README.md'),
    classifiers=[
    ],
)
